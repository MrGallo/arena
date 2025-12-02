import pygame


class Sprite(pygame.sprite.Sprite):
    IMAGE_SURFACE_SIZE = (300, 300)

    def __init__(self, champion, position, width):
        pygame.sprite.Sprite.__init__(self)
        self.champ = champion
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2(*position)
        self.size = width, width

    
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