from abc import ABC, abstractmethod
from typing import Optional, Self, ClassVar

import pygame

from arena.base_view import BaseView


class BaseGame(ABC):
    game: ClassVar['BaseGame']

    def __init__(self) -> None:
        BaseGame.game = self

        pygame.init()
        pygame.font.init()

        WIDTH = 640
        HEIGHT = 480
        SIZE = (WIDTH, HEIGHT)

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.current_view: BaseView

        self.create()

    @staticmethod
    def instance() -> 'BaseGame':
        if BaseGame.game is None:
            BaseGame()
        return BaseGame.game

    @classmethod
    def set_current_view(cls, view: BaseView) -> None:
        BaseGame.instance().current_view = view

    @abstractmethod
    def create(self) -> None: ...

    def run(self) -> None:
        running = True
        while running:
            # EVENT HANDLING
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.current_view.event_loop(events)
            self.current_view.update()
            self.current_view.draw(self.screen)

            # Must be the last two lines
            # of the game loop
            pygame.display.flip()
            self.clock.tick(30)
            # ---------------------------

        pygame.quit()
