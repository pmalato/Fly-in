from src.parser import Parser
from src.map import Map
from src.tracker import Tracker
from src.scheduler import Scheduler
from src.errors import (
    FlyInError
)


def main() -> None:
    try:
        parser: Parser = Parser()
        parser.start()
        map: Map = Map(parser)
        map.define_link_cost()
        tracker: Tracker = Tracker(map)
        scheduler: Scheduler = Scheduler(tracker, map)
        scheduler.run()
        print(f"Turn count: {scheduler.get_count()}")
    except (FlyInError, IOError, LookupError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
