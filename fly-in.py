from src.map import Map
from src.errors import (
    FlyInError
)


def main() -> None:
    try:
        test = Map()
        test.store_hubs()
        test.store_links()
        next = test.get_link_list()
        for x in next:
            print(f"{x.get_connection()[0].get_id()} - {x.get_connection()[1].get_id()},"
                  f" {x.get_metadata()}")
    except (FlyInError, IOError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
