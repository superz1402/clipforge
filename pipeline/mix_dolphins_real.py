import subprocess,json
P='/downloads/dolphins';F='/downloads/footage-dolphins'
starts=json.load(open(P+'/starts.json'));end=float(open(P+'/end.txt').read());edges=starts+[end]
# All scenes: Pexels-licensed real footage (https://www.pexels.com/license/).
# Single source D3 (claudio baroni, Pexels 35610558), aerial pod over sand flats.
# Verified-free zones: t=4-18.5 and t=19-32.3 (t>=33 has boat, t~37 snorkeler selfie; both avoided).
# Vertical source: scale to fill 1080x1920, crop center 1080x810 band as fg window.
shots=[4.5,10.5,18.5,26.5,6.0,20.0,12.0]
credit='claudio baroni | Pexels'
outs=[]
for i,ss in enumerate(shots):
 d=edges[i+1]-edges[i];out=f'{P}/realshot{i}.mp4';outs.append(out)
 vf=(f"[0:v]setpts=(PTS-STARTPTS),split=2[b][f];"
     f"[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:2,eq=brightness=-0.3[bg];"
     f"[f]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:810:0:555[fg];"
     f"[bg][fg]overlay=0:410,drawtext=text='{credit}':fontcolor=white:fontsize=27:x=(w-tw)/2:y=1780,setsar=1,fps=30[v]")
 subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(ss),'-i',f'{F}/D3-claudio-35610558.mp4','-filter_complex',vf,'-map','[v]','-an','-t',str(d),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',out],check=True)
open(P+'/concat.txt','w').write(''.join(f"file '{x}'\n"for x in outs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',P+'/concat.txt','-i',P+'/mix.mp3','-vf','ass='+P+'/cap.ass','-map','0:v','-map','1:a','-t',str(end),'-c:v','libx264','-preset','medium','-crf','25','-maxrate','2.5M','-bufsize','5M','-c:a','aac','-b:a','160k','-movflags','+faststart','/downloads/dolphins-real-am_onyx.mp4'],check=True)
print('total',end)
