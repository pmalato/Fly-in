from src.parser import Parser
from src.map import Map, Zone, Connection
from src.drone import Drone
from src.tracker import Tracker
from src.scheduler import Scheduler
from src.visualizer import Display
from src.errors import (
    FlyInError
)


def main() -> None:
    """Initialize and run the drone simulation system.

    Parses configuration data, sets up the map, trackers, and scheduler,
    and executes the visualization display for the simulation turns.
    """
    try:
        parser: Parser = Parser()
        parser.start()
        map: Map = Map(parser)
        hubs: list[Zone] = map.get_hubs()
        links: list[Connection] = map.get_connections()
        map.define_link_cost()
        tracker: Tracker = Tracker(map)
        scheduler: Scheduler = Scheduler(tracker, map)
        drones: list[Drone] = scheduler.get_drones()
        display: Display = Display(drones, hubs, links, 0)
        display.exe(scheduler)
        turns: int = scheduler.get_count()
        print(f"Turn count: {turns}")
    except (FlyInError, IOError, LookupError) as error:
        print("ERROR: ", error)


if __name__ == "__main__":
    main()
