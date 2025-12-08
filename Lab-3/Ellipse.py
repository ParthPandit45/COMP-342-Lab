import glfw
from OpenGL.GL import *
import time

WIN_W, WIN_H = 900, 550
buf = []

def mid_ellipse(cx, cy, rx, ry):
    """Midpoint Ellipse Algorithm (generator version, no prints)"""
    x, y = 0, ry
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    d1 = ry*ry - rx*rx*ry + 0.25*rx*rx

    # Region 1
    while dx < dy:
        pts = [(cx + x, cy + y), (cx - x, cy + y),
               (cx + x, cy - y), (cx - x, cy - y)]
        for p in pts: yield p
        if d1 < 0:
            x += 1
            dx += 2*ry*ry
            d1 += dx + ry*ry
        else:
            x += 1; y -= 1
            dx += 2*ry*ry; dy -= 2*rx*rx
            d1 += dx - dy + ry*ry

    # Region 2
    d2 = ry*ry*(x+0.5)**2 + rx*rx*(y-1)**2 - rx*rx*ry*ry
    while y >= 0:
        pts = [(cx + x, cy + y), (cx - x, cy + y),
               (cx + x, cy - y), (cx - x, cy - y)]
        for p in pts: yield p
        if d2 > 0:
            y -= 1
            dy -= 2*rx*rx
            d2 += rx*rx - dy
        else:
            y -= 1; x += 1
            dx += 2*ry*ry; dy -= 2*rx*rx
            d2 += dx - dy + rx*rx

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5)
    glColor3f(0.1, 1.0, 0.4)
    glBegin(GL_POINTS)
    for x, y in buf:
        glVertex2i(x, y)
    glEnd()

def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIN_W, 0, WIN_H, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.08, 0.08, 0.10, 1)

def run():
    if not glfw.init(): raise RuntimeError("GLFW init fail")
    win = glfw.create_window(WIN_W, WIN_H, "Midpoint Ellipse", None, None)
    if not win: glfw.terminate(); raise RuntimeError("Window fail")
    glfw.make_context_current(win)
    setup()

    gen = mid_ellipse(WIN_W//2, WIN_H//2, 300, 150)
    last = time.time()

    while not glfw.window_should_close(win):
        glfw.poll_events()
        if time.time() - last >= 0.00001:
            try: buf.append(next(gen))
            except StopIteration: pass
            last = time.time()
        render()
        glfw.swap_buffers(win)
    glfw.terminate()

if __name__ == "__main__":
    run()
