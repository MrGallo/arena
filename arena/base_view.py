from typing import List
from abc import ABC, abstractmethod

import pygame


class BaseView(ABC):
    @abstractmethod
    def event_loop(self, events: List[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
