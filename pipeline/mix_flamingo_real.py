import subprocess,json,os
P='/downloads/flamingo';F='/downloads/footage-flamingo'
starts=json.load(open(P+'/starts.json'));end=float(open(P+'/end.txt').read());edges=starts+[end]
# All scenes use Pexels-licensed real footage (https://www.pexels.com/license/).
# shot: (file, seek_seconds, speed, crop_filter_or_None, credit)
shots=[
 ('E-amit-rai-40078384.mp4',9.0,1.0,None,'Amit Rai | Pexels'),
 ('A-nicky-pe-8368094.mp4',0.5,1.0,None,'Nicky Pe | Pexels'),
 ('A-nicky-pe-8368094.mp4',5.5,1.0,None,'Nicky Pe | Pexels'),
 ('A-nicky-pe-8368094.mp4',12.75,1.0,None,'Nicky Pe | Pexels'),
 ('E-amit-rai-40078384.mp4',15.0,1.0,None,'Amit Rai | Pexels'),
 ('E-amit-rai-40078384.mp4',22.5,1.0,None,'Amit Rai | Pexels'),
 ('C-group-24812188.mp4',5.0,1.0,'crop=2560:1120:0:320','Magda Ehlers | Pexels'),
]
outs=[]
for i,shot in enumerate(shots):
 d=edges[i+1]-edges[i];out=f'{P}/realshot{i}.mp4';outs.append(out)
 src,ss,speed,crop,credit=shot
 pre=f'crop={crop[5:]},' if crop else ''
 vf=f"[0:v]setpts=(PTS-STARTPTS)/{speed},{pre}split=2[b][f];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:2,eq=brightness=-0.3[bg];[f]scale=1080:810:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:410,drawtext=text='{credit}':fontcolor=white:fontsize=27:x=(w-tw)/2:y=1780,setsar=1,fps=30[v]"
 cmd=['ffmpeg','-loglevel','error','-y','-ss',str(ss),'-i',f'{F}/{src}','-filter_complex',vf,'-map','[v]','-an','-t',str(d),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',out]
 subprocess.run(cmd,check=True)
open(P+'/concat.txt','w').write(''.join(f"file '{x}'\n"for x in outs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',P+'/concat.txt','-i',P+'/mix.mp3','-vf','ass='+P+'/cap.ass','-map','0:v','-map','1:a','-t',str(end),'-c:v','libx264','-preset','medium','-crf','25','-maxrate','2.5M','-bufsize','5M','-c:a','aac','-b:a','160k','-movflags','+faststart','/downloads/flamingo-real-am_onyx.mp4'],check=True)
print('total',end)
