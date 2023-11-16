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

        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.SIZE = (self.WIDTH, self.HEIGHT)
        self.fullscreen = True

        self.screen = pygame.display.set_mode(self.SIZE)
        # self.screen = pygame.display.set_mode(self.SIZE, pygame.FULLSCREEN)
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
    def create(self) -> None:
        pass

    def run(self) -> None:
        running = True
        while running:
            # EVENT HANDLING
            events = pygame.event.get()
            # print(events)
            for event in events:
                if event.type == pygame.QUIT:
                    # print(event)
                    running = False
                elif event.type == pygame.KEYUP:
                    # TODO: weird bug that keydown escape is triggered randomly in the game loop
                    if event.key == pygame.K_ESCAPE:
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
