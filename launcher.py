"""ElbowOS Neon Cabinet — colourful game picker."""
import importlib
import sys
import pygame
from common import BG, PANEL, PINK, CYAN, YELLOW, LIME, WHITE, GOLD, PURPLE, draw_text

GAMES = [
    ("Pipe Hero", "Original Mario-style platformer", "pipe_hero", PINK),
    ("Star Raiders", "Wave shooter / invaders style", "star_raiders", CYAN),
    ("Maze Muncher", "Pellet-maze chomper", "maze_muncher", YELLOW),
    ("Neon 2048", "Slide-merge puzzle", "neon_2048", LIME),
    ("Neon Craps", "Pass-line casino dice", "neon_craps", GOLD),
    ("Colour Klondike", "Drag-and-drop solitaire", "klondike", PURPLE),
    ("Connect Glow", "Four-in-a-row table game", "connect_glow", PINK),
    ("Sky Racer", "Neon highway dodge", "sky_racer", CYAN),
]

W, H = 820, 620


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("ElbowOS Neon Cabinet")
    clock = pygame.time.Clock()
    selected = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    return
                if e.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(GAMES)
                if e.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(GAMES)
                if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    _launch(GAMES[selected][2])
                    pygame.display.set_mode((W, H))
                    pygame.display.set_caption("ElbowOS Neon Cabinet")
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for i, _g in enumerate(GAMES):
                    r = pygame.Rect(60, 120 + i * 52, 700, 46)
                    if r.collidepoint(mx, my):
                        selected = i
                        _launch(GAMES[i][2])
                        pygame.display.set_mode((W, H))
                        pygame.display.set_caption("ElbowOS Neon Cabinet")

        screen.fill(BG)
        draw_text(screen, "ELBOWOS NEON CABINET", 34, GOLD, center=(W // 2, 36), bold=True)
        draw_text(screen, "https://x.com/ElbowOS", 18, CYAN, center=(W // 2, 70))
        draw_text(screen, "Full-colour Python 3 originals  •  not ROM emulators", 16, WHITE, center=(W // 2, 94))

        for i, (name, blurb, _mod, col) in enumerate(GAMES):
            r = pygame.Rect(60, 120 + i * 52, 700, 46)
            pygame.draw.rect(screen, PANEL if i != selected else (40, 32, 72), r, border_radius=8)
            if i == selected:
                pygame.draw.rect(screen, col, r, 2, border_radius=8)
            draw_text(screen, f"{i + 1}  {name}", 22, col if i == selected else WHITE, topleft=(r.x + 16, r.y + 10), bold=True)
            draw_text(screen, blurb, 16, WHITE, topleft=(r.x + 280, r.y + 14))

        draw_text(screen, "UP/DOWN  ENTER play  ESC quit", 16, WHITE, center=(W // 2, H - 28))
        pygame.display.flip()
        clock.tick(60)


def _launch(modname):
    pygame.display.quit()
    pygame.init()
    mod = importlib.import_module(modname)
    mod.run()
    pygame.quit()
    pygame.init()


if __name__ == "__main__":
    run()
    sys.exit(0)
