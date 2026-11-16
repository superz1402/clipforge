# Original geometric-optics diagrams and landscape animation. Illustrative, not an angular scale.
import cairo,math,sys,subprocess,random
from birds_anim import *
import birds_anim as B
COL=[(1,.27,.27),(1,.6,.2),(1,.9,.3),(.3,.85,.4),(.3,.6,1),(.45,.3,.8),(.7,.35,.9)]
def bg(c):sky(c,(.08,.2,.42),(.35,.62,.75))
def arc(c,cx,cy,r,full=False,reverse=False,alpha=1):
 for i in range(7):
  co=COL[6-i if reverse else i];c.set_source_rgba(*co,alpha);c.set_line_width(18);c.arc(cx,cy,r-i*18,math.pi,3*math.pi if full else 2*math.pi);c.stroke()
def landscape(c,t):
 bg(c);hills(c,(.07,.25,.17))
 # rain on the right, sun to the left
 c.set_source_rgb(1,.9,.55);c.arc(130,650,65,0,6.3);c.fill()
 for i in range(25):
  x=700+(i*59)%340;y=450+(i*83+t*120)%750;c.set_source_rgba(.7,.88,1,.6);c.set_line_width(4);c.move_to(x,y);c.line_to(x-10,y+25);c.stroke()
def line(c,p,q,col=(1,1,1),w=8):c.set_source_rgb(*col);c.set_line_width(w);c.move_to(*p);c.line_to(*q);c.stroke()
def norm(v):
 l=math.hypot(*v);return(v[0]/l,v[1]/l)
def refract(d,n,ratio):
 # n is the boundary normal pointing toward the incident medium.
 co=-(d[0]*n[0]+d[1]*n[1]);k=1-ratio*ratio*(1-co*co)
 return norm((ratio*d[0]+(ratio*co-math.sqrt(k))*n[0],ratio*d[1]+(ratio*co-math.sqrt(k))*n[1]))
def trace(ri):
 p=(-math.sqrt(1-.86**2),-.86);d=refract((1,0),p,1/ri);u=-2*(p[0]*d[0]+p[1]*d[1]);q=(p[0]+u*d[0],p[1]+u*d[1]);dot=d[0]*q[0]+d[1]*q[1];d=(d[0]-2*dot*q[0],d[1]-2*dot*q[1]);u=-2*(q[0]*d[0]+q[1]*d[1]);z=(q[0]+u*d[0],q[1]+u*d[1]);v=refract(d,(-z[0],-z[1]),ri);return p,q,z,(z[0]+.6*v[0],z[1]+.6*v[1])
def drop(c,t,exit=True):
 cx,cy,r=650,800,250;c.set_source_rgba(.4,.75,1,.3);c.arc(cx,cy,r,0,6.3);c.fill();c.set_source_rgba(.7,.92,1,.9);c.set_line_width(6);c.arc(cx,cy,r,0,6.3);c.stroke()
 cv=lambda p:(cx+r*p[0],cy+r*p[1]);p,q,z,v=trace(1.337);line(c,(30,cy+r*p[1]),cv(p),(1,.97,.8),15);line(c,cv(p),cv(q),(1,.97,.8),9)
 if exit:
  for col,ri in [(COL[0],1.331),(COL[3],1.337),(COL[6],1.343)]:
   p,q,z,v=trace(ri);line(c,cv(q),cv(z),col,6);line(c,cv(z),cv(v),col,7)
 # traveling pulse highlights entry ray
 x=40+(cv(p)[0]-40)*((t*.5)%1);c.set_source_rgb(1,1,.8);c.arc(x,cy+r*p[1],11,0,6.3);c.fill()
def person(c,x,y):
 c.set_source_rgb(.07,.1,.18);c.arc(x,y-90,35,0,6.3);c.fill();line(c,(x,y-50),(x,y+70),(.07,.1,.18),24);line(c,(x,y+70),(x-50,y+160),(.07,.1,.18),20);line(c,(x,y+70),(x+50,y+160),(.07,.1,.18),20)
def s1(c,t):landscape(c,t);arc(c,540,1150,420);text(c,'SUNLIGHT + WATER DROPS',540,510,46)
def s2(c,t):
 bg(c);drop(c,t,False);text(c,'LIGHT BENDS AS IT ENTERS',540,350,47);text(c,'REFRACTION',540,470,54,(1,.9,.5));text(c,'DIAGRAM - NOT TO SCALE',540,1190,29)
def s3(c,t):
 bg(c);drop(c,t,True);text(c,'BEND -> REFLECT -> BEND',540,350,47);text(c,'COLORS SEPARATE',540,470,52,(1,.9,.5));text(c,'DIAGRAM - NOT TO SCALE',540,1190,29)
def s4(c,t):
 landscape(c,t);person(c,420,950);arc(c,870,950,190);text(c,'SUN BEHIND YOU',300,330,42,(1,.9,.5));text(c,'DROPS AHEAD',800,440,42);line(c,(130,650),(400,850),(1,.9,.5),8)
 text(c,'THE VIEWING ANGLE MATTERS',540,1200,43)
def s5(c,t):
 bg(c);arc(c,540,850,330,True);text(c,'THE FULL RAINBOW: A CIRCLE',540,350,44)
 # fade a ground mask away, revealing the otherwise hidden lower part of the ring.
 al=1-prog(t,1,4);c.set_source_rgba(.06,.22,.15,al);c.rectangle(0,850,1080,1070);c.fill();text(c,'GROUND HIDES PART OF IT',540,490,41);text(c,'AIRBORNE VIEW CAN REVEAL IT',540,1220,36)
def s6(c,t):
 bg(c);arc(c,540,1150,290);arc(c,540,1150,460,False,True,.5);text(c,'TWO INTERNAL REFLECTIONS',540,350,44);text(c,'FAINTER. COLORS REVERSED.',540,490,44)
def s7(c,t):
 bg(c);arc(c,540,850,330,True);text(c,'WHERE DOES A CIRCLE END?',540,350,45,(1,.9,.5));c.set_source_rgb(1,1,1);c.set_line_width(7);a=t*.45;c.arc(540+330*math.cos(a),850+330*math.sin(a),26,0,6.3);c.stroke()
SC=[s1,s2,s3,s4,s5,s6,s7]
def lframe(c,t):
 i=max(k for k in range(len(SC))if t>=ST[k]-1e-6);SC[i](c,t-ST[i])
B.frame=lframe
if __name__=='__main__':
 out=sys.argv[1]if len(sys.argv)>1 else 'anim.mp4';surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H);c=cairo.Context(surf)
 p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
 for i in range(int(T_END*FPS)+3):lframe(c,i/FPS);p.stdin.write(bytes(surf.get_data()))
 p.stdin.close();sys.exit(p.wait())
