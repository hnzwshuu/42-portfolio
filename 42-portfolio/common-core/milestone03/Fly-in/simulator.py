"""Validate flight schedules and convert movements into per-turn tokens."""

from models import DroneMap
from schedule import Flight, Reservations


class SimulationError(RuntimeError):
    """Indicate that a path or flight schedule violates movement rules."""


class Simulator:
    """Validate all drone schedules before returning per-turn movements."""

    def __init__(
        self,
        drone_map: DroneMap,
        paths: list[list[str]],
        departures: list[int],
    ) -> None:
        """Store the map, per-drone paths, and initial waiting turns.

        PathFinder supplies paths and matching departures, where each
        departure value is the number of turns to wait at the start.
        Raise SimulationError if these inputs fail path validation.

        Args:
            drone_map: Map supplying the fleet size, zones, and connections.
            paths: One start-to-end zone-name path per drone, ordered by
                drone ID starting with D1.
            departures: Nonnegative initial waiting-turn counts in the same
                order as paths; zero means no delay before the first move.
        """
        self.drone_map = drone_map
        self.paths = paths
        self.departures = departures
        self._validate_paths()

    def _validate_paths(self) -> None:
        """Raise SimulationError for invalid paths or initial waiting turns."""
        if len(self.paths) != self.drone_map.drone_count:
            raise SimulationError("one path is required for each drone")
        for path in self.paths:
            if len(path) < 2 or path[0] != self.drone_map.start:
                raise SimulationError("each path must begin at start_hub")
            if path[-1] != self.drone_map.end:
                raise SimulationError("each path must finish at end_hub")
            if self.drone_map.end in path[:-1]:
                raise SimulationError("a delivered drone cannot leave end_hub")
            for name in path:
                zone = self.drone_map.zones.get(name)
                if zone is None or zone.zone_type == "blocked":
                    raise SimulationError(f"unavailable zone '{name}'")
            for first, second in zip(path, path[1:]):
                if second not in self.drone_map.neighbours[first]:
                    message = f"missing connection {first}-{second}"
                    raise SimulationError(message)
        if len(self.departures) != len(self.paths):
            raise SimulationError("one departure is required per drone")
        for waiting_turns in self.departures:
            if waiting_turns < 0:
                raise SimulationError("departure turns cannot be negative")

    def run(self) -> list[list[str]]:
        """Return movement tokens grouped by turn without displaying them.

        Raise SimulationError if the planned flights exceed capacity.
        Restricted-zone travel emits a transit token before arrival.

        Returns:
            Lists of movement tokens in chronological turn order, with index
            zero representing turn one. Each inner list is in drone ID order;
            turns without movement are empty lists.
        """
        flights = self._plan()
        last_turn = 0
        for flight in flights.values():
            last_turn = max(last_turn, flight.arrivals[-1])
        turns: list[list[str]] = [[] for _ in range(last_turn)]
        for drone_id in sorted(flights):
            flight = flights[drone_id]
            for index in range(1, len(flight.path)):
                source = flight.path[index - 1]
                destination = flight.path[index]
                arrival_turn = flight.arrivals[index]
                arrival_index = arrival_turn - 1
                if self.drone_map.zones[destination].move_cost == 2:
                    transit_index = arrival_index - 1
                    token = f"D{drone_id}-{source}-{destination}"
                    turns[transit_index].append(token)
                turns[arrival_index].append(f"D{drone_id}-{destination}")
        return turns

    def _plan(self) -> dict[int, Flight]:
        """Return capacity-checked flights keyed by one-based drone IDs.

        Raise SimulationError if any flight conflicts with prior bookings.

        Returns:
            A dictionary mapping each one-based drone ID to its validated
            Flight, containing the path and corresponding arrival turns.
        """
        reservations = Reservations(self.drone_map)
        flights: dict[int, Flight] = {}
        for index in range(len(self.paths)):
            path = self.paths[index]
            waiting_turns = self.departures[index]
            flight = self._nonstop_flight(path, waiting_turns)
            self._check_flight(reservations, flight)
            reservations.reserve(flight)
            flights[index + 1] = flight
        return flights

    def _nonstop_flight(self, path: list[str], waiting_turns: int) -> Flight:
        """Return a flight that waits at the start, then follows path nonstop.

        waiting_turns sets the initial delay; each destination's move cost
        determines the next arrival turn.

        Args:
            path: Zone names from start to end, including both endpoints.
            waiting_turns: Nonnegative number of turns spent at the start
                before beginning the first movement.

        Returns:
            A Flight containing the supplied path and its arrival turns.
            The first arrival is zero at the start; later arrivals include
            the initial delay and cumulative movement costs, with no stops.
        """
        turn = waiting_turns
        arrivals = [0]
        for name in path[1:]:
            turn += self.drone_map.zones[name].move_cost
            arrivals.append(turn)
        return Flight(path, arrivals)

    def _check_flight(
        self, reservations: Reservations, flight: Flight
    ) -> None:
        """Check a nonstop flight against existing capacity reservations.

        Raise SimulationError on a zone or connection capacity conflict.
        The reservations are not modified.

        Args:
            reservations: Existing zone and connection usage to check against.
            flight: Nonstop flight whose arrival and departure capacities
                must remain compatible with the existing reservations.
        """
        for index in range(1, len(flight.path)):
            source = flight.path[index - 1]
            destination = flight.path[index]
            arrival_turn = flight.arrivals[index]
            travel_time = self.drone_map.zones[destination].move_cost
            if not reservations.has_room(destination, arrival_turn):
                message = f"zone capacity exceeded at turn {arrival_turn}"
                raise SimulationError(message)
            departure_turn = arrival_turn - travel_time + 1
            if not reservations.can_depart(
                source, destination, departure_turn
            ):
                raise SimulationError("connection capacity exceeded")
