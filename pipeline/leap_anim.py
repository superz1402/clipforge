# Original vector scenes about Gregorian leap-year corrections. NASA sources in CREDITS.md.
import math,sys,subprocess,cairo
from birds_anim import *
import birds_anim as B
GOLD=(1,.8,.3);BLUE=(.3,.7,1);GREEN=(.35,.9,.65)
def bg(c):sky(c,(.035,.04,.13),(.09,.14,.3))
def ball(c,x,y,r,col):c.set_source_rgb(*col);c.arc(x,y,r,0,6.3);c.fill()
def orbit(c,t):
 c.set_source_rgba(.7,.8,1,.35);c.set_line_width(5);c.save();c.translate(540,800);c.scale(1,.7);c.arc(0,0,350,0,6.3);c.stroke();c.restore();ball(c,540,800,95,GOLD)
 a=t*.65; x=540+350*math.cos(a);y=800+245*math.sin(a);ball(c,x,y,50,BLUE)
 c.save();c.arc(x,y,50,0,6.3);c.clip();ball(c,x+15+14*math.sin(t*2),y,28,GREEN);c.restore()
def card(c,day,x=540,y=800,w=650,h=660):
 c.set_source_rgb(.94,.95,.99);c.rectangle(x-w/2,y-h/2,w,h);c.fill();c.set_source_rgb(.85,.24,.3);c.rectangle(x-w/2,y-h/2,w,130);c.fill()
 text(c,'FEBRUARY',x,y-h/2+90,58);text(c,str(day),x,y+110,200,(.1,.14,.25),outline=False)
def clock(c,x,y,t,r=120):
 ball(c,x,y,r,(.92,.95,1));
 for k in range(12):
  a=k*math.pi/6;c.set_source_rgb(.1,.14,.25);c.arc(x+(r-18)*math.sin(a),y-(r-18)*math.cos(a),4,0,6.3);c.fill()
 a=t; c.set_source_rgb(.13,.2,.35);c.set_line_width(9);c.move_to(x,y);c.line_to(x+65*math.sin(a),y-65*math.cos(a));c.stroke();c.move_to(x,y);c.line_to(x-30,y-45);c.stroke()
def s1(c,t):
 bg(c);card(c,'29')
def s2(c,t):
 bg(c);orbit(c,t);text(c,'CALENDAR: 365 DAYS',540,370,50);text(c,'ORBIT: ABOUT 365.25 DAYS',540,1170,46,GOLD)
def s3(c,t):
 bg(c);text(c,'ABOUT 6 EXTRA HOURS / YEAR',540,330,46,GOLD)
 for k in range(4):
  x=230+(k%2)*620;y=580+(k//2)*400;clock(c,x,y,t+k,105);text(c,'~6 h',x,y+160,48)
 text(c,'4 YEARS -> ABOUT 1 DAY',540,1190,47,GREEN)
def s4(c,t):
 bg(c);card(c,'29',y=830,w=560,h=570);text(c,'KEEP CALENDAR + SEASONS',540,350,46,GREEN);text(c,'IN STEP',540,430,56,GREEN)
 for k,col in enumerate((GREEN,GOLD,(1,.45,.2),BLUE)):
  a=t*.35+k*math.pi/2;ball(c,540+380*math.cos(a),830+350*math.sin(a),24,col)
def s5(c,t):
 bg(c);orbit(c,t);text(c,'THE QUARTER IS APPROXIMATE',540,350,43,GOLD);text(c,'A LITTLE LESS THAN 365.25',540,450,42)
 text(c,'EVERY 4 YEARS IS TOO MUCH',540,1190,42,(1,.5,.4))
def s6(c,t):
 bg(c);text(c,'CENTURY YEAR?',540,350,58);text(c,'MUST DIVIDE BY 400',540,470,53,GOLD)
 for year,y,col,note in [('2000',760,GREEN,'LEAP YEAR'),('2100',1050,(1,.45,.4),'SKIP LEAP DAY')]:
  text(c,year,300,y,92,col);text(c,note,750,y-10,40,col)
 text(c,'GREGORIAN CALENDAR',540,1190,36)
def s7(c,t):
 bg(c);card(c,'29',y=800,w=540,h=560);clock(c,860,1050,t*2,100)
 text(c,'BONUS DAY?',540,350,64,GOLD);text(c,'OR: DEADLINE EXTENSION?',540,1190,44,GREEN)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC)) if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1] if len(sys.argv)>1 else 'anim.mp4';only=[float(x) for x in sys.argv[2:]];surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 if only:
  for t in only:lframe(c,t);surf.write_to_png(f'af_{t}.png')
  sys.exit()
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
