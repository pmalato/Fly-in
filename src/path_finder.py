from src.map import Zone, Map


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

    def dijkstra_algo(self) -> None:
        ...
