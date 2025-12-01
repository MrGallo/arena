from abc import ABC, abstractmethod

import pygame

from arena.sprite import Sprite
from arena.settings import Settings


class Objective(ABC):
    INCOMPLETE = "incomplete"
    SUCCESS = "success"
    FAILURE = "failure"

    def __init__(self, arena, display_string="Unnamed Objective"):
        self.status = Objective.INCOMPLETE
        self.arena = arena  # bound on mission.add_objective()
        self.display_string = display_string

    @abstractmethod
    def success(self) -> bool:
        """Return True if the objective is satisfied."""
        pass

    def failure(self) -> bool:
        """Return True if a failure condition has been met."""
        return False

    def update(self):
        if self.status != Objective.INCOMPLETE:
            return

        if self.failure():
            self.status = Objective.FAILURE

        elif self.success():
            self.status = Objective.SUCCESS

    def draw(self, surface: pygame.Surface):
        pass


class Mission(Objective):
    def __init__(self, arena, display_string="Unnamed Mission"):
        super().__init__(arena, display_string)
        self.arena
        self.objectives = []

    def add_objective(self, objective):
        self.objectives.append(objective)

    def add_objectives(self, objectives):
        for obj in objectives:
            self.objectives.append(obj)

    def update(self):
        for obj in self.objectives:
            obj.update()
        
        super().update()
    
    def success(self) -> bool:
        if self.failure():
            return False
        return all(obj.status == Objective.SUCCESS for obj in self.objectives)
        
    def failure(self) -> bool:
        return any(obj.status == Objective.FAILURE for obj in self.objectives)
    
    def draw(self, surface: pygame.Surface):
        for obj in self.objectives:
            obj.draw(surface)
        


class WithinRangeObjective(Objective):
    def __init__(self,
                 arena,
                 champion: Sprite,
                 location: tuple[int, int],
                 radius,
                 display_string=None):
        if display_string is None:
            display_string = f"Get within {radius} pixels of {location}"
        super().__init__(arena, display_string)
        self.champion = champion
        self.location = pygame.Vector2(*location)
        self.radius = radius
    
    def success(self) -> bool:
        champ_pos = pygame.Vector2(self.champion.rect.center)
        diff: pygame.Vector2 = champ_pos - self.location
        return diff.magnitude_squared() < self.radius ** 2
    
    def draw(self, surface: pygame.Surface):
        fade_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        center = (self.radius, self.radius)

        # Draw from large → small for proper layering
        for r in range(self.radius, 0, -1):
            alpha = 255 - (255 * r / self.radius)
            color = (255, 255, 0, alpha)

            pygame.draw.circle(fade_surf, color, center, r)

        blit_pos = (self.location.x - self.radius, self.location.y - self.radius)
        surface.blit(fade_surf, blit_pos)


class StopWithinRangeObjective(WithinRangeObjective):
    def __init__(self,
                 arena,
                 champion: Sprite,
                 location: tuple[int, int],
                 radius):
        super().__init__(arena, champion, location, radius, f"Stop within {radius} pixels of {location}")
    
    def success(self) -> bool:
        champ_pos = pygame.Vector2(self.champion.rect.center)
        diff: pygame.Vector2 = champ_pos - self.location
        is_stopped = self.champion.velocity.magnitude_squared() == 0
        return diff.magnitude_squared() < self.radius ** 2 and is_stopped
    