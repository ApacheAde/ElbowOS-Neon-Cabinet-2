"""Colour Klondike — simplified full-colour solitaire."""
import random
import sys
import pygame
from common import BG, WHITE, GOLD, PINK, CYAN, LIME, RED, draw_text

W, H = 960, 640
SUITS = [("\u2665", RED), ("\u2666", PINK), ("\u2660", CYAN), ("\u2663", LIME)]
RANKS = "A23456789TJQK"
CW, CH = 78, 108


def make_deck():
    deck = [(r, s, col) for s, col in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


def color_of(card):
    return card[2]


def rank_i(card):
    return RANKS.index(card[0])


def can_stack(moving, onto):
    if onto is None:
        return moving[0] == "K"
    return color_of(moving) != color_of(onto) and rank_i(moving) + 1 == rank_i(onto)


def can_foundation(moving, pile):
    if not pile:
        return moving[0] == "A"
    top = pile[-1]
    return moving[1] == top[1] and rank_i(moving) == rank_i(top) + 1


def draw_card(surf, card, x, y, face=True):
    rect = pygame.Rect(x, y, CW, CH)
    if not face:
        pygame.draw.rect(surf, (50, 40, 110), rect, border_radius=8)
        pygame.draw.rect(surf, PINK, rect, 2, border_radius=8)
        pygame.draw.rect(surf, CYAN, rect.inflate(-14, -14), 1, border_radius=6)
        return rect
    pygame.draw.rect(surf, WHITE, rect, border_radius=8)
    pygame.draw.rect(surf, card[2], rect, 2, border_radius=8)
    label = card[0].replace("T", "10")
    draw_text(surf, label, 18, card[2], topleft=(x + 6, y + 6), bold=True)
    draw_text(surf, card[1], 28, card[2], center=(x + CW // 2, y + CH // 2))
    return rect


def _take(src, tableau, waste, foundations):
    if src == "waste":
        waste.pop()
    elif src[0] == "found":
        foundations[src[1]].pop()
    else:
        _, pi, ni = src
        del tableau[pi][ni:]


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Colour Klondike — ElbowOS")
    clock = pygame.time.Clock()

    def deal():
        deck = make_deck()
        tableau = [[] for _ in range(7)]
        hidden = [0] * 7
        for i in range(7):
            for j in range(i + 1):
                tableau[i].append(deck.pop())
            hidden[i] = i
        stock = deck
        waste = []
        foundations = [[] for _ in range(4)]
        return tableau, hidden, stock, waste, foundations

    tableau, hidden, stock, waste, foundations = deal()
    dragging = None
    drag_pos = (0, 0)
    won = False

    def pile_rects():
        rects = []
        for i, pile in enumerate(tableau):
            x = 40 + i * (CW + 24)
            if not pile:
                rects.append((pygame.Rect(x, 180, CW, CH), i, -1))
            for n, _c in enumerate(pile):
                y = 180 + n * 26
                rects.append((pygame.Rect(x, y, CW, CH), i, n))
        return rects

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                tableau, hidden, stock, waste, foundations = deal()
                dragging = None
                won = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not won:
                mx, my = e.pos
                stock_r = pygame.Rect(40, 40, CW, CH)
                waste_r = pygame.Rect(40 + CW + 20, 40, CW, CH)
                if stock_r.collidepoint(mx, my):
                    if stock:
                        waste.append(stock.pop())
                    elif waste:
                        stock = list(reversed(waste))
                        waste = []
                    continue
                if waste and waste_r.collidepoint(mx, my):
                    dragging = ([waste[-1]], "waste")
                    drag_pos = (mx, my)
                    continue
                for i, pile in enumerate(foundations):
                    fr = pygame.Rect(420 + i * (CW + 16), 40, CW, CH)
                    if pile and fr.collidepoint(mx, my):
                        dragging = ([pile[-1]], ("found", i))
                        drag_pos = (mx, my)
                for rect, pi, ni in reversed(pile_rects()):
                    if ni >= 0 and ni >= hidden[pi] and rect.collidepoint(mx, my):
                        dragging = (tableau[pi][ni:], ("tab", pi, ni))
                        drag_pos = (mx, my)
                        break
            if e.type == pygame.MOUSEMOTION and dragging:
                drag_pos = e.pos
            if e.type == pygame.MOUSEBUTTONUP and dragging:
                cards, src = dragging
                mx, my = e.pos
                placed = False
                for i in range(4):
                    fr = pygame.Rect(420 + i * (CW + 16), 40, CW, CH)
                    if fr.collidepoint(mx, my) and len(cards) == 1 and can_foundation(cards[0], foundations[i]):
                        foundations[i].append(cards[0])
                        _take(src, tableau, waste, foundations)
                        placed = True
                        break
                if not placed:
                    for i, pile in enumerate(tableau):
                        x = 40 + i * (CW + 24)
                        y = 180 + max(0, len(pile) - 1) * 26
                        target = pygame.Rect(x, y, CW, CH + 40)
                        onto = pile[-1] if pile else None
                        if target.collidepoint(mx, my) and can_stack(cards[0], onto):
                            if src[0] == "tab" and src[1] == i:
                                break
                            tableau[i].extend(cards)
                            _take(src, tableau, waste, foundations)
                            placed = True
                            break
                dragging = None
                for i, pile in enumerate(tableau):
                    if pile and hidden[i] >= len(pile):
                        hidden[i] = max(0, len(pile) - 1)
                    if pile and hidden[i] == len(pile):
                        hidden[i] = len(pile) - 1
                if all(len(f) == 13 for f in foundations):
                    won = True

        screen.fill(BG)
        draw_text(screen, "COLOUR KLONDIKE", 24, GOLD, topleft=(40, 8), bold=True)
        draw_text(screen, "Drag cards  click stock  R new deal  ESC", 16, WHITE, topleft=(280, 12))
        stock_r = pygame.Rect(40, 40, CW, CH)
        if stock:
            draw_card(screen, stock[-1], 40, 40, face=False)
        else:
            pygame.draw.rect(screen, (40, 36, 70), stock_r, 2, border_radius=8)
        if waste:
            hide = dragging and dragging[1] == "waste"
            if not hide:
                draw_card(screen, waste[-1], 40 + CW + 20, 40)
        for i, pile in enumerate(foundations):
            x = 420 + i * (CW + 16)
            pygame.draw.rect(screen, (40, 36, 70), (x, 40, CW, CH), 2, border_radius=8)
            hide = dragging and dragging[1] == ("found", i)
            if pile and not hide:
                draw_card(screen, pile[-1], x, 40)
        skip = None
        if dragging and dragging[1][0] == "tab":
            skip = (dragging[1][1], dragging[1][2])
        for i, pile in enumerate(tableau):
            x = 40 + i * (CW + 24)
            if not pile:
                pygame.draw.rect(screen, (40, 36, 70), (x, 180, CW, CH), 2, border_radius=8)
            for n, card in enumerate(pile):
                if skip and skip[0] == i and n >= skip[1]:
                    continue
                face = n >= hidden[i]
                draw_card(screen, card, x, 180 + n * 26, face=face)
        if dragging:
            mx, my = drag_pos
            for i, card in enumerate(dragging[0]):
                draw_card(screen, card, mx - CW // 2, my - 20 + i * 26)
        if won:
            draw_text(screen, "TABLE CLEARED!", 48, GOLD, center=(W // 2, H // 2), bold=True)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
    sys.exit(0)
