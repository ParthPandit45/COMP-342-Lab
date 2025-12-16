import glfw, sys
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D

def inside(p, edge, bounds):
    x, y = p
    xm, ym, xM, yM = bounds
    return (edge == 'left'   and x >= xm) or \
           (edge == 'right'  and x <= xM) or \
           (edge == 'bottom' and y >= ym) or \
           (edge == 'top'    and y <= yM)

def intersect(p1, p2, edge, bounds):
    x1, y1 = p1; x2, y2 = p2
    xm, ym, xM, yM = bounds
    if edge == 'left':   x=xm; y=y1+(y2-y1)*(xm-x1)/(x2-x1)
    if edge == 'right':  x=xM; y=y1+(y2-y1)*(xM-x1)/(x2-x1)
    if edge == 'bottom': y=ym; x=x1+(x2-x1)*(ym-y1)/(y2-y1)
    if edge == 'top':    y=yM; x=x1+(x2-x1)*(yM-y1)/(y2-y1)
    return (x, y)

def clip_polygon(poly, bounds):
    for edge in ['left','right','bottom','top']:
        output=[]; s=poly[-1]
        for e in poly:
            if inside(e, edge, bounds):
                if not inside(s, edge, bounds): output.append(intersect(s,e,edge,bounds))
                output.append(e)
            elif inside(s, edge, bounds): output.append(intersect(s,e,edge,bounds))
            s=e
        poly=output
    return poly

def draw_poly(poly, r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_LINE_LOOP)
    for x,y in poly: glVertex2f(x,y)
    glEnd()

def rect(xm,ym,xM,yM):
    glColor3f(0.8,0.8,0.2)   # Consistent yellowish color
    glBegin(GL_LINE_LOOP)
    for p in [(xm,ym),(xM,ym),(xM,yM),(xm,yM)]: glVertex2f(*p)
    glEnd()

if not glfw.init(): sys.exit()
w,h=800,600; win=glfw.create_window(w,h,"Sutherland-Hodgman",None,None)
glfw.make_context_current(win); gluOrtho2D(0,w,0,h)

xm,ym,xM,yM=200,150,600,450

# Partially inside polygon
poly = [(150,500),(650,500),(550,300),(250,200),(100,100)]
clipped = clip_polygon(poly,(xm,ym,xM,yM))

while not glfw.window_should_close(win):
    glClear(GL_COLOR_BUFFER_BIT)
    rect(xm,ym,xM,yM)        # Rectangle in yellow
    draw_poly(poly,1,0,0)    # Original polygon in red
    if clipped: draw_poly(clipped,0,1,0)  # Clipped polygon in green
    glfw.swap_buffers(win); glfw.poll_events()

glfw.terminate()