"""Connect Glow — colourful Connect Four."""
import sys
import pygame
from common import BG, PINK, CYAN, YELLOW, WHITE, RED, GOLD, draw_text

COLS, ROWS = 7, 6
CELL = 78
PAD = 10
BOARD_W = COLS * CELL + (COLS + 1) * PAD
BOARD_H = ROWS * CELL + (ROWS + 1) * PAD
W, H = max(BOARD_W + 40, 640), BOARD_H + 140
OX = (W - BOARD_W) // 2
OY = 80


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Connect Glow — ElbowOS")
    clock = pygame.time.Clock()
    grid = [[0] * COLS for _ in range(ROWS)]
    turn = 1
    winner = 0
    hover = 0

    def drop(col, who):
        for r in range(ROWS - 1, -1, -1):
            if grid[r][col] == 0:
                grid[r][col] = who
                return r
        return None

    def check(who):
        def four(cells):
            return all(grid[r][c] == who for r, c in cells)

        for r in range(ROWS):
            for c in range(COLS):
                if c + 3 < COLS and four([(r, c + i) for i in range(4)]):
                    return True
                if r + 3 < ROWS and four([(r + i, c) for i in range(4)]):
                    return True
                if r + 3 < ROWS and c + 3 < COLS and four([(r + i, c + i) for i in range(4)]):
                    return True
                if r + 3 < ROWS and c - 3 >= 0 and four([(r + i, c - i) for i in range(4)]):
                    return True
        return False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.MOUSEMOTION:
                mx = e.pos[0] - OX - PAD
                hover = max(0, min(COLS - 1, mx // (CELL + PAD)))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                grid = [[0] * COLS for _ in range(ROWS)]
                turn, winner = 1, 0
            if e.type == pygame.MOUSEBUTTONDOWN and not winner:
                row = drop(hover, turn)
                if row is not None:
                    if check(turn):
                        winner = turn
                    elif all(grid[0][c] for c in range(COLS)):
                        winner = -1
                    else:
                        turn = 2 if turn == 1 else 1

        screen.fill(BG)
        draw_text(screen, "CONNECT GLOW", 32, GOLD, center=(W // 2, 28), bold=True)
        pygame.draw.rect(screen, (30, 50, 140), (OX, OY, BOARD_W, BOARD_H), border_radius=16)
        for r in range(ROWS):
            for c in range(COLS):
                x = OX + PAD + c * (CELL + PAD) + CELL // 2
                y = OY + PAD + r * (CELL + PAD) + CELL // 2
                val = grid[r][c]
                col = (18, 16, 36) if val == 0 else (PINK if val == 1 else CYAN)
                pygame.draw.circle(screen, col, (x, y), CELL // 2 - 4)
                if val:
                    pygame.draw.circle(screen, WHITE, (x - 10, y - 10), 6)

        if not winner:
            hx = OX + PAD + hover * (CELL + PAD) + CELL // 2
            pygame.draw.circle(screen, PINK if turn == 1 else CYAN, (hx, OY - 18), 14)

        if winner == 1:
            draw_text(screen, "PINK CONNECTS FOUR!", 26, PINK, center=(W // 2, H - 40), bold=True)
        elif winner == 2:
            draw_text(screen, "CYAN CONNECTS FOUR!", 26, CYAN, center=(W // 2, H - 40), bold=True)
        elif winner == -1:
            draw_text(screen, "DRAW — board full", 24, YELLOW, center=(W // 2, H - 40))
        else:
            draw_text(screen, "Click a column   R reset   ESC", 16, WHITE, center=(W // 2, H - 36))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
