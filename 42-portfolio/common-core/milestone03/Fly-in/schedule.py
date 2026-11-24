"""Reserve zone and connection capacity for scheduled drone movements."""

from collections import Counter
from dataclasses import dataclass

from models import DroneMap


@dataclass
class Flight:
    """Store one drone's path and corresponding arrival turns.

    Each path[i] corresponds to arrivals[i], with arrivals[0] set to zero
    at the start. For example, path=['s', 'r', 't'] and arrivals=[0, 2, 3]
    describe arrivals at r on turn two and t on turn three. Gaps between
    arrivals include waiting and the travel time into restricted zones.
    """

    path: list[str]
    arrivals: list[int]


class Reservations:
    """Count reserved drones for each zone or connection at each turn."""

    def __init__(self, drone_map: DroneMap) -> None:
        """Store the map and initialize empty zone and connection counters.

        Each counter returns zero for an unreserved location and turn.

        Args:
            drone_map: Map supplying zone and connection capacities and
                identifying the unlimited start and end zones.
        """
        self.drone_map = drone_map
        self.zone_usage: Counter[tuple[str, int]] = Counter()
        self.connection_usage: Counter[tuple[str, int]] = Counter()

    def has_room(self, zone_name: str, turn: int) -> bool:
        """Return whether a named zone has room for one more drone at turn.

        The start and end zones have unlimited capacity.

        Args:
            zone_name: Name of the zone whose available capacity is checked.
            turn: One-based simulation turn at which a drone would occupy it.

        Returns:
            True for the start or end zone, or if another drone fits within
            the zone's capacity at turn; False if that capacity is exhausted.
        """
        if zone_name in {self.drone_map.start, self.drone_map.end}:
            return True
        capacity = self.drone_map.zones[zone_name].max_drones
        return self.zone_usage[(zone_name, turn)] < capacity

    def can_depart(self, first: str, second: str, turn: int) -> bool:
        """Return whether another drone may depart between zones at turn.

        Both directions share the connection's capacity. Only the departure
        turn is reserved, even when travel into a restricted zone takes two
        turns.

        Args:
            first: Name of the departure zone.
            second: Name of the destination zone connected to first.
            turn: One-based departure turn, not the later arrival turn
                when the destination is restricted.

        Returns:
            True if the shared connection has capacity for another departure
            at turn; False if its departure capacity is exhausted. Destination
            zone capacity is not checked here.
        """
        connection = self.drone_map.connection_between(first, second)
        used = self.connection_usage[(connection.key, turn)]
        return used < connection.max_capacity

    def reserve(self, flight: Flight) -> None:
        """Add a flight's connection departures and zone occupancy to usage.

        A drone occupies its source zone while waiting, but releases it on
        the departure turn. The start zone is not counted.

        Args:
            flight: Scheduled path and arrival turns whose departures and
                zone occupancy are added to the existing usage counters.
        """
        for index in range(len(flight.path) - 1):
            source = flight.path[index]
            destination = flight.path[index + 1]
            travel_time = self.drone_map.zones[destination].move_cost
            arrival_turn = flight.arrivals[index + 1]
            departure_turn = arrival_turn - travel_time + 1
            connection = self.drone_map.connection_between(source, destination)
            self.connection_usage[(connection.key, departure_turn)] += 1
            if source == self.drone_map.start:
                continue
            for turn in range(flight.arrivals[index], departure_turn):
                self.zone_usage[(source, turn)] += 1
