# Original simplified geyser plumbing cross-sections. Not to scale; individual systems vary.
import cairo,math,sys,subprocess,random
from birds_anim import *
import birds_anim as B
AQUA=(.35,.8,1);GOLD=(1,.8,.3)
def bg(c):sky(c,(.12,.28,.42),(.6,.72,.65))
def dot(c,x,y,r,col=AQUA):c.set_source_rgb(*col);c.arc(x,y,r,0,6.3);c.fill()
def line(c,x,y,u,v,col=AQUA,w=8):c.set_source_rgb(*col);c.set_line_width(w);c.move_to(x,y);c.line_to(u,v);c.stroke()
def arrow(c,x,y,u,v,col=GOLD):
 line(c,x,y,u,v,col);a=math.atan2(v-y,u-x)
 for k in (-.6,.6):line(c,u,v,u-25*math.cos(a+k),v-25*math.sin(a+k),col)
def ground(c):
 c.set_source_rgb(.25,.2,.17);c.rectangle(0,940,1080,980);c.fill();line(c,0,940,1080,940,(.5,.45,.3),12)
def plumbing(c,t,fill=1,bubbles=True):
 ground(c);c.set_source_rgb(.04,.12,.18);c.rectangle(490,940,100,210);c.fill();c.arc(540,1110,105,0,6.3);c.fill()
 c.set_source_rgb(*AQUA);c.rectangle(506,940+(1-fill)*200,68,210*fill);c.fill();c.arc(540,1110,86,0,6.3);c.fill()
 # narrow throat in the conduit
 c.set_source_rgb(.25,.2,.17);c.rectangle(490,985,28,32);c.fill();c.rectangle(562,985,28,32);c.fill()
 # hot rock adjacent, not magma poured into water
 for k in range(5):dot(c,790+(k%2)*55,1060+(k//2)*45,34,(.82,.25,.1))
 arrow(c,745,1110,650,1110,(1,.5,.2));text(c,'HOT ROCK',820,1210,32,(1,.75,.45))
 if bubbles:
  for i in range(10):
   q=(t*.35+i/10)%1;dot(c,535+16*math.sin(i*3),1155-q*150,5+6*q,(.95,.98,1))
def plume(c,t,scale=1):
 # fixed nonzero stream at every scene start, animated parcel travel.
 for i in range(45):
  q=(i/45+t*.55)%1;spread=15+80*q;x=540+spread*math.sin(i*2.4);y=930-470*q*scale
  c.set_source_rgba(.87,.96,1,.75*(1-q)+.2);c.arc(x,y,8+21*q,0,6.3);c.fill()
 for i in range(9):
  q=(i/9+t*.15)%1;c.set_source_rgba(.95,.98,1,.18*(1-q));c.arc(540+100*math.sin(i+q*3),500-q*110,50+60*q,0,6.3);c.fill()
def rain(c,t):
 for i in range(18):
  x=90+(i*79)%900;y=480+(i*51+t*180)%360;line(c,x,y,x-10,y+28,AQUA,4)
def gauge(c,t,low=False):
 x,y=230,690;dot(c,x,y,130,(.92,.94,.93));a=(-.3 if low else -2.8)+.05*math.sin(t*3);line(c,x,y,x+90*math.cos(a),y+90*math.sin(a),(.65,.15,.12),11);text(c,'LOWER'if low else 'HIGH',x,y+200,42,GOLD)
def s1(c,t):
 bg(c);ground(c);plume(c,t);text(c,'SUDDEN WATER + STEAM',540,480,47)
def s2(c,t):
 bg(c);plumbing(c,t);rain(c,t);arrow(c,900,750,900,1040,AQUA);arrow(c,890,1040,650,1070,AQUA)
 text(c,'HEAT + WATER + PLUMBING',540,340,44);text(c,'GROUNDWATER SEEPS DOWN',540,460,43)
def s3(c,t):
 bg(c);plumbing(c,t);gauge(c,t);text(c,'PRESSURE CHANGES BOILING',540,340,44);text(c,'HOTTER THAN SURFACE BOILING',650,520,32)
 arrow(c,540,700,540,900);text(c,'STILL LIQUID',760,780,40,GOLD)
def s4(c,t):
 bg(c);plumbing(c,t);plume(c,t,.35);text(c,'BUBBLES + A NARROW PASSAGE',540,340,42)
 # enlarged throat callout above the subterranean section
 c.set_source_rgb(.25,.2,.17);c.rectangle(160,520,200,280);c.fill();c.set_source_rgb(*AQUA);c.rectangle(220,520,80,280);c.fill();c.set_source_rgb(.25,.2,.17);c.rectangle(210,600,30,45);c.fill();c.rectangle(280,600,30,45);c.fill()
 for i in range(5):dot(c,260,780-((t*80+i*32)%130),13,(.95,.98,1))
 text(c,'THROAT DETAIL',260,480,30);text(c,'WATER IS PUSHED OUT',700,650,36);text(c,'PRESSURE STARTS TO FALL',650,780,35,GOLD)
def s5(c,t):
 bg(c);plumbing(c,t);plume(c,t);text(c,'PRESSURE DROP -> MORE STEAM',540,340,41)
 text(c,'EXPANSION DRIVES ERUPTION',540,460,40,GOLD)
def s6(c,t):
 bg(c);plumbing(c,t,.45+.55*prog(t,0,4),False);rain(c,t);arrow(c,900,750,900,1040,AQUA);arrow(c,890,1040,650,1070,AQUA)
 text(c,'COOL / DEPLETED -> ERUPTION ENDS',540,340,35);text(c,'REFILL. REHEAT. REPEAT.',540,460,47,GOLD)
def s7(c,t):
 bg(c);ground(c);plume(c,t);text(c,'LEAST RELAXING FOUNTAIN?',540,350,46,GOLD)
 text(c,'PRESSURE COOKER ENERGY',540,470,43)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
