import pygame


class Sprite(pygame.sprite.Sprite):
    IMAGE_SURFACE_SIZE = (300, 300)

    def __init__(self, champion, position, width):
        pygame.sprite.Sprite.__init__(self)
        self.champ = champion
        self.velocity = pygame.Vector2()
        self.size = width, width
        self.rect = pygame.Rect(*position, *self.size)

    
    def draw(self, surface):
        self.champ.draw(surface)

    @property
    def image(self):
        surf = pygame.Surface(self.IMAGE_SURFACE_SIZE, pygame.SRCALPHA)
        self.champ.draw(surf)
        return pygame.transform.scale(surf, self.size)

    def get_rect(self):
        return self.rect