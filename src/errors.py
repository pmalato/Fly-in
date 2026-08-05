class FlyInError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MissingSeperatorError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Missing valid seperator") -> None:
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


class InvalidKeyError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid Key") -> None:
        super().__init__(f"{message}, line {lineno}")


class MissingStartEndError(FlyInError):
    def __init__(self, message: str = "Invalid file format - "
                 "Missing 'start_hub' or 'end_hub'") -> None:
        super().__init__(message)


class DuplicateKeysError(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Duplicate Keys") -> None:
        super().__init__(f"{message}, line {lineno}")


class DuplicateValues(FlyInError):
    def __init__(self, lineno: int, message: str = "Invalid file format - "
                 "Repeated hub/connection") -> None:
        super().__init__(f"{message}, line {lineno}")


class MatchError(FlyInError):
    def __init__(self, lineno: int, message: str = "Error while matching"
                 ) -> None:
        super().__init__(f"{message}, line {lineno}")
