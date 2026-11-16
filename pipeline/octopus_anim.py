# Original cartoon octopus and circulatory schematics; not anatomical positioning or molecular structure.
import cairo,math,sys,subprocess,random
from birds_anim import *
import birds_anim as B
BLUE=(.3,.65,1);GOLD=(1,.8,.3);RED=(.95,.25,.3);PURPLE=(.65,.3,.65)
R=random.Random(29);BUB=[(R.randrange(1080),R.randrange(1300),R.uniform(7,18))for _ in range(18)]
def bg(c,t):
 sky(c,(.02,.07,.19),(.03,.25,.35))
 for x,y,r in BUB:
  c.set_source_rgba(.6,.9,1,.17);c.set_line_width(3);c.arc(x,(y-t*35)%1800,r,0,6.3);c.stroke()
def dot(c,x,y,r,col):c.set_source_rgb(*col);c.arc(x,y,r,0,6.3);c.fill()
def line(c,x,y,u,v,col=BLUE,w=8):c.set_source_rgb(*col);c.set_line_width(w);c.move_to(x,y);c.line_to(u,v);c.stroke()
def arrow(c,x,y,u,v,col=BLUE):
 line(c,x,y,u,v,col);a=math.atan2(v-y,u-x)
 for k in (-.6,.6):line(c,u,v,u-25*math.cos(a+k),v-25*math.sin(a+k),col)
def octo(c,x,y,t,s=1):
 c.save();c.translate(x,y);c.scale(s,s);c.set_line_cap(cairo.LINE_CAP_ROUND)
 # Eight independently visible arms, fanned out beneath the mantle.
 ends=[(-310,80),(-240,145),(-150,205),(-55,230),(55,230),(150,205),(240,145),(310,80)]
 for k,(xx,yy) in enumerate(ends):
  side=-1 if xx<0 else 1;yy+=9*math.sin(t*2+k);root=(k-3.5)*21
  c.set_source_rgb(*PURPLE);c.set_line_width(28);c.move_to(root,65);c.curve_to(root+side*45,170,xx-side*40,yy+55,xx,yy);c.stroke()
  dot(c,xx-side*14,yy+10,5,(.9,.6,.85));dot(c,xx-side*30,yy+23,5,(.9,.6,.85))
 c.set_source_rgb(*PURPLE);c.save();c.scale(1,1.1);c.arc(0,-30,150,0,6.3);c.fill();c.restore()
 for xx in (-65,65):
  dot(c,xx,0,35,(.97,.98,1));dot(c,xx+6,4,15,(.05,.07,.13))
 c.set_source_rgb(.25,.08,.25);c.set_line_width(7);c.arc(0,60,24,.2,2.9);c.stroke();c.restore()
def heart(c,x,y,size=65,col=RED,t=0):
 s=size*(1+.06*math.sin(t*6));c.save();c.translate(x,y);c.scale(s/70,s/70);c.set_source_rgb(*col);c.move_to(0,58);c.curve_to(-125,-20,-40,-100,0,-35);c.curve_to(40,-100,125,-20,0,58);c.fill();c.restore()
def protein(c,x,y,t,col,label):
 for k in range(13):
  a=k*.7+t*.16;r=90+30*math.sin(k*2.2);dot(c,x+r*math.cos(a),y+r*math.sin(a),36,col)
 dot(c,x,y,75,GOLD);text(c,label,x,y+12,26,(.1,.12,.2),outline=False)
def s1(c,t):
 bg(c,t);octo(c,540,850,t,1.3);text(c,'BLUE BLOOD. NOT ROYALTY.',540,500,47,GOLD)
def s2(c,t):
 bg(c,t);text(c,'HUMANS: HEMOGLOBIN',540,350,49);protein(c,540,800,t,RED,'IRON');text(c,'OXYGEN-CARRYING PROTEIN',540,1140,43);text(c,'PROTEIN SCHEMATIC',540,1210,28)
def s3(c,t):
 bg(c,t);text(c,'OCTOPUSES: HEMOCYANIN',540,350,47);protein(c,540,800,t,BLUE,'COPPER');text(c,'DIFFERENT PROTEIN. BLUE BLOOD.',540,1140,39);text(c,'PROTEIN SCHEMATIC',540,1210,28)
def s4(c,t):
 bg(c,t);text(c,'SAME JOB. DIFFERENT METAL.',540,350,46,GOLD);protein(c,280,760,t,RED,'IRON');protein(c,800,760,t,BLUE,'COPPER');text(c,'OXYGEN TRANSPORT',540,1110,52)
 for i in range(4):
  x=90+(i*230+t*100)%900;dot(c,x,500,15,(.7,.9,1));dot(c,x+24,500,15,(.7,.9,1))
def s5(c,t):
 bg(c,t);octo(c,540,900,t,1.1);text(c,'THREE HEARTS',540,350,68,GOLD)
 for i in range(3):heart(c,290+i*250,550,60,t=t+i*.3)
 text(c,'ICONS - NOT ORGAN POSITIONS',540,1210,27)
def s6(c,t):
 bg(c,t);text(c,'TWO HEARTS -> GILLS',540,350,50);text(c,'THIRD HEART -> BODY',540,465,50,GOLD)
 for x in (240,840):
  heart(c,x,690,55,t=t);arrow(c,x,760,x,920)
  for i in range(5):line(c,x-60,950+i*20,x+60,950+i*20,(.6,.8,.9),7)
  text(c,'GILL',x,1110,36);arrow(c,x,1035,540,1060)
 heart(c,540,1060,55,t=t+.2);arrow(c,540,1125,540,1190);text(c,'BODY',540,1240,29,GOLD)
 text(c,'FLOW SCHEMATIC',540,580,28)
def s7(c,t):
 bg(c,t);octo(c,540,840,t,1.25);text(c,'PREMIUM PLUMBING?',540,350,59,GOLD)
 for i in range(3):heart(c,320+i*220,540,38,t=t+i*.4)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
