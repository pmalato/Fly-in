import copy
import re
from typing import Any
from src.errors import (
    MissingDroneCountError,
    MissingSeperatorError,
    PositiveIntError,
    HubError,
    HubDetailsError,
    InvalidKeyError,
    DuplicateKeysError,
    HubDetailsZoneError,
    NonExistentNameError,
    ConnectionDetailError,
    DuplicateHubNameError,
    DuplicateCoordinatesError,
    DuplicateConnectionError,
    MissingStartEndError,
    MatchError
    )


class Parser:
    def __init__(self) -> None:
        self._line_count: dict[str, int] = {}
        self._drone_count: int = 0
        self._raw: dict[str, list[str]] = {}
        self._hub: dict[str, list[Any]] = {}
        self._connect: dict[str, list[Any]] = {}

    def file_reader(self, file_name: str) -> None:
        line_count: int = 0
        with open(file_name, "r") as file:
            text: list[str] = file.readlines()
            for line in text:
                line = line.strip()
                line_count += 1
                if line.startswith("#") or line == "":
                    continue
                if ": " not in line:
                    raise MissingSeperatorError(line_count)
                else:
                    key, value = line.split(": ")
                    if key == "start_hub" and "start_hub" in self._raw or \
                            key == "end_hub" and "end_hub" in self._raw:
                        raise DuplicateKeysError(line_count,
                                                 "Invalid file format"
                                                 "There must exactly be 1 "
                                                 "'start_hub' and 1 'end_hub'")
                    elif key in self._raw:
                        key = f"{line_count}" + key
                    self._line_count |= {value: line_count}
                    if key == "nb_drones" or\
                            key.endswith("hub") or\
                            key.endswith("connection"):
                        self._raw |= {key: [value]}
                    else:
                        raise InvalidKeyError(line_count)
        if "end_hub" not in self._raw or "start_hub" not in self._raw:
            raise MissingStartEndError()

    def drone_count(self) -> int:
        if not self._raw["nb_drones"]:
            raise MissingDroneCountError()
        self._drone_count = int(self._raw["nb_drones"][0])
        if self._drone_count <= 0:
            raise PositiveIntError(self._line_count["nb_drones"])
        return self._drone_count

    def duplicate_coordinates(self, x: int, y: int) -> str:
        for i in self._hub:
            for _ in self._hub[i]:
                k, z = self._hub[i][1], self._hub[i][2]
                if k == x and z == y:
                    return i
        return ""

    def duplicate_name(self, name: str) -> "str":
        for i in self._hub:
            if self._hub[i][0] == name:
                return i
        return ""

    def duplicate_connections(self, name1: str, name2: str) -> str:
        for i in self._connect:
            if self._connect[i][0] == {name1: name2} or\
                    self._connect[i][0] == {name2: name1}:
                return i
        return ""

    def convert_hub(self) -> None:
        new_dict: dict[str, list[Any]] = {}
        for i in self._raw:
            if i.endswith("hub"):
                new_dict[i] = copy.deepcopy(self._raw[i])
        pattern: str = r"^(\S+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[(.*?)\])?$"
        name: str = ""
        x: int
        y: int
        details: dict[str, Any] = {}
        arg1: str = ""
        arg2: str = ""
        arg3: str = ""
        words: list[str]
        for i in new_dict:
            for j in new_dict[i]:
                match = re.match(pattern, j)
                if match:
                    name, arg1, arg2, arg3 = match.groups()
                    if self.duplicate_name(name) != "":
                        raise DuplicateHubNameError(
                            self.duplicate_name(name), self._line_count[j])
                    if not name or not arg1 or not arg2:
                        raise HubError(self._line_count[j])
                    try:
                        x = int(arg1)
                        y = int(arg2)
                        if self.duplicate_coordinates(x, y) != "":
                            raise DuplicateCoordinatesError(
                                self.duplicate_coordinates(x, y),
                                self._line_count[j])
                        details = {}
                        if arg3:
                            words = arg3.split(" ")
                            for k in words:
                                if "=" not in k:
                                    raise HubDetailsError(
                                        self._line_count[j])
                                key, value = k.split("=")
                                if key != "zone" and \
                                        key != "color" and \
                                        key != "max_drones":
                                    raise HubDetailsError(
                                        self._line_count[j])
                                if key == "zone" and not \
                                        (value == "normal" or
                                            value == "blocked" or
                                            value == "restricted" or
                                            value == "priority"):
                                    raise HubDetailsZoneError(
                                        self._line_count[j])
                                if key in details:
                                    raise DuplicateKeysError(
                                        self._line_count[j])
                                if key == "max_drones":
                                    if i == "start_hub" or\
                                            i == "end_hub":
                                        continue
                                    value = int(value)
                                    if value <= 0:
                                        raise PositiveIntError(
                                            self._line_count[j])
                                details |= {key: value}
                    except ValueError:
                        raise HubError(self._line_count[j])
                else:
                    raise MatchError(self._line_count[j])
                self._hub |= {i: [name, x, y, details]}

    def convert_connection(self) -> None:
        new_dict: dict[str, list[Any]] = {}
        for i in self._raw:
            if i.endswith("connection"):
                new_dict[i] = copy.deepcopy(self._raw[i])
        pattern: str = r"^(\S+)-(\S+)(?:\s+\[+(\S+)\])?$"
        name1: str = ""
        name2: str = ""
        arg3: str = ""
        detail: dict[str, int]
        for i in new_dict:
            for j in new_dict[i]:
                match = re.match(pattern, j)
                if match:
                    name1, name2, arg3 = match.groups()
                    if self.duplicate_connections(name1, name2) != "":
                        raise DuplicateConnectionError(
                            self.duplicate_connections(name1, name2),
                            self._line_count[j])
                    if self.duplicate_name(name1) == "" or\
                            self.duplicate_name(name2) == "":
                        raise NonExistentNameError(
                            name1, name2, self._line_count[j])
                    detail = {}
                    if arg3:
                        if "=" not in arg3:
                            raise ConnectionDetailError(self._line_count[j])
                        else:
                            key, value = arg3.split("=")
                            if key in detail:
                                raise DuplicateKeysError(self._line_count[j])
                            if key != "max_link_capacity":
                                raise ConnectionDetailError(
                                    self._line_count[j])
                            try:
                                value = int(value)
                                if value <= 0:
                                    raise PositiveIntError(self._line_count[j])
                            except ValueError:
                                raise ConnectionDetailError(
                                    self._line_count[j])
                        detail |= {key: value}
                    if detail != {}:
                        self._connect |= {i: [{name1: name2}, detail]}
                    else:
                        self._connect |= {i: [{name1: name2}]}
                else:
                    raise MatchError(self._line_count[j])

    def get_lines(self) -> dict[str, list[str]]:
        return self._raw

    def get_hubs(self) -> dict[str, list[Any]]:
        return self._hub

    def get_connection(self) -> dict[str, list[Any]]:
        return self._connect
