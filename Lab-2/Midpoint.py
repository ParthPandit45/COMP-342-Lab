import glfw
from OpenGL.GL import *
import time

WIN_W, WIN_H = 900, 550
buf = []


def mid_circle(cx, cy, r):
    x, y, d, i = 0, r, 1 - r, 0

    while x <= y:
        pts = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]

        print(f"[{i:03}] x={x:3} y={y:3} d={d:4} → {pts[0]}")
        i += 1

        for p in pts:
            yield p

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


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
    win = glfw.create_window(WIN_W, WIN_H, "Midpoint Circle", None, None)
    if not win:
        glfw.terminate()
        raise RuntimeError("Window fail")

    glfw.make_context_current(win)
    setup()

    print("\n### MIDPOINT CIRCLE LOG ###\nIdx | x  y  d → point\n--------------------------")
    gen = mid_circle(450, 275, 200)

    last = time.time()

    while not glfw.window_should_close(win):
        glfw.poll_events()

        if time.time() - last >= 0.001:   # 🔥 faster animation
            try: buf.append(next(gen))
            except StopIteration: pass
            last = time.time()

        render()
        glfw.swap_buffers(win)

    glfw.terminate()


if __name__ == "__main__":
    run()
