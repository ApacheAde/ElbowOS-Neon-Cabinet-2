"""Pipe Hero — original Mario-style platformer (not an emulator)."""
import sys
import pygame
from common import BG, PINK, CYAN, YELLOW, LIME, ORANGE, WHITE, RED, GOLD, draw_text

W, H = 960, 540
GRAVITY = 0.55
JUMP = -11.5


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.alive = True
        self.coins = 0
        self.lives = 3

    def update(self, keys, platforms):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -4.4
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 4.4
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False
        self.vy += GRAVITY
        self.rect.x += int(self.vx)
        self._collide(platforms, "x")
        self.rect.y += int(self.vy)
        self.on_ground = False
        self._collide(platforms, "y")
        if self.rect.top > H + 80:
            self.alive = False

    def _collide(self, platforms, axis):
        for p in platforms:
            if self.rect.colliderect(p):
                if axis == "x":
                    if self.vx > 0:
                        self.rect.right = p.left
                    elif self.vx < 0:
                        self.rect.left = p.right
                else:
                    if self.vy > 0:
                        self.rect.bottom = p.top
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        self.rect.top = p.bottom
                        self.vy = 0

    def draw(self, surf, cam):
        r = self.rect.move(-cam, 0)
        body = pygame.Rect(r.x, r.y + 8, r.w, r.h - 8)
        pygame.draw.rect(surf, (255, 90, 70), body, border_radius=6)
        pygame.draw.rect(surf, (40, 90, 255), (r.x, r.y + 20, r.w, 10))
        hat = pygame.Rect(r.x - 2, r.y, r.w + 4, 12)
        pygame.draw.rect(surf, RED, hat, border_radius=4)
        eye_x = r.centerx + (6 if self.facing > 0 else -6)
        pygame.draw.circle(surf, WHITE, (eye_x, r.y + 16), 4)
        pygame.draw.circle(surf, (20, 20, 30), (eye_x + self.facing * 1, r.y + 16), 2)


class Walker:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 30, 28)
        self.left = left
        self.right = right
        self.dir = 1
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.dir * 2
        if self.rect.left < self.left or self.rect.right > self.right:
            self.dir *= -1

    def draw(self, surf, cam):
        if not self.alive:
            return
        r = self.rect.move(-cam, 0)
        pygame.draw.ellipse(surf, (180, 90, 40), r)
        pygame.draw.ellipse(surf, (90, 40, 20), r.inflate(-10, -14))
        pygame.draw.circle(surf, WHITE, (r.centerx - 6, r.y + 10), 4)
        pygame.draw.circle(surf, WHITE, (r.centerx + 6, r.y + 10), 4)


def build_world():
    plats = [
        pygame.Rect(0, 500, 2200, 40),
        pygame.Rect(180, 420, 140, 18),
        pygame.Rect(380, 360, 120, 18),
        pygame.Rect(560, 300, 160, 18),
        pygame.Rect(820, 380, 180, 18),
        pygame.Rect(1080, 320, 140, 18),
        pygame.Rect(1280, 420, 160, 18),
        pygame.Rect(1500, 340, 200, 18),
        pygame.Rect(1780, 260, 140, 18),
        pygame.Rect(1960, 420, 180, 18),
        pygame.Rect(700, 500, 80, 40),
    ]
    coins = [
        pygame.Rect(220, 380, 16, 16),
        pygame.Rect(420, 320, 16, 16),
        pygame.Rect(600, 260, 16, 16),
        pygame.Rect(880, 340, 16, 16),
        pygame.Rect(1120, 280, 16, 16),
        pygame.Rect(1540, 300, 16, 16),
        pygame.Rect(1820, 220, 16, 16),
        pygame.Rect(2000, 380, 16, 16),
    ]
    foes = [
        Walker(400, 472, 240, 700),
        Walker(860, 352, 820, 1000),
        Walker(1520, 312, 1500, 1700),
        Walker(1100, 472, 1000, 1400),
    ]
    flag = pygame.Rect(2100, 360, 16, 140)
    return plats, coins, foes, flag


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Hero — ElbowOS")
    clock = pygame.time.Clock()
    player = Player(60, 400)
    plats, coins, foes, flag = build_world()
    cam = 0
    won = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                player = Player(60, 400)
                plats, coins, foes, flag = build_world()
                won = False

        keys = pygame.key.get_pressed()
        if player.alive and not won:
            player.update(keys, plats)
            for f in foes:
                f.update()
                if f.alive and player.rect.colliderect(f.rect):
                    if player.vy > 0 and player.rect.bottom - f.rect.top < 18:
                        f.alive = False
                        player.vy = -8
                    else:
                        player.alive = False
            for c in coins[:]:
                if player.rect.colliderect(c):
                    coins.remove(c)
                    player.coins += 1
            if player.rect.colliderect(flag):
                won = True
            cam = max(0, min(player.rect.centerx - W // 3, 2200 - W))

        if not player.alive:
            player.lives -= 1
            if player.lives > 0:
                saved = player.coins, player.lives
                player = Player(60, 400)
                player.coins, player.lives = saved

        screen.fill((28, 160, 230))
        pygame.draw.rect(screen, (40, 200, 90), (0, 500, W, 40))
        for i in range(12):
            cloud_x = (i * 220 - cam // 3) % (W + 200) - 80
            pygame.draw.ellipse(screen, (240, 250, 255), (cloud_x, 40 + (i % 3) * 30, 90, 36))
            pygame.draw.ellipse(screen, (240, 250, 255), (cloud_x + 30, 28 + (i % 3) * 30, 70, 34))

        for p in plats:
            r = p.move(-cam, 0)
            if r.right < 0 or r.left > W:
                continue
            pygame.draw.rect(screen, (90, 190, 70), r, border_radius=3)
            pygame.draw.rect(screen, (60, 130, 40), r, 2, border_radius=3)

        pygame.draw.rect(screen, LIME, flag.move(-cam, 0))
        pygame.draw.polygon(
            screen,
            GOLD,
            [(flag.x - cam + 16, flag.y + 8), (flag.x - cam + 70, flag.y + 24), (flag.x - cam + 16, flag.y + 40)],
        )

        for c in coins:
            r = c.move(-cam, 0)
            pygame.draw.ellipse(screen, GOLD, r)
            pygame.draw.ellipse(screen, YELLOW, r.inflate(-6, -4))

        for f in foes:
            f.draw(screen, cam)
        player.draw(screen, cam)

        draw_text(screen, f"COINS {player.coins}", 22, GOLD, topleft=(16, 12), bold=True)
        draw_text(screen, f"LIVES {max(player.lives, 0)}", 22, PINK, topleft=(160, 12), bold=True)
        draw_text(screen, "ARROWS/AD  SPACE jump   R restart   ESC quit", 16, WHITE, topleft=(16, H - 28))
        draw_text(screen, "Pipe Hero  •  ElbowOS", 16, CYAN, topleft=(720, 12))

        if won:
            draw_text(screen, "LEVEL CLEAR!", 54, GOLD, center=(W // 2, H // 2 - 20), bold=True)
            draw_text(screen, "Press R to play again", 22, WHITE, center=(W // 2, H // 2 + 30))
        elif player.lives <= 0 and not player.alive:
            draw_text(screen, "GAME OVER", 54, RED, center=(W // 2, H // 2 - 20), bold=True)
            draw_text(screen, "Press R to retry", 22, WHITE, center=(W // 2, H // 2 + 30))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
