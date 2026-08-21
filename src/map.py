from src.parser import Parser
from typing import Any


class Zone():
    def __init__(
            self, id: str, coord: tuple[int, int],
            metadata: dict[str, Any]) -> None:
        self._id: str = id
        self._coord: tuple[int, int] = coord
        self._metadata: dict[str, Any] = metadata

    def get_id(self) -> str:
        return self._id

    def get_coordinates(self) -> tuple[int, int]:
        return self._coord

    def get_metadata(self) -> dict[str, Any]:
        return self._metadata


class Connection():
    def __init__(
            self, zone1: Zone, zone2: Zone,
            metadata: dict[str, int]) -> None:
        self._connection: tuple[Zone, Zone] = zone1, zone2
        self._metadata: dict[str, int] = metadata

    def get_connection(self) -> tuple[Zone, Zone]:
        return self._connection

    def get_metadata(self) -> dict[str, int]:
        return self._metadata


class Map():
    def __init__(self, parsed: Parser) -> None:
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
        for x in self._hub_list:
            if x.get_id() == hub_name:
                return x
        return Zone("none", (-1, -1), {"none": "none"})

    def store_connections(self) -> None:
        self.set_boundaries()
        links: dict[str, list[Any]] = self._parsed.get_connection()
        for x in links:
            self._connections += [links[x]]

    def store_connection_list(self) -> list[Connection]:
        self.store_connections()
        Hub1: Zone
        Hub2: Zone
        data: dict[str, int]
        for x in self._connections:
            Hub1 = self.find_hub(x[0][0])
            Hub2 = self.find_hub(x[0][1])
            data = x[1]
            self._connection_list += [Connection(Hub1, Hub2, data)]
        return self._connection_list

    def make_links(self) -> None:
        temp: dict[Zone, list[tuple[Zone, int]]] = {}
        self.store_connection_list()
        for x in self._connection_list:
            if x.get_connection()[0] in self._adjacent:
                self._adjacent[x.get_connection()[0]] += [
                    (x.get_connection()[1],
                     x.get_metadata()["max_link_capacity"])]
                continue
            self._adjacent |= {
                x.get_connection()[0]:
                [(x.get_connection()[1],
                  x.get_metadata()["max_link_capacity"])]}
        for y in self._connection_list:
            if y.get_connection()[1] in temp:
                temp[y.get_connection()[1]] += [
                    (y.get_connection()[0],
                     y.get_metadata()["max_link_capacity"])]
                continue
            temp |= {
                y.get_connection()[1]:
                [(y.get_connection()[0],
                  y.get_metadata()["max_link_capacity"])]}
        for z in temp:
            if z in self._adjacent:
                for k in temp[z]:
                    self._adjacent[z] += [k]
                continue
            self._adjacent |= {z: temp[z]}

    def get_hub_cost(self, zone: Zone) -> int:
        if zone.get_metadata()["zone"] == "normal" or\
                zone.get_metadata()["zone"] == "priority":
            return 1
        elif zone.get_metadata()["zone"] == "restricted":
            return 2
        else:
            return -1

    def define_link_cost(self) -> None:
        self.make_links()
        for x in self._adjacent:
            for y in self._adjacent[x]:
                self._costs |= {
                    (x, y[0]): (
                        self.get_hub_cost(y[0]), y[0].get_metadata()["zone"])}
                self._costs |= {
                    (y[0], x): (
                        self.get_hub_cost(x), y[0].get_metadata()["zone"])}

    def get_drones(self) -> int:
        return self._drones

    def get_boundaries(self) -> tuple[int, int, int, int]:
        return self._boundaries

    def get_hubs(self) -> list[Zone]:
        return self._hub_list

    def get_start(self) -> Zone:
        return self._start

    def get_end(self) -> Zone:
        return self._end

    def get_adjacent(self) -> dict[Zone, list[tuple[Zone, int]]]:
        return self._adjacent

    def get_costs(self) -> dict[tuple[Zone, Zone], tuple[int, str]]:
        return self._costs
