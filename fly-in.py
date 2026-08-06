from typing import Any
from src.parser import Parser
from src.errors import (
    FlyInError
)


def main() -> None:
    dict2: dict[str, Any] = {}
    try:
        test = Parser()
        test.file_reader("src/maps/challenger/01_the_impossible_dream.txt")
        test.convert_hub()
        dict2 = test.get_hubs()
        for x in dict2:
            print(x, " ", dict2[x])
    except FlyInError as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
