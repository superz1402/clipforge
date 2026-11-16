# Original schematic vector animation; no external visual assets.
import math,sys,subprocess,cairo,random
from birds_anim import *
import birds_anim as B
BLUE=(.3,.7,1);CYAN=(.55,.92,1);GOLD=(1,.8,.35)
def bg(c):sky(c,(.025,.08,.18),(.06,.2,.34))
def line(c,x,y,u,v,col=CYAN,w=5):
 c.set_source_rgb(*col);c.set_line_width(w);c.move_to(x,y);c.line_to(u,v);c.stroke()
def dot(c,x,y,r,col):c.set_source_rgb(*col);c.arc(x,y,r,0,6.3);c.fill()
def molecule(c,x,y,s=1):
 for a in (-2.5,-.65):
  u=x+30*s*math.cos(a);v=y+30*s*math.sin(a);line(c,x,y,u,v,(.8,.9,1),8*s);dot(c,u,v,12*s,(.96,.97,1))
 dot(c,x,y,21*s,(.95,.25,.3))
def cube(c,x,y,size=230,face=False):
 c.set_source_rgba(.6,.9,1,.93);c.rectangle(x-size/2,y-size/2,size,size);c.fill();c.set_source_rgb(.9,.98,1);c.set_line_width(8);c.rectangle(x-size/2,y-size/2,size,size);c.stroke();line(c,x-size*.35,y-size*.25,x+size*.25,y-size*.35,(.9,.99,1),7)
 if face:
  for xx in (-.18,.18):dot(c,x+xx*size,y,8,(.05,.16,.25))
  c.set_source_rgb(.05,.16,.25);c.set_line_width(6);c.arc(x,y+size*.09,size*.14,0,math.pi);c.stroke()
def tank(c,t,waterline=850):
 c.set_source_rgb(.05,.4,.65);c.rectangle(120,waterline,840,1200-waterline);c.fill();c.set_source_rgba(.7,.9,1,.7);c.set_line_width(8);c.move_to(120,550);c.line_to(120,1200);c.line_to(960,1200);c.line_to(960,550);c.stroke()
 for i in range(3):line(c,140,waterline+i*10,940,waterline+i*10,(.3,.65,.85),3)
def s1(c,t):
 bg(c);tank(c,t);cube(c,540,920+9*math.sin(t*2),260);text(c,'SOLID WATER. STILL FLOATING.',540,480,46,CYAN)
def s2(c,t):
 bg(c);text(c,'DENSITY = MASS / VOLUME',540,350,47,GOLD)
 for k,n in enumerate((16,8)):
  x0=100+k*490;c.set_source_rgba(.5,.8,1,.3);c.rectangle(x0,550,380,470);c.fill()
  for i in range(n):dot(c,x0+60+(i%4)*85,610+(i//4)*100+4*math.sin(t*2+i),20,CYAN)
 text(c,'MORE IN SAME SPACE',300,1160,36);text(c,'LESS IN SAME SPACE',790,1160,36)
def s3(c,t):
 bg(c);text(c,'HYDROGEN BONDS',540,350,55,CYAN);text(c,'A MORE OPEN STRUCTURE',540,470,45)
 pts=[(540+270*math.cos(i*math.pi/3),850+270*math.sin(i*math.pi/3))for i in range(6)]
 for i,(x,y) in enumerate(pts):
  u,v=pts[(i+1)%6];c.set_dash([12,10]);line(c,x,y,u,v,(.6,.8,.95),6);c.set_dash([])
 for x,y in pts:molecule(c,x,y,1.5+.03*math.sin(t*2))
 text(c,'MOLECULAR SCHEMATIC',540,1200,31)
def s4(c,t):
 bg(c);text(c,'SAME WATER. MORE ROOM.',540,350,52,GOLD)
 for k,sp in enumerate((70,100)):
  cx=290+k*510;size=sp*3.3;c.set_source_rgba(.5,.8,1,.22);c.rectangle(cx-size/2,820-size/2,size,size);c.fill()
  for i in range(9):dot(c,cx+(i%3-1)*sp,820+(i//3-1)*sp+(5*math.sin(t*3+i) if k==0 else 0),16,CYAN)
 text(c,'LIQUID',290,1100,45);text(c,'ICE',800,1100,45);text(c,'LOWER DENSITY',800,1180,37,GOLD)
def s5(c,t):
 bg(c);text(c,'ABOUT 9% EXPANSION',540,350,54,GOLD);text(c,'FRESH WATER -> ICE',540,470,46)
 # side-by-side schematics explicitly not a quantitative scale.
 c.set_source_rgb(.05,.5,.75);c.rectangle(175,725,250,250);c.fill();c.set_source_rgb(.8,.95,1);c.set_line_width(7);c.move_to(175,680);c.line_to(175,975);c.line_to(425,975);c.line_to(425,680);c.stroke();cube(c,790,850,300);text(c,'LIQUID',300,1100,43);text(c,'ICE',790,1100,43)
 text(c,'SCHEMATIC - NOT TO SCALE',540,1200,30)
def s6(c,t):
 bg(c);tank(c,t,770);cube(c,540,890+6*math.sin(t*2),300);line(c,130,770,950,770,(.45,.8,1),10)
 text(c,'LOWER-DENSITY ICE',540,380,50,CYAN);text(c,'DENSER LIQUID WATER',540,1140,44)
 text(c,'MUCH OF THE ICE IS SUBMERGED',540,490,37)
def s7(c,t):
 bg(c);tank(c,t);cube(c,540,920+9*math.sin(t*2),270,True);text(c,'TAKING UP SPACE?',540,400,58,GOLD)
 text(c,'OR REFUSING TO LEAVE?',540,510,48,CYAN)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
