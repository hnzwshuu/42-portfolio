"""Generate schema-constrained JSON values from public SDK logits."""

import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from src.grammar import Grammar, State


def encode(model: Any, text: str) -> list[int]:
    """Tokenize text using the SDK and flatten its single-row result.

    Args:
        model: SDK model whose encode method returns a single-row tensor.
        text: Text to tokenize.

    Returns:
        Token IDs as a Python list.
    """
    return [int(token) for token in model.encode(text).tolist()[0]]


def byte_decoder() -> dict[str, int]:
    """Return the inverse of Qwen's byte-level BPE character mapping.

    Returns:
        Visible BPE characters mapped to their original byte values.
    """
    visible_bytes = list(range(33, 127)) + list(range(161, 173))
    visible_bytes += list(range(174, 256))
    character_to_byte = {
        chr(byte_value): byte_value
        for byte_value in visible_bytes
    }
    next_extra_code_point = 256
    for byte_value in range(256):
        if byte_value not in visible_bytes:
            character_to_byte[chr(next_extra_code_point)] = byte_value
            next_extra_code_point += 1
    return character_to_byte


def trie_root() -> list[dict[int, int]]:
    """Return a fresh trie containing only an empty root node.

    Returns:
        A one-element list containing an empty root-node mapping.
    """
    return [{}]


class Vocabulary(BaseModel):
    """A token-byte vocabulary with a prefix trie and decoding caches.

    Attributes:
        model_config: Pydantic settings for internal data structures.
        tokens: Token IDs mapped to their original byte sequences.
        children: Trie nodes mapping bytes to child node indices.
        terminals: Trie node indices mapped to completed token IDs.
        grammars: Compiled grammars keyed by schema and terminator.
        masks: Allowed tokens and next states cached by grammar and state.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    tokens: dict[int, bytes] = Field(default_factory=dict)
    children: list[dict[int, int]] = Field(default_factory=trie_root)
    terminals: dict[int, list[int]] = Field(default_factory=dict)
    grammars: dict[str, Grammar] = Field(default_factory=dict)
    masks: dict[str, dict[State, dict[int, State]]] = Field(
        default_factory=dict
    )

    @classmethod
    def from_model(cls, model: Any) -> 'Vocabulary':
        """Load the SDK vocabulary and build a trie of token bytes.

        Args:
            model: SDK model exposing get_path_to_vocab_file().

        Returns:
            A vocabulary excluding special tokens and empty byte strings.

        Raises:
            OSError: If the vocabulary file cannot be read.
            ValueError: If the vocabulary JSON, token IDs, or byte-level
                BPE mapping are invalid, or no usable tokens remain.
        """
        path = Path(model.get_path_to_vocab_file())
        with path.open(encoding='utf-8') as handle:
            raw_vocabulary = json.load(handle)
        if not isinstance(raw_vocabulary, dict) or not raw_vocabulary:
            raise ValueError('The SDK vocabulary must be a nonempty object.')
        vocabulary = cls()
        character_to_byte = byte_decoder()
        for token_text, token_id in raw_vocabulary.items():
            if type(token_id) is not int or token_id < 0:
                raise ValueError('The SDK vocabulary contains an invalid ID.')
            if token_text.startswith('<|') and token_text.endswith('|>'):
                continue
            try:
                token_bytes = bytes(
                    character_to_byte[character]
                    for character in token_text
                )
            except KeyError as error:
                raise ValueError('This model requires a byte-level BPE '
                                 'vocabulary, such as Qwen3.') from error
            if not token_bytes:
                continue
            if token_id in vocabulary.tokens:
                raise ValueError('The SDK vocabulary contains duplicate IDs.')
            vocabulary.tokens[token_id] = token_bytes
            trie_node = 0
            for byte_value in token_bytes:
                next_trie_node = vocabulary.children[trie_node].get(
                    byte_value,
                )
                if next_trie_node is None:
                    next_trie_node = len(vocabulary.children)
                    vocabulary.children[trie_node][byte_value] = next_trie_node
                    vocabulary.children.append({})
                trie_node = next_trie_node
            vocabulary.terminals.setdefault(trie_node, []).append(token_id)
        if not vocabulary.tokens:
            raise ValueError('No usable tokens in the SDK vocabulary.')
        return vocabulary

    def allowed(self, schema_key: str, grammar: Grammar, grammar_state: State
                ) -> dict[int, State]:
        """Find complete tokens that preserve a valid grammar prefix.

        Args:
            schema_key: Cache key identifying the grammar and terminator.
            grammar: State machine for the current scalar value.
            grammar_state: Current epsilon-closed set of active nodes.

        Returns:
            A cached mapping of allowed token IDs to their next states.
            Callers must not modify the returned mapping.
        """
        schema_cache = self.masks.setdefault(schema_key, {})
        if grammar_state in schema_cache:
            return schema_cache[grammar_state]
        allowed_tokens: dict[int, State] = {}
        states_to_check = [(0, grammar_state)]
        while states_to_check:
            trie_node, current_grammar_state = states_to_check.pop()
            for token_id in self.terminals.get(trie_node, ()):
                allowed_tokens[token_id] = current_grammar_state
            for byte_value, next_trie_node in self.children[trie_node].items():
                next_grammar_state = grammar.step(
                    current_grammar_state,
                    byte_value,
                )
                if next_grammar_state:
                    states_to_check.append(
                        (next_trie_node, next_grammar_state),
                    )
        schema_cache[grammar_state] = allowed_tokens
        return allowed_tokens


def finite_json(value: Any) -> bool:
    """Check that a parsed JSON value contains no non-finite floats.

    Args:
        value: Parsed value, including any nested lists or dictionaries.

    Returns:
        Whether every contained float is finite.
    """
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(finite_json(item) for item in value.values())
    if isinstance(value, list):
        return all(finite_json(item) for item in value)
    return True


def allowed_logits(
    logits: np.ndarray[Any, Any],
    allowed_token_ids: Iterable[int],
) -> np.ndarray[Any, Any]:
    """Mask disallowed and non-finite logits with negative infinity.

    Args:
        logits: One-dimensional model logits indexed by token ID.
        allowed_token_ids: Permitted token IDs; out-of-range IDs are ignored.

    Returns:
        A new masked array, leaving the original logits unchanged.
    """
    masked_logits = np.full(logits.shape, -np.inf)
    for token_id in allowed_token_ids:
        if (
            0 <= token_id < len(logits)
            and np.isfinite(logits[token_id])
        ):
            masked_logits[token_id] = logits[token_id]
    return masked_logits


def generate_json_value(
    model: Any,
    input_ids: list[int],
    schema: dict[str, Any],
    vocabulary: Vocabulary,
    terminator: bytes,
    initial_bytes: bytes = b'',
    max_tokens: int = 256,
) -> tuple[Any, list[int]]:
    """Generate one JSON scalar while masking invalid next tokens.

    Fixed grammar bytes are appended directly. Model logits choose among
    valid alternatives, with every byte of each token checked. Vocabulary
    caches may be updated, but the supplied input IDs are not modified.

    Args:
        model: SDK model providing tokenization and next-token logits.
        input_ids: Model context, including any initial value bytes.
        schema: Validated scalar parameter schema.
        vocabulary: Token bytes, prefix trie, and reusable decoding caches.
        terminator: Nonempty byte sequence required after the value.
        initial_bytes: Value prefix already present in the model context.
        max_tokens: Positive budget for newly appended tokens, including
            forced grammar tokens.

    Returns:
        The parsed scalar and extended context IDs, including the
        terminator. The terminator is excluded from the parsed value.

    Raises:
        ValueError: If the schema, prefix, terminator, budget, or logits
            are invalid, generation cannot finish within the budget, no
            valid token has a finite score, or the result is invalid JSON
            or contains a non-finite number.
    """
    if max_tokens <= 0:
        raise ValueError('max_tokens must be positive.')
    if not terminator:
        raise ValueError('A JSON value terminator is required.')
    schema_key = (
        json.dumps(schema, ensure_ascii=True, sort_keys=False)
        + ':' + terminator.hex()
    )
    if schema_key not in vocabulary.grammars:
        vocabulary.grammars[schema_key] = Grammar.compile(schema, terminator)
    grammar = vocabulary.grammars[schema_key]
    grammar_state = grammar.closure(frozenset([grammar.start]))
    grammar_state = grammar.consume(grammar_state, initial_bytes)
    if not grammar_state:
        raise ValueError('The initial bytes do not match the JSON schema.')
    model_input_ids = list(input_ids)
    generated_bytes = bytearray(initial_bytes)
    used_token_count = 0

    while grammar.end not in grammar_state:
        if used_token_count >= max_tokens:
            raise ValueError(f'Generation exceeded {max_tokens} tokens.')

        fixed_bytes, next_state = grammar.forced(grammar_state)
        if fixed_bytes:
            try:
                forced_text = fixed_bytes.decode('utf-8')
            except UnicodeDecodeError:
                forced_text = ''
            if forced_text:
                forced_ids = encode(model, forced_text)
                if used_token_count + len(forced_ids) > max_tokens:
                    raise ValueError('Generation exceeded the token budget.')
                model_input_ids.extend(forced_ids)
                used_token_count += len(forced_ids)
                generated_bytes.extend(fixed_bytes)
                grammar_state = next_state
                continue

        allowed_tokens = vocabulary.allowed(
            schema_key,
            grammar,
            grammar_state,
        )
        logits = np.asarray(
            model.get_logits_from_input_ids(model_input_ids),
            dtype=np.float64,
        )
        if logits.ndim != 1 or not len(logits):
            raise ValueError('The SDK returned an invalid logits vector.')
        masked_logits = allowed_logits(logits, allowed_tokens)

        while True:
            if not np.isfinite(masked_logits).any():
                raise ValueError('No valid next token has a finite score.')
            selected_token_id = int(np.argmax(masked_logits))
            if grammar.end not in allowed_tokens[selected_token_id]:
                break

            completed_bytes = (
                bytes(generated_bytes)
                + vocabulary.tokens[selected_token_id]
            )
            try:
                value = json.loads(completed_bytes[:-len(terminator)])
                is_valid_json = finite_json(value)
            except (ValueError, UnicodeError):
                is_valid_json = False
            if is_valid_json:
                break
            masked_logits[selected_token_id] = -np.inf

        generated_bytes.extend(vocabulary.tokens[selected_token_id])
        model_input_ids.append(selected_token_id)
        used_token_count += 1
        grammar_state = allowed_tokens[selected_token_id]

    value = json.loads(bytes(generated_bytes[:-len(terminator)]))
    if not finite_json(value):
        raise ValueError('The model generated a non-finite number.')
    return value, model_input_ids
