# Topic scenes: Moon tidal locking (NASA). Primitives from birds_anim.py. Run in dir with starts.json, words.json, end.txt.
import math, sys, subprocess, cairo, random
from birds_anim import *
import birds_anim as B
SPACE = ((0.02, 0.02, 0.07), (0.06, 0.05, 0.16))
STARS = [(random.Random(i).uniform(0, 1080), random.Random(i + 99).uniform(0, 1920), i) for i in range(70)]
def space(c, t=0):
    sky(c, *SPACE)
    for x, y, p in STARS: c.set_source_rgba(1, 1, 1, 0.3 + 0.3 * math.sin(t * 2 + p)); c.arc(x, y, 2.2, 0, 6.3); c.fill()
def earth(c, x, y, r=90):
    c.set_source_rgb(0.2, 0.45, 0.9); c.arc(x, y, r, 0, 6.3); c.fill(); c.set_source_rgb(0.25, 0.7, 0.35)
    for dx, dy, rr in ((-25, -20, 30), (30, 15, 24), (-10, 40, 18)): c.arc(x + dx, y + dy, rr, 0, 6.3); c.fill()
def moon(c, x, y, r, rot, lit=None):
    """rot: angle of the near-side marker direction (radians). lit: angle toward sun or None."""
    c.set_source_rgb(0.75, 0.75, 0.78); c.arc(x, y, r, 0, 6.3); c.fill()
    for a, d, rr in ((0.3, 0.45, 0.18), (2.1, 0.5, 0.14), (3.8, 0.35, 0.2), (5.0, 0.55, 0.12)):
        c.set_source_rgb(0.55, 0.55, 0.6); c.arc(x + r * d * math.cos(a + rot), y + r * d * math.sin(a + rot), r * rr, 0, 6.3); c.fill()
    c.set_source_rgb(0.9, 0.2, 0.2); c.save(); c.translate(x, y); c.rotate(rot); c.move_to(r * 0.95, 0); c.line_to(r * 0.6, -r * 0.25); c.line_to(r * 0.6, r * 0.25); c.close_path(); c.fill(); c.restore()
    if lit is not None:
        c.save(); c.arc(x, y, r, 0, 6.3); c.clip()
        c.set_source_rgba(0.02, 0.02, 0.08, 0.8); c.save(); c.translate(x, y); c.rotate(lit + math.pi); c.rectangle(0, -r - 5, r + 5, 2 * r + 10); c.fill(); c.restore(); c.restore()
def orbit(c, cx, cy, R, w, t, spin=1.0, r=55, ring=True):
    a = t * w
    if ring: c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(4); c.arc(cx, cy, R, 0, 6.3); c.stroke()
    mx, my = cx + R * math.cos(a), cy + R * math.sin(a)
    # marker points to Earth when spin=1 (rot = a + pi); spin=0 keeps fixed direction
    rot = (a + math.pi) if spin == 1 else math.pi
    return mx, my, rot
def s1(c, t):
    space(c, t); cx, cy = 540, 780; earth(c, cx, cy, 110); mx, my, rot = orbit(c, cx, cy, 390, 0.9, t); moon(c, mx, my, 90, rot)
def s2(c, t):
    space(c, t); cx, cy = 540, 780; earth(c, cx, cy, 110); mx, my, rot = orbit(c, cx, cy, 390, 0.9, t); moon(c, mx, my, 90, rot)
    text(c, '1 SPIN = 1 ORBIT', 540, 330, 66, (1, 0.9, 0.5), alpha=prog(t, 1.5, 2.2)); text(c, 'ABOUT 27 DAYS', 540, 1190, 44, (0.8, 0.9, 1), alpha=prog(t, 4, 5))
def s3(c, t):
    space(c, t); cx, cy = 540, 780; earth(c, cx, cy, 110); mx, my, rot = orbit(c, cx, cy, 390, 0.9, t); moon(c, mx, my, 90, rot)
    c.set_source_rgba(0.9, 0.2, 0.2, 0.6); c.set_line_width(5); c.set_dash([14, 12]); c.move_to(mx, my); c.line_to(cx, cy); c.stroke(); c.set_dash([])
    text(c, 'ALWAYS FACING EARTH', 540, 330, 56, (1, 0.6, 0.6), alpha=prog(t, 1, 1.8))
def s4(c, t):
    space(c, t)
    for k, (cx, spin, lab) in enumerate(((290, 0, 'NO SPIN: ALL SIDES'), (790, 1, 'SYNCED: ONE SIDE'))):
        cy = 760; c.save(); earth(c, cx, cy, 50); mx, my, rot = orbit(c, cx, cy, 190, 0.9, t, spin); moon(c, mx, my, 38, rot); c.restore()
        text(c, lab, cx, 1030, 30, (1, 1, 1))
    text(c, 'ANY OTHER RATE', 540, 330, 56, (1, 0.9, 0.5), alpha=prog(t, 2, 2.8)); text(c, 'DIFFERENT PARTS SHOW', 540, 410, 44, (0.8, 0.9, 1), alpha=prog(t, 2, 2.8))
def s5(c, t):
    space(c, t); text(c, 'TIDAL LOCKING', 540, 330, 70, (1, 0.9, 0.5), alpha=prog(t, 0.3, 1))
    for i, (cx, cy, R, w, pr) in enumerate(((290, 760, 170, 1.1, 60), (790, 760, 170, 0.7, 45), (540, 1100, 170, 0.9, 52))):
        col = [(0.9, 0.6, 0.3), (0.5, 0.7, 0.9), (0.8, 0.5, 0.7)][i]
        c.set_source_rgb(*col); c.arc(cx, cy, pr, 0, 6.3); c.fill(); mx, my, rot = orbit(c, cx, cy, R + 60, w, t + i); moon(c, mx, my, 30, rot)
    text(c, 'ALL LARGE MOONS IN OUR SOLAR SYSTEM', 540, 1230, 30, (1, 1, 1), alpha=prog(t, 3, 4))
def s6(c, t):
    space(c, t); cx, cy = 600, 800; R = 300; w = 0.55
    for yy in range(-6, 7): c.set_source_rgba(1, 0.95, 0.6, 0.12); c.set_line_width(6); c.move_to(0, cy + yy * 110); c.line_to(1080, cy + yy * 110); c.stroke()
    text(c, 'SUNLIGHT', 150, 560, 40, (1, 0.95, 0.6)); earth(c, cx, cy, 80)
    a = t * w + 0.8; mx, my = cx + R * math.cos(a), cy + R * math.sin(a); rot = a + math.pi
    moon(c, mx, my, 60, rot, lit=math.pi)  # sun comes from the left (angle pi) -> left half lit
    newm = math.cos(a) < -0.7  # moon on sun side of Earth
    text(c, 'NEW MOON: FAR SIDE IS SUNNY' if newm else 'THE FAR SIDE GETS SUNLIGHT TOO', 540, 330, 40, (1, 0.9, 0.5) if newm else (1, 1, 1))
def s7(c, t):
    space(c, t); mx, my = 540, 1000; moon(c, mx, my, 170, 0.0 if False else -0.0 + math.pi * 1.5 + 0.0, None)
    c.set_source_rgb(0.97, 0.97, 1); c.save(); c.translate(540, 520); c.scale(1.5, 1); c.arc(0, 0, 330, 0, 6.3); c.restore(); c.fill()
    c.move_to(520, 620); c.line_to(560, 790); c.line_to(600, 620); c.close_path(); c.fill()
    text(c, 'KEEPING AN EYE ON US?', 540, 500, 50, (0.1, 0.1, 0.25), outline=False); text(c, 'OR: TOO SHY TO TURN?', 540, 600, 48, (0.8, 0.1, 0.1), outline=False)
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
