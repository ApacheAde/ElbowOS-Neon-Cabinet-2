"""Neon 2048 — sliding tile puzzle."""
import random
import sys
import pygame
from common import BG, WHITE, GOLD, draw_text

W, H = 520, 640
SIZE = 4
CELL = 108
PAD = 12
BOARD = SIZE * CELL + (SIZE + 1) * PAD
OX = (W - BOARD) // 2
OY = 90

COLORS = {
    0: (36, 32, 58),
    2: (90, 200, 220),
    4: (80, 180, 255),
    8: (90, 255, 170),
    16: (255, 210, 80),
    32: (255, 160, 60),
    64: (255, 100, 80),
    128: (255, 80, 160),
    256: (200, 90, 255),
    512: (140, 90, 255),
    1024: (255, 70, 120),
    2048: (255, 215, 70),
}


def empty():
    return [[0] * SIZE for _ in range(SIZE)]


def spawn(grid):
    spots = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0]
    if not spots:
        return
    r, c = random.choice(spots)
    grid[r][c] = 4 if random.random() < 0.1 else 2


def compress_line(line):
    nums = [n for n in line if n]
    out, score = [], 0
    i = 0
    while i < len(nums):
        if i + 1 < len(nums) and nums[i] == nums[i + 1]:
            out.append(nums[i] * 2)
            score += nums[i] * 2
            i += 2
        else:
            out.append(nums[i])
            i += 1
    out += [0] * (SIZE - len(out))
    return out, score


def move(grid, direction):
    new = [row[:] for row in grid]
    gained = 0
    if direction == "left":
        for r in range(SIZE):
            new[r], s = compress_line(new[r])
            gained += s
    elif direction == "right":
        for r in range(SIZE):
            rev, s = compress_line(list(reversed(new[r])))
            new[r] = list(reversed(rev))
            gained += s
    elif direction == "up":
        for c in range(SIZE):
            col, s = compress_line([new[r][c] for r in range(SIZE)])
            gained += s
            for r in range(SIZE):
                new[r][c] = col[r]
    elif direction == "down":
        for c in range(SIZE):
            col, s = compress_line(list(reversed([new[r][c] for r in range(SIZE)])))
            gained += s
            col = list(reversed(col))
            for r in range(SIZE):
                new[r][c] = col[r]
    changed = new != grid
    return new, gained, changed


def can_move(grid):
    if any(0 in row for row in grid):
        return True
    for r in range(SIZE):
        for c in range(SIZE):
            v = grid[r][c]
            if c + 1 < SIZE and grid[r][c + 1] == v:
                return True
            if r + 1 < SIZE and grid[r + 1][c] == v:
                return True
    return False


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon 2048 — ElbowOS")
    clock = pygame.time.Clock()
    grid = empty()
    spawn(grid)
    spawn(grid)
    score = 0
    best = 0
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
                    grid = empty()
                    spawn(grid)
                    spawn(grid)
                    score = 0
                    won = False
                mapping = {
                    pygame.K_LEFT: "left",
                    pygame.K_a: "left",
                    pygame.K_RIGHT: "right",
                    pygame.K_d: "right",
                    pygame.K_UP: "up",
                    pygame.K_w: "up",
                    pygame.K_DOWN: "down",
                    pygame.K_s: "down",
                }
                if e.key in mapping and can_move(grid):
                    grid, gained, changed = move(grid, mapping[e.key])
                    if changed:
                        score += gained
                        best = max(best, score)
                        spawn(grid)
                        if any(2048 in row for row in grid):
                            won = True

        screen.fill(BG)
        draw_text(screen, "NEON 2048", 36, GOLD, center=(W // 2, 28), bold=True)
        draw_text(screen, f"SCORE {score}", 20, WHITE, topleft=(OX, 54))
        draw_text(screen, f"BEST {best}", 20, WHITE, topleft=(OX + 200, 54))
        pygame.draw.rect(screen, (28, 24, 50), (OX, OY, BOARD, BOARD), border_radius=12)
        for r in range(SIZE):
            for c in range(SIZE):
                v = grid[r][c]
                x = OX + PAD + c * (CELL + PAD)
                y = OY + PAD + r * (CELL + PAD)
                col = COLORS.get(v, (255, 255, 255))
                pygame.draw.rect(screen, col, (x, y, CELL, CELL), border_radius=10)
                if v:
                    shade = (20, 16, 30)
                    draw_text(screen, str(v), 28 if v < 1000 else 22, shade, center=(x + CELL // 2, y + CELL // 2), bold=True)

        if not can_move(grid):
            draw_text(screen, "NO MOVES — R to reset", 22, (255, 90, 110), center=(W // 2, H - 40), bold=True)
        elif won:
            draw_text(screen, "2048! Keep going or R reset", 20, GOLD, center=(W // 2, H - 40))
        else:
            draw_text(screen, "ARROWS / WASD   R reset   ESC", 16, WHITE, center=(W // 2, H - 36))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
