from src.map import Zone


class Drone():
    """A single drone agent moving through the zone graph.

    Tracks the drone's current zone, its planned path, its transit
    state (waiting, in transit, arrived) and how many turns it has
    spent waiting, so the scheduler can decide when to replan it.
    """
    WAIT: str = "waiting"
    IN_TRANSIT: str = "in_transit"
    ARRIVED: str = "arrived"

    def __init__(self, id: str, c_zone: Zone) -> None:
        """Initialize a drone at its starting zone.

        Args:
            id: Unique identifier for the drone (e.g. "D1").
            c_zone: The zone the drone currently occupies.
        """
        self._id: str = id
        self._czone: Zone = c_zone
        self._state: str = Drone.WAIT
        self._path: list[Zone] = []
        self._nzone: Zone
        self._goal: Zone
        self._path_i: int = -1
        self._arrival_turn: int = 0
        self._wait_turns: int = 0

    def wait(self) -> None:
        """Increment the number of consecutive turns spent waiting"""
        self._wait_turns += 1

    def reset_wait(self) -> None:
        """Reset the number of consecutive tuns spent waiting to 0"""
        self._wait_turns = 0

    def set_path(self, new_path: list[Zone]) -> None:
        """Assign a new path to the drone and reset its progress along it.

        Args:
            new_path: Ordered list of zones from the drone's current
                position to its goal.
        """
        self._path = new_path
        self._czone = self._path[0]
        self._path_i = 0
        self._nzone = self._path[1]
        self._goal = self._path[-1]

    def start_transit(self, next_zone: Zone, arrival_turn: int) -> None:
        """Put the drone in transit toward the next zone on its path.

        Args:
            next_zone: The zone the drone is moving toward.
            arrival_turn: The simulation turn at which the drone will
                arrive at ``next_zone``.
        """
        self._state = Drone.IN_TRANSIT
        self._nzone = next_zone
        self._arrival_turn = arrival_turn

    def advance(self) -> None:
        """Move the internal path index forward and update the next zone."""
        self._path_i += 1
        if self._path_i + 1 < len(self._path):
            self._nzone = self._path[self._path_i + 1]

    def update_from_link(self) -> None:
        self._czone = self._nzone

    def stop_transit(self) -> None:
        """Complete the current transit, arriving at the next zone.

        Updates the drone's current zone to the previously targeted
        zone, resets its state to waiting, and advances the path
        index.
        """
        self._czone = self._nzone
        self._arrival_turn = -1
        self._state = Drone.WAIT
        self.advance()

    def finish(self) -> None:
        """Mark the drone as arrived at its final destination."""
        self._path = []
        self._path_i = 0
        self._state = Drone.ARRIVED

    def get_id(self) -> str:
        """Returns the drone's unique identifier."""
        return self._id

    def get_state(self) -> str:
        """Returns the drone's current state (waiting/in_transit/finished)"""
        return self._state

    def get_wait_turns(self) -> int:
        """Returns the amount of consecutive turns the drone has waited"""
        return self._wait_turns

    def get_current(self) -> Zone:
        """Returns the zone/hub where drone is at the moment"""
        return self._czone

    def get_remaining_path(self) -> list[Zone]:
        "Returns the path ahead for the drone to complete"
        return self._path[self._path_i:]

    def get_next(self) -> Zone:
        "Returns the zone the drone is aiming to traverse to"
        return self._nzone
