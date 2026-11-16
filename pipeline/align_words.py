#!/usr/bin/env python3
"""Align script words to base.en recognition (WHISPER_MODEL overrides) using normalized characters.
Handles ASR digits vs spoken numbers and hyphenated words; stores transcript and timing QA.
Usage: align_words.py narr.wav words.json. Requires faster-whisper and num2words.
"""
import json,re,sys,statistics,difflib,os,numpy as np,soundfile as sf
from faster_whisper import WhisperModel
from num2words import num2words
wav,wj=sys.argv[1:3]
m=WhisperModel(os.environ.get('WHISPER_MODEL','base.en'),compute_type='int8',cpu_threads=2)
audio,sr=sf.read(wav); starts=json.load(open(os.path.join(os.path.dirname(wav),'starts.json'))) if os.path.exists(os.path.join(os.path.dirname(wav),'starts.json')) else [0]
W=[]
for start,end in zip(starts,starts[1:]+[len(audio)/sr]):
 clip=audio[int(start*sr):int(end*sr)];clip=np.concatenate([clip,np.zeros(int(sr*.5))]).astype(np.float32)
 # faster-whisper numpy input is always 16kHz; use a file so the reader resamples correctly.
 import tempfile
 with tempfile.NamedTemporaryFile(suffix='.wav') as f:
  sf.write(f.name,clip,sr);seg,_=m.transcribe(f.name,word_timestamps=True,condition_on_previous_text=False)
  W.extend((max(start,w.start+start),min(end,w.end+start),w.word.strip()) for ss in seg for w in ss.words)
merged=[]
for s,e,w in W:
 if w.startswith(',') and re.match(r'^,\d',w) and merged and re.search(r'\d$',merged[-1][2]):
  ps,pe,pw=merged.pop();merged.append((ps,e,pw+w))
 else:merged.append((s,e,w))
W=merged
json.dump(W,open(wj+'.transcript.json','w'),indent=2)
def norm(x):
 def number(m):
  try:return num2words(int(m[1]),to='ordinal' if m[2] else 'cardinal')
  except:return m[0]
 x=re.sub(r'(?<=\d),(?=\d)','',x.lower()); x=re.sub(r'(\d+)(st|nd|rd|th)?',number,x)
 return re.sub('[^a-z]','',x)
# Keep reference word boundaries while comparing flattened letter streams.
ref=json.load(open(wj));a='';bounds=[]
for _,_,word in ref:
 n=norm(word);bounds.append((len(a),len(a)+len(n)));a+=n
b='';times=[]
for s,e,word in W:
 n=norm(word);b+=n
 for k in range(len(n)):times.append((s+(e-s)*k/len(n),s+(e-s)*(k+1)/len(n)))
match={}
for block in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
 for k in range(block.size):match[block.a+k]=block.b+k
out=[];err=[];matched=0
for (s,e),(o,d,w) in zip(bounds,ref):
 ix=[match[k] for k in range(s,e) if k in match]
 if len(ix)>=max(1,(e-s)*.75):
  st,en=times[min(ix)][0],times[max(ix)][1];err.append(o-st);o,d=st,max(en-st,.05);matched+=1
 out.append([round(o,3),round(d,3),w])
# Unmatched estimates can cross a recognized neighbor. Fail rather than create backwards captions.
if any(x[0]>y[0] for x,y in zip(out,out[1:])):raise RuntimeError('nonmonotonic aligned captions; inspect transcript before encoding')
json.dump(ref,open(wj+'.est','w'));json.dump(out,open(wj,'w'))
qa={'matched':matched,'words':len(ref),'mean_estimate_error':statistics.mean(err),'p90_abs_estimate_error':sorted(abs(x) for x in err)[int(len(err)*.9)],'max_abs_estimate_error':max(abs(x) for x in err)}
json.dump(qa,open(wj+'.qa.json','w'),indent=2);print('QA',qa)
