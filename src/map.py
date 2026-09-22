from src.parser import Parser
from typing import Any


class Zone():
    """A single node in the drone routing graph.

    Represents a hub parsed from the map file: its identifier,
    coordinates and metadata (zone type, color, max drone capacity).
    """
    def __init__(
            self, id: str, coord: tuple[int, int],
            metadata: dict[str, Any]) -> None:
        """Initialize a zone.

        Args:
            id: Unique name of the zone.
            coord: (x, y) integer coordinates of the zone.
            metadata: Dict with keys ``zone``, ``color`` and
                ``max_drones``.
        """
        self._id: str = id
        self._coord: tuple[int, int] = coord
        self._metadata: dict[str, Any] = metadata

    def get_id(self) -> str:
        """Return the zone's unique name."""
        return self._id

    def get_coordinates(self) -> tuple[int, int]:
        """Return the zone's (x, y) coordinates."""
        return self._coord

    def get_type(self) -> str:
        """Return the zone's type (normal, blocked, restricted, priority)."""
        return str(self._metadata["zone"])

    def get_color(self) -> str:
        """Return the zone's display color."""
        return str(self._metadata["color"])

    def get_max_drones(self) -> int:
        """Return the maximum number of drones the zone can hold at once."""
        return int(self._metadata["max_drones"])


class Connection():
    """A bidirectional edge linking two zones in the routing graph."""
    def __init__(
            self, id: str, zone1: Zone, zone2: Zone,
            metadata: dict[str, int]) -> None:
        """Initialize a connection.

        Args:
            id: Unique identifier for this connection (e.g. "link1").
            zone1: First zone linked by the connection.
            zone2: Second zone linked by the connection.
            metadata: Dict with the ``max_link_capacity`` key.
        """
        self._id = id
        self._connection: tuple[Zone, Zone] = zone1, zone2
        self._metadata: dict[str, int] = metadata

    def get_id(self) -> str:
        """Return the connection's unique identifier."""
        return self._id

    def get_connection(self) -> tuple[Zone, Zone]:
        """Return the pair of zones linked by this connection."""
        return self._connection

    def get_capacity(self) -> int:
        """Return the maximum number of drones that may use this
        connection simultaneously."""
        return self._metadata["max_link_capacity"]


class Map():
    """Builds and holds the full routing graph derived from a Parser.

    Turns the raw parsed hub/connection data into ``Zone``/``Connection``
    objects, an adjacency list, and a per-edge cost table used by the
    pathfinding algorithm.
    """
    def __init__(self, parsed: Parser) -> None:
        """Initialize the map from a parser instance.

        Args:
            parsed: A ``Parser`` that has already run ``start()``.
        """
        self._parsed: Parser = parsed
        self._drones = self._parsed.drone_count()
        self._hub_list: list[Zone] = []
        self._start: Zone
        self._end: Zone
        self._connections: list[Any] = []
        self._connection_list: list[Connection] = []
        self._adjacent: dict[Zone, list[tuple[Zone, int]]] = {}
        self._costs: dict[tuple[Zone, Zone], tuple[int, str]] = {}
        self._boundaries: tuple[int, int, int, int]

    def store_hubs(self) -> None:
        """Build ``Zone`` objects from the parsed hubs and identify the
        start and end zones."""
        hubs: dict[str, list[Any]] = self._parsed.get_hubs()
        temp: str
        for x in hubs:
            self._hub_list += [
                Zone(hubs[x][0], (hubs[x][1], hubs[x][2]), hubs[x][3])]
        for y in hubs:
            if y == "start_hub":
                temp = hubs[y][0]
                for z in self._hub_list:
                    if z.get_id() == temp:
                        self._start = z
        for i in hubs:
            if i == "end_hub":
                temp = hubs[i][0]
                for j in self._hub_list:
                    if j.get_id() == temp:
                        self._end = j

    def set_boundaries(self) -> None:
        """Compute the (min_x, min_y, max_x, max_y) bounding box of all
        hubs, after building the hub list."""
        self.store_hubs()
        hubs: dict[str, list[Any]] = self._parsed.get_hubs()
        starter: str = next(iter(hubs))
        min_x: int = hubs[starter][1]
        max_x: int = hubs[starter][1]
        min_y: int = hubs[starter][2]
        max_y: int = hubs[starter][2]
        for x in hubs:
            if hubs[x][1] < min_x:
                min_x = hubs[x][1]
            elif hubs[x][1] > max_x:
                max_x = hubs[x][1]
            if hubs[x][2] < min_y:
                min_y = hubs[x][2]
            elif hubs[x][2] > max_y:
                max_y = hubs[x][2]
        self._boundaries = min_x, min_y, max_x, max_y

    def find_hub(self, hub_name: str) -> Zone:
        """Find a zone by its name.

        Args:
            hub_name: Name of the zone to look up.

        Returns:
            The matching ``Zone``, or a placeholder "none" zone if no
            zone with that name exists.
        """
        for x in self._hub_list:
            if x.get_id() == hub_name:
                return x
        return Zone("none", (-1, -1), {"none": "none"})

    def store_connections(self) -> None:
        """Collect the raw parsed connection data, after computing
        boundaries."""
        self.set_boundaries()
        links: dict[str, list[Any]] = self._parsed.get_connection()
        for x in links:
            self._connections += [links[x]]

    def store_connection_list(self) -> list[Connection]:
        """Build ``Connection`` objects linking the appropriate zones.

        Returns:
            The list of ``Connection`` objects built.
        """
        self.store_connections()
        Hub1: Zone
        Hub2: Zone
        data: dict[str, int]
        i: int = 1
        for x in self._connections:
            Hub1 = self.find_hub(x[0][0])
            Hub2 = self.find_hub(x[0][1])
            data = x[1]
            self._connection_list += [Connection(f"link{i}", Hub1, Hub2, data)]
            i += 1
        return self._connection_list

    def make_links(self) -> None:
        """Build the bidirectional adjacency list from the connection
        list, mapping each zone to its neighbors and the link capacity."""
        temp: dict[Zone, list[tuple[Zone, int]]] = {}
        self.store_connection_list()
        for x in self._connection_list:
            if x.get_connection()[0] in self._adjacent:
                self._adjacent[x.get_connection()[0]] += [
                    (x.get_connection()[1],
                     x.get_capacity())]
                continue
            self._adjacent |= {
                x.get_connection()[0]:
                [(x.get_connection()[1],
                  x.get_capacity())]}
        for y in self._connection_list:
            if y.get_connection()[1] in temp:
                temp[y.get_connection()[1]] += [
                    (y.get_connection()[0],
                     y.get_capacity())]
                continue
            temp |= {
                y.get_connection()[1]:
                [(y.get_connection()[0],
                  y.get_capacity())]}
        for z in temp:
            if z in self._adjacent:
                for k in temp[z]:
                    self._adjacent[z] += [k]
                continue
            self._adjacent |= {z: temp[z]}

    def get_hub_cost(self, zone: Zone) -> int:
        """Return the movement cost, in turns, of entering a zone.

        Args:
            zone: The destination zone.

        Returns:
            1 for normal/priority zones, 2 for restricted zones, and
            -1 for any other (i.e. blocked) zone type.
        """
        if zone.get_type() == "normal" or\
                zone.get_type() == "priority":
            return 1
        elif zone.get_type() == "restricted":
            return 2
        else:
            return -1

    def define_link_cost(self) -> None:
        """Build the per-edge cost table (movement cost and destination
        zone type) for every adjacency, after building the links."""
        self.make_links()
        for x in self._adjacent:
            for y in self._adjacent[x]:
                self._costs |= {
                    (x, y[0]): (
                        self.get_hub_cost(y[0]), y[0].get_type())}

    def get_drones(self) -> int:
        """Return the total number of drones declared in the map file."""
        return self._drones

    def get_boundaries(self) -> tuple[int, int, int, int]:
        """Return the (min_x, min_y, max_x, max_y) bounding box of the
        map."""
        return self._boundaries

    def get_hubs(self) -> list[Zone]:
        """Return the list of all zones in the map."""
        return self._hub_list

    def get_connections(self) -> list[Connection]:
        """Return the list of all connections in the map."""
        return self._connection_list

    def get_start(self) -> Zone:
        """Return the start zone."""
        return self._start

    def get_end(self) -> Zone:
        """Return the end zone."""
        return self._end

    def get_adjacent(self) -> dict[Zone, list[tuple[Zone, int]]]:
        """Return the adjacency list mapping each zone to its neighbors
        and the corresponding link capacities."""
        return self._adjacent

    def get_costs(self) -> dict[tuple[Zone, Zone], tuple[int, str]]:
        """Return the per-edge cost table mapping (from_zone, to_zone) to
        (movement cost, destination zone type)."""
        return self._costs
