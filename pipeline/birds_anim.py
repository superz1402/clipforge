import cairo, math, random, json, subprocess, sys
W, H, FPS = 1080, 1920, 30
END = float(open('end.txt').read()) + 0.05 if __import__('os').path.exists('end.txt') else 48.81
ST = json.load(open('starts.json')) + [END]
WORDS = json.load(open('words.json'))
T_END = END
try: t_closer = [o for o, d, w in WORDS if w.lower().startswith('closer')][0] - 0.5
except IndexError: t_closer = 0
RNG = random.Random(7)

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, a, b): return ease((t - a) / (b - a))

def sky(c, top, bot):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    c.set_source(g); c.paint()

def hills(c, col=(0.07, 0.05, 0.1)):
    c.set_source_rgb(*col)
    c.move_to(0, 1560)
    c.curve_to(250, 1480, 500, 1600, 760, 1500)
    c.curve_to(900, 1450, 1000, 1500, 1080, 1480)
    c.line_to(1080, 1920); c.line_to(0, 1920); c.close_path(); c.fill()

def wire(c, y, x0=-20, x1=1100, sag=18):
    c.set_source_rgb(0.08, 0.06, 0.1); c.set_line_width(7)
    c.move_to(x0, y); c.curve_to(x0 + (x1 - x0) * 0.3, y + sag, x0 + (x1 - x0) * 0.7, y + sag, x1, y); c.stroke()

def wire_y(y, x, sag=18):
    u = clamp((x + 20) / 1120)
    return y + 3 * sag * u * (1 - u) * 0.9

def bird(c, x, y, s=1.0, flap=None, face=1, col=(0.06, 0.05, 0.09), eye=1.0, alert=0.0, tilt=0.0):
    c.save(); c.translate(x, y); c.scale(face * s, s); c.rotate(tilt * face)
    body = col
    if alert > 0:
        body = tuple(col[i] * (1 - alert) + (0.35, 0.12, 0.06)[i] * alert for i in range(3))
    c.set_source_rgb(*body)
    c.move_to(-20, 4); c.line_to(-62, 18); c.line_to(-58, 2); c.line_to(-20, -6); c.close_path(); c.fill()
    c.save(); c.scale(1.0, 0.72); c.arc(0, 0, 30, 0, 2 * math.pi); c.restore(); c.fill()
    c.arc(26, -14, 15, 0, 2 * math.pi); c.fill()
    c.move_to(38, -17); c.line_to(54, -11); c.line_to(38, -8); c.close_path()
    c.set_source_rgb(0.95, 0.65, 0.15); c.fill()
    c.set_source_rgb(1, 1, 1); c.arc(30, -17, 5.2 * eye, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0, 0, 0); c.arc(31, -17, 2.4 * eye, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*[v * 0.8 for v in body])
    if flap is None:
        c.save(); c.translate(-2, -2); c.move_to(0, 0); c.curve_to(-20, -6, -44, 6, -52, 18); c.curve_to(-30, 20, -8, 14, 6, 6); c.close_path(); c.fill(); c.restore()
    else:
        ang = math.sin(flap)
        c.save(); c.translate(-2, -10); c.rotate(-ang - 0.2)
        c.move_to(0, 0); c.curve_to(-10, -50, -40, -90, -70, -100); c.curve_to(-60, -60, -40, -20, 10, 6); c.close_path(); c.fill()
        c.restore()
        c.save(); c.translate(-2, -10); c.rotate(-ang * 0.7 - 0.45); c.scale(0.8, 0.8)
        c.set_source_rgb(*[v * 0.65 for v in body])
        c.move_to(0, 0); c.curve_to(-10, -50, -40, -90, -70, -100); c.curve_to(-60, -60, -40, -20, 10, 6); c.close_path(); c.fill(); c.restore()
    c.restore()

def text(c, s, x, y, size=44, col=(1, 1, 1), bold=True, alpha=1.0, outline=True):
    c.select_font_face('DejaVu Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    e = c.text_extents(s)
    c.move_to(x - e.width / 2 - e.x_bearing, y)
    if outline:
        c.text_path(s); c.set_source_rgba(0, 0, 0, 0.85 * alpha); c.set_line_width(size * 0.14); c.stroke_preserve()
        c.set_source_rgba(col[0], col[1], col[2], alpha); c.fill()
    else:
        c.set_source_rgba(col[0], col[1], col[2], alpha); c.show_text(s)

RNG_B = {i: [random.Random(i * 11 + j).random() for j in range(8)] for i in range(12)}

def burst(c, cx, cy, t, r_max=260, col=(1, 0.85, 0.4), seed=1, n=24, flash_on=True):
    if t < 0: return
    r = RNG_B[seed]
    k = clamp(t / 1.4)
    flash = clamp(1 - t / 0.18)
    if flash > 0 and flash_on:
        c.set_source_rgba(1, 1, 0.9, 0.55 * flash); c.paint()
    for i in range(n):
        a = 2 * math.pi * i / n + r[i % len(r)] * 0.2
        d = r_max * (1 - (1 - k) ** 2.2) * (0.75 + 0.25 * r[i % len(r)])
        x = cx + d * math.cos(a); y = cy + d * math.sin(a) + 90 * k * k
        al = clamp(1.3 - k * 1.3)
        c.set_source_rgba(col[0], col[1], col[2], al); c.arc(x, y, 9 * (1 - 0.5 * k), 0, 2 * math.pi); c.fill()
        c.set_source_rgba(col[0], col[1], col[2], al * 0.3); c.set_line_width(5)
        c.move_to(cx + d * 0.7 * math.cos(a), cy + d * 0.7 * math.sin(a)); c.line_to(x, y); c.stroke()
    for j in range(3):
        rt = t - j * 0.25
        if rt > 0:
            c.set_source_rgba(1, 1, 1, clamp(0.5 - rt * 0.5)); c.set_line_width(6)
            c.arc(cx, cy, rt * 520, 0, 2 * math.pi); c.stroke()

S1_BIRDS = []
for i in range(7):
    x = 150 + i * 130 + RNG.uniform(-15, 15)
    S1_BIRDS.append(dict(x=x, delay=0.55 + RNG.uniform(0, 0.35), vx=RNG.uniform(-260, 260), vy=-RNG.uniform(260, 520), sz=RNG.uniform(0.8, 1.05), ph=RNG.uniform(0, 6)))
S4_BIRDS = []
for row, yy in enumerate((790, 1030)):
    for i in range(6):
        x = 130 + i * 164 + (row * 40)
        S4_BIRDS.append(dict(x=x, y=yy, row=row, vx=RNG.uniform(-200, 260), vy=-RNG.uniform(300, 520), ph=RNG.uniform(0, 6)))
S6_BIRDS = []
for i in range(14):
    S6_BIRDS.append(dict(x=RNG.uniform(250, 830), y=RNG.uniform(520, 1000), w=RNG.uniform(0.6, 1.4), ph=RNG.uniform(0, 6), s=RNG.uniform(0.55, 0.9), seed=RNG.uniform(0, 10)))
STARS = [(RNG.uniform(0, W), RNG.uniform(0, 1300), RNG.uniform(0, 6.28)) for _ in range(70)]
DUSK = ((0.16, 0.11, 0.33), (0.93, 0.47, 0.35))

def scene1(c, t):
    sky(c, *DUSK); hills(c)
    wy = 900; wire(c, wy)
    bang = 0.35
    for b in S1_BIRDS:
        lt = t - bang - b['delay']
        by = wire_y(wy, b['x']) - 14
        if lt < 0:
            alert = clamp((t - bang) / 0.4) * 0.7 if t > bang else 0
            bird(c, b['x'], by + math.sin(t * 2 + b['ph']) * 1.5, b['sz'], None, 1 if b['x'] < 540 else -1, alert=alert, eye=1 + alert * 0.6)
        else:
            x = b['x'] + b['vx'] * lt; y = by + b['vy'] * lt - 120 * lt * lt
            if -150 < x < W + 150 and y > -200:
                bird(c, x, y, b['sz'], lt * 24 + b['ph'], 1 if b['vx'] > 0 else -1, tilt=-0.35 if b['vx'] > 0 else 0.35)
    burst(c, 800, 380, t - bang, 300)
    if t > 1.4:
        for i in range(6):
            fx = 200 + i * 140 + 25 * math.sin(t * 1.5 + i); fy = 760 + ((t - 1.4) * 70 + i * 60) % 260
            c.set_source_rgba(0.06, 0.05, 0.09, 0.7); c.save(); c.translate(fx, fy); c.rotate(math.sin(t + i)); c.scale(1, 0.25); c.arc(0, 0, 18, 0, 2 * math.pi); c.restore(); c.fill()
    q = prog(t, 3.3, 4.2)
    if q > 0: text(c, '?', 540, 640, 330, (1, 1, 1), alpha=q)

def scene2(c, t):
    sky(c, *DUSK); hills(c)
    for k, (bx, by) in enumerate(((220, 420), (860, 480), (480, 320))):
        lt = t - 0.2 - k * 1.7
        if lt >= 0: burst(c, bx, by, lt % 4.2, 200, (1, 0.7 - 0.2 * k, 0.4 + 0.2 * k), seed=k + 2, flash_on=False)
    wire(c, 1150, sag=10)
    a = prog(t, 2.3, 2.7)
    bird(c, 540, 1135, 2.6 * (1 + 0.05 * math.sin(t * 14) * a), None, 1, alert=a * 0.5, eye=1 + a * 0.9)
    q = prog(t, 2.2, 2.6)
    if q > 0:
        c.save(); c.translate(600, 760); c.scale(0.8 + 0.4 * q, 0.8 + 0.4 * q)
        c.set_source_rgba(0.9, 0.12, 0.1, q); c.move_to(-34, -150); c.line_to(34, -150); c.line_to(18, 10); c.line_to(-18, 10); c.close_path(); c.fill()
        c.arc(0, 52, 20, 0, 2 * math.pi); c.fill(); c.restore()

def scene3(c, t):
    sky(c, *DUSK); hills(c)
    f = prog(t, 0.2, 0.9)
    text(c, 'FIGHT', 300, 520, 64, (1, 1, 1), alpha=1 - 0.65 * f)
    text(c, 'FLIGHT', 780, 520, 84, (1, 0.95, 0.4), alpha=0.5 + 0.5 * f)
    c.set_source_rgba(1, 1, 1, 0.5 - 0.4 * f); c.set_line_width(8); c.rectangle(120, 440, 360, 110); c.stroke()
    c.set_source_rgba(1, 0.9, 0.3, 0.2 + 0.8 * f); c.set_line_width(10); c.rectangle(560, 430, 440, 130); c.stroke()
    lift = prog(t, 1.2, 3.8)
    y = 1250 - lift * 600 - 20 * math.sin(t * 6); x = 540 + lift * 200
    if t < 1.1:
        wire(c, 1300, sag=8); bird(c, 540, 1285, 2.0, None, 1, alert=0.5, eye=1.5)
    else:
        bird(c, x, y, 2.0 + lift * 0.3, t * (16 + lift * 10), 1, alert=0.4 * (1 - lift), tilt=-0.5 * lift)
        for i in range(6):
            c.set_source_rgba(1, 1, 1, 0.35 * lift); c.set_line_width(5)
            yy = y + 60 + i * 28; c.move_to(x - 160 - i * 20, yy); c.line_to(x - 300 - i * 20, yy + 30); c.stroke()

def scene4(c, t):
    sky(c, *DUSK); hills(c)
    wire(c, 790, sag=12); wire(c, 1030, sag=12)
    first = S4_BIRDS[2]
    for i, b in enumerate(S4_BIRDS):
        wy = wire_y(790 if b['row'] == 0 else 1030, b['x'], 12) - 12
        d = math.hypot(b['x'] - first['x'], b['y'] - first['y'])
        t_go = 0.5 + d / 520.0 * 1.6 + (0 if i == 2 else 0.25)
        alert = clamp((t - (t_go - 0.45)) / 0.4)
        if t < t_go:
            bird(c, b['x'], wy, 0.85, None, 1 if b['x'] < 540 else -1, alert=alert * 0.75, eye=1 + alert * 0.7)
        else:
            lt = t - t_go
            x = b['x'] + b['vx'] * lt; y = wy + b['vy'] * lt - 120 * lt * lt
            if -150 < x < W + 150 and y > -200:
                bird(c, x, y, 0.85, lt * 22 + b['ph'], 1 if b['vx'] > 0 else -1, tilt=-0.3 if b['vx'] > 0 else 0.3)
    rt = t - 0.5
    if rt > 0:
        c.set_source_rgba(1, 0.6, 0.2, clamp(0.55 - rt * 0.22)); c.set_line_width(8)
        c.arc(first['x'], wire_y(790, first['x'], 12) - 12, rt * 520, 0, 2 * math.pi); c.stroke()
    text(c, 'ONE TAKES OFF...', 540, 420, 56, (1, 0.95, 0.5), alpha=prog(t, 0.2, 0.7) * (1 - prog(t, 4.2, 4.8)))

def scene5(c, t):
    sky(c, (0.05, 0.05, 0.15), (0.12, 0.13, 0.3))
    hills(c, (0.04, 0.04, 0.08))
    text(c, 'BIRDS IN FLIGHT, SEEN BY WEATHER RADAR', 540, 250, 38, (0.8, 0.9, 1))
    split = t_closer - ST[4]
    if t < split:
        base = 1000
        grow = prog(t, 0.5, 1.4)
        c.set_source_rgb(0.5, 0.65, 0.9); c.rectangle(210, base - 50 * grow, 250, 50 * grow); c.fill()
        g2 = prog(t, 1.8, 3.8); h2 = 560 * g2
        c.set_source_rgb(1, 0.65, 0.2); c.rectangle(620, base - h2, 250, h2); c.fill()
        if g2 > 0.3:
            c.set_source_rgb(0.05, 0.05, 0.15); c.save(); c.translate(745, base - 300); c.rotate(-0.25); c.rectangle(-150, -10, 300, 20); c.fill(); c.restore()
        text(c, 'OTHER NIGHTS', 335, base + 60, 34)
        text(c, "NEW YEAR'S EVE", 745, base + 60, 34)
        text(c, '1x', 335, base - 80, 56, (0.8, 0.9, 1), alpha=grow)
        text(c, '~1000x', 745, base - h2 - 30, 80, (1, 0.9, 0.5), alpha=g2)
        text(c, 'average; bar not to scale', 540, base + 118, 28, (0.8, 0.85, 1), bold=False)
    else:
        lt = t - split
        cx, cy = 230, 760
        burst(c, cx, cy, lt % 2.6, 120, seed=5, flash_on=False)
        for i, (r, a) in enumerate(((220, 0.55), (420, 0.35), (640, 0.2))):
            ap = prog(lt, 0.3 + i * 0.5, 0.9 + i * 0.5)
            c.set_source_rgba(1, 0.65, 0.2, a * ap); c.set_line_width(10); c.arc(cx, cy, r, -1.2, 1.2); c.stroke()
        ap = prog(lt, 0.2, 1.2)
        text(c, 'FIREWORKS', 230, 960, 40, alpha=ap)
        g = cairo.LinearGradient(120, 0, 1000, 0)
        g.add_color_stop_rgb(0, 1, 0.55, 0.1); g.add_color_stop_rgb(1, 0.3, 0.4, 0.8)
        c.set_source(g); c.rectangle(120, 1010, 860 * ap, 40); c.fill()
        text(c, 'CLOSE: STRONGEST', 290, 1100, 34, (1, 0.8, 0.5), alpha=ap)
        text(c, 'FAR: WEAKER', 840, 1100, 34, (0.7, 0.8, 1), alpha=ap)
        text(c, 'STILL ~10x UP TO ~10 km AWAY', 540, 1170, 40, (1, 1, 1), alpha=prog(lt, 1.8, 2.5))

def scene6(c, t):
    sky(c, (0.02, 0.03, 0.1), (0.06, 0.08, 0.2))
    for x, y, p in STARS:
        c.set_source_rgba(1, 1, 1, 0.4 + 0.4 * math.sin(t * 2 + p)); c.arc(x, y, 2.5, 0, 2 * math.pi); c.fill()
    hills(c, (0.02, 0.02, 0.05))
    for b in S6_BIRDS:
        x = b['x'] + 160 * math.sin(t * b['w'] + b['seed']) + 80 * math.sin(t * 2.3 * b['w'] + b['seed'] * 2)
        y = b['y'] + 120 * math.cos(t * b['w'] * 0.9 + b['seed']) + 50 * math.sin(t * 3 + b['seed'])
        dx = -b['w'] * math.cos(t * b['w'] + b['seed'])
        bird(c, x, y, b['s'], t * 14 + b['ph'], 1 if dx > 0 else -1, col=(0.75, 0.78, 0.9), tilt=0.5 * math.sin(t * 3 + b['seed']))
    e = 1 - 0.75 * prog(t, 0.6, 5.6)
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(8); c.rectangle(310, 230, 460, 80); c.stroke(); c.rectangle(770, 252, 22, 36); c.fill()
    col = (0.3, 0.85, 0.4) if e > 0.5 else ((1, 0.8, 0.2) if e > 0.32 else (1, 0.3, 0.2))
    c.set_source_rgb(*col); c.rectangle(318, 238, 444 * e, 64); c.fill()
    text(c, 'ENERGY', 540, 205, 40)

def scene7(c, t):
    sky(c, *DUSK); hills(c)
    if t > 0.5: burst(c, 820, 1000, (t - 0.5) % 3.6, 220, seed=7, flash_on=False)
    wire(c, 1180, sag=10)
    bird(c, 540, 1165, 2.6, None, 1, tilt=0.18 * math.sin(t * 1.4) * prog(t, 0.3, 1.0), eye=1.2)
    q = prog(t, 1.2, 1.8)
    if q > 0:
        c.set_source_rgba(1, 1, 1, 0.95 * q)
        c.save(); c.translate(540, 560); c.scale(1, 0.6); c.arc(0, 0, 440, 0, 2 * math.pi); c.restore(); c.fill()
        for (x, y, r) in ((480, 840, 30), (440, 900, 20), (410, 945, 11)):
            c.arc(x, y, r, 0, 2 * math.pi); c.fill()
        text(c, 'BAN FIREWORKS?', 540, 510, 52, (0.1, 0.1, 0.25), alpha=q, outline=False)
        text(c, 'OR: HUMANS =', 540, 590, 44, (0.1, 0.1, 0.25), alpha=q, outline=False)
        text(c, 'NATURAL DISASTER', 540, 655, 52, (0.75, 0.12, 0.1), alpha=q, outline=False)

def frame(c, t):
    if t < ST[1]: scene1(c, t)
    elif t < ST[2]: scene2(c, t - ST[1])
    elif t < ST[3]: scene3(c, t - ST[2])
    elif t < ST[4]: scene4(c, t - ST[3])
    elif t < ST[5]: scene5(c, t - ST[4])
    elif t < ST[6]: scene6(c, t - ST[5])
    else: scene7(c, t - ST[6])

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'anim.mp4'
    only = [float(x) for x in sys.argv[2:]]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if only:
        for t in only:
            frame(c, t); surf.write_to_png(f'af_{t}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(T_END * FPS) + 3):
        frame(c, i / FPS); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()
