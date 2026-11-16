# Original octopus camouflage diagrams. Uses original reusable octopus character.
import cairo,math,sys,subprocess,random
from birds_anim import *
from octopus_anim import octo,bg,line,dot,arrow,PURPLE,GOLD
import birds_anim as B
BROWN=(.4,.28,.18);RED=(.8,.2,.12);SAND=(.68,.57,.37)
def cell(c,x,y,q,r=100):
 # Radial muscles control a pigment sac; diagram, not tissue dimensions.
 for k in range(10):
  a=k*math.pi/5;ri=r*(.2+.7*q);xo=x+r*1.5*math.cos(a);yo=y+r*1.5*math.sin(a);xi=x+ri*math.cos(a);yi=y+ri*math.sin(a);line(c,xi,yi,xo,yo,(1,.75,.35),8)
 dot(c,x,y,r*(.2+.7*q),BROWN)
def skin(c,t,q=None):
 c.set_source_rgb(.9,.77,.62);c.rectangle(90,560,900,540);c.fill()
 for i in range(15):
  x=180+(i%5)*180;y=670+(i//5)*165;qq=(.5+.45*math.sin(t*2+i*.9))if q is None else q
  cell(c,x,y,qq,52)
def sceneocto(c,t,col=PURPLE):
 bg(c,t);c.set_source_rgb(*SAND);c.rectangle(0,1160,1080,760);c.fill()
 # Adjacent rock makes the matching target visible, not a disappearing trick.
 c.set_source_rgb(*BROWN);c.save();c.translate(820,1020);c.scale(1.8,1);c.arc(0,0,100,0,6.3);c.fill();c.restore()
 octo(c,480,820,t,1.1,col)
def s1(c,t):
 q=.5+.5*math.sin(t*1.1);col=tuple(PURPLE[i]*(1-q)+BROWN[i]*q for i in range(3));sceneocto(c,t,col)
def s2(c,t):
 bg(c,t);skin(c,t);text(c,'CHROMATOPHORES',540,350,61,GOLD);text(c,'STRETCHY PIGMENT SACS',540,470,49);text(c,'ENLARGED SKIN SCHEMATIC',540,1190,30)
def s3(c,t):
 bg(c,t);q=.15+.8*prog(t,0,3);cell(c,540,800,q,220)
 text(c,'MUSCLES PULL THE SAC OPEN',540,350,45,GOLD);text(c,'MORE PIGMENT VISIBLE',540,470,49)
 for k in (-1,1):arrow(c,540+k*140,800,540+k*310,800,GOLD)
 text(c,'SCHEMATIC - NOT TO SCALE',540,1210,29)
def s4(c,t):
 bg(c,t);q=.95-.8*prog(t,0,3);cell(c,540,800,q,220);text(c,'MUSCLES RELAX. SAC SHRINKS.',540,350,43,GOLD);text(c,'LESS PIGMENT VISIBLE',540,470,49);text(c,'SCHEMATIC - NOT TO SCALE',540,1210,29)
def s5(c,t):
 bg(c,t);skin(c,t);text(c,'PATTERNS ACROSS THE SKIN',540,350,45,GOLD);text(c,'BLEND WITH THE BACKGROUND',540,470,44);text(c,'PIGMENT CONTROL IS ONE PART',540,1190,34)
def s6(c,t):
 bg(c,t);text(c,'PAPILLAE CHANGE TEXTURE',540,350,47,GOLD);text(c,'SMOOTH -> BUMPY / SPIKY',540,470,45)
 # A magnified side view of the skin surface, not a complete animal outline.
 c.set_source_rgb(*SAND);c.move_to(100,1120);c.line_to(100,900)
 for x in range(100,981,8):
  q=.25+.75*prog(t,0,3);y=900-q*110*(.5+.5*math.cos((x-100)*math.pi/90))**4;c.line_to(x,y)
 c.line_to(980,1120);c.close_path();c.fill();text(c,'ENLARGED SKIN PROFILE',540,1200,30)
def s7(c,t):
 q=.5+.5*math.sin(t);col=tuple(PURPLE[i]*(1-q)+BROWN[i]*q for i in range(3));sceneocto(c,t,col);text(c,'BUILT-IN SPECIAL EFFECTS?',540,350,47,GOLD)
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
