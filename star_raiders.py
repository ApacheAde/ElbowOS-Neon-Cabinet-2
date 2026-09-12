"""Star Raiders — colourful space-invader style shooter."""
import random
import sys
import pygame
from common import BG, PINK, CYAN, YELLOW, LIME, WHITE, RED, PURPLE, GOLD, draw_text

W, H = 800, 600
ORANGE = (255, 140, 50)


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Star Raiders — ElbowOS")
    clock = pygame.time.Clock()

    ship = pygame.Rect(W // 2 - 16, H - 60, 32, 28)
    bullets = []
    enemies = []
    particles = []
    score = 0
    lives = 3
    wave = 1
    cooldown = 0
    over = False
    stars = [(random.randint(0, W), random.randint(0, H), random.randint(1, 3)) for _ in range(70)]

    def spawn_wave(n):
        rows = 3 + min(n, 3)
        cols = 7
        for r in range(rows):
            for c in range(cols):
                enemies.append(
                    {
                        "rect": pygame.Rect(70 + c * 90, 50 + r * 48, 36, 26),
                        "dir": 1,
                        "color": random.choice([PINK, CYAN, LIME, PURPLE, ORANGE]),
                    }
                )

    spawn_wave(wave)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r and over:
                return run()

        keys = pygame.key.get_pressed()
        if not over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ship.x = max(10, ship.x - 7)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ship.x = min(W - 42, ship.x + 7)
            cooldown = max(0, cooldown - 1)
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and cooldown == 0:
                bullets.append(pygame.Rect(ship.centerx - 2, ship.y - 10, 4, 14))
                cooldown = 12

            for b in bullets[:]:
                b.y -= 11
                if b.bottom < 0:
                    bullets.remove(b)

            edge = False
            for en in enemies:
                en["rect"].x += en["dir"] * (1 + wave * 0.25)
                if en["rect"].right > W - 10 or en["rect"].left < 10:
                    edge = True
            if edge:
                for en in enemies:
                    en["dir"] *= -1
                    en["rect"].y += 12

            for en in enemies[:]:
                for b in bullets[:]:
                    if en["rect"].colliderect(b):
                        enemies.remove(en)
                        if b in bullets:
                            bullets.remove(b)
                        score += 10 * wave
                        for _ in range(10):
                            particles.append(
                                [en["rect"].centerx, en["rect"].centery, random.uniform(-3, 3), random.uniform(-3, 3), en["color"], 20]
                            )
                        break
                if en in enemies and (en["rect"].colliderect(ship) or en["rect"].bottom >= H - 40):
                    lives -= 1
                    enemies.clear()
                    bullets.clear()
                    ship.x = W // 2 - 16
                    if lives <= 0:
                        over = True
                    else:
                        spawn_wave(wave)

            if not enemies and not over:
                wave += 1
                spawn_wave(wave)

            for p in particles[:]:
                p[0] += p[2]
                p[1] += p[3]
                p[5] -= 1
                if p[5] <= 0:
                    particles.remove(p)

        screen.fill(BG)
        for i, (sx, sy, sz) in enumerate(stars):
            sy = (sy + sz) % H
            stars[i] = (sx, sy, sz)
            pygame.draw.circle(screen, WHITE, (sx, int(sy)), sz)

        pygame.draw.polygon(screen, CYAN, [(ship.centerx, ship.y), (ship.left, ship.bottom), (ship.right, ship.bottom)])
        pygame.draw.rect(screen, PINK, (ship.centerx - 3, ship.bottom - 6, 6, 8))

        for b in bullets:
            pygame.draw.rect(screen, YELLOW, b)
        for en in enemies:
            pygame.draw.rect(screen, en["color"], en["rect"], border_radius=6)
            pygame.draw.rect(screen, WHITE, en["rect"].inflate(-18, -14))
        for p in particles:
            pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), 3)

        draw_text(screen, f"SCORE {score}", 22, GOLD, topleft=(12, 8), bold=True)
        draw_text(screen, f"WAVE {wave}", 22, CYAN, topleft=(220, 8), bold=True)
        draw_text(screen, f"LIVES {lives}", 22, PINK, topleft=(360, 8), bold=True)
        draw_text(screen, "A/D or arrows  SPACE fire  ESC quit", 16, WHITE, topleft=(12, H - 24))
        if over:
            draw_text(screen, "DESTROYED", 56, RED, center=(W // 2, H // 2 - 10), bold=True)
            draw_text(screen, "Press R to reboot the raid", 22, WHITE, center=(W // 2, H // 2 + 36))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
