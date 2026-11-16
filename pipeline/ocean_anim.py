# Original vector animation: ocean salinity. Scientific sources in CREDITS.md.
import math,sys,subprocess,cairo,random
from birds_anim import *
import birds_anim as B
AQUA=(.25,.85,.95); GOLD=(1,.8,.35)
def bg(c): sky(c,(.025,.075,.18),(.04,.25,.38))
def dot(c,x,y,r=9,col=GOLD):
 c.set_source_rgb(*col); c.arc(x,y,r,0,6.3); c.fill()
def line(c,x,y,u,v,col=AQUA,width=9):
 c.set_source_rgb(*col); c.set_line_width(width); c.move_to(x,y); c.line_to(u,v); c.stroke()
def arrow(c,x,y,u,v,col=AQUA):
 line(c,x,y,u,v,col,12); a=math.atan2(v-y,u-x)
 for s in (-.6,.6): line(c,u,v,u-30*math.cos(a+s),v-30*math.sin(a+s),col,12)
def water(c,t,y=900):
 c.set_source_rgb(.05,.42,.7); c.move_to(0,1920); c.line_to(0,y)
 for x in range(0,1081,10): c.line_to(x,y+18*math.sin(x/90+t*2))
 c.line_to(1080,1920); c.close_path(); c.fill()
def rock(c,x,y,s=1):
 c.set_source_rgb(.42,.46,.5); c.move_to(x-90*s,y); c.line_to(x-60*s,y-120*s); c.line_to(x+30*s,y-155*s); c.line_to(x+100*s,y-30*s); c.line_to(x+80*s,y+10*s); c.close_path();c.fill()
 line(c,x-30*s,y-100*s,x+5*s,y-60*s,(.65,.68,.69),6)
def rain(c,t,x0=100,x1=980,top=360,bottom=730):
 for i in range(18):
  x=x0+(i*83)%(x1-x0); y=top+(i*59+t*220)%(bottom-top); line(c,x,y,x-12,y+35,AQUA,5)
def salt(c,t,n=35,y0=970):
 r=random.Random(8)
 for i in range(n): dot(c,r.uniform(70,1010),y0+r.uniform(0,200)+9*math.sin(t+i),7)
def s1(c,t):
 bg(c);water(c,t,950);text(c,'FRESH RIVERS',300,570,49,AQUA);text(c,'SALTY SEA',750,820,60)
 arrow(c,180,680,780,980); salt(c,t,28,1030)
def s2(c,t):
 bg(c);rain(c,t);rock(c,360,1000,1.8);water(c,t,1150)
 for i in range(12):
  q=(t*.16+i/12)%1;dot(c,450+480*q,1030+100*q,8)
 text(c,'SLIGHTLY ACIDIC RAIN',540,300,49,AQUA);text(c,'ROCKS RELEASE MINERALS',540,650,48)
def s3(c,t):
 bg(c);water(c,t,850);text(c,'RIVERS DELIVER MINERALS',540,340,49);arrow(c,90,560,880,850)
 for i in range(20):
  q=(i/20+t*.14)%1;dot(c,100+820*q,580+290*q,8)
 # stylized organism plus remaining mineral dots, labels explicitly distinguish roles
 c.set_source_rgb(.4,.85,.5);c.arc(280,1050,85+7*math.sin(t*2),0,6.3);c.fill()
 for i in range(6):dot(c,280+100*math.cos(i),1050+100*math.sin(i),12,(.4,.85,.5))
 salt(c,t,24,1030);text(c,'SOME USED',280,1190,38);text(c,'OTHERS REMAIN',770,1190,38,GOLD)
def s4(c,t):
 bg(c);rain(c,t,70,450,440,680);text(c,'RAIN REFILLS RIVERS',540,330,51,AQUA)
 water(c,t,970);text(c,'TODAY: PROBABLY BALANCED',540,720,47)
 arrow(c,130,880,440,880,GOLD);arrow(c,650,1080,960,1080,GOLD)
 text(c,'SALT IN',280,830,42,GOLD);text(c,'SALT OUT',800,1180,42,GOLD)
 text(c,'NOT ENDLESSLY SALTIER',540,560,47)
def s5(c,t):
 bg(c);water(c,t,300);c.set_source_rgb(.16,.18,.2);c.rectangle(0,1110,1080,810);c.fill()
 for x in (360,730):
  rock(c,x,1110,1.2)
  for i in range(16):
   q=(t*.2+i/16)%1;dot(c,x+45*math.sin(i+q*5),980-q*520,6+12*q,(.7,.82,.82))
 text(c,'HYDROTHERMAL VENTS',540,380,52);text(c,'MINERALS FROM BELOW',540,620,46,GOLD)
def s6(c,t):
 bg(c);text(c,'BY ONE ESTIMATE',540,330,52,GOLD)
 c.set_source_rgb(.22,.47,.25);c.rectangle(100,1120,880,90);c.fill()
 g=.18+.82*prog(t,0,3);c.set_source_rgb(.94,.93,.82);c.rectangle(200,1120-580*g,680,580*g);c.fill()
 text(c,'SALT OVER ALL LAND',540,440,48);text(c,'MORE THAN 500 FEET',540,570,48)
 text(c,'ILLUSTRATION - NOT TO SCALE',540,1200,31)
def s7(c,t):
 bg(c);water(c,t,970);salt(c,t,40,1020)
 # salt cellar character
 c.save();c.translate(540,720);c.rotate(.06*math.sin(t*2));c.set_source_rgb(.92,.95,.94);c.rectangle(-130,-140,260,310);c.fill();c.set_source_rgb(.5,.58,.62);c.rectangle(-145,-190,290,70);c.fill()
 for x in (-70,0,70):dot(c,x,-160,8,(.1,.15,.18))
 for x in (-50,50):dot(c,x,-30,11,(.1,.15,.18))
 c.set_source_rgb(.1,.15,.18);c.set_line_width(7);c.arc(0,15,42,.15,3);c.stroke();c.restore()
 text(c,'COLLECTOR OR HOARDER?',540,400,53,GOLD)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC)) if t>=ST[k]-1e-6); SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1] if len(sys.argv)>1 else 'anim.mp4'; only=[float(x) for x in sys.argv[2:]]
 surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 if only:
  for t in only:lframe(c,t);surf.write_to_png(f'af_{t}.png')
  sys.exit()
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
