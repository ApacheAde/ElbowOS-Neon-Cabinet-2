"""Maze Muncher — Pac-Man inspired neon maze."""
import random
import sys
import pygame
from common import BG, PINK, CYAN, YELLOW, LIME, WHITE, RED, PURPLE, GOLD, draw_text

TILE = 28
RAW = [
    "11111111111111111111",
    "10000000011000000001",
    "10111011111011101101",
    "13000000000000000031",
    "10110111111111011011",
    "10010000011000001001",
    "11110111011011101111",
    "10000001000010000001",
    "10111101011010111101",
    "10000000000000000001",
    "10110111111111011011",
    "10000000011000000001",
    "11111111111111111111",
]
ROWS, COLS = len(RAW), len(RAW[0])
W, H = COLS * TILE, ROWS * TILE + 50


def build():
    walls, pellets, powers = [], [], []
    for y, row in enumerate(RAW):
        for x, ch in enumerate(row):
            r = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            if ch == "1":
                walls.append(r)
            elif ch == "0":
                pellets.append(pygame.Rect(r.centerx - 3, r.centery - 3, 6, 6))
            elif ch == "3":
                powers.append(pygame.Rect(r.centerx - 7, r.centery - 7, 14, 14))
    return walls, pellets, powers


def blocked(rect, walls, dx, dy):
    nxt = rect.move(dx, dy)
    return any(nxt.colliderect(w.inflate(-2, -2)) for w in walls)


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Maze Muncher — ElbowOS")
    clock = pygame.time.Clock()
    walls, pellets, powers = build()
    player = pygame.Rect(TILE + 4, TILE + 4, TILE - 8, TILE - 8)
    ghosts = [
        {"rect": pygame.Rect(9 * TILE + 4, 7 * TILE + 4, TILE - 8, TILE - 8), "color": RED, "dir": (1, 0)},
        {"rect": pygame.Rect(10 * TILE + 4, 7 * TILE + 4, TILE - 8, TILE - 8), "color": PINK, "dir": (-1, 0)},
        {"rect": pygame.Rect(8 * TILE + 4, 9 * TILE + 4, TILE - 8, TILE - 8), "color": CYAN, "dir": (0, -1)},
    ]
    vx = vy = 0
    score = 0
    power = 0
    over = False
    won = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if e.key == pygame.K_r:
                    return run()
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    vx, vy = -3, 0
                if e.key in (pygame.K_RIGHT, pygame.K_d):
                    vx, vy = 3, 0
                if e.key in (pygame.K_UP, pygame.K_w):
                    vx, vy = 0, -3
                if e.key in (pygame.K_DOWN, pygame.K_s):
                    vx, vy = 0, 3

        if not over and not won:
            if not blocked(player, walls, vx, vy):
                player.x += vx
                player.y += vy
            for p in pellets[:]:
                if player.colliderect(p):
                    pellets.remove(p)
                    score += 10
            for p in powers[:]:
                if player.colliderect(p):
                    powers.remove(p)
                    power = 300
                    score += 50
            if power:
                power -= 1
            dirs = [(3, 0), (-3, 0), (0, 3), (0, -3)]
            for g in ghosts:
                if random.random() < 0.04 or blocked(g["rect"], walls, *g["dir"]):
                    random.shuffle(dirs)
                    for d in dirs:
                        if not blocked(g["rect"], walls, *d):
                            g["dir"] = d
                            break
                if not blocked(g["rect"], walls, *g["dir"]):
                    g["rect"].x += g["dir"][0]
                    g["rect"].y += g["dir"][1]
                if g["rect"].colliderect(player):
                    if power:
                        g["rect"].topleft = (9 * TILE + 4, 7 * TILE + 4)
                        score += 200
                    else:
                        over = True
            if not pellets and not powers:
                won = True

        screen.fill(BG)
        for w in walls:
            pygame.draw.rect(screen, (40, 70, 200), w, border_radius=4)
            pygame.draw.rect(screen, CYAN, w, 1, border_radius=4)
        for p in pellets:
            pygame.draw.rect(screen, GOLD, p)
        for p in powers:
            pygame.draw.ellipse(screen, LIME if pygame.time.get_ticks() // 200 % 2 else WHITE, p)
        pygame.draw.circle(screen, YELLOW, player.center, player.w // 2)
        mouth = 0.4 if pygame.time.get_ticks() // 120 % 2 else 0.05
        pygame.draw.circle(screen, BG, (player.centerx + 6, player.centery), 6 if mouth > 0.2 else 2)
        for g in ghosts:
            col = WHITE if power and pygame.time.get_ticks() // 150 % 2 else g["color"]
            pygame.draw.circle(screen, col, (g["rect"].centerx, g["rect"].centery - 2), g["rect"].w // 2)
            pygame.draw.rect(screen, col, (g["rect"].x, g["rect"].centery - 2, g["rect"].w, g["rect"].h // 2 + 2))
            pygame.draw.circle(screen, WHITE, (g["rect"].centerx - 5, g["rect"].centery - 4), 4)
            pygame.draw.circle(screen, WHITE, (g["rect"].centerx + 5, g["rect"].centery - 4), 4)

        draw_text(screen, f"SCORE {score}", 20, GOLD, topleft=(8, H - 40), bold=True)
        if power:
            draw_text(screen, "POWER", 20, LIME, topleft=(180, H - 40), bold=True)
        draw_text(screen, "ARROWS move   R restart   ESC", 16, WHITE, topleft=(300, H - 38))
        if over:
            draw_text(screen, "CAUGHT!", 48, RED, center=(W // 2, H // 2), bold=True)
        if won:
            draw_text(screen, "MAZE CLEARED!", 42, GOLD, center=(W // 2, H // 2), bold=True)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
