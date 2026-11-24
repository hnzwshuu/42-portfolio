"""Convert validated simulation turns into drone positions for display."""

from models import DroneMap


Point = tuple[float, float]


class Playback:
    """Track drone coordinates and zone locations during replay.

    Locations are zone names, or None for drones in transit.
    """

    def __init__(self, drone_map: DroneMap, turns: list[list[str]]) -> None:
        """Store the replay inputs and initialize all drones at the start.

        Args:
            drone_map: Map providing zone names and coordinates.
            turns: Validated movement tokens grouped by turn.
        """
        self.drone_map = drone_map
        self.turns = turns
        self.reset()

    @property
    def finished(self) -> bool:
        """Return whether every simulation turn has been applied.

        Returns:
            True if the turn counter equals the number of recorded turns,
            including an empty replay; False otherwise.
        """
        return self.turn == len(self.turns)

    def reset(self) -> None:
        """Reset the turn counter and place every drone at the start zone."""
        self.turn = 0
        start = self._zone_position(self.drone_map.start)
        self.positions: dict[int, Point] = {}
        self.locations: dict[int, str | None] = {}

        for drone_id in range(1, self.drone_map.drone_count + 1):
            self.positions[drone_id] = start
            self.locations[drone_id] = self.drone_map.start

    def _zone_position(self, name: str) -> Point:
        """Return the named zone's coordinates as a floating-point pair.

        Args:
            name: Name of an existing zone in the replay map.

        Returns:
            The zone's (x, y) map coordinates as a pair of floats.
        """
        zone = self.drone_map.zones[name]
        return (float(zone.x), float(zone.y))

    def step(self) -> None:
        """Apply the next turn to drone positions and advance the counter.

        In-transit drones use the connection midpoint. Stationary drones
        retain their positions. Calls after the final turn have no effect.
        """
        if self.finished:
            return

        for movement in self.turns[self.turn]:
            parts = movement.split("-")
            drone_id = int(parts[0][1:])

            if len(parts) == 2:
                destination = parts[1]
                self.positions[drone_id] = self._zone_position(destination)
                self.locations[drone_id] = destination
            else:
                source = self._zone_position(parts[1])
                destination_point = self._zone_position(parts[2])
                self.positions[drone_id] = (
                    (source[0] + destination_point[0]) / 2,
                    (source[1] + destination_point[1]) / 2,
                )
                self.locations[drone_id] = None

        self.turn += 1
