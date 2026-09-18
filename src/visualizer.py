from src.map import Zone, Connection
import pygame
from pygame.surface import Surface


class Display():
    def __init__(self, hubs: list[Zone], links: list[Connection]) -> None:
        self._bg_img: Surface = pygame.image.load("./src/images/Sumeru.webp")
        self._drone1: Surface = pygame.image.load(
            "src/images/floating_anemo_fungus.png")
        self._drone2: Surface = pygame.image.load(
            "src/images/floating_dendro_fungus.png")
        self._drone3: Surface = pygame.image.load(
            "src/images/floating_hydro_fungus.png")
        self._hubs: list[Zone] = hubs
        self._links: list[Connection] = links
        self._edges: tuple[int, int, int, int]
        self._width: int = 0
        self._height: int = 0
        self.set_edges()
        pygame.init()
        self._background: Surface = pygame.image.load("src/images/Sumeru.webp")
        self._screen: Surface = pygame.display.set_mode((1920, 1080))
        self._running: bool = True

    def set_edges(self) -> None:
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
        swidth: float
        sheight: float
        cx: float = self._width / 2
        cy: float = self._height / 2
        x: float = coords[0] - cx
        y: float = coords[1] - cy
        swidth, sheight = self._screen.get_size()
        return (
            swidth / 2 + x * swidth * 0.035,
            sheight / 2 + y * sheight * 0.035)

    def exe(self) -> None:
        zone1: tuple[float, float]
        zone2: tuple[float, float]
        x: float
        y: float
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
            self._screen.blit(self._background, (0, 0))
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
            pygame.display.flip()
        pygame.quit()
