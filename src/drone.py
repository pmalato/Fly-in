from src.path_finder import PathFinder


class Drone():
    def __init__(self) -> None:
        self._id: int = 0
        self._zone: int = 0
        self._path: PathFinder
