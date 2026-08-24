from src.map import Zone


class Drone():
    def __init__(
            self, id: str, c_zone: Zone,
            path: list[Zone], state: str,
            max_turns: int) -> None:
        self._id: str = id
        self._zone: Zone = c_zone
        self._path: list[Zone] = path
        self._state: str = state
        self._turns: int = max_turns

    def set_zone(self, new_zone: Zone) -> None:
        self._zone = new_zone

    def set_path(self, new_path: list[Zone]) -> None:
        self._path = new_path

    def set_state(self, new_state: str) -> None:
        self._state = new_state

    def set_turns(self, cost: int) -> None:
        self._turns -= cost

    def get_id(self) -> str:
        return self._id

    def get_turns(self) -> int:
        return self._turns
