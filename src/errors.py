class FlyInError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MissingDroneCountError(FlyInError):
    def __init__(self, message: str = "Missing 'nb_drones' key") -> None:
        super().__init__(message)


class MissingSeperatorError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Missing valid seperator") -> None:
        super().__init__(f"{message}, line {lineno}")


class PositiveIntError(FlyInError):
    def __init__(self, lineno: int, message: str = "Integer value must "
                 "be positive") -> None:
        super().__init__(f"{message}, line {lineno}")


class HubError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Hub must follow the structure 'hub_name: "
                 "name(str) x_value(positive int) "
                 "y_value(positive int) [optional_details]'"
                 ) -> None:
        super().__init__(f"{message}, line {lineno}")


class HubDetailsError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Hub details are optional, but they must follow "
                 "'zone=value(str)' or 'color=value(str)'"
                 " or 'max_capacity=value(positive int)'"
                 ) -> None:
        super().__init__(f"{message}, line {lineno}")


class HubDetailsZoneError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Acceptable zone values:\n"
                 "'normal', 'blocked', 'restricted' and 'priority'") -> None:
        super().__init__(f"{message}, line {lineno}")


class NonExistentNameError(FlyInError):
    def __init__(self, name1: str, name2: str, lineno: int,
                 message: str = "Invalid file format -") -> None:
        super().__init__(f"{message} {name1} or {name2} are non-existent hubs,"
                         f" line {lineno}")


class ConnectionDetailError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Coonection detail is optional, but should follow "
                 "'max_link_capacity=value(int)' format") -> None:
        super().__init__(f"{message}, line {lineno}")


class InvalidKeyError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid Key") -> None:
        super().__init__(f"{message}, line {lineno}")


class InvalidConnectionError(FlyInError):
    def __init__(self, lineno: int,
                 message: str = "Invalid file format - "
                 "You can't link to the same hub") -> None:
        super().__init__(f"{message}, line {lineno}")


class MissingStartEndError(FlyInError):
    def __init__(self, message: str = "Invalid file format - "
                 "Missing 'start_hub' or 'end_hub'") -> None:
        super().__init__(message)


class DuplicateKeysError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Duplicate Keys") -> None:
        super().__init__(f"{message}, line {lineno}")


class DuplicateHubNameError(FlyInError):
    def __init__(self, hub: str, lineno: int,
                 message: str = "Invalid file format - "
                 "Duplicate hub_name") -> None:
        super().__init__(f"{message}, hub {hub} line {lineno}")


class DuplicateCoordinatesError(FlyInError):
    def __init__(self, hub: str, lineno: int,
                 message: str = "Invalid file format - "
                 "Duplicate coordinates found") -> None:
        super().__init__(f"{message}, hub {hub} line {lineno}")


class DuplicateConnectionError(FlyInError):
    def __init__(
            self, connection: str, lineno: int,
            message: str = "Invalid file format - Duplicate connection found"
            ) -> None:
        super().__init__(f"{message}, connection {connection} line {lineno}")


class MatchError(FlyInError):
    def __init__(self, lineno: int, message: str = "Error while matching"
                 ) -> None:
        super().__init__(f"{message}, line {lineno}")


class UnsolveableMapError(FlyInError):
    def __init__(self, message: str = "Unsolvable map") -> None:
        super().__init__(message)
