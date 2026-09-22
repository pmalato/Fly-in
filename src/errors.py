class FlyInError(Exception):
    """Base class for all custom errors raised by the Fly-in project."""
    def __init__(self, message: str):
        super().__init__(message)


class MissingDroneCountError(FlyInError):
    """Initialize the error with a message.

    Args:
        message: Human-readable description of the error.
    """
    def __init__(self, message: str = "Missing 'nb_drones' key") -> None:
        """Initialize the error with a message.

        Args:
            message: Human-readable description of the error.
        """
        super().__init__(message)


class MissingSeperatorError(FlyInError):
    """Raised when the map file is missing the ``nb_drones`` key."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Missing valid seperator") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class PositiveIntError(FlyInError):
    """Raised when an integer value that must be positive is not."""
    def __init__(self, lineno: int, message: str = "Integer value must "
                 "be positive") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class HubError(FlyInError):
    """Raised when a hub definition line does not match the expected
    structure."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Hub must follow the structure 'hub_name: "
                 "name(str) x_value(positive int) "
                 "y_value(positive int) [optional_details]'"
                 ) -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class HubDetailsError(FlyInError):
    """Raised when a hub's optional metadata block is malformed."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Hub details are optional, but they must follow "
                 "'zone=value(str)' or 'color=value(str)'"
                 " or 'max_capacity=value(positive int)'"
                 ) -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class HubDetailsZoneError(FlyInError):
    """Raised when a hub's ``zone`` metadata value is not a valid zone
    type."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Acceptable zone values:\n"
                 "'normal', 'blocked', 'restricted' and 'priority'") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class NonExistentNameError(FlyInError):
    """Raised when a connection references a hub name that was not
    defined."""
    def __init__(self, name1: str, name2: str, lineno: int,
                 message: str = "Invalid file format -") -> None:
        """Initialize the error.

        Args:
            name1: First hub name referenced by the connection.
            name2: Second hub name referenced by the connection.
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message} {name1} or {name2} are non-existent hubs,"
                         f" line {lineno}")


class ConnectionDetailError(FlyInError):
    """Raised when a connection's optional metadata block is malformed."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Coonection detail is optional, but should follow "
                 "'max_link_capacity=value(int)' format") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class InvalidKeyError(FlyInError):
    """Raised when a map file line uses a key that is not recognized."""
    def __init__(self, lineno: int, message: str = "Invalid Key") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class InvalidConnectionError(FlyInError):
    """Raised when a connection links a hub to itself."""
    def __init__(self, lineno: int,
                 message: str = "Invalid file format - "
                 "You can't link to the same hub") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class MissingStartEndError(FlyInError):
    """Raised when the map file is missing ``start_hub`` or ``end_hub``."""
    def __init__(self, message: str = "Invalid file format - "
                 "Missing 'start_hub' or 'end_hub'") -> None:
        """Initialize the error.

        Args:
            message: Human-readable description of the error.
        """
        super().__init__(message)


class DuplicateKeysError(FlyInError):
    """Raised when the same metadata key appears more than once."""
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Duplicate Keys") -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class DuplicateHubNameError(FlyInError):
    """Raised when two hubs share the same name."""
    def __init__(self, hub: str, lineno: int,
                 message: str = "Invalid file format - "
                 "Duplicate hub_name") -> None:
        """Initialize the error.

        Args:
            hub: Name of the duplicated hub.
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, hub {hub} line {lineno}")


class DuplicateCoordinatesError(FlyInError):
    """Raised when two hubs share the same coordinates."""
    def __init__(self, hub: str, lineno: int,
                 message: str = "Invalid file format - "
                 "Duplicate coordinates found") -> None:
        """Initialize the error.

        Args:
            hub: Name of the hub with the duplicated coordinates.
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, hub {hub} line {lineno}")


class DuplicateConnectionError(FlyInError):
    """Raised when the same connection is defined more than once."""
    def __init__(
            self, connection: str, lineno: int,
            message: str = "Invalid file format - Duplicate connection found"
            ) -> None:
        """Initialize the error.

        Args:
            connection: Identifier of the duplicated connection.
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, connection {connection} line {lineno}")


class MatchError(FlyInError):
    """Raised when a line does not match the expected regular expression."""
    def __init__(self, lineno: int, message: str = "Error while matching"
                 ) -> None:
        """Initialize the error.

        Args:
            lineno: Line number where the error occurred.
            message: Human-readable description of the error.
        """
        super().__init__(f"{message}, line {lineno}")


class UnsolveableMapError(FlyInError):
    """Raised when no valid solution exists for the given map (e.g. a
    deadlock or an unreachable end zone)."""
    def __init__(self, message: str = "Unsolvable map") -> None:
        """Initialize the error.

        Args:
            message: Human-readable description of the error.
        """
        super().__init__(message)
