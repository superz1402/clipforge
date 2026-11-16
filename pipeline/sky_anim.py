# Topic scenes: why the sky is blue (NASA SpacePlace / NOAA). Primitives from birds_anim.py.
import math, sys, subprocess, cairo, random
from birds_anim import *
import birds_anim as B
BLUE = (0.35, 0.6, 1.0); RED = (1.0, 0.35, 0.3)
def sun(c, x, y, r=90, col=(1, 0.95, 0.7)):
    for k, a in ((2.2, 0.12), (1.6, 0.2)): c.set_source_rgba(1, 0.9, 0.5, a); c.arc(x, y, r * k, 0, 6.3); c.fill()
    c.set_source_rgb(*col); c.arc(x, y, r, 0, 6.3); c.fill()
def day(c): sky(c, (0.15, 0.35, 0.85), (0.55, 0.78, 1.0))
def s1(c, t):
    day(c); sun(c, 200, 420); text(c, 'WHITE SUNLIGHT', 540, 760, 54, (1, 1, 1), alpha=prog(t, 0.3, 1))
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(26); c.move_to(300, 450); c.line_to(1080, 800); c.stroke()
def s2(c, t):
    sky(c, (0.04, 0.05, 0.15), (0.1, 0.1, 0.25))
    for k, (col, wl, y) in enumerate(((BLUE, 70, 700), (RED, 170, 1000))):
        c.set_source_rgb(*col); c.set_line_width(14); c.move_to(0, y)
        for x in range(0, 1081, 6): c.line_to(x, y + 90 * math.sin((x - t * 250) / wl * 2 * math.pi))
        c.stroke()
    text(c, 'BLUE: SHORTER WAVES', 540, 540, 46, BLUE); text(c, 'RED: LONGER WAVES', 540, 840, 46, RED)
def s3(c, t):
    day(c); r = random.Random(4); sun(c, 150, 330, 70)
    c.set_source_rgba(1, 1, 1, 0.55); c.set_line_width(22); c.move_to(220, 360); c.line_to(1080, 860); c.stroke()
    for i in range(14):
        x, y = 300 + i * 55, 390 + i * 32 + r.uniform(-8, 8)
        c.set_source_rgb(1, 1, 1); c.arc(x, y, 12, 0, 6.3); c.fill()
        a = prog(t, 0.5 + i * 0.15, 1.2 + i * 0.15)
        for k in range(8):
            ang = k * math.pi / 4 + i; L = 70 * a
            c.set_source_rgba(0.1, 0.3, 1, 0.9 * a); c.set_line_width(5); c.move_to(x, y); c.line_to(x + L * math.cos(ang), y + L * math.sin(ang)); c.stroke()
    text(c, 'BLUE SCATTERS MORE', 540, 1180, 46, (1, 1, 1), alpha=prog(t, 3, 4))
def s4(c, t):
    sky(c, (0.04, 0.05, 0.15), (0.1, 0.1, 0.25)); base = 1050; g = prog(t, 0.4, 2.5)
    c.set_source_rgb(*RED); c.rectangle(260, base - 100 * g, 220, 100 * g); c.fill(); c.set_source_rgb(*BLUE); c.rectangle(600, base - 400 * g, 220, 400 * g); c.fill()
    text(c, 'RED', 370, base + 60, 44); text(c, 'BLUE', 710, base + 60, 44); text(c, 'ABOUT 4x STRONGER', 710, base - 450, 44, (0.7, 0.85, 1), alpha=g)
    text(c, 'SCATTERING STRENGTH', 540, 400, 50, (1, 1, 1))
def s5(c, t):
    sky(c, (0.15, 0.35, 0.85), (0.92, 0.95, 1.0)); hills(c, (0.1, 0.25, 0.15))
    text(c, 'OVERHEAD: DEEP BLUE', 540, 380, 48, (1, 1, 1)); text(c, 'HORIZON: PALE', 540, 1200, 48, (0.15, 0.2, 0.4), outline=False, alpha=prog(t, 1, 2))
    y = 1100; c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(10); c.move_to(100, y); c.line_to(100 + 900 * prog(t, 0.5, 4), y); c.stroke()
    text(c, 'MORE AIR, MORE SCATTERING', 540, 1000, 40, (0.1, 0.15, 0.35), outline=False, alpha=prog(t, 3, 4))
def s6(c, t):
    sky(c, (0.25, 0.2, 0.5), (1.0, 0.55, 0.25)); hills(c, (0.1, 0.05, 0.08)); sun(c, 540, 1380 - 25 * min(t, 6), 110, (1, 0.7, 0.3))
    c.set_source_rgba(1, 0.8, 0.5, 0.6); c.set_line_width(10); c.move_to(100, 1450); c.line_to(100 + 880 * prog(t, 0.5, 4), 1450); c.stroke()
    text(c, 'LONGER PATH THROUGH AIR', 540, 500, 48, (1, 1, 1), alpha=prog(t, 1, 2))
def s7(c, t):
    day(c); sun(c, 880, 330, 80)
    c.set_source_rgb(0.97, 0.97, 1); c.save(); c.translate(540, 900); c.scale(1.5, 1); c.arc(0, 0, 330, 0, 6.3); c.restore(); c.fill()
    c.move_to(520, 1000); c.line_to(560, 1170); c.line_to(600, 1000); c.close_path(); c.fill()
    text(c, 'SHOWING OFF?', 540, 880, 54, (0.1, 0.1, 0.25), outline=False); text(c, 'OR: BAD AT KEEPING LIGHT IN?', 540, 980, 40, (0.8, 0.1, 0.1), outline=False)
SC = [s1, s2, s3, s4, s5, s6, s7]
def lframe(c, t):
    i = max(k for k in range(len(SC)) if t >= ST[k] - 1e-6); SC[i](c, t - ST[i])
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
