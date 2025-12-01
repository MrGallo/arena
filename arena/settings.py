import pygame
pygame.font.init()


class Settings:
    class Color:
        text_heading = "#000000"
        text_subheading = "#595959"
        text_body = "#000000"
        text_success = "#048b04"
        text_danger = "#b33333"
    class Font:
        jumbo = pygame.font.SysFont("Arial", 100)
        heading = pygame.font.SysFont("Arial", 30)
        body = pygame.font.SysFont("Arial", 15)