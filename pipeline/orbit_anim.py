# Original vector orbital/free-fall illustrations, not to scale or orbital simulation.
import cairo,math,sys,subprocess,random
from birds_anim import *
import birds_anim as B
BLUE=(.25,.6,1);GREEN=(.25,.75,.5);GOLD=(1,.8,.3)
R=random.Random(37);STARS2=[(R.randrange(1080),R.randrange(1920),R.uniform(1,3),R.random()*6.3)for _ in range(95)]
def bg(c,t):
 sky(c,(.015,.02,.08),(.035,.065,.17))
 for x,y,r,p in STARS2:c.set_source_rgba(.8,.88,1,.4+.3*math.sin(t+p));c.arc(x,y,r,0,6.3);c.fill()
def line(c,x,y,u,v,col=GOLD,w=7):c.set_source_rgb(*col);c.set_line_width(w);c.move_to(x,y);c.line_to(u,v);c.stroke()
def arrow(c,x,y,u,v,col=GOLD):
 line(c,x,y,u,v,col);a=math.atan2(v-y,u-x)
 for k in (-.55,.55):line(c,u,v,u-27*math.cos(a+k),v-27*math.sin(a+k),col)
def earth(c,x,y,r,t=0):
 c.save();c.arc(x,y,r,0,6.3);c.clip();c.set_source_rgb(*BLUE);c.paint()
 for i in range(4):
  c.set_source_rgb(*GREEN);xx=x+r*.65*math.sin(i*2.4+t*.1);yy=y-r*.7+i*r*.45;c.save();c.translate(xx,yy);c.rotate(i);c.scale(1.6,1);c.arc(0,0,r*.22,0,6.3);c.fill();c.restore()
 c.restore();c.set_source_rgba(.4,.7,1,.5);c.set_line_width(12);c.arc(x,y,r+7,0,6.3);c.stroke()
def astronaut(c,x,y,s=1,a=0):
 c.save();c.translate(x,y);c.rotate(a);c.scale(s,s)
 c.set_source_rgb(.85,.9,.96);c.rectangle(-40,-10,80,115);c.fill()
 for k in (-1,1):line(c,k*35,10,k*80,40,(.85,.9,.96),26);line(c,k*23,100,k*35,155,(.85,.9,.96),28)
 c.set_source_rgb(.9,.94,1);c.arc(0,-55,58,0,6.3);c.fill();c.set_source_rgb(.07,.12,.2);c.arc(0,-55,42,0,6.3);c.fill();line(c,-26,-74,5,-88,(.5,.7,.85),7)
 c.set_source_rgb(.2,.4,.6);c.rectangle(-24,20,48,45);c.fill();c.restore()
def station(c,x,y,s=1,a=0):
 c.save();c.translate(x,y);c.rotate(a);c.scale(s,s)
 c.set_source_rgb(.7,.75,.85);c.rectangle(-70,-25,140,50);c.fill();line(c,-170,0,170,0,(.8,.85,.9),10)
 for side in (-1,1):
  c.set_source_rgb(.12,.32,.6);c.rectangle(side*120-35,-110,70,220);c.fill()
  for k in range(8):line(c,side*120-35,-110+k*30,side*120+35,-110+k*30,(.4,.65,.9),2)
 c.restore()
def window(c):
 c.set_source_rgba(.5,.65,.8,.5);c.set_line_width(18);c.rectangle(95,450,890,760);c.stroke()
def s1(c,t):
 bg(c,t);earth(c,540,1850,460,t);astronaut(c,500+50*math.sin(t*.6),780+30*math.sin(t),2,-.2+.12*math.sin(t))
def s2(c,t):
 bg(c,t);earth(c,540,1570,560,t);station(c,540,700,1.7);arrow(c,540,850,540,1090)
 text(c,'ABOUT 90% OF SURFACE GRAVITY',540,360,43,GOLD);text(c,'STILL PULLING TOWARD EARTH',540,460,40)
def s3(c,t):
 bg(c,t);window(c);dy=20*math.sin(t*.9);astronaut(c,410,800+dy,1.5,.2);c.set_source_rgb(1,.3,.3);c.arc(740,800+dy,35,0,6.3);c.fill()
 for x in (260,540,820):arrow(c,x,1010,x,1150)
 text(c,'EVERYTHING FALLS TOGETHER',540,350,48,GOLD);text(c,'CABIN VIEW',540,530,35)
def s4(c,t):
 bg(c,t);earth(c,540,850,260,t);c.set_source_rgba(.65,.8,1,.6);c.set_line_width(5);c.arc(540,850,385,0,6.3);c.stroke()
 a=-math.pi/2+t*.45;x=540+385*math.cos(a);y=850+385*math.sin(a);station(c,x,y,.55,a+math.pi/2)
 arrow(c,x,y,x-105*math.sin(a),y+105*math.cos(a),(.4,1,.65));arrow(c,x,y,x-80*math.cos(a),y-80*math.sin(a),GOLD)
 text(c,'SIDEWAYS MOTION + GRAVITY',540,340,44);text(c,'CONTINUOUS FREE FALL',540,1190,45,GOLD)
# Dimensionless central-gravity integration for the thought experiment paths.
def path(mult):
 x,y=0.,-330.;vx,vy=math.sqrt(10000000/330)*mult,0.;pts=[];dt=.015
 for _ in range(1500):
  r=math.hypot(x,y)
  if r<230:break
  pts.append((540+x,950+y));ax=-10000000*x/r**3;ay=-10000000*y/r**3
  vx+=ax*dt;vy+=ay*dt;x+=vx*dt;y+=vy*dt
 return pts
PATHS=[path(v)for v in (.45,.72,1.)]
def s5(c,t):
 bg(c,t);earth(c,540,950,230,t);text(c,'A THOUGHT EXPERIMENT',540,350,47,GOLD)
 text(c,'HIGH ABOVE THE ATMOSPHERE',540,470,39);text(c,'SCHEMATIC - NOT TO SCALE',540,560,29)
 for k,pts in enumerate(PATHS):
  c.set_source_rgba(.4,.7,1,.35+k*.2);c.set_line_width(5);c.move_to(*pts[0])
  for p in pts:c.line_to(*p)
  c.stroke();i=int((t*.18)%1*len(pts));x,y=pts[i];c.set_source_rgb(1,.7,.25);c.arc(x,y,13,0,6.3);c.fill()
def s6(c,t):
 bg(c,t);astronaut(c,540,740+10*math.sin(t),1.6);c.set_source_rgb(.4,.5,.6);c.rectangle(310,1050,460,130);c.fill();c.set_source_rgb(.1,.2,.22);c.rectangle(390,1080,300,70);c.fill();text(c,'0',540,1135,60,(.5,1,.7),outline=False)
 text(c,'MASS: STILL THERE',540,350,55);text(c,'IDEAL FREE-FALL SCALE',540,480,43,GOLD);text(c,"WEIGHTLESS ISN'T GRAVITY-FREE",540,1210,39)
def s7(c,t):
 bg(c,t);earth(c,540,1850,460,t);astronaut(c,540+60*math.sin(t),780+25*math.cos(t),2,.2*math.sin(t));text(c,'MISSING THE FLOOR?',540,400,57,GOLD)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
