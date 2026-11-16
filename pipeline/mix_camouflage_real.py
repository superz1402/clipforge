import subprocess,json,os
P='/downloads/camouflage';starts=json.load(open(P+'/starts.json'));end=float(open(P+'/end.txt').read());edges=starts+[end]
# scenes3/4 use explanatory original diagrams. All other scenes use verified licensed live-action footage.
shots=[('/downloads/footage/octopus0.ogv',0,1),('/downloads/footage/octopus0.ogv',9,1),None,None,('/downloads/footage/octopus0.ogv',25,1),('/downloads/footage/octopus1.ogv',0,.77),('/downloads/footage/octopus0.ogv',41,1)]
outs=[]
for i,shot in enumerate(shots):
 d=edges[i+1]-edges[i];out=f'{P}/realshot{i}.mp4';outs.append(out)
 if shot:
  src,ss,speed=shot;credit='Silke Baron (prilfish) | CC BY 2.0'if 'octopus0' in src else 'Caldwell et al. | PLOS ONE | CC BY 4.0'
  vf=f"[0:v]setpts=(PTS-STARTPTS)/{speed},split=2[b][f];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:2,eq=brightness=-0.3[bg];[f]scale=1080:810:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:410,drawtext=text='{credit}':fontcolor=white:fontsize=27:x=(w-tw)/2:y=1780,setsar=1,fps=30[v]"
  cmd=['ffmpeg','-loglevel','error','-y','-ss',str(ss),'-i',src,'-filter_complex',vf,'-map','[v]','-an','-t',str(d),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',out]
 else:
  cmd=['ffmpeg','-loglevel','error','-y','-ss',str(edges[i]),'-i',P+'/anim.mp4','-an','-t',str(d),'-vf','setsar=1,fps=30','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',out]
 subprocess.run(cmd,check=True)
open(P+'/concat.txt','w').write(''.join(f"file '{x}'\n"for x in outs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',P+'/concat.txt','-i',P+'/mix.mp3','-vf','ass='+P+'/cap.ass','-map','0:v','-map','1:a','-t',str(end),'-c:v','libx264','-preset','medium','-crf','25','-maxrate','2.5M','-bufsize','5M','-c:a','aac','-b:a','160k','-movflags','+faststart','/downloads/camouflage-real-am_michael.mp4'],check=True)
print('real duration',sum(edges[i+1]-edges[i]for i,x in enumerate(shots)if x),'total',end)
