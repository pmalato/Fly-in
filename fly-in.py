from src.map import Map
from src.errors import (
    FlyInError
)


def main() -> None:
    try:
        test = Map()
        some = test.get_link()
        for x in some:
            print(x)
    except (FlyInError, IOError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
