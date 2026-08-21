from src.map import Zone


class Drone():
    def __init__(
            self, id: int, c_zone: Zone,
            path: list[tuple[Zone, int]], state: str,
            max_turns: int) -> None:
        self._id: int = id
        self._zone: Zone = c_zone
        self._path: list[tuple[Zone, int]] = path
        self._state: str = state
        self._turns: int = max_turns

    def set_zone(self, new_zone: Zone) -> None:
        self._zone = new_zone

    def set_path(self, new_path: list[tuple[Zone, int]]) -> None:
        self._path = new_path

    def set_state(self, new_state: str) -> None:
        self._state = new_state

    def set_turns(self, cost: int) -> None:
        self._turns -= cost

    def get_turns(self) -> int:
        return self._turns
