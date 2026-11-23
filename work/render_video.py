#!/usr/bin/env python3
"""Render 'Lumen Run — Day 1 vs Day 7' (1080x1920, 30fps, 27.0s) with PIL.

Mirrors game/game.js exactly: same constants (ground, start, speed, gap, spike,
coins, flag) and the same scripted playthrough (jump over the gap at t=2.5s,
jump over the spike at t=3.35s). Day 1 and day 7 share the map, the start and
the finish — only the amount going on differs. Written fresh in this session.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(OUT, 'frames')
os.makedirs(FRAMES, exist_ok=True)

W, H = 1080, 1920
GROUND_Y = 1250
START_X, SPEED = 180, 140
FLAG_X = 1000
GAP = (480, 560)
SPIKE_X = 700
COINS = {1: [600], 7: [300, 400, 500, 600, 860, 900, 940]}
COIN_Y = 1130
FPS = 30

FONT_DIR = '/home/hatch/workspace/makefun/entries/bring-the-humans-03/fonts'
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
F_BIG = font('Inter-Bold.ttf', 96)
F_MED = font('Inter-Bold.ttf', 64)
F_SMALL = font('Inter-Bold.ttf', 46)
F_TINY = font('Inter-Bold.ttf', 38)
F_HUD = font('Inter-Bold.ttf', 54)
F_SCORE = font('Inter-Bold.ttf', 44)

MAGENTA = (230, 0, 126)
INK = (25, 20, 25)
WHITE = (255, 255, 255)

def lerp(a, b, u):
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))

def build_bg(day):
    img = Image.new('RGB', (W, H), (201, 201, 201))
    d = ImageDraw.Draw(img)
    if day == 1:
        d.rectangle([0, 0, W, GROUND_Y], fill=(201, 201, 201))
        d.rectangle([0, GROUND_Y, W, H], fill=(138, 138, 138))
    else:
        for y in range(GROUND_Y):
            d.line([(0, y), (W, y)], fill=lerp((126, 200, 247), (223, 243, 255), y / GROUND_Y))
        d.ellipse([790, 130, 970, 310], fill=(255, 217, 77))  # sun
        for cx, cy in [(220, 260), (520, 180), (800, 320)]:
            d.ellipse([cx - 90, cy - 34, cx + 90, cy + 34], fill=(255, 255, 255))
        d.ellipse([-120, GROUND_Y - 120, 520, GROUND_Y + 120], fill=(143, 206, 110))
        d.ellipse([720, GROUND_Y - 140, 1200, GROUND_Y + 140], fill=(143, 206, 110))
        d.rectangle([0, GROUND_Y, W, H], fill=(93, 162, 74))
        for x in [120, 340, 640, 900]:  # trees
            d.rectangle([x - 12, GROUND_Y - 170, x + 12, GROUND_Y], fill=(122, 74, 33))
            d.ellipse([x - 70, GROUND_Y - 280, x + 70, GROUND_Y - 140], fill=(47, 158, 68))
        for x in [220, 420, 560, 760, 940]:  # flowers
            d.ellipse([x - 12, GROUND_Y - 36, x + 12, GROUND_Y - 12], fill=(255, 107, 157))
            d.ellipse([x - 5, GROUND_Y - 29, x + 5, GROUND_Y - 19], fill=(255, 255, 255))
    # gap (both builds): a hole in the ground
    d.rectangle([GAP[0], GROUND_Y, GAP[1], GROUND_Y + 260],
                fill=(201, 201, 201) if day == 1 else (223, 243, 255))
    d.rectangle([GAP[0] - 6, GROUND_Y, GAP[0], GROUND_Y + 260], fill=(111, 111, 111) if day == 1 else (62, 122, 51))
    d.rectangle([GAP[1], GROUND_Y, GAP[1] + 6, GROUND_Y + 260], fill=(111, 111, 111) if day == 1 else (62, 122, 51))
    # finish flag (both builds)
    d.rectangle([FLAG_X, GROUND_Y - 220, FLAG_X + 8, GROUND_Y], fill=(51, 51, 51))
    d.polygon([(FLAG_X + 8, GROUND_Y - 220), (FLAG_X + 110, GROUND_Y - 185),
               (FLAG_X + 8, GROUND_Y - 150)], fill=(255, 89, 100))
    return img

BG = {1: build_bg(1), 7: build_bg(7)}

def jump_y(t):
    """Scripted jumps: over the gap (t 2.5-3.5) and over the spike (t 3.35-4.45)."""
    for start, dur, h in [(2.5, 1.0, 220), (3.35, 1.1, 240)]:
        if start <= t < start + dur:
            u = (t - start) / dur
            return -h * 4 * u * (1 - u)
    return 0.0

def player_xy(t):
    x = min(FLAG_X, START_X + SPEED * t)
    return x, GROUND_Y - 70 + jump_y(t)

def coins_state(day, t):
    """A coin is collected once the player has run past it low enough to grab it
    (same rule as game.js: jump height above the coin line misses it)."""
    px, _ = player_xy(t)
    out = []
    for cx in COINS[day]:
        t_coin = (cx - START_X) / SPEED
        got = px >= cx - 46 and jump_y(t_coin) > -120
        out.append((cx, got, t_coin if got else None))
    return out

def draw_frame(day, t, label=None, sublabel=None, confetti_t=None, score_override=None):
    img = BG[day].copy()
    d = ImageDraw.Draw(img, 'RGBA')
    px, py = player_xy(t)
    # trail (day 7)
    if day == 7:
        for i in range(12):
            tx = px - 46 - i * 9
            ty = py + (jump_y(t - i * 0.016) - jump_y(t)) * 0.4
            a = max(0, int(150 - i * 13))
            d.ellipse([tx - 13, ty - 13, tx + 13, ty + 13], fill=(255, 217, 77, a))
    # coins
    for cx, got, got_at in coins_state(day, t):
        if got:
            if got_at is not None and 0 <= t - got_at < 0.35:  # sparkle
                r = 26 + (t - got_at) * 90
                d.ellipse([cx - r, COIN_Y - r, cx + r, COIN_Y + r],
                          outline=(255, 207, 61), width=5)
            continue
        d.ellipse([cx - 26, COIN_Y - 26, cx + 26, COIN_Y + 26], fill=(255, 207, 61))
        d.text((cx, COIN_Y), '$', font=F_SMALL, fill=(200, 147, 10), anchor='mm')
    # spike (day 7)
    if day == 7:
        d.polygon([(SPIKE_X - 26, GROUND_Y), (SPIKE_X, GROUND_Y - 64),
                   (SPIKE_X + 26, GROUND_Y)], fill=(61, 61, 61))
    # player
    body = (85, 85, 85) if day == 1 else (255, 89, 100)
    d.rounded_rectangle([px - 34, py - 34, px + 34, py + 34], radius=10, fill=body)
    d.rectangle([px + 6, py - 20, px + 20, py - 6], fill=WHITE)
    d.rectangle([px + 24, py - 20, px + 38, py - 6], fill=WHITE)
    d.rectangle([px + 11, py - 15, px + 17, py - 9], fill=(17, 17, 17))
    d.rectangle([px + 29, py - 15, px + 35, py - 9], fill=(17, 17, 17))
    # confetti (finish, day 7)
    if confetti_t is not None and day == 7:
        rng = random.Random(7)
        for i in range(90):
            cx0 = FLAG_X + (rng.random() - 0.5) * 500
            cy0 = 500 + rng.random() * 200
            vx = (rng.random() - 0.5) * 260
            vy = 60 + rng.random() * 220
            col = [(255, 89, 100), (255, 217, 77), (77, 171, 255), (81, 224, 122)][i % 4]
            d.rectangle([cx0 + vx * confetti_t, cy0 + vy * confetti_t,
                         cx0 + vx * confetti_t + 12, cy0 + vy * confetti_t + 18], fill=col)
    # HUD
    d.text((48, 48), 'DAY 1' if day == 1 else 'DAY 7', font=F_HUD,
           fill=(85, 85, 85) if day == 1 else (18, 51, 34))
    if day == 7:
        got_n = sum(1 for _, got, _ in coins_state(day, t) if got)
        score = got_n * 100 if score_override is None else score_override
        d.text((48, 130), 'SCORE %d' % score, font=F_SCORE, fill=(18, 51, 34))
        d.text((W - 48, 48), 'COINS %d/%d' % (got_n, len(COINS[7])), font=F_SCORE,
               fill=(18, 51, 34), anchor='ra')
    if t >= (FLAG_X - START_X) / SPEED:
        d.text((W // 2, 620), 'FINISH!', font=F_BIG, fill=(18, 51, 34), anchor='ma')
    # label bars
    if label:
        d.rectangle([0, H - 370, W, H - 180], fill=(25, 20, 25, 215))
        d.text((W // 2, H - 340), label, font=F_MED, fill=WHITE, anchor='ma')
        if sublabel:
            d.text((W // 2, H - 255), sublabel, font=F_SMALL, fill=(255, 217, 77), anchor='ma')
    return img

def text_card(lines, accent=None):
    img = Image.new('RGB', (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 26], fill=MAGENTA)
    d.rectangle([0, H - 26, W, H], fill=MAGENTA)
    y = 640
    for line, f in lines:
        d.text((W // 2, y), line, font=f, fill=WHITE, anchor='ma')
        y += f.size + 46
    if accent:
        d.text((W // 2, y + 30), accent, font=F_SMALL, fill=(255, 217, 77), anchor='ma')
    return img

SEGMENTS = []  # (kind, day, t0, t1, label, sublabel)
# kind: 'card' (lines) | 'run' (gameplay)
HOOK = [('My AI agent built', F_BIG), ('a tiny game.', F_BIG),
        ('Then updated it', F_BIG), ('EVERY DAY', F_BIG), ('for a week.', F_BIG)]
CTA = [('Your turn.', F_BIG), ('Start yours at', F_BIG), ('make.fun', F_BIG)]

def add(kind, dur, **kw):
    SEGMENTS.append((kind, dur, kw))

add('card', 3.0, lines=HOOK, accent='DAY 1  vs  DAY 7 — same map, same start')
add('run', 6.0, day=1, label='DAY 1', sublabel='a grey square, one coin, flat ground')
add('run', 6.0, day=7, label='DAY 7', sublabel='same map, same start — one week later')
# identical-moment match cuts: same moment, day 1 then day 7
for (t0, label) in [(2.4, 'THE JUMP'), (2.9, 'THE COIN'), (5.0, 'THE FINISH')]:
    add('run', 1.0, day=1, t0=t0, label='DAY 1 — ' + label, sublabel='same moment')
    add('run', 1.0, day=7, t0=t0, label='DAY 7 — ' + label, sublabel='same moment')
# close: day-7 finish + confetti + CTA card
add('run', 2.0, day=7, t0=4.0, label='DAY 7', sublabel='the newer build, played')
add('run', 1.5, day=7, t0=5.85, confetti=True, label=None, sublabel=None)
add('card', 2.5, lines=CTA, accent=None)

def render():
    idx = 0
    for kind, dur, kw in SEGMENTS:
        n = int(round(dur * FPS))
        for i in range(n):
            u = i / FPS
            if kind == 'card':
                img = text_card(kw['lines'], kw.get('accent'))
            else:
                t = kw.get('t0', 0.0) + u
                conf = None
                if kw.get('confetti'):
                    conf = u + 0.15
                img = draw_frame(kw['day'], t, label=kw.get('label'),
                                 sublabel=kw.get('sublabel'), confetti_t=conf)
            img.save(os.path.join(FRAMES, 'frame_%04d.png' % idx))
            idx += 1
    print('frames:', idx, 'duration: %.2fs' % (idx / FPS))

if __name__ == '__main__':
    render()
