"""Neon Craps — simple pass-line casino dice game."""
import random
import sys
import pygame
from common import BG, PANEL, PINK, CYAN, YELLOW, LIME, WHITE, RED, GOLD, draw_text

W, H = 800, 560


def roll():
    return random.randint(1, 6), random.randint(1, 6)


def pip_centers(n):
    c = (0.5, 0.5)
    spots = {
        1: [c],
        2: [(0.28, 0.28), (0.72, 0.72)],
        3: [(0.28, 0.28), c, (0.72, 0.72)],
        4: [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)],
        5: [(0.28, 0.28), (0.72, 0.28), c, (0.28, 0.72), (0.72, 0.72)],
        6: [(0.28, 0.22), (0.72, 0.22), (0.28, 0.5), (0.72, 0.5), (0.28, 0.78), (0.72, 0.78)],
    }
    return spots[n]


def draw_die(surf, x, y, n, size=90):
    pygame.draw.rect(surf, WHITE, (x, y, size, size), border_radius=12)
    pygame.draw.rect(surf, (200, 200, 220), (x, y, size, size), 3, border_radius=12)
    for px, py in pip_centers(n):
        pygame.draw.circle(surf, (30, 24, 50), (int(x + px * size), int(y + py * size)), 8)


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Craps — ElbowOS")
    clock = pygame.time.Clock()
    bank = 200
    bet = 10
    point = None
    dice = (3, 4)
    msg = "Pass-line bet. SPACE to roll the come-out."
    spinning = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if e.key == pygame.K_UP:
                    bet = min(50, bank, bet + 5)
                if e.key == pygame.K_DOWN:
                    bet = max(5, bet - 5)
                if e.key == pygame.K_r:
                    bank, bet, point = 200, 10, None
                    msg = "Bank reset. SPACE to roll."
                if e.key == pygame.K_SPACE and spinning == 0 and bank >= bet:
                    spinning = 18

        if spinning:
            dice = roll()
            spinning -= 1
            if spinning == 0:
                total = sum(dice)
                if point is None:
                    if total in (7, 11):
                        bank += bet
                        msg = f"Come-out {total} — NATURAL! +${bet}"
                    elif total in (2, 3, 12):
                        bank -= bet
                        msg = f"Come-out {total} — CRAPS. -${bet}"
                    else:
                        point = total
                        msg = f"Point is {point}. Roll {point} before 7."
                else:
                    if total == point:
                        bank += bet
                        msg = f"Hit the point {point}! +${bet}"
                        point = None
                    elif total == 7:
                        bank -= bet
                        msg = "Seven-out. Line loses."
                        point = None
                    else:
                        msg = f"Rolled {total}. Point still {point}."
                if bank < bet:
                    bet = max(5, bank)

        screen.fill(BG)
        pygame.draw.rect(screen, (18, 90, 48), (40, 70, 720, 300), border_radius=16)
        pygame.draw.rect(screen, GOLD, (40, 70, 720, 300), 3, border_radius=16)
        draw_text(screen, "NEON CRAPS", 36, GOLD, center=(W // 2, 36), bold=True)
        draw_text(screen, "PASS LINE", 22, WHITE, center=(W // 2, 100), bold=True)
        if point:
            draw_text(screen, f"POINT {point}", 28, YELLOW, center=(W // 2, 140), bold=True)
        else:
            draw_text(screen, "COME-OUT ROLL", 24, CYAN, center=(W // 2, 140))

        draw_die(screen, 250, 190, dice[0])
        draw_die(screen, 460, 190, dice[1])
        draw_text(screen, f"= {sum(dice)}", 32, WHITE, center=(W // 2, 330), bold=True)

        pygame.draw.rect(screen, PANEL, (40, 390, 720, 140), border_radius=12)
        draw_text(screen, f"BANK  ${bank}", 28, LIME, topleft=(60, 408), bold=True)
        draw_text(screen, f"BET   ${bet}", 28, PINK, topleft=(60, 450), bold=True)
        draw_text(screen, msg, 20, WHITE, topleft=(280, 416))
        draw_text(screen, "SPACE roll   UP/DOWN bet   R reset   ESC", 16, CYAN, topleft=(280, 456))
        draw_text(screen, "Pass line: 7/11 win, 2/3/12 lose, else set point.", 16, WHITE, topleft=(280, 486))
        if bank <= 0:
            draw_text(screen, "BUSTED — press R", 26, RED, center=(W // 2, 530), bold=True)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
