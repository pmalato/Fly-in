from src.parser import Parser
from src.map import Map, Zone, Connection
from src.tracker import Tracker
from src.scheduler import Scheduler
from src.visualizer import Display
from src.errors import (
    FlyInError
)


def main() -> None:
    try:
        parser: Parser = Parser()
        parser.start()
        map: Map = Map(parser)
        hubs: list[Zone] = map.get_hubs()
        links: list[Connection] = map.get_connections()
        map.define_link_cost()
        tracker: Tracker = Tracker(map)
        scheduler: Scheduler = Scheduler(tracker, map)
        scheduler.run()
        print(f"Turn count: {scheduler.get_count()}")
        display: Display = Display(hubs, links)
        display.exe()
    except (FlyInError, IOError, LookupError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
