# Topic scenes: thunder (NWS sources). Reuses primitives from birds_anim.py. Run in a dir with starts.json, words.json, end.txt.
import math, random, sys, subprocess, cairo
from birds_anim import *
import birds_anim as B
STORM = ((0.05, 0.06, 0.14), (0.16, 0.14, 0.26))
def cloud(c, x, y, s=1.0, col=(0.22, 0.22, 0.3)):
    c.set_source_rgb(*col)
    for dx, dy, r in ((-160, 20, 90), (-60, -30, 120), (70, -10, 110), (170, 30, 80), (0, 40, 120)):
        c.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi); c.fill()
def bolt(c, x0, y0, x1, y1, seed, alpha=1.0, w=14):
    r = random.Random(seed); pts = [(x0, y0)]; n = 14
    for i in range(1, n):
        u = i / n; pts.append((x0 + (x1 - x0) * u + r.uniform(-60, 60), y0 + (y1 - y0) * u))
    pts.append((x1, y1))
    for lw, col, a in ((w * 3, (0.6, 0.6, 1), 0.25), (w, (1, 1, 1), 1)):
        c.set_source_rgba(*col, a * alpha); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
    return pts
def ground(c): hills(c, (0.03, 0.03, 0.06))
def s1(c, t):
    sky(c, *STORM); cloud(c, 540, 480, 1.4); ground(c)
    ph = t % 2.2
    bolt(c, 540, 560, 600, 1500, int(t // 2.2), 0.18, 8)
    if ph < 0.35:
        c.set_source_rgba(1, 1, 1, 0.25 * (1 - ph / 0.35)); c.paint()
        bolt(c, 540, 560, 600, 1500, int(t // 2.2), 1 - ph / 0.35)
    if t < 4.2: text(c, 'BANG', 540, 1000, 140, (1, 0.9, 0.4), alpha=prog(t, 3.0, 3.2)) if False else None
def s2(c, t):
    sky(c, *STORM); ground(c); base = 1180
    g1 = max(0.3, prog(t, 0.0, 1.0)); g2 = max(0.15, prog(t, 0.8, 3.0))
    c.set_source_rgb(1, 0.8, 0.2); c.rectangle(180, base - 110 * g1, 240, 110 * g1); c.fill()
    c.set_source_rgb(0.8, 0.8, 1); c.rectangle(640, base - 550 * g2, 240, 550 * g2); c.fill()
    text(c, "SUN'S SURFACE", 300, base + 60, 30, alpha=g1); text(c, 'LIGHTNING CHANNEL', 760, base + 60, 30, alpha=g2)
    text(c, '1x', 300, base - 130, 60, (1, 0.9, 0.5), alpha=g1)
    text(c, '5x', 760, base - 570, 90, (0.9, 0.9, 1), alpha=g2)
    text(c, 'UP TO 50,000 F', 760, base - 650, 40, (1, 0.7, 0.5), alpha=prog(t, 3.2, 4))
def s3(c, t):
    sky(c, *STORM); ground(c); cx = 540
    heat = max(0.35, prog(t, 0.0, 0.6))
    c.set_source_rgba(1, 0.4, 0.1, 0.5 * heat); c.set_line_width(40); c.move_to(cx, 500); c.line_to(cx, 1500); c.stroke()
    bolt(c, cx, 500, cx, 1500, 3, heat)
    for k in range(5):
        r = ((t - 0.1 - k * 0.45) % 2.2) * 320
        if t > 0.1 and r > 0:
            a = max(0, 1 - r / 700) * 0.6
            c.set_source_rgba(1, 0.75, 0.4, a); c.set_line_width(8); c.save(); c.translate(cx, 1000); c.scale(r / 500, 1); c.arc(0, 0, 500, 0, 2 * math.pi); c.restore(); c.stroke()
    text(c, 'HEAT', 540, 380, 70, (1, 0.6, 0.3), alpha=heat)
    text(c, 'EXPAND', 540, 300, 70, (1, 0.9, 0.5), alpha=prog(t, 3, 3.6)); text(c, 'SHOCK WAVE', 540, 220, 70, (1, 1, 1), alpha=prog(t, 7, 7.6))
def s4(c, t):
    sky(c, *STORM); ground(c); cx, cy = 540, 900
    ph = (t % 2.0) / 2.0; r = 120 + 260 * (math.sin(ph * math.pi) ** 2 if ph < 0.5 else (1 - (ph - 0.5) * 2) ** 0 * math.cos((ph - 0.5) * math.pi) ** 2)
    c.set_source_rgba(1, 0.7, 0.3, 0.35); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill()
    for i in range(1, 4):
        c.set_source_rgba(0.8, 0.9, 1, max(0, 0.6 - i * 0.15)); c.set_line_width(6); c.arc(cx, cy, r + i * 90 + 30 * math.sin(t * 6), 0, 2 * math.pi); c.stroke()
    text(c, 'EXPAND', 540, 380, 70, (1, 0.9, 0.5), alpha=1 if ph < 0.5 else 0.3); text(c, 'CONTRACT', 540, 300, 70, (0.7, 0.85, 1), alpha=1 if ph >= 0.5 else 0.3)
    text(c, 'SOUND WAVE = THUNDER', 540, 1190, 40, (1, 1, 1), alpha=prog(t, 2.5, 3.2))
def s5(c, t):
    sky(c, *STORM); cloud(c, 300, 330, 0.9); ground(c)
    bx = 250; pts = [(bx + 30 * math.sin(i), 420 + i * 100) for i in range(11)]
    c.set_source_rgb(1, 1, 1); c.set_line_width(12); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
    lx, ly = 880, 1130
    c.set_source_rgb(0.9, 0.9, 0.95); c.arc(lx, ly - 40, 24, 0, 2 * math.pi); c.fill(); c.rectangle(lx - 18, ly - 15, 36, 70); c.fill()
    sp = 260
    for i, (px, py) in enumerate(pts):
        d = math.hypot(lx - px, ly - py); age = t - 0.4 - d / sp
        r = (t - 0.4) * sp
        if r > 0 and r < d + 60:
            c.set_source_rgba(1, 0.8, 0.4, 0.5 * max(0, 1 - r / (d + 60))); c.set_line_width(5); c.arc(px, py, r, 0, 2 * math.pi); c.stroke()
    text(c, 'NEAR: SHARP CRACK', 540, 300, 44, (1, 0.9, 0.5), alpha=prog(t, 0.5, 1.2)); text(c, 'FAR: LOW RUMBLE', 540, 220, 44, (0.7, 0.85, 1), alpha=prog(t, 4, 5))
def s6(c, t):
    sky(c, (0.04, 0.05, 0.12), (0.1, 0.12, 0.22)); ground(c); cx, cy = 540, 880
    g = max(0.15, prog(t, 0.0, 3.0)); r = 440 * g
    c.set_source_rgba(0.6, 0.8, 1, 0.12); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill(); c.set_source_rgba(0.6, 0.8, 1, 0.8); c.set_line_width(8); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    bolt(c, cx, cy - 120, cx, cy + 40, 9, 1, 8)
    text(c, 'ABOUT 10 MILES', 540, 360, 64, (1, 1, 1), alpha=g); text(c, 'AUDIBLE RANGE, TYPICALLY', 540, 440, 36, (0.8, 0.9, 1), alpha=g)
def s7(c, t):
    sky(c, *STORM); ground(c); cloud(c, 540, 1000, 1.3)
    ph = t % 1.8
    if ph < 0.25: c.set_source_rgba(1, 1, 1, 0.18); c.paint()
    c.set_source_rgb(0.97, 0.97, 1); c.save(); c.translate(540, 560); c.scale(1.5, 1); c.arc(0, 0, 330, 0, 2 * math.pi); c.restore(); c.fill()
    c.move_to(520, 660); c.line_to(560, 790); c.line_to(600, 660); c.close_path(); c.fill()
    text(c, 'SHOWING OFF?', 540, 540, 54, (0.1, 0.1, 0.25), outline=False); text(c, 'OR: GO INSIDE!', 540, 640, 52, (0.8, 0.1, 0.1), outline=False)
SC = [s2, s1, s3, s4, s5, s6, s7]  # index = narration sentence
def lframe(c, t):
    i = max(k for k in range(len(SC)) if t >= ST[k] - 1e-6); SC[i](c, t - ST[i])
    if t < 0.05: pass
B.frame = lframe
if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'anim.mp4'; only = [float(x) for x in sys.argv[2:]]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if only:
        for t in only: lframe(c, t); surf.write_to_png(f'af_{t}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(T_END * FPS) + 3): lframe(c, i / FPS); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()
