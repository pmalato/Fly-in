from src.errors import UnsolveableMapError
from src.drone import Drone
from src.map import Map, Zone, Connection
from src.tracker import Tracker
from src.path_finder import PathFinder


class Scheduler():
    MAX_WAIT: int = 3
    MAX_TURNS: int = 500

    def __init__(self, tracker: Tracker, map: Map) -> None:
        self._tracker: Tracker = tracker
        self._map: Map = map
        self._start: Zone = map.get_start()
        self._goal: Zone = map.get_end()
        self._num_drones: int = map.get_drones()
        self._path_object: PathFinder = PathFinder(map)
        self._drone_list: list[Drone] = [Drone(
            f"D{y}", self._start) for y in range(1, self._num_drones + 1)]
        for x in self._drone_list:
            self._tracker.lock_zone(self._start, x)
        self._count: int = 0

    def check_everyone(self) -> bool:
        for x in self._drone_list:
            if x.get_state() != Drone.ARRIVED:
                return False
        return True

    def find_link(self, zone1: Zone, zone2: Zone) -> Connection | None:
        for x in self._tracker.get_link():
            if x.get_connection() == (zone1, zone2) or\
                    x.get_connection() == (zone2, zone1):
                return x
        return None

    def resolve_arrivals(
            self, arrived: list[tuple[Drone, Connection]]) -> None:
        temp_drone_list: list[Drone] = []
        for drone, link in arrived:
            temp_drone_list += [drone]
            drone.stop_transit()
            self._tracker.unlock_connection(
                drone, link, self._tracker.get_turn())
            if drone.get_current() == self._goal:
                drone.finish()

    def waiting_drones(self) -> None:
        arrival_turn: int
        czone: Zone | None
        cost: int
        nzone: Zone | None
        temp_link: Connection | None
        if not self.check_everyone():
            print(f"Turn {self._count + 1}:", end=" ")
        for x in self._drone_list:
            czone = x.get_current()
            nzone = x.get_next()
            if not czone or not nzone:
                continue
            temp_link = self.find_link(czone, nzone)
            if not temp_link:
                continue
            cost = self._map.get_hub_cost(nzone)
            if x.get_state() == Drone.IN_TRANSIT:
                print(
                    f"{x.get_id()}-"
                    f"{nzone.get_id()}",
                    end=" ")
                continue
            if not self._tracker.can_enter_zone(nzone) or \
                    not self._tracker.can_use_connection(temp_link):
                x.wait()
                if x.get_wait_turns() >= self.MAX_WAIT:
                    self.replan(x)
                continue
            if not self._tracker.can_use_connection(temp_link):
                continue
            arrival_turn = self._tracker.get_turn() + cost
            self._tracker.unlock_zone(czone, x)
            self._tracker.lock_zone(nzone, x)
            self._tracker.lock_connection(
                x, temp_link, arrival_turn)
            x.start_transit(nzone, arrival_turn)
            print(
                f"{x.get_id()}-"
                f"{temp_link.get_id() if cost > 1 else nzone.get_id()}",
                end=" ")

    def run(self) -> None:
        arrived: list[tuple[Drone, Connection]] = []
        for x in self._drone_list:
            path: list[Zone] = self._path_object.dijkstra_algo(self._start)
            self._path_object.reserve_path(path)
            x.set_path(path)
        while not self.check_everyone():
            if self._count > self.MAX_TURNS:
                raise UnsolveableMapError(
                    "Deadlock: Drones stuck for too many turns")
            arrived = self._tracker.advance_turn()
            self.resolve_arrivals(arrived)
            if self.check_everyone():
                break
            self.waiting_drones()
            print()
            self._count += 1

    def replan(self, drone: Drone) -> None:
        czone: Zone | None = drone.get_current()
        if not czone:
            return
        self._path_object.release_path(drone.get_remaining_path())
        new_path: list[Zone] = self._path_object.dijkstra_algo(czone)
        self._path_object.reserve_path(new_path)
        drone.set_path(new_path)
        drone.reset_wait()

    def get_count(self) -> int:
        return self._count
