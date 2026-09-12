"""Sky Racer — neon highway dodge-em-up."""
import random
import sys
import pygame
from common import BG, PINK, CYAN, YELLOW, LIME, WHITE, RED, GOLD, PURPLE, draw_text

W, H = 480, 720


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Sky Racer — ElbowOS")
    clock = pygame.time.Clock()
    car = pygame.Rect(W // 2 - 18, H - 110, 36, 60)
    lanes = [90, 186, 282, 378]
    traffic = []
    coins = []
    speed = 6
    score = 0
    dist = 0
    over = False
    spawn = 0
    road_y = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                return run()

        keys = pygame.key.get_pressed()
        if not over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                car.x = max(70, car.x - 7)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                car.x = min(W - 106, car.x + 7)
            spawn -= 1
            if spawn <= 0:
                lane = random.choice(lanes)
                col = random.choice([PINK, CYAN, PURPLE, YELLOW, LIME])
                traffic.append({"rect": pygame.Rect(lane - 18, -70, 36, 60), "color": col})
                if random.random() < 0.4:
                    coins.append(pygame.Rect(random.choice(lanes) - 10, -30, 20, 20))
                spawn = max(18, 48 - dist // 400)
            for t in traffic:
                t["rect"].y += speed
            traffic[:] = [t for t in traffic if t["rect"].y < H + 20]
            for c in coins:
                c.y += speed
            coins[:] = [c for c in coins if c.y < H + 20]
            for t in traffic:
                if car.colliderect(t["rect"].inflate(-6, -8)):
                    over = True
            for c in coins[:]:
                if car.colliderect(c):
                    coins.remove(c)
                    score += 25
            dist += 1
            score += 1
            speed = 6 + dist / 800
            road_y = (road_y + speed) % 40

        screen.fill((16, 14, 28))
        pygame.draw.rect(screen, (36, 36, 48), (60, 0, 360, H))
        pygame.draw.rect(screen, GOLD, (60, 0, 8, H))
        pygame.draw.rect(screen, GOLD, (412, 0, 8, H))
        for y in range(-40, H, 40):
            pygame.draw.rect(screen, WHITE, (W // 2 - 4, y + int(road_y), 8, 22))
        for t in traffic:
            pygame.draw.rect(screen, t["color"], t["rect"], border_radius=8)
            pygame.draw.rect(screen, WHITE, t["rect"].inflate(-16, -36))
        for c in coins:
            pygame.draw.ellipse(screen, GOLD, c)
        pygame.draw.rect(screen, CYAN, car, border_radius=8)
        pygame.draw.rect(screen, PINK, (car.x + 8, car.y + 10, 20, 14), border_radius=3)
        pygame.draw.rect(screen, YELLOW, (car.x + 6, car.bottom - 10, 8, 6))
        pygame.draw.rect(screen, YELLOW, (car.right - 14, car.bottom - 10, 8, 6))

        draw_text(screen, f"SCORE {score}", 22, GOLD, topleft=(12, 10), bold=True)
        draw_text(screen, "A/D steer  R retry  ESC", 16, WHITE, topleft=(12, H - 28))
        if over:
            draw_text(screen, "CRASHED", 48, RED, center=(W // 2, H // 2), bold=True)
            draw_text(screen, "Press R", 22, WHITE, center=(W // 2, H // 2 + 40))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
