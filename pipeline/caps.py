#!/usr/bin/env python3
"""caps.py words.json end_sec hook_text out.ass  (hook with \\N for line break). 3-word chunks, width<=820px @80pt."""
import json, re, sys
from PIL import ImageFont
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
ws = json.load(open(sys.argv[1])); END = float(sys.argv[2]); hook = sys.argv[3]
t = lambda s: f"{int(s//3600)}:{int(s%3600//60):02d}:{s%60:05.2f}"
wd = lambda c: f.getlength(" ".join(w for _, _, w in c).upper())
ch = []; cur = []
for o, d, w in ws:
    if cur and (len(cur) >= 3 or wd(cur + [(o, d, w)]) > 820): ch.append(cur); cur = []
    cur.append((o, d, w))
    if re.search(r'[.,?!:]$|\.\.\.$', w): ch.append(cur); cur = []
if cur: ch.append(cur)
hdr = open(__file__.rsplit('/', 1)[0] + '/caps_header.ass').read()
ev = ["[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i, c in enumerate(ch):
    s = c[0][0]; e = ch[i+1][0][0] if i+1 < len(ch) else END; e = min(e, s + 2.6)
    txt = ' '.join(w for _, _, w in c).upper(); fs = ''
    if wd(c) > 820: fs = '\\fs%d' % int(80*820/wd(c))
    ev.append(f"Dialogue: 0,{t(s)},{t(e)},Cap,,0,0,0,,{{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100){fs}}}{txt}")
ev.append(f"Dialogue: 1,{t(0.1)},{t(4.4)},Hook,,0,0,0,,{hook}")
open(sys.argv[4], 'w').write(hdr + "\n".join(ev) + "\n")
