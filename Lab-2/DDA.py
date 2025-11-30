import glfw
from OpenGL.GL import *
import time

WIN_WIDTH, WIN_HEIGHT = 900, 550
plot_buffer = []


def dda_line(x0, y0, x1, y1):
    """DDA line algorithm supporting all slopes."""
    dx = x1 - x0
    dy = y1 - y0

    steps = int(max(abs(dx), abs(dy)))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x0
    y = y0

    for i in range(steps + 1):
        print(f"[{i:03}] pixel=({round(x):3},{round(y):3})  x={x:.2f} y={y:.2f}")
        yield round(x), round(y)
        x += x_inc
        y += y_inc


def render_pixels():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(6)

    glBegin(GL_POINTS)
    glColor3f(0.3, 0.8, 1.0)  # Cyan-ish for DDA
    for px, py in plot_buffer:
        glVertex2i(px, py)
    glEnd()


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIN_WIDTH, 0, WIN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.08, 0.08, 0.10, 1)


def run():
    global plot_buffer

    if not glfw.init():
        raise RuntimeError("GLFW init failed")
    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "DDA Line", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Window creation failed")

    glfw.make_context_current(window)
    setup_projection()

    print("\n### DDA LINE LOG ###")
    print("Idx | pixel (x,y) | float (x,y) values")

    stream = dda_line(80, 90, 820, 430)
    last = time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        if time.time() - last >= 0.004:  # smooth animation
            try:
                px, py = next(stream)
                plot_buffer.append((px, py))
            except StopIteration:
                pass
            last = time.time()

        render_pixels()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    run()
