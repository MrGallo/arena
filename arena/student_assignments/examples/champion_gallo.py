"""
CHAMPION WORKSHOP
Use this program to create your champion. It will show a large version of your Champion (300x300)
as well as a smaller version (50x50) so you can make sure it looks good at both sizes.

Although it might take a little getting used to, this class-based system will allow easier
integration into a larger code-base.
"""

from typing import ClassVar, List, Tuple

import pygame


class Champion:
    def __init__(self) -> None:
        # Initialize variables here
        # ones named self. can be accessed from
        # all the object's methods (functions).
        self.size = 300
        self.circle_x = 0

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        # You can have custom events trigger here
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("You pressed a key!")

    def update(self) -> None:
        self.circle_x += 1

    def draw(self, surface: pygame.Surface) -> None:
        # The surface to draw on will be 300x300 pixels in size.
        # the background will be transparent.
        pygame.draw.circle(surface, (200, 200, 0), (self.circle_x, self.size // 2), 50)


# _____ DO NOT TOUCH CODE BELOW HERE _________

class BaseView:
    CHAMP_SIZE = 300
    SMALL_FACTOR = 1 / 6

    def __init__(self) -> None:
        self.champion = Champion()
        self.champion_offset: Tuple[int, int] = (0, 0)

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        self.champion.handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.champion_offset is not None:
                    offset_x, offset_y = self.champion_offset
                    mx, my = event.pos
                    rel_x, rel_y = mx - offset_x, my - offset_y
                    if rel_x > 0 and rel_x < self.CHAMP_SIZE and rel_y > 0 and rel_y < self.CHAMP_SIZE:
                        print(f"({rel_x}, {rel_y})")
                    else:
                        print("Click out of bounds")

    def update(self) -> None:
        self.champion.update()

    def draw(self, surface: pygame.Surface) -> None:
        
        champ_img = pygame.Surface((300, 300), pygame.SRCALPHA)
        self.champion.draw(champ_img)
        
        champ_small = pygame.transform.scale_by(champ_img, self.SMALL_FACTOR)

        # Draw Cell
        cell = pygame.Surface((self.CHAMP_SIZE + 50 + self.CHAMP_SIZE * self.SMALL_FACTOR + 1, self.CHAMP_SIZE + 2), pygame.SRCALPHA)

        cell.blit(champ_img, (1, 1))
        champ_small_rect = champ_small.get_rect()
        champ_small_rect.move_ip(self.CHAMP_SIZE + 50, self.CHAMP_SIZE // 2 - self.CHAMP_SIZE // 2 * self.SMALL_FACTOR)
        cell.blit(champ_small, champ_small_rect.topleft)

        # border
        pygame.draw.rect(cell, (150, 150, 150), champ_img.get_rect().inflate(2, 2).move(1, 1), width=1)
        pygame.draw.rect(cell, (150, 150, 150), champ_small_rect.inflate(2, 2), width=1)

        # Draw cell on surface
        surface.fill((230, 230, 230))
        cell_rect = cell.get_rect()
        cell_rect.move_ip(surface.get_width() // 2 - cell.get_width() // 2, surface.get_height() // 2 - cell.get_height() // 2)
        self.champion_offset = cell_rect.topleft
        pygame.draw.rect(surface, (210, 210, 210), cell_rect.inflate(40, 40))
        surface.blit(cell, cell_rect.topleft)


class BaseGame:
    game: ClassVar['BaseGame']

    def __init__(self) -> None:
        BaseGame.game = self

        pygame.init()
        pygame.font.init()

        self.WIDTH = 640
        self.HEIGHT = 480
        self.SIZE = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(self.SIZE)
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


if __name__ == "__main__":
    game = BaseGame()
    game.instance().set_current_view(BaseView())
    game.run()
