from typing import List
from abc import ABC, abstractmethod

import pygame


class BaseView(ABC):
    @abstractmethod
    def event_loop(self, events: List[pygame.event.Event]) -> None: ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...
