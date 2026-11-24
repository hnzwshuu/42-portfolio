"""Find capacity-constrained route combinations using minimum-cost flow."""

from dataclasses import dataclass

from models import DroneMap


@dataclass
class _Edge:
    """Store a residual edge whose reverse edge can undo an earlier choice."""

    source: int
    destination: int
    reverse_index: int
    remaining_capacity: int
    initial_capacity: int
    travel_time: int
    priority_cost: int


class RouteFlow:
    """Find short route combinations by revising flow in a residual graph.

    Each lane supports one departure per turn. A route with capacity two
    can provide two lanes. The lane_count and total_travel_time attributes
    track the number of selected lanes and their combined travel time.
    """

    def __init__(self, drone_map: DroneMap) -> None:
        """Build a residual graph by splitting each usable zone into two nodes.

        Args:
            drone_map: Map supplying zones, capacities, and movement costs.

        Raises:
            ValueError: If the start or end zone is blocked.
        """
        self.lane_count = 0
        self.total_travel_time = 0
        self._drone_count = drone_map.drone_count
        self._zone_names: list[str] = []
        for name, zone in drone_map.zones.items():
            if zone.zone_type != "blocked":
                self._zone_names.append(name)

        entrance_nodes: dict[str, int] = {}
        for zone_index, name in enumerate(self._zone_names):
            entrance_nodes[name] = 2 * zone_index

        if (
            drone_map.start not in entrance_nodes
            or drone_map.end not in entrance_nodes
        ):
            raise ValueError("no path exists from start_hub to end_hub")
        self._start_node = entrance_nodes[drone_map.start] + 1
        self._end_node = entrance_nodes[drone_map.end]
        node_count = 2 * len(self._zone_names)
        self._graph: list[list[_Edge]] = [[] for _ in range(node_count)]

        for name in self._zone_names:
            capacity = drone_map.zones[name].max_drones
            if name in {drone_map.start, drone_map.end}:
                capacity = self._drone_count
            entrance = entrance_nodes[name]
            exit_node = entrance + 1
            self._add_edge(entrance, exit_node, capacity, travel_time=0)

        self._add_connections(drone_map, entrance_nodes)

    def _add_connections(
        self, drone_map: DroneMap, entrance_nodes: dict[str, int]
    ) -> None:
        """Add usable map connections from exit nodes to entrance nodes.

        Args:
            drone_map: Map supplying connections, capacities, and zone costs.
            entrance_nodes: Usable zone names mapped to entrance-node indices;
                each corresponding exit node has the next index.
        """
        for connection in drone_map.connections.values():
            for first, second in (
                (connection.first, connection.second),
                (connection.second, connection.first),
            ):
                if first not in entrance_nodes or second not in entrance_nodes:
                    continue
                if first == drone_map.end or second == drone_map.start:
                    continue
                zone = drone_map.zones[second]
                priority_cost = 0
                if zone.zone_type == "priority":
                    priority_cost = -1
                self._add_edge(
                    entrance_nodes[first] + 1,
                    entrance_nodes[second],
                    connection.max_capacity,
                    zone.move_cost,
                    priority_cost,
                )

    def _add_edge(
        self,
        source: int,
        destination: int,
        capacity: int,
        travel_time: int,
        priority_cost: int = 0,
    ) -> None:
        """Add a forward edge with capacity and its reverse residual edge.

        Args:
            source: Index of the forward edge's source in the residual graph.
            destination: Index of its destination in the residual graph.
            capacity: Maximum forward flow, capped at the fleet size.
            travel_time: Primary per-unit cost in turns; zero within a zone.
            priority_cost: Secondary per-unit cost used to break travel-time
                ties. Lower values are preferred; the default is zero.
        """
        capacity = min(capacity, self._drone_count)
        forward = _Edge(
            source=source,
            destination=destination,
            reverse_index=len(self._graph[destination]),
            remaining_capacity=capacity,
            initial_capacity=capacity,
            travel_time=travel_time,
            priority_cost=priority_cost,
        )
        backward = _Edge(
            source=destination,
            destination=source,
            reverse_index=len(self._graph[source]),
            remaining_capacity=0,
            initial_capacity=0,
            travel_time=-travel_time,
            priority_cost=-priority_cost,
        )
        self._graph[source].append(forward)
        self._graph[destination].append(backward)

    def augment(self) -> bool:
        """Increase flow along the cheapest available residual path.

        Update residual capacities, lane_count, and total_travel_time.

        Returns:
            True if lanes were added, or False if no more are needed or found.
        """
        if self.lane_count == self._drone_count:
            return False
        path = self._shortest_path()
        if path is None:
            return False

        added_lanes = self._drone_count - self.lane_count
        for edge in path:
            added_lanes = min(added_lanes, edge.remaining_capacity)

        for edge in path:
            reverse_edge = self._graph[edge.destination][edge.reverse_index]
            edge.remaining_capacity -= added_lanes
            reverse_edge.remaining_capacity += added_lanes
            self.total_travel_time += added_lanes * edge.travel_time
        self.lane_count += added_lanes
        return True

    def _shortest_path(self) -> list[_Edge] | None:
        """Return the cheapest residual path using Bellman-Ford, or None.

        Compare costs by travel time first and priority cost second. Reverse
        edges may have negative costs, allowing earlier routes to be revised.

        Returns:
            The cheapest residual path as edges in start-to-end order, or
            None if no path with positive remaining capacity reaches the end.
        """
        node_count = len(self._graph)
        distances: list[tuple[int, int] | None] = [None] * node_count
        previous: list[_Edge | None] = [None] * node_count
        distances[self._start_node] = (0, 0)
        for _ in range(node_count - 1):
            changed = False
            for source, edges in enumerate(self._graph):
                distance = distances[source]
                if distance is None:
                    continue
                travel_time, priority_cost = distance
                for edge in edges:
                    if edge.remaining_capacity == 0:
                        continue
                    candidate = (
                        travel_time + edge.travel_time,
                        priority_cost + edge.priority_cost,
                    )
                    old_distance = distances[edge.destination]
                    if old_distance is None or candidate < old_distance:
                        distances[edge.destination] = candidate
                        previous[edge.destination] = edge
                        changed = True
            if not changed:
                break
        if distances[self._end_node] is None:
            return None
        return self._restore_path(previous)

    def _restore_path(self, previous: list[_Edge | None]) -> list[_Edge]:
        """Follow predecessors backward and return edges in travel order.

        Args:
            previous: Predecessor edges indexed by destination node, with
                None where no predecessor was recorded by the path search.

        Returns:
            A list of residual edges ordered from the start node to the end.
        """
        path: list[_Edge] = []
        current = self._end_node
        while current != self._start_node:
            edge = previous[current]
            if edge is None:
                raise RuntimeError("flow path is incomplete")
            path.append(edge)
            current = edge.source
        path.reverse()
        return path

    def paths(self) -> list[list[str]]:
        """Return one zone-name path per selected lane without changing flow.

        Returns:
            One start-to-end list of zone names per selected lane. Identical
            routes may appear more than once. If no lanes are selected,
            the result is an empty list.

        Raises:
            RuntimeError: If the current flow cannot be decomposed into paths.
        """
        remaining: list[list[int]] = []
        for edges in self._graph:
            used_capacities = []
            for edge in edges:
                used = edge.initial_capacity - edge.remaining_capacity
                used_capacities.append(max(0, used))
            remaining.append(used_capacities)

        paths: list[list[str]] = []
        for _ in range(self.lane_count):
            current = self._start_node
            path = [self._zone_names[current // 2]]
            while current != self._end_node:
                chosen_index = None
                for edge_index, used in enumerate(remaining[current]):
                    if used > 0:
                        chosen_index = edge_index
                        break
                if chosen_index is None:
                    raise RuntimeError("flow cannot be decomposed into paths")
                remaining[current][chosen_index] -= 1
                current = self._graph[current][chosen_index].destination
                if current % 2 == 0:
                    path.append(self._zone_names[current // 2])
            paths.append(path)
        return paths
