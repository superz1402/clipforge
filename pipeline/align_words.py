#!/usr/bin/env python3
"""align_words.py narr.wav words.json  -> rewrites words.json with faster-whisper (tiny.en, MIT) word starts where words match; else keeps estimate. Prints error stats (QA)."""
import json, re, sys, statistics
from faster_whisper import WhisperModel
wav, wj = sys.argv[1], sys.argv[2]
m = WhisperModel('tiny.en', compute_type='int8', cpu_threads=2)
seg, _ = m.transcribe(wav, word_timestamps=True)
W = [(w.start, w.end, w.word.strip()) for s in seg for w in s.words]
ref = json.load(open(wj)); n = lambda x: re.sub(r'\W', '', x.lower()); i = 0; errs = []; hit = {}
for s, e, w in W:
    for j in range(i, min(i + 10, len(ref))):
        if n(ref[j][2]) == n(w): errs.append(ref[j][0] - s); hit[j] = (s, e); i = j + 1; break
out = []
for j, (o, d, w) in enumerate(ref):
    if j in hit: o, d = hit[j][0], hit[j][1] - hit[j][0]
    out.append([round(o, 3), round(max(d, 0.05), 3), w])
json.dump(ref, open(wj + '.est', 'w')); json.dump(out, open(wj, 'w'))
print('QA matched %d/%d words, estimate error mean %.2fs p90 %.2fs max %.2fs (replaced by whisper times)' % (len(errs), len(ref), statistics.mean(errs), sorted(abs(x) for x in errs)[int(len(errs) * .9)], max(abs(x) for x in errs)))
