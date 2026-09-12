"""Shared neon palette and tiny helpers for the ElbowOS cabinet."""
import pygame

BG = (10, 8, 26)
PANEL = (22, 18, 48)
PINK = (255, 72, 168)
CYAN = (0, 230, 255)
YELLOW = (255, 220, 70)
LIME = (90, 255, 140)
ORANGE = (255, 140, 50)
PURPLE = (168, 90, 255)
WHITE = (245, 245, 255)
RED = (255, 70, 90)
BLUE = (70, 130, 255)
GOLD = (255, 200, 60)


def font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("consolas,dejavusansmono,menlo,monospace", size, bold=bold)


def draw_text(surf, text, size, color, center=None, topleft=None, bold=False):
    f = font(size, bold)
    img = f.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = center
    if topleft:
        rect.topleft = topleft
    surf.blit(img, rect)
    return rect


def vignette_fill(surf, color=BG):
    surf.fill(color)
    w, h = surf.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 40), (0, 0, w, h), border_radius=0)
    surf.blit(overlay, (0, 0))
