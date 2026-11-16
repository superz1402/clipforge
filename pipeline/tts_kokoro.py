#!/usr/bin/env python3
"""Kokoro-82M (Apache-2.0 weights) via kokoro-onnx (MIT). Usage: tts_kokoro.py script.json voice outdir
script.json: {"sentences":[{"text":..,"speed":1.0,"gap":0.35}, ...]}
Writes narr.wav, words.json [[start,dur,word]...], starts.json (sentence starts), end.txt.
Word timings are proportional to characters within each sentence (kokoro-onnx has no word boundaries)."""
import json, sys, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = '/downloads/kokoro/'
sc = json.load(open(sys.argv[1])); voice = sys.argv[2]; out = sys.argv[3]
k = Kokoro(D + 'kokoro-v1.0.onnx', D + 'voices-v1.0.bin')
SR = 24000; t = 0.0; chunks = []; words = []; starts = []
for s in sc['sentences']:
    a, sr = k.create(s['text'], voice=voice, speed=s.get('speed', 1.0), lang='en-us')
    # trim leading/trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]
    a = a[max(nz[0] - 600, 0): nz[-1] + 1200] if len(nz) else a
    dur = len(a) / sr; starts.append(round(t, 3))
    ws = s['text'].split(); wt = [len(re.sub(r'\W', '', w)) + 2 for w in ws]; tot = sum(wt); c = t
    for w, l in zip(ws, wt):
        d = dur * l / tot; words.append([round(c, 3), round(d, 3), w]); c += d
    chunks.append(a); gap = s.get('gap', 0.35); chunks.append(np.zeros(int(sr * gap), dtype=np.float32)); t += dur + gap
audio = np.concatenate(chunks[:-1]); sf.write(out + '/narr.wav', audio, SR)
json.dump(words, open(out + '/words.json', 'w')); json.dump(starts, open(out + '/starts.json', 'w'))
open(out + '/end.txt', 'w').write('%.2f' % (len(audio) / SR)); print(voice, 'end', len(audio) / SR, 'words', len(words))
