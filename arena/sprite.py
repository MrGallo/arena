from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import pygame

from arena.stats import Stats, ActiveModifiers, StatModifier, CalculatedStats
from arena.mission import Mission


class Sprite(pygame.sprite.Sprite):
    IMAGE_SURFACE_SIZE = (300, 300)

    def __init__(self, champion, position, width):
        pygame.sprite.Sprite.__init__(self)
        self.champ = champion
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2(*position)
        self.size = width, width

        if hasattr(champion, "Stats"):
            self.base_stats = Stats(
                str=champion.Stats.STR,
                agi=champion.Stats.AGI,
                int=champion.Stats.INT
            )
        else:
            self.base_stats = Stats(10, 10, 10)

        # Stat penalty if too many points
        if self.base_stats.STR + self.base_stats.AGI + self.base_stats.INT > 30:
            self.base_stats = Stats(str=5, agi=5, int=5)
        
        self.active_modifiers = ActiveModifiers()
        self.stats = CalculatedStats(self.base_stats, self.active_modifiers)
    
    def draw(self, surface):
        self.champ.draw(surface)

    @property
    def image(self):
        surf = pygame.Surface(self.IMAGE_SURFACE_SIZE, pygame.SRCALPHA)
        self.champ.draw(surf)
        return pygame.transform.scale(surf, self.size)

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.size)

    def get_rect(self):
        return self.rect