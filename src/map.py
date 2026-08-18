from pathlib import Path
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
    def __init__(self) -> None:
        self._parsed: Parser = Parser()
        map_path = Path(__file__).resolve().parent / "maps" /\
            "challenger" / "01_the_impossible_dream.txt"
        self._parsed.file_reader(map_path)
        self._parsed.convert_hub()
        self._parsed.convert_connection()
        self._hub_list: list[Zone] = []
        self._connections: list[Any] = []
        self._connection_list: list[Connection] = []
        self._boundaries: tuple[int, int, int, int]

    def store_hubs(self) -> None:
        hubs: dict[str, list[Any]] = self._parsed.get_hubs()
        for x in hubs:
            self._hub_list += [
                Zone(hubs[x][0], (hubs[x][1], hubs[x][2]), hubs[x][3])]

    def find_hub(self, hub_name: str) -> Zone:
        for x in self._hub_list:
            if x.get_id() == hub_name:
                return x
        return Zone("none", (-1, -1), {"none": "none"})

    def store_links(self) -> None:
        links: dict[str, list[Any]] = self._parsed.get_connection()
        for x in links:
            self._connections += [links[x]]

    def get_link_list(self) -> list[Connection]:
        Hub1: Zone
        Hub2: Zone
        data: dict[str, int]
        for x in self._connections:
            Hub1 = self.find_hub(x[0][0])
            Hub2 = self.find_hub(x[0][1])
            data = x[1]
            self._connection_list += [Connection(Hub1, Hub2, data)]
        return self._connection_list

    def check_boundaries(self) -> tuple[int, int, int, int]:
        hubs: dict[str, list[Any]] = self._parsed.get_hubs()
        min_x: int = 0
        max_x: int = 0
        min_y: int = 0
        max_y: int = 0
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
        return self._boundaries
