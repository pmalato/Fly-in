from src.errors import UnsolveableMapError
from src.map import Zone, Map
from heapq import heappop, heappush


class PathFinder():
    def __init__(self, map: Map) -> None:
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

    def dijkstra_algo(self, current: Zone) -> list[Zone]:
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
                n_zone = y[0]
                if n_zone in visited or \
                        n_zone.get_type() == "blocked":
                    continue
                n_cost = self._cost[(c_zone, n_zone)][0]
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
