"""Store zone, connection, and map data for drone routing."""

from dataclasses import dataclass, field


@dataclass
class Zone:
    """Describe a zone's position, movement type, color, and capacity."""

    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: str | None = None
    max_drones: int = 1

    @property
    def move_cost(self) -> int:
        """Return two travel turns for restricted zones, otherwise one.

        Returns:
            The travel cost in turns: 2 for a restricted zone, otherwise 1.
        """
        if self.zone_type == "restricted":
            return 2
        return 1


@dataclass
class Connection:
    """Store a bidirectional connection and its shared capacity."""

    first: str
    second: str
    max_capacity: int = 1

    @property
    def key(self) -> str:
        """Return a direction-independent key such as 'a-b'.

        Returns:
            The two endpoint names sorted lexicographically and joined
            with a dash, giving the same key for either direction.
        """
        return "-".join(sorted((self.first, self.second)))


@dataclass
class DroneMap:
    """Store the drone count, zones, connections, and route endpoints."""

    drone_count: int
    zones: dict[str, Zone]
    connections: dict[str, Connection]
    start: str
    end: str
    neighbours: dict[str, list[str]] = field(default_factory=dict)

    def build_neighbours(self) -> None:
        """Rebuild the adjacency lists from all bidirectional connections."""
        self.neighbours = {}
        for name in self.zones:
            self.neighbours[name] = []
        for connection in self.connections.values():
            self.neighbours[connection.first].append(connection.second)
            self.neighbours[connection.second].append(connection.first)

    def connection_between(self, first: str, second: str) -> Connection:
        """Return the connection between two zone names.

        Raise KeyError if no connection exists between the zones.

        Args:
            first: Name of one endpoint zone.
            second: Name of the other endpoint zone; order is irrelevant.

        Returns:
            The stored Connection object joining first and second,
            regardless of the order of those endpoint names.
        """
        key = "-".join(sorted((first, second)))
        return self.connections[key]
