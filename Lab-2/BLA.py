import glfw
from OpenGL.GL import *
import time

WIN_WIDTH, WIN_HEIGHT = 900, 550
plot_buffer = []

def generate_bresenham_points(xs, ys, xe, ye):
    dx, dy = abs(xe - xs), abs(ye - ys)
    sx, sy = (1 if xs < xe else -1), (1 if ys < ye else -1)
    x, y = xs, ys
    err = dx - dy

    i = 0
    while True:
        print(f"[{i:03}]  px=({x:4},{y:4})   err={err:5}")
        yield x, y
        if x == xe and y == ye: break

        e2 = err * 2
        if e2 > -dy: err -= dy; x += sx
        if e2 <  dx: err += dx; y += sy
        i += 1


def render_pixels():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(6)
    glBegin(GL_POINTS)
    glColor3f(0.2, 0.8, 1.0)      # distinguish from DDA
    for px, py in plot_buffer:
        glVertex2i(px, py)
    glEnd()


def setup_projection():
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    glOrtho(0, WIN_WIDTH, 0, WIN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    glClearColor(0.07, 0.07, 0.11, 1)


def run():
    global plot_buffer

    if not glfw.init(): raise RuntimeError("GLFW init failed")
    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "Bresenham Visualizer", None, None)
    if not window: glfw.terminate(); raise RuntimeError("Window create failed")

    glfw.make_context_current(window)
    setup_projection()

    print("\n### BRESENHAM LOG ###")
    print("Idx |   px(x,y)   | err")
    print("-----------------------------")

    stream = generate_bresenham_points(80, 90, 820, 430)
    last_t = time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        if time.time() - last_t >= 0.006:
            try:  plot_buffer.append(next(stream))
            except StopIteration: pass
            last_t = time.time()

        render_pixels()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    run()
