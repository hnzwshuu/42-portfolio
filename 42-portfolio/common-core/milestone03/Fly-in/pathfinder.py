"""Select routes and departure times to minimize fleet completion time."""

import heapq

from flow import RouteFlow
from models import DroneMap


class PathFinder:
    """Choose capacity-constrained lanes and schedule drone departures.

    RouteFlow supplies route lanes, each supporting one departure per turn.
    """

    def __init__(self, drone_map: DroneMap) -> None:
        """Store the map and initialize departure delays and completion time.

        Args:
            drone_map: Map containing the fleet size and route constraints.
        """
        self.drone_map = drone_map
        self.departures: list[int] = []
        self.turn_count = 0

    def create_paths(self) -> list[list[str]]:
        """Select routes and store departure delays and fleet completion time.

        Returns:
            One zone-name path per drone, in drone identifier order.
            The matching departures entry records turns spent waiting at start.

        Raises:
            ValueError: If no usable path connects the start and end zones.
        """
        flow = RouteFlow(self.drone_map)
        drone_count = self.drone_map.drone_count
        best_turn_count: int | None = None
        best_lanes: list[list[str]] = []

        while flow.augment():
            required_turns = (
                drone_count + flow.total_travel_time - 1
            ) // flow.lane_count
            if best_turn_count is None or required_turns < best_turn_count:
                best_turn_count = required_turns
                best_lanes = flow.paths()

        if not best_lanes:
            raise ValueError("no path exists from start_hub to end_hub")
        return self._assign_departures(best_lanes)

    def _assign_departures(self, lanes: list[list[str]]) -> list[list[str]]:
        """Assign each drone to the next lane offering the earliest arrival.

        Return per-drone paths and update departures and turn_count. Priority
        cost breaks ties between lanes with equal next-arrival times.

        Args:
            lanes: Nonempty list of start-to-end zone-name paths, each
                supporting one departure per turn. Repeated paths represent
                separate lanes of available capacity.

        Returns:
            One copied zone-name path per drone, in drone identifier order.
            Each path matches the entry at the same index in departures.
        """
        arrival_queue: list[tuple[int, int, int]] = []
        travel_times: list[int] = []
        for lane_index, path in enumerate(lanes):
            travel_time = 0
            priority_cost = 0
            for name in path[1:]:
                zone = self.drone_map.zones[name]
                travel_time += zone.move_cost
                if zone.zone_type == "priority":
                    priority_cost -= 1
            travel_times.append(travel_time)
            heapq.heappush(
                arrival_queue, (travel_time, priority_cost, lane_index)
            )

        paths: list[list[str]] = []
        self.departures = []
        for _ in range(self.drone_map.drone_count):
            arrival_turn, priority_cost, lane_index = heapq.heappop(
                arrival_queue
            )
            paths.append(lanes[lane_index].copy())
            waiting_turns = arrival_turn - travel_times[lane_index]
            self.departures.append(waiting_turns)
            self.turn_count = arrival_turn
            next_slot = (arrival_turn + 1, priority_cost, lane_index)
            heapq.heappush(arrival_queue, next_slot)
        return paths
