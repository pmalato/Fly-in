import re
from typing import Any
from src.errors import (
    MissingSeperatorError,
    HubError,
    HubDetailsError,
    InvalidKeyError,
    DuplicateKeysError,
    DuplicateValues,
    MissingStartEndError,
    MatchError
    )


class Parser:
    def __init__(self) -> None:
        self._line_count: dict[str, int] = {}
        self._raw: dict[str, list[str]] = {}
        self._hub: dict[str, list[Any]] = {}
        self._connect: list[Any] = []

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
                    if key == "start_hub" and self._raw["start_hub"] or \
                            key == "end_hub" and self._raw["end_hub"]:
                        raise DuplicateKeysError(line_count,
                                                 "Invalid file format"
                                                 "There must exactly be 1 "
                                                 "'start_hub' and 1 'end_hub'")
                    if value in self._line_count:
                        raise DuplicateValues(line_count)
                    self._line_count |= {value: line_count}
                    if key in self._raw:
                        self._raw[key] += [value]
                    elif key == "nb_drones" or\
                            key.endswith("hub") or\
                            key == "connection":
                        self._raw |= {key: [value]}
                    else:
                        raise InvalidKeyError(line_count)
        if not self._raw["start_hub"] or not self._raw["end_hub"]:
            raise MissingStartEndError()

    def convert_hub(self) -> None:
        pattern: str = r"^(\S+)\s+(\d+)\s+(\d+)(?:\s+\[(.*?)\])?$"
        name: str = ""
        x: int
        y: int
        details: dict[str, Any] = {}
        arg1: str = ""
        arg2: str = ""
        arg3: str = ""
        words: list[str]
        for i in self._raw:
            for j in self._raw[i]:
                if i.endswith("hub"):
                    match = re.match(pattern, j)
                    if match:
                        name, arg1, arg2, arg3 = match.groups()
                        if not name or not arg1 or not arg2:
                            raise HubError(self._line_count[i])
                        try:
                            x = int(arg1)
                            y = int(arg2)
                            if arg3:
                                words = arg3.split(" ")
                                for k in words:
                                    if "=" not in words:
                                        raise HubDetailsError(
                                            self._line_count[i])
                                    key, value = k.split("=")
                                    if key != "zone" and \
                                            key != "color" and \
                                            key != "max_drones":
                                        raise HubDetailsError(
                                            self._line_count[i])
                                    # FIQUEI AQUI!!! Tratar de valid details values
                                    if key in details:
                                        raise DuplicateKeysError(
                                            self._line_count[i])
                                    if key == "max_drones":
                                        value = int(value)
                                    details |= {key: value}
                        except ValueError:
                            raise HubError(self._line_count[i])
                    else:
                        raise MatchError(self._line_count[i])
                else:
                    raise InvalidKeyError(self._line_count[i])

    def get_lines(self) -> dict[str, list[str]]:
        return self._raw

    def get_hubs(self) -> dict[str, list[Any]]:
        return self._hub
