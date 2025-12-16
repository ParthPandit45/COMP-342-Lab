import glfw, sys
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D

def clip(x1,y1,x2,y2,xm,ym,xM,yM):
	dx,dy=x2-x1,y2-y1
	p=[-dx,dx,-dy,dy]
	q=[x1-xm,xM-x1,y1-ym,yM-y1]
	u1,u2=0,1
	for pi,qi in zip(p,q):
		if pi==0 and qi<0: return False,None
		if pi:
			u=qi/pi
			if pi<0: u1=max(u1,u)
			else:    u2=min(u2,u)
	if u1>u2: return False,None
	return True,(x1+u1*dx,y1+u1*dy,x1+u2*dx,y1+u2*dy)

def line(a,b,c,d,r,g,b2):
	glColor3f(r,g,b2)
	glBegin(GL_LINES)
	glVertex2f(a,b); glVertex2f(c,d)
	glEnd()

def rect(xm,ym,xM,yM):
	glColor3f(0.2, 0.6, 1.0)
	glBegin(GL_LINE_LOOP)
	for p in [(xm,ym),(xM,ym),(xM,yM),(xm,yM)]: glVertex2f(*p)
	glEnd()

if not glfw.init(): sys.exit()
w,h=800,600
win=glfw.create_window(w,h,"Liang–Barsky",None,None)
glfw.make_context_current(win)
gluOrtho2D(0,w,0,h)

xm,ym,xM,yM=200,150,600,450
L0=(100,500,700,100)
ok,C=clip(*L0,xm,ym,xM,yM)

while not glfw.window_should_close(win):
	glClear(GL_COLOR_BUFFER_BIT)
	rect(xm,ym,xM,yM)
	line(*L0,1,0,0)
	if ok: line(*C,0,1,0)
	glfw.swap_buffers(win); glfw.poll_events()

glfw.terminate()
