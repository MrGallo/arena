from typing import List

import pygame

from arena.my_game import MyGame
from arena.base_view import BaseView


class PlayView(BaseView):
    def __init__(self) -> None:
        self.circle = pygame.Rect(50, 50, 60, 60)
        self.circle_dx = 3
        self.circle_dy = 3
        self.score = 0

        self.score_font = pygame.font.SysFont("Arial", 30)

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    from arena.pause_view import PauseView
                    MyGame.set_current_view(PauseView(self))

    def update(self) -> None:
        self.score += 1
        self.score_text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))

        self.circle.x += self.circle_dx
        self.circle.y += self.circle_dy

        # ACCESSING WORLD BOUNDARY
        world_boundary_size = MyGame.game.screen.get_size()
        width, height = world_boundary_size
        if self.circle.x + self.circle.width > width or self.circle.x < 0:
            self.circle_dx *= -1
        if self.circle.y + self.circle.height > height or self.circle.y < 0:
            self.circle_dy *= -1

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))
        pygame.draw.circle(surface, (0, 0, 200), self.circle.center, self.circle.width // 2)
        surface.blit(self.score_text, (10, 10))
