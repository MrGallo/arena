from typing import List

import pygame

from arena.base_view import BaseView


class BattleView(BaseView):
    def __init__(self) -> None:
        # self.score_font = pygame.font.SysFont("Arial", 30)
        self.arena_bg: pygame.surface.Surface
        self._draw_arena_bg()
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 10
    
    def _draw_arena_bg(self) -> None:
        cellsize = 50
        wall_thickness = 4
        grid_width = (1920 * 2) // cellsize
        grid_height = (1080 * 2) // cellsize
        width = grid_width * cellsize + wall_thickness * 2
        height = grid_height * cellsize + wall_thickness * 2
        self.arena_bg = pygame.surface.Surface((width, height))
        self.arena_bg.fill("#9b7653")
        width, height = self.arena_bg.get_size()
        for x in range(wall_thickness, width, cellsize):
            pygame.draw.line(self.arena_bg, "#7E5F44", (x, 0), (x, height), 2)
        
        for y in range(wall_thickness, height, cellsize):
            pygame.draw.line(self.arena_bg, "#7E5F44", (0, y), (width, y), 2)

        # border wall
        pygame.draw.rect(self.arena_bg, (30, 30, 30), (0, 0, width, height), wall_thickness)

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                dx, dy = event.rel
                self.camera_x -= dx
                self.camera_y -= dy
            elif event.type == pygame.MOUSEWHEEL:
                self.scale += event.y
                self.scale = min(10, max(self.scale, 5))
                print(self.scale)


    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))
        scaled = pygame.transform.scale_by(self.arena_bg, self.scale/10)
        width, height = surface.get_size()
        surface.blit(scaled, (-scaled.get_width() // 2 + width // 2 - self.camera_x, -scaled.get_height() // 2 + height // 2 - self.camera_y))
