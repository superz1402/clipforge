import math,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920; S=2
FB=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s*S)
T0=11.5; T1=32.7; FPS=30
BG=(8,22,48)
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def prog(t,a,b): return ease((t-a)/(b-a))
def txt(d,xy,s,fill,anchor='mm',f=None):
    d.text((xy[0]*S,xy[1]*S),s,fill=fill,font=f or FB(40),anchor=anchor)
def medusa(d,cx,cy,sc=1,ten=1,col=(120,220,255)):
    sc*=1.5
    r=70*sc
    d.pieslice([ (cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r*0.9)*S],180,360,fill=col)
    if ten>0.02:
        c=tuple(int(BG[i]+(col[i]-BG[i])*ten) for i in range(3))
        for k in range(-3,4):
            x=cx+k*r/3.6
            pts=[(x*S,(cy+2)*S)]
            for j in range(1,8):
                pts.append(((x+8*math.sin(j*1.1+k))*S,(cy+2+j*14*sc)*S))
            d.line(pts,fill=c,width=int(4*S),joint='curve')
def polyp(d,cx,cy,sc=1,col=(255,190,120)):
    sc*=1.5
    d.rounded_rectangle([(cx-16*sc)*S,(cy-70*sc)*S,(cx+16*sc)*S,(cy+60*sc)*S],radius=14*S,fill=col)
    d.ellipse([(cx-34*sc)*S,(cy+50*sc)*S,(cx+34*sc)*S,(cy+80*sc)*S],fill=col)
    for k in(-1,0,1):
        d.line([(cx*S,(cy-62*sc)*S),((cx+k*34*sc)*S,(cy-110*sc)*S)],fill=col,width=int(7*S))
def larva(d,cx,cy,col=(150,255,170)):
    sc=1.5
    d.ellipse([(cx-26*sc)*S,(cy-52*sc)*S,(cx+26*sc)*S,(cy+52*sc)*S],fill=col)
def arrow(d,a,b,col,p=1,w=8):
    x=a[0]+(b[0]-a[0])*p; y=a[1]+(b[1]-a[1])*p
    d.line([(a[0]*S,a[1]*S),(x*S,y*S)],fill=col,width=w*S)
    if p>0.95:
        ang=math.atan2(b[1]-a[1],b[0]-a[0])
        for s in(-0.5,0.5):
            d.line([(b[0]*S,b[1]*S),((b[0]-30*math.cos(ang+s))*S,(b[1]-30*math.sin(ang+s))*S)],fill=col,width=w*S)
def frame(t):
    im=Image.new('RGB',(W*S,H*S),BG); d=ImageDraw.Draw(im)
    if t<27.0:
        y=450
        X=[190,540,890]
        lab=['LARVA','POLYP','ADULT']
        # highlight by narration
        hl=[prog(t,11.7,12.0),prog(t,12.7,13.0),prog(t,13.7,14.0)]
        larva(d,X[0],y); polyp(d,X[1],y+10); medusa(d,X[2],y-10)
        for i in range(3):
            c=(255,255,255) if hl[i]>0.5 else (110,130,170)
            txt(d,(X[i],y+165),lab[i],c)
        txt(d,(540,165),'NORMAL LIFE CYCLE',(255,255,255),f=FB(44))
        a1=prog(t,12.3,12.8); a2=prog(t,13.3,13.8)
        if a1>0: arrow(d,(X[0]+80,y),(X[1]-100,y),(255,255,255),a1)
        if a2>0: arrow(d,(X[1]+100,y),(X[2]-130,y),(255,255,255),a2)
        # stress
        if t>=14.6:
            fl=prog(t,14.6,15.0)
            txt(d,(X[2],y-190),'STRESS',(255,90,90),f=FB(52))
            if int(t*6)%2==0 or t>17.5: txt(d,(X[2]+0,y-140),'injury / starvation',(255,150,150),f=FB(30))
        # reverse arc
        rp=prog(t,18.3,25.5)
        if rp>0:
            n=40; k=int(n*rp)
            pts=[]
            for i in range(k+1):
                u=i/n; ang=math.pi*u
                pts.append(((X[2]-(X[2]-X[1])*u*1.0)*S, (y+250+90*math.sin(ang))*S))
            if len(pts)>1: d.line(pts,fill=(255,90,90),width=10*S,joint='curve')
            txt(d,(540,y+420),'LIFE CYCLE REVERSES',(255,110,110),f=FB(46))
        # morph icon
        if t>=18.3:
            my=1000
            a=prog(t,20.3,21.5)   # bell shrinks
            b=prog(t,21.6,23.2)   # tentacles vanish
            c=prog(t,23.4,25.7)   # become polyp
            if c<1:
                medusa(d,540,my,sc=1-0.45*a,ten=1-b,col=tuple(int(v*(1-c)+BG[i]*c) for i,v in enumerate((120,220,255))))
            if c>0:
                p=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); pd=ImageDraw.Draw(p)
                polyp(pd,540,my+10,sc=0.85,col=(255,190,120,int(255*c)))
                im.paste(p,(0,0),p); d=ImageDraw.Draw(im)
            lab2='bell shrinks' if t<21.5 else ('tentacles disappear' if t<23.3 else ('juvenile polyp' if t>=25.3 else 'body reorganises'))
            txt(d,(540,1140),lab2.upper(),(255,255,255),f=FB(36))
    else:
        txt(d,(540,330),'TRANSDIFFERENTIATION',(255,255,255),f=FB(50))
        txt(d,(540,420),'a specialised cell becomes a different cell type',(170,200,240),f=FB(28))
        cA=(80,150,255); cB=(255,170,70)
        m=prog(t,29.6,31.8)
        cols=[(60,110,255),(80,200,140),(255,120,160)]
        for i in range(3):
            x=270+i*270
            start=cols[i]; end=(255,200,70)
            q=prog(t,29.2+i*0.6,30.6+i*0.6)
            c=tuple(int(start[j]*(1-q)+end[j]*q) for j in range(3))
            r=95
            d.ellipse([(x-r)*S,(640-r)*S,(x+r)*S,(640+r)*S],fill=c)
            d.ellipse([(x-28)*S,(640-28)*S,(x+28)*S,(640+28)*S],fill=(20,30,60))
            if q>0.5:
                d.regular_polygon(((x)*S,(640)*S,r*0.55*S),6,fill=c) if False else None
        txt(d,(540,820),'old job  ->  new job',(255,255,255),f=FB(40))
        rb=prog(t,31.2,32.4)
        if rb>0:
            txt(d,(540,960),'= REBUILT BODY',(255,210,100),f=FB(48))
    im=im.resize((W,H),Image.LANCZOS)
    return im
n=int((T1-T0)*FPS)
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','schem.mp4'],stdin=subprocess.PIPE)
for i in range(n):
    p.stdin.write(frame(T0+i/FPS).tobytes())
p.stdin.close();p.wait()
if len(sys.argv)>1:
    for t in (12.2,13.9,16,20.8,22.5,24,26.5,28,30.5,32):
        frame(t).resize((360,640)).save(f'sf_{t}.png')
