from src.drone import Drone
from src.map import Map, Zone
from src.tracker import Tracker
from src.path_finder import PathFinder


class Scheduler():
    def __init__(self, tracker: Tracker, map: Map) -> None:
        self._tracker: Tracker = tracker
        self._map: Map = map
        self._start: Zone = map.get_start()
        self._num_drones: int = map.get_drones()
        self._path_list: list[PathFinder] = [
            PathFinder(map) for _ in range(0, self._num_drones)]
        self._drone_list: list[Drone] = [Drone(
            f"D{y}", self._start) for y in range(1, self._num_drones + 1)]
