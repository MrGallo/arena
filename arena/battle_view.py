from typing import List
from collections import deque
import math

import pygame

from arena.base_view import BaseView, GameEntity
from arena.battle_api import BattleAPI
from arena.sprite import Sprite
from arena.mission import Mission, WithinRangeObjective
from arena.action import Action
from arena.settings import Settings


class BattleView(BaseView):
    GROUND_LAYER = 0
    MOVABLE_OBJECT_LAYER = 1

    cellsize = 50
    wall_thickness = 4
    grid_width = (1920 * 2) // cellsize
    grid_height = (1080 * 2) // cellsize
    width = grid_width * cellsize + wall_thickness * 2
    height = grid_height * cellsize + wall_thickness * 2
    size = width, height

    def __init__(self, champion_classes, spawn_points) -> None:
        self.champ_sprite_map = {}
        champions = [champ_class() for champ_class in champion_classes]

        self.boundary_rect = pygame.Rect(0, 0, *self.size)
        # self.score_font = pygame.font.SysFont("Arial", 30)
        self.scalable_surfaces = [
            pygame.surface.Surface(self.size),                      # Ground and grid
            pygame.surface.Surface(self.size, pygame.SRCALPHA),     # movable object layer
        ]
        self.overlay_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self._draw_arena_bg()
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 10
        self.actions = deque() 

        self.champ_sprite_group = pygame.sprite.Group() 
        for champ, spawn_point in zip(champions, spawn_points):
            champ_sprite = Sprite(champ, spawn_point, self.cellsize)
            champ_sprite.add(self.champ_sprite_group)
            self.champ_sprite_map[champ] = champ_sprite
        
        self.mission = Mission(self)

    
    def _draw_arena_bg(self) -> None:
        bg = self.scalable_surfaces[self.GROUND_LAYER]
        bg.fill("#a48c76")
        width, height = bg.get_size()
        for x in range(self.wall_thickness, width, self.cellsize):
            pygame.draw.line(bg, "#7C736C", (x, 0), (x, height), 2)
        
        for y in range(self.wall_thickness, height, self.cellsize):
            pygame.draw.line(bg, "#7C736C", (0, y), (width, y), 2)

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
        for sprite in self.champ_sprite_group:
            sprite.champ.update()
            battle_api = BattleAPI(sprite.champ, self)
            sprite.champ.battle_plan(battle_api)
            self.actions += battle_api._drain()
        self._process_actions()
        self.mission.update()

    def _process_actions(self):
        while (self.actions):
            action_name, champ, *args = self.actions.popleft()
            champ_sprite = self.champ_sprite_map[champ]

            getattr(self, action_name)(champ_sprite, *args)
    
    def move(self, champ_sprite, displacement):
        moved_rect = champ_sprite.rect.move(*displacement) 
        if self.boundary_rect.contains(moved_rect):
            champ_sprite.rect.move_ip(*displacement)
        else:
            pass  # Send boundary event, stuck event?  

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))

        # clear movable objects layer
        self.scalable_surfaces[self.MOVABLE_OBJECT_LAYER].fill((0, 0, 0, 0))

        # draw champs
        self.champ_sprite_group.draw(self.scalable_surfaces[self.MOVABLE_OBJECT_LAYER])

        self.mission.draw(self.scalable_surfaces[self.MOVABLE_OBJECT_LAYER])

        # for champ_sprite in self.champ_sprite_map.values():
        #     champ_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        #     champ_sprite.draw(champ_surf)
        #     scaled = pygame.transform.scale(champ_surf, (self.cellsize, self.cellsize))
        #     self.arena_layers[self.MOVABLE_OBJECT_LAYER].blit(scaled, champ_sprite.position)

        for layer in self.scalable_surfaces:
            scaled = pygame.transform.scale_by(layer, self.scale / 10)
            width, height = surface.get_size()
            surface.blit(scaled, (-scaled.get_width() // 2 + width // 2 - self.camera_x, -scaled.get_height() // 2 + height // 2 - self.camera_y))

        # HUD
        # Heading
        self.overlay_surface.fill((0, 0, 0, 0))
        heading_text = Settings.Font.heading.render(
            f"{self.mission.display_string} [{self.mission.status.capitalize()}]",
            True,
            Settings.Color.text_heading
        )
        self.overlay_surface.blit(heading_text, (0, 0)) 

        # Objectives
        heading_height = heading_text.get_height()
        text_height = Settings.Font.body.size("|")[1]
        for i, obj in enumerate(self.mission.objectives):
            y = i * (text_height + 5) + heading_height + 5 
            obj_text = Settings.Font.body.render(f"{obj.display_string} [{obj.status}]",
                                                 True,
                                                 Settings.Color.text_body)
            self.overlay_surface.blit(obj_text, (0, y))

        surface.blit(self.overlay_surface, (0, 0))


class ChampionShowcase(BattleView):
    def __init__(self, champion_classes: List[GameEntity]) -> None:
        # for _ in range(6):
        #     champion_classes += champion_classes
        spawn_points = []
        padding = 15
        row_width = math.floor(math.sqrt(len(champion_classes)))
        pixel_width = row_width * (self.cellsize + padding) 
        x_offset = self.width // 2 - pixel_width // 2
        y_offset = self.height // 2 - pixel_width // 2
        for i, champ_class in enumerate(champion_classes):
            row_num = i // row_width 
            col_num = i % row_width
            x = col_num * self.cellsize + col_num * padding + x_offset
            y = row_num * self.cellsize + row_num * padding + y_offset
            spawn_points.append((x, y))

        super().__init__(champion_classes, spawn_points)



class TestBattle_ReachGoal(BattleView):
    def __init__(self, champion_classes: List[GameEntity]):
        spawn_points = ((self.width * 0.65, self.height // 2 - self.cellsize // 2),)
        super().__init__(champion_classes, spawn_points)
        self.mission.add_objective(
            WithinRangeObjective(
                self,
                self.champ_sprite_group.sprites()[0],
                (self.width // 3, self.height // 2),
                100
            )
        ) 
    
    def update(self):
        super().update()
        print(self.mission.status)