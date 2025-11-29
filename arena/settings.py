import pygame
pygame.font.init()


class Settings:
    class Color:
        text_heading = "#000000"
        text_body = "#000000"
    class Font:
        heading = pygame.font.SysFont("Arial", 30)
        body = pygame.font.SysFont("Arial", 15)