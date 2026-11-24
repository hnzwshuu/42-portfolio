"""Compile JSON scalar schemas into byte-level state machines."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

State = frozenset[int]
Edge = tuple[frozenset[int], int]


class Grammar(BaseModel):
    """A byte-level state machine for a JSON scalar and its terminator.

    Attributes:
        model_config: Pydantic settings for internal data structures.
        edges: Source nodes mapped to allowed byte sets and target nodes.
        epsilon: Transitions that consume no input bytes.
        start: Initial node identifier.
        end: Accepting node identifier.
        count: Number of allocated nodes.
        transitions: Cached transitions from state sets on single bytes.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    edges: dict[int, list[Edge]] = Field(default_factory=dict)
    epsilon: dict[int, set[int]] = Field(default_factory=dict)
    start: int = 0
    end: int = 0
    count: int = 0
    transitions: dict[tuple[State, int], State] = Field(default_factory=dict)

    def node(self) -> int:
        """Allocate a node identifier and advance the node count.

        Returns:
            Identifier assigned to the newly allocated node.
        """
        index = self.count
        self.count += 1
        return index

    def edge(self, source: int, target: int, values: bytes) -> None:
        """Add a transition accepting any one of the supplied bytes.

        Args:
            source: Starting node identifier.
            target: Destination node identifier.
            values: Bytes accepted by the transition.
        """
        self.edges.setdefault(source, []).append((frozenset(values), target))

    def empty(self, source: int, target: int) -> None:
        """Add a transition that consumes no input bytes.

        Args:
            source: Starting node identifier.
            target: Destination node identifier.
        """
        self.epsilon.setdefault(source, set()).add(target)

    def literal(self, source: int, target: int, value: bytes) -> None:
        """Add a path accepting an exact byte sequence.

        Args:
            source: Starting node identifier.
            target: Destination node identifier.
            value: Bytes to accept, or empty bytes for an epsilon path.
        """
        if not value:
            self.empty(source, target)
        for index, byte_value in enumerate(value):
            next_node = target if index == len(value) - 1 else self.node()
            self.edge(source, next_node, bytes([byte_value]))
            source = next_node

    def closure(self, state: State) -> State:
        """Find all nodes reachable without consuming input.

        Args:
            state: Current set of active nodes.

        Returns:
            The supplied nodes and all nodes reachable by epsilon paths.
        """
        result = set(state)
        pending = list(state)
        while pending:
            for target in self.epsilon.get(pending.pop(), ()):
                if target not in result:
                    result.add(target)
                    pending.append(target)
        return frozenset(result)

    def step(self, state: State, byte_value: int) -> State:
        """Consume one byte and cache the resulting state set.

        Args:
            state: Current active nodes, including their epsilon closure.
            byte_value: Input byte as an integer.

        Returns:
            The next epsilon-closed state set, or an empty set if invalid.
        """
        key = (state, byte_value)
        if key not in self.transitions:
            targets: set[int] = set()
            for source in state:
                for allowed_bytes, target in self.edges.get(source, ()):
                    if byte_value in allowed_bytes:
                        targets.add(target)
            self.transitions[key] = self.closure(frozenset(targets))
        return self.transitions[key]

    def consume(self, state: State, value: bytes) -> State:
        """Consume a byte sequence from the supplied state set.

        Args:
            state: Current active nodes, including their epsilon closure.
            value: Byte sequence to validate.

        Returns:
            The final state set, or an empty set if any byte is invalid.
        """
        for byte_value in value:
            state = self.step(state, byte_value)
            if not state:
                break
        return state

    def forced(self, state: State) -> tuple[bytes, State]:
        """Follow transitions while only one next byte is possible.

        Args:
            state: Current active nodes, including their epsilon closure.

        Returns:
            Forced bytes and the resulting state set. Stops at acceptance,
            a choice between bytes, or a state with no outgoing bytes.
        """
        output = bytearray()
        while self.end not in state:
            chars: set[int] = set()
            for source in state:
                for values, _ in self.edges.get(source, ()):
                    chars.update(values)
            if len(chars) != 1:
                break
            byte_value = next(iter(chars))
            output.append(byte_value)
            state = self.step(state, byte_value)
        return bytes(output), state

    def string(self, source: int, target: int) -> None:
        """Add a path accepting an ASCII JSON string with JSON escapes.

        Non-ASCII characters must use Unicode escapes.

        Args:
            source: Node before the opening quote.
            target: Node after the closing quote.
        """
        body, escape = self.node(), self.node()
        self.edge(source, body, b'"')
        self.edge(body, target, b'"')
        self.edge(body, escape, b'\\')
        self.edge(escape, body, b'"\\/bfnrt')
        self.edge(body, body, bytes(c for c in range(32, 128)
                                    if c not in (34, 92)))
        unicode_node = self.node()
        self.edge(escape, unicode_node, b'u')
        for index in range(4):
            following = body if index == 3 else self.node()
            self.edge(unicode_node, following, b'0123456789abcdefABCDEF')
            unicode_node = following

    def number(self, source: int, target: int, integer: bool) -> None:
        """Add a path accepting JSON number syntax.

        Args:
            source: Starting node identifier.
            target: Node after the number.
            integer: Whether to exclude fractional and exponent parts.
        """
        sign, zero, digits = self.node(), self.node(), self.node()
        self.edge(source, sign, b'-')
        self.empty(source, sign)
        self.edge(sign, zero, b'0')
        self.edge(sign, digits, b'123456789')
        self.edge(digits, digits, b'0123456789')
        self.empty(zero, target)
        self.empty(digits, target)
        if integer:
            return
        point, fraction = self.node(), self.node()
        exponent, exponent_sign, exponent_digits = (
            self.node(), self.node(), self.node()
        )
        for part in (zero, digits):
            self.edge(part, point, b'.')
            self.edge(part, exponent, b'eE')
        self.edge(point, fraction, b'0123456789')
        self.edge(fraction, fraction, b'0123456789')
        self.edge(fraction, exponent, b'eE')
        self.empty(fraction, target)
        self.edge(exponent, exponent_sign, b'+-')
        self.empty(exponent, exponent_sign)
        self.edge(exponent_sign, exponent_digits, b'0123456789')
        self.edge(exponent_digits, exponent_digits, b'0123456789')
        self.empty(exponent_digits, target)

    def value(self, source: int, target: int, schema: dict[str, Any]) -> None:
        """Add a path for the scalar type specified by a schema.

        Args:
            source: Starting node identifier.
            target: Node after the scalar value.
            schema: Validated parameter schema containing a type field.

        Raises:
            ValueError: If the scalar type is unsupported.
        """
        kind = schema['type']
        if kind == 'string':
            self.string(source, target)
        elif kind in ('number', 'integer'):
            self.number(source, target, kind == 'integer')
        elif kind == 'boolean':
            for literal in (b'true', b'false'):
                self.literal(source, target, literal)
        else:
            raise ValueError(f'Unsupported argument type: {kind}')

    @classmethod
    def compile(cls, schema: dict[str, Any], terminator: bytes) -> 'Grammar':
        """Build a grammar for one scalar value followed by a terminator.

        Args:
            schema: Validated parameter schema containing a type field.
            terminator: Exact bytes expected after the scalar value.

        Returns:
            A grammar with its start and accepting nodes configured.

        Raises:
            ValueError: If the scalar type is unsupported.
        """
        grammar = cls()
        grammar.start, grammar.end = grammar.node(), grammar.node()
        value_end = grammar.node()
        grammar.value(grammar.start, value_end, schema)
        grammar.literal(value_end, grammar.end, terminator)
        return grammar
