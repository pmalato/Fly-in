from src.map import Zone, Connection
import pygame
from pygame.surface import Surface


class Display():
    def __init__(self, hubs: list[Zone], links: list[Connection]) -> None:
        self._bg_img = pygame.image.load("./src/images/Sumeru.webp")
        self._hubs: list[Zone] = hubs
        self._links: list[Connection] = links
        pygame.init()
        self._screen: Surface = pygame.display.set_mode((1800, 1800))
        self._running: bool = True

    def scale(self, coords: tuple[int, int]) -> None:
        ...

    def exe(self) -> None:
        zone1: tuple[int, int]
        zone2: tuple[int, int]
        x: int
        y: int
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self._screen.fill("brown")
            for hub in self._hubs:
                x = hub.get_coordinates()[0] * 10
                y = hub.get_coordinates()[1] * 10
                if hub.get_color() == "none":
                    pygame.draw.circle(
                        self._screen, "purple", (x, y), 10)
                else:
                    pygame.draw.circle(
                        self._screen, hub.get_color(),
                        (x, y), 10)
            for link in self._links:
                zone1 = link.get_connection()[0].get_coordinates()
                zone2 = link.get_connection()[1].get_coordinates()
                pygame.draw.line(self._screen, "white", zone1, zone2, 2)
            pygame.display.flip()
        pygame.quit()
