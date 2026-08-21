from src.map import Zone, Connection, Map


class PathFinder():
    def __init__(self) -> None:
        self._map_instance: Map = Map()
        self._map_instance.define_link_cost()
        self._hubs: list[Zone] = self._map_instance.get_hubs()
        self._start: Zone = self._map_instance.get_start()
        self._end: Zone = self._map_instance.get_end()
        self._adjancy: dict[Zone, list[Connection]]
        self._adjancy = self._map_instance.get_adjacent()
        self._cost: dict[tuple[Zone, Zone], tuple[int, str]]
        self._cost = self._map_instance.get_costs()

    def dijkstra_algo(self) -> None:
        ...
