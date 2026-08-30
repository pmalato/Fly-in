from src.map import Zone


class Drone():
    WAIT: str = "waiting"
    IN_TRANSIT: str = "in_transit"
    ARRIVED: str = "arrived"

    def __init__(self, id: str, c_zone: Zone) -> None:
        self._id: str = id
        self._czone: Zone | None = c_zone
        self._state: str = Drone.WAIT
        self._path: list[Zone] = []
        self._nzone: Zone | None = None
        self._goal: Zone | None = None
        self._path_i: int = -1
        self._arrival_turn: int = 0

    def set_path(self, new_path: list[Zone]) -> None:
        self._path = new_path
        self._czone = self._path[0]
        self._path_i = 0
        self._nzone = self._path[1]
        self._goal = self._path[-1]

    def start_transit(self, next_zone: Zone, arrival_turn: int) -> None:
        self._state = Drone.IN_TRANSIT
        self._nzone = next_zone
        self._arrival_turn = arrival_turn

    def advance(self) -> None:
        self._path_i += 1
        if self._path_i + 1 < len(self._path):
            self._nzone = self._path[self._path_i + 1]
        else:
            self._nzone = None

    def stop_transit(self) -> None:
        self._czone = self._nzone
        self._arrival_turn = -1
        self._state = Drone.WAIT
        self.advance()

    def finish(self) -> None:
        self._path = []
        self._nzone = None
        self._path_i = 0
        self._state = Drone.ARRIVED

    def get_id(self) -> str:
        return self._id

    def get_state(self) -> str:
        return self._state

    def get_current(self) -> Zone | None:
        return self._czone

    def get_next(self) -> Zone | None:
        return self._nzone
