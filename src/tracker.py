from src.drone import Drone
from src.map import Map, Zone, Connection


class Tracker():
    def __init__(self, map: Map) -> None:
        self._map: Map = map
        self._hubs: list[Zone] = map.get_hubs()
        self._links: list[Connection] = map.get_connections()
        self._turns: int = 0
        self._zone_occupancy: dict[Zone, set[Drone]]
        self._zone_occupancy = {x: set() for x in self._hubs}
        self._link_occupancy: dict[Connection, set[tuple[Drone, int]]]
        self._link_occupancy = {y: set() for y in self._links}

    def can_enter_zone(self, zone: Zone) -> bool:
        capacity: int = zone.get_max_drones()
        return len(self._zone_occupancy[zone]) < capacity

    def can_use_connection(self, link: Connection) -> bool:
        capacity: int = link.get_capacity()
        return len(self._link_occupancy[link]) < capacity

    def lock_zone(self, zone: Zone, drone: Drone) -> None:
        self._zone_occupancy[zone] |= {drone}

    def unlock_zone(self, zone: Zone, drone: Drone) -> None:
        self._zone_occupancy[zone].remove(drone)

    def lock_connection(
            self, drone: Drone, link: Connection, arrival_turn: int) -> None:
        self._link_occupancy[link] |= {(drone, arrival_turn)}

    def unlock_connection(
            self, drone: Drone, link: Connection, arrival_turn: int) -> None:
        self._link_occupancy[link].remove((drone, arrival_turn))

    def advance_turn(self) -> list[tuple[Drone, Connection]]:
        successful_moves: list[tuple[Drone, Connection]] = []
        self._turns += 1
        for key, value in self._link_occupancy.items():
            for drone, turn in value:
                if turn == self._turns:
                    successful_moves += [(drone, key)]
        return successful_moves
