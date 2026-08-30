from src.parser import Parser
from src.map import Map
from src.errors import (
    FlyInError
)


def main() -> None:
    try:
        parser = Parser()
        parser.start()
        test = Map(parser)
        test.define_link_cost()
        next = test.get_costs()
        for x in next:
            print(f"{x[0].get_id()} - {x[1].get_id()}: ", end="")
            print(next[x])
    except (FlyInError, IOError, LookupError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
