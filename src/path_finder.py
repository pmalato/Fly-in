from src.errors import UnsolveableMapError
from src.map import Zone, Map
from heapq import heappop, heappush


class PathFinder():
    """Computes congestion-aware shortest paths through the zone graph.

    Wraps a hand-rolled Dijkstra implementation whose edge costs grow
    with how many drones already occupy a destination zone or are
    scheduled on a given connection, so drones routed later are
    naturally steered around congestion created by earlier ones.
    """
    def __init__(self, map: Map) -> None:
        """Initialize the path finder from a built ``Map``.

        Args:
            map: A ``Map`` whose adjacency and cost tables have been
                built (e.g. via ``define_link_cost``).
        """
        self._map: Map = map
        self._drones = self._map.get_drones()
        self._hubs: list[Zone] = self._map.get_hubs()
        self._start: Zone = self._map.get_start()
        self._end: Zone = self._map.get_end()
        self._adjancy: dict[Zone, list[tuple[Zone, int]]]
        self._adjancy = self._map.get_adjacent()
        self._cost: dict[tuple[Zone, Zone], tuple[int, str]]
        self._cost = self._map.get_costs()
        self._counter: int = 0
        self._zone_load: dict[Zone, int] = {}
        self._link_load: dict[tuple[Zone, Zone], int] = {}

    def edge_cost(self, czone: Zone, nzone: Zone, cost: int) -> int:
        """Compute the effective cost of moving from one zone to another.

        Adds to the base movement cost extra wait turns proportional to
        how congested the destination zone and the connection used
        currently are.

        Args:
            czone: The zone the drone is moving from.
            nzone: The zone the drone is moving to.
            cost: The capacity of the connection between the two zones.

        Returns:
            The total number of turns this move is expected to cost.
        """
        base: int = self._cost[(czone, nzone)][0]
        link: tuple[Zone, Zone]
        zone_wait: int = 0
        if nzone != self._end:
            capacity: int = nzone.get_max_drones()
            load: int = self._zone_load.get(nzone, 0)
            zone_wait = load // capacity
        if (czone, nzone) in self._link_load:
            link = czone, nzone
        else:
            link = nzone, czone
        link_wait: int = self._link_load.get(link, 0) // cost
        return base + max(zone_wait, link_wait)

    def reserve_path(self, path: list[Zone]) -> None:
        """Increment the load counters for every edge along a path.

        Args:
            path: Ordered list of zones a drone will travel through.
        """
        for i in range(0, len(path) - 1):
            czone, nzone = path[i], path[i + 1]
            if nzone != self._end:
                self._zone_load[nzone] = self._zone_load.get(nzone, 0) + 1
            key: tuple[Zone, Zone] = czone, nzone
            self._link_load[key] = self._link_load.get(key, 0) + 1

    def release_path(self, path: list[Zone]) -> None:
        """Decrement the load counters for every edge along a path.

        Args:
            path: Ordered list of zones to release the reservation for.
        """
        for i in range(0, len(path) - 1):
            czone, nzone = path[i], path[i + 1]
            if nzone != self._end:
                self._zone_load[nzone] = self._zone_load.get(nzone, 0) - 1
            key: tuple[Zone, Zone] = czone, nzone
            self._link_load[key] = self._link_load.get(key, 0) - 1

    def dijkstra_algo(self, current: Zone) -> list[Zone]:
        """Compute the least-cost path from a zone to the end zone.

        Runs a Dijkstra search over the adjacency graph using a binary
        heap, with ``priority`` zones given precedence on cost ties,
        and congestion-aware edge costs from ``edge_cost``.

        Args:
            current: The zone to start the search from.

        Returns:
            The ordered list of zones from ``current`` to the end zone
            (inclusive of both).

        Raises:
            UnsolveableMapError: If no path to the end zone exists.
        """
        distance: dict[Zone, int] = {}
        predecessor: dict[Zone, Zone] = {}
        visited: set[Zone] = set()
        heap_queue: list[tuple[int, int, int, Zone]] = []
        cost: int = 0
        n_cost: int
        new_cost: int
        priority: int = 1
        c_zone: Zone
        n_zone: Zone
        new_list: list[Zone] = []
        i: int = 0
        distance[current] = 0
        heappush(heap_queue, (cost, priority, self._counter, current))
        while self._end not in visited:
            if not heap_queue:
                raise UnsolveableMapError()
            cost, _, _, c_zone = heappop(heap_queue)
            if c_zone in visited:
                continue
            visited |= {c_zone}
            if c_zone == self._end:
                break
            for y in self._adjancy[c_zone]:
                n_zone, link_cost = y
                if n_zone in visited or \
                        n_zone.get_type() == "blocked":
                    continue
                n_cost = self.edge_cost(c_zone, n_zone, link_cost)
                new_cost = cost + n_cost
                if new_cost < distance.get(n_zone, float('inf')):
                    distance[n_zone] = new_cost
                    if n_zone.get_type() == "priority":
                        priority = 0
                    else:
                        priority = 1
                    self._counter += 1
                    predecessor[n_zone] = c_zone
                    heappush(
                        heap_queue,
                        (new_cost, priority, self._counter, n_zone))
        new_list += [self._end]
        while new_list[i] != current:
            new_list += [predecessor[new_list[i]]]
            i += 1
        return new_list[::-1]
