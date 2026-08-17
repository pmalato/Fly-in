from pathlib import Path
from src.parser import Parser
from typing import Any


class Map():
    def __init__(self) -> None:
        self._parsed: Parser = Parser()
        map_path = Path(__file__).resolve().parent / "maps" /\
            "challenger" / "01_the_impossible_dream.txt"
        self._parsed.file_reader(map_path)
        self._parsed.convert_hub()
        self._parsed.convert_connection()
        self._boundaries: tuple[int, int, int, int]
        self._hubs: dict[str, list[Any]] = {}
        self._connections: list[Any] = []

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

    def get_hub(self) -> dict[str, list[Any]]:
        hubs: dict[str, list[Any]] = self._parsed.get_hubs()
        for x in hubs:
            self._hubs |= {hubs[x][0]: [(hubs[x][1], hubs[x][2]), hubs[x][3]]}
        return self._hubs

    def get_link(self) -> list[Any]:
        links: dict[str, list[Any]] = self._parsed.get_connection()
        for x in links:
            self._connections += [links[x]]
        return self._connections
