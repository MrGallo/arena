from typing import List

import pygame

from arena.base_view import BaseView, GameEntity


class BattleView(BaseView):
    def __init__(self) -> None:
        self.cellsize = 50
        self.wall_thickness = 4
        self.grid_width = (1920 * 2) // self.cellsize
        self.grid_height = (1080 * 2) // self.cellsize
        self.width = self.grid_width * self.cellsize + self.wall_thickness * 2
        self.height = self.grid_height * self.cellsize + self.wall_thickness * 2
        self.size = self.width, self.height
        # self.score_font = pygame.font.SysFont("Arial", 30)
        self.arena_layers = [
            pygame.surface.Surface(self.size),
            pygame.surface.Surface(self.size, pygame.SRCALPHA),
        ]
        self._draw_arena_bg()
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 10
    
    def _draw_arena_bg(self) -> None:
        bg = self.arena_layers[0]
        bg.fill("#9b7653")
        width, height = bg.get_size()
        for x in range(self.wall_thickness, width, self.cellsize):
            pygame.draw.line(bg, "#7E5F44", (x, 0), (x, height), 2)
        
        for y in range(self.wall_thickness, height, self.cellsize):
            pygame.draw.line(bg, "#7E5F44", (0, y), (width, y), 2)

        # border wall
        pygame.draw.rect(bg, (30, 30, 30), (0, 0, width, height), self.wall_thickness)

    def _grid_pos_to_img_pos(self, grid_pos) -> tuple[int, int]:
        x, y = grid_pos
        return (
            x * self.cellsize + self.wall_thickness + 1,
            y * self.cellsize + self.wall_thickness + 1 
        )

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                dx, dy = event.rel
                self.camera_x -= dx
                self.camera_y -= dy
            elif event.type == pygame.MOUSEWHEEL:
                self.scale += event.y
                self.scale = min(10, max(self.scale, 5))

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))
        for layer in self.arena_layers:
            scaled = pygame.transform.scale_by(layer, self.scale / 10)
            width, height = surface.get_size()
            surface.blit(scaled, (-scaled.get_width() // 2 + width // 2 - self.camera_x, -scaled.get_height() // 2 + height // 2 - self.camera_y))


class ChampionShowcase(BattleView):
    def __init__(self, champion_classes: List[GameEntity]) -> None:
        super().__init__()
        self.champions = [champ_class() for champ_class in champion_classes]

    def update(self) -> None:
        super().update()
        for champ in self.champions:
            champ.update()
    
    def draw(self, surface: pygame.Surface) -> None:

        champion_images = []
        for champ in self.champions:
            champ_img = pygame.Surface((300, 300), pygame.SRCALPHA)
            champ.draw(champ_img)
            scaled = pygame.transform.scale(champ_img, (self.cellsize, self.cellsize))
            champion_images.append(scaled)
        

        for img in champion_images:
            grid_pos = (self.grid_width//2, self.grid_height//2)
            img_pos = self._grid_pos_to_img_pos(grid_pos)

            self.arena_layers[1].blit(img, img_pos)


        super().draw(surface)
