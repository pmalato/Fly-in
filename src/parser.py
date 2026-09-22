import sys
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
    InvalidConnectionError,
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
    """Reads and validates the custom map file format.

    Reads the file given as the first command-line argument, splits it
    into raw key/value lines, then converts the hub and connection
    lines into structured data ready to be consumed by ``Map``.
    """
    def __init__(self) -> None:
        """Initialize the parser, reading the map file path from
        ``sys.argv[1]``."""
        self._filename: str = sys.argv[1]
        self._line_count: dict[str, int] = {}
        self._drone_count: int = 0
        self._raw: dict[str, list[str]] = {}
        self._hub: dict[str, list[Any]] = {}
        self._connect: dict[str, list[Any]] = {}

    def file_reader(self) -> None:
        """Read the map file line by line and populate ``self._raw``.

        Validates that each non-comment, non-blank line has a
        ``key: value`` separator, that ``start_hub``/``end_hub`` are not
        duplicated, and that recognized keys are used. Raises the
        appropriate ``FlyInError`` subclass on any violation.
        """
        line_count: int = 0
        with open(self._filename, "r") as file:
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
        """Parse and validate the number of drones.

        Returns:
            The number of drones declared by ``nb_drones``.

        Raises:
            MissingDroneCountError: If ``nb_drones`` is missing/empty.
            PositiveIntError: If the value is not a positive integer.
        """
        if not self._raw["nb_drones"]:
            raise MissingDroneCountError()
        self._drone_count = int(self._raw["nb_drones"][0])
        if self._drone_count <= 0:
            raise PositiveIntError(self._line_count["nb_drones"])
        return self._drone_count

    def duplicate_coordinates(self, x: int, y: int) -> str:
        """Check whether a hub already exists at the given coordinates.

        Args:
            x: X coordinate to check.
            y: Y coordinate to check.

        Returns:
            The key of the hub already at these coordinates, or an
            empty string if none exists.
        """
        for i in self._hub:
            for _ in self._hub[i]:
                k, z = self._hub[i][1], self._hub[i][2]
                if k == x and z == y:
                    return i
        return ""

    def duplicate_name(self, name: str) -> "str":
        """Check whether a hub with the given name already exists.

        Args:
            name: Hub name to check.

        Returns:
            The key of the hub with that name, or an empty string if
            none exists.
        """
        for i in self._hub:
            if self._hub[i][0] == name:
                return i
        return ""

    def duplicate_connections(self, name1: str, name2: str) -> str:
        """Check whether a connection between two hubs already exists.

        Args:
            name1: First hub name.
            name2: Second hub name.

        Returns:
            The key of the existing connection (in either direction),
            or an empty string if none exists.
        """
        for i in self._connect:
            if self._connect[i][0] == {name1: name2} or\
                    self._connect[i][0] == {name2: name1}:
                return i
        return ""

    def convert_hub(self) -> None:
        """Parse all raw hub lines into structured hub data.

        Validates the hub line syntax, coordinates, and metadata
        (``zone``, ``color``, ``max_drones``), applying defaults where
        needed and raising the appropriate ``FlyInError`` subclass on
        any violation. Populates ``self._hub``.
        """
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
                            if "zone" not in details:
                                details |= {"zone": "normal"}
                            if "color" not in details:
                                details |= {"color": None}
                            if "max_drones" not in details:
                                details |= {"max_drones": 1}
                        else:
                            details |= {
                                "zone": "normal",
                                "color": None,
                                "max_drones": 1
                            }
                    except ValueError:
                        raise HubError(self._line_count[j])
                else:
                    raise MatchError(self._line_count[j])
                if i == "start_hub" or i == "end_hub":
                    details["max_drones"] = sys.maxsize
                self._hub |= {i: [name, x, y, details]}

    def convert_connection(self) -> None:
        """Parse all raw connection lines into structured connection data.

        Validates the connection line syntax, that the linked hubs
        exist and are not identical, that the connection is not a
        duplicate, and that any ``max_link_capacity`` metadata is a
        positive integer. Populates ``self._connect``.
        """
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
                    if name1 == name2:
                        raise InvalidConnectionError(self._line_count[j])
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
                    else:
                        detail |= {"max_link_capacity": 1}
                    self._connect |= {i: [(name1, name2), detail]}
                else:
                    raise MatchError(self._line_count[j])

    def start(self) -> None:
        """Run the full parsing pipeline: read the file, then convert
        hubs and connections into structured data."""
        self.file_reader()
        self.convert_hub()
        self.convert_connection()

    def get_lines(self) -> dict[str, list[str]]:
        """Return the raw parsed ``key: value`` lines."""
        return self._raw

    def get_hubs(self) -> dict[str, list[Any]]:
        """Return the structured hub data keyed by their raw file key."""
        return self._hub

    def get_connection(self) -> dict[str, list[Any]]:
        """Return the structured connection data keyed by their raw file
        key."""
        return self._connect
