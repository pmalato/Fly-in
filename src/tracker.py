from src.map import Map


class Tracker():
    def __init__(self, map: Map) -> None:
        self._map: Map = map
        self._turns: int = 0
