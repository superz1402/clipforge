import subprocess,json,os
P='/downloads/sharks';F='/downloads/footage-sharks'
starts=json.load(open(P+'/starts.json'));end=float(open(P+'/end.txt').read());edges=starts+[end]
# All scenes use Pexels-licensed real footage (https://www.pexels.com/license/).
# shot: (file, seek_seconds, speed, credit)
shots=[
 ('S1-florian-18052777.mp4',0,0.8,'Florian Delée | Pexels'),
 ('S2-yusuf-31683428.mp4',0,0.6,'Yusuf Mahammed | Pexels'),
 ('F1-julien-31693357.mp4',0,1.0,'Julien Goettelmann | Pexels'),
 ('S1-florian-18052777.mp4',5.76,0.8,'Florian Delée | Pexels'),
 ('S6-lachlan-6510690.mp4',0,0.95,'Lachlan Ross | Pexels'),
 ('S5-closeup-36329346.mp4',0,0.95,'Magda Ehlers | Pexels'),
 ('S5-closeup-36329346.mp4',5.7,0.88,'Magda Ehlers | Pexels'),
]
outs=[]
for i,shot in enumerate(shots):
 d=edges[i+1]-edges[i];out=f'{P}/realshot{i}.mp4';outs.append(out)
 src,ss,speed,credit=shot
 vf=f"[0:v]setpts=(PTS-STARTPTS)/{speed},split=2[b][f];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:2,eq=brightness=-0.3[bg];[f]scale=1080:810:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:410,drawtext=text='{credit}':fontcolor=white:fontsize=27:x=(w-tw)/2:y=1780,setsar=1,fps=30[v]"
 cmd=['ffmpeg','-loglevel','error','-y','-ss',str(ss),'-i',f'{F}/{src}','-filter_complex',vf,'-map','[v]','-an','-t',str(d),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',out]
 subprocess.run(cmd,check=True)
open(P+'/concat.txt','w').write(''.join(f"file '{x}'\n"for x in outs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',P+'/concat.txt','-i',P+'/mix.mp3','-vf','ass='+P+'/cap.ass','-map','0:v','-map','1:a','-t',str(end),'-c:v','libx264','-preset','medium','-crf','25','-maxrate','2.5M','-bufsize','5M','-c:a','aac','-b:a','160k','-movflags','+faststart','/downloads/sharks-real-am_michael.mp4'],check=True)
print('total',end)
