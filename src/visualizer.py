from random import Random
from src.map import Zone, Connection
from src.drone import Drone
from src.scheduler import Scheduler
import pygame
from pygame.surface import Surface


class Display():
    """Graphical (pygame) renderer for the drone routing simulation.

    Draws the zone graph, connections and drone positions on screen,
    and lets the user step through the simulation turn by turn using
    the keyboard.
    """
    def __init__(
            self, drones: list[Drone],
            hubs: list[Zone],
            links: list[Connection],
            turns: int) -> None:
        """Initialize the display, loading assets and computing the
        coordinate scaling.

        Args:
            drones: The fleet of drones to display.
            hubs: The list of zones to display.
            links: The list of connections to display.
            turns: Initial turn count (unused beyond storage).
        """
        self._bg_img: Surface = pygame.image.load("src/images/Sumeru.webp")
        self._drone1: Surface = pygame.image.load(
            "src/images/floating_anemo_fungus.png")
        self._drone2: Surface = pygame.image.load(
            "src/images/floating_dendro_fungus.png")
        self._drone3: Surface = pygame.image.load(
            "src/images/floating_hydro_fungus.png")
        self._drone1 = pygame.transform.scale(self._drone1, (50, 50))
        self._drone2 = pygame.transform.scale(self._drone2, (50, 50))
        self._drone3 = pygame.transform.scale(self._drone3, (50, 50))
        self._drones: list[Drone] = drones
        self._hubs: list[Zone] = hubs
        self._links: list[Connection] = links
        self._turns: int = turns
        self._drone_img: dict[str, Surface] = {
            x.get_id(): Random(int(x.get_id().removeprefix('D'))).choice(
                [self._drone1, self._drone2,
                 self._drone3]) for x in self._drones}
        self._edges: tuple[int, int, int, int]
        self._width: int = 0
        self._height: int = 0
        self.set_edges()
        pygame.init()
        self._screen: Surface = pygame.display.set_mode((1920, 1080))
        self._running: bool = True
        self._font = pygame.font.SysFont(None, 17)

    def set_edges(self) -> None:
        """Compute the map's coordinate bounding box and pixel size,
        used to scale zone coordinates to screen coordinates."""
        listx: list[int] = [x.get_coordinates()[0] for x in self._hubs]
        listy: list[int] = [y.get_coordinates()[1] for y in self._hubs]
        self._edges = (max(listx), max(listy), min(listx), min(listy))
        self._width = self._edges[0] - self._edges[2]
        self._height = self._edges[1] - self._edges[3]
        if not self._width:
            self._width = 1
        if not self._height:
            self._height = 1

    def scale(self, coords: tuple[int, int]) -> tuple[float, float]:
        """Convert map coordinates to screen pixel coordinates.

        Args:
            coords: The (x, y) map coordinates to convert.

        Returns:
            The corresponding (x, y) pixel position on screen.
        """
        swidth: float
        sheight: float
        cx: float = self._width / 2
        cy: float = self._height / 2
        x: float = coords[0] - cx
        y: float = coords[1] - cy
        swidth, sheight = self._screen.get_size()
        return (
            swidth / 2 + x * swidth * 0.042,
            sheight / 2 + y * sheight * 0.045)

    def display_drone(self) -> None:
        """Draw every drone at its current zone's screen position."""
        for drone in self._drones:
            if drone.get_current():
                self._screen.blit(
                    self._drone_img[drone.get_id()],
                    self._drone_img[drone.get_id()].get_rect(
                        center=self.scale(
                            drone.get_current().get_coordinates())))

    def exe(self, scheduler: Scheduler) -> None:
        """Run the main render/event loop, driving the simulation.

        Renders the background, connections, zones and drones every
        frame, and advances the underlying ``Scheduler`` generator by
        one turn each time the user presses SPACE or the right arrow
        key. Handles fullscreen toggling and quitting.

        Args:
            scheduler: The ``Scheduler`` whose ``run()`` generator
                drives the simulation being visualized.
        """
        zone1: tuple[float, float]
        zone2: tuple[float, float]
        x: float
        y: float
        gen = iter(scheduler.run())
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    if event.key == pygame.K_SPACE or \
                            event.key == pygame.K_RIGHT:
                        try:
                            next(gen)
                        except StopIteration:
                            print("Iteration over, press ESC or close the GUI")
                            break
            self._screen.blit(self._bg_img, (0, 0))
            for link in self._links:
                zone1 = self.scale(link.get_connection()[0].get_coordinates())
                zone2 = self.scale(link.get_connection()[1].get_coordinates())
                pygame.draw.line(self._screen, "white", zone1, zone2, 2)
            for hub in self._hubs:
                x, y = self.scale(hub.get_coordinates())
                if hub.get_color() == "none" or \
                        hub.get_color() == "rainbow":
                    pygame.draw.circle(
                        self._screen, "purple", (x, y), 15)
                else:
                    pygame.draw.circle(
                        self._screen, hub.get_color(),
                        (x, y), 15)
                self._screen.blit(
                    self._font.render(
                        hub.get_id(), True, "black"), (x - 30, y + 15))
            self.display_drone()
            pygame.display.flip()
        pygame.quit()
