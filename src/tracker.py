from src.map import Map


class Trcaker():
    def __init__(self) -> None:
        self._turns: int = 0
        self._c_map: Map = Map()
