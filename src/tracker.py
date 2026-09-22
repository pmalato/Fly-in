from src.drone import Drone
from src.map import Map, Zone, Connection


class Tracker():
    """Enforces zone and connection capacity constraints at runtime.

    Keeps track, turn by turn, of which drones occupy which zones and
    connections, and exposes the checks the scheduler needs to decide
    whether a move is currently legal.
    """
    def __init__(self, map: Map) -> None:
        """Initialize the tracker with empty occupancy for every zone
        and connection.

        Args:
            map: The built ``Map`` whose zones and connections are to
                be tracked.
        """
        self._map: Map = map
        self._hubs: list[Zone] = map.get_hubs()
        self._links: list[Connection] = map.get_connections()
        self._turn: int = 0
        self._zone_occupancy: dict[Zone, set[Drone]]
        self._zone_occupancy = {x: set() for x in self._hubs}
        self._link_occupancy: dict[Connection, set[tuple[Drone, int]]]
        self._link_occupancy = {y: set() for y in self._links}

    def can_enter_zone(self, zone: Zone) -> bool:
        """Check whether a zone has free capacity for another drone.

        Args:
            zone: The zone to check.

        Returns:
            True if the zone's current occupancy is below its maximum
            capacity.
        """
        capacity: int = zone.get_max_drones()
        return len(self._zone_occupancy[zone]) < capacity

    def can_use_connection(self, link: Connection) -> bool:
        """Check whether a connection has free capacity for another drone.

        Args:
            link: The connection to check.

        Returns:
            True if the connection's current usage is below its
            maximum capacity.
        """
        capacity: int = link.get_capacity()
        return len(self._link_occupancy[link]) < capacity

    def lock_zone(self, zone: Zone, drone: Drone) -> None:
        """Mark a zone as occupied by a drone.

        Args:
            zone: The zone being entered.
            drone: The drone entering the zone.
        """
        self._zone_occupancy[zone] |= {drone}

    def unlock_zone(self, zone: Zone, drone: Drone) -> None:
        """Release a drone's occupancy of a zone.

        Args:
            zone: The zone being left.
            drone: The drone leaving the zone.
        """
        self._zone_occupancy[zone].remove(drone)

    def lock_connection(
            self, drone: Drone, link: Connection, arrival_turn: int) -> None:
        """Reserve a connection slot for a drone in transit.

        Args:
            drone: The drone using the connection.
            link: The connection being used.
            arrival_turn: The turn at which the drone will finish
                traversing the connection.
        """
        self._link_occupancy[link] |= {(drone, arrival_turn)}

    def unlock_connection(
            self, drone: Drone, link: Connection, arrival_turn: int) -> None:
        """Release a drone's reserved slot on a connection.

        Args:
            drone: The drone that finished using the connection.
            link: The connection that was used.
            arrival_turn: The arrival turn the reservation was made
                under.
        """
        self._link_occupancy[link].remove((drone, arrival_turn))

    def advance_turn(self) -> list[tuple[Drone, Connection]]:
        """Advance the simulation clock by one turn.

        Returns:
            The list of (drone, connection) pairs whose transit ends
            on the new current turn.
        """
        successful_moves: list[tuple[Drone, Connection]] = []
        self._turn += 1
        for key, value in self._link_occupancy.items():
            for drone, turn in value:
                if turn == self._turn:
                    successful_moves += [(drone, key)]
        return successful_moves

    def get_turn(self) -> int:
        """Return the current simulation turn number."""
        return self._turn

    def get_link(self) -> list[Connection]:
        """Return the list of all connections in the map."""
        return self._links
