import glfw
from OpenGL.GL import *
import time

WIN_WIDTH, WIN_HEIGHT = 900, 550
plot_buffer = []


def generate_dda_points(xs, ys, xe, ye):
    dx, dy = xe - xs, ye - ys
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        yield xs, ys, xs, ys
        return

    sx, sy = dx / steps, dy / steps
    x, y = xs, ys

    for i in range(steps + 1):
        rx, ry = round(x), round(y)

        # Clean padded DDA log
        print(f"[{i:03}]  raw=({x:7.3f},{y:7.3f})  →  pixel=({rx:3},{ry:3})")

        yield rx, ry, x, y
        x += sx
        y += sy


def render_pixels():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(6)

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.55, 0.15)

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
        raise RuntimeError("Failed to initialize GLFW")

    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT, "DDA Visualizer", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create window")

    glfw.make_context_current(window)
    setup_projection()

    print("\n### DDA COMPUTATION LOG ###")
    print("Idx |      raw floats      →    pixel")
    print("-------------------------------------------")

    stream = generate_dda_points(80, 90, 820, 430)
    last = time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        if time.time() - last >= 0.006:
            try:
                px, py, _, _ = next(stream)
                plot_buffer.append((px, py))
            except StopIteration:
                pass
            last = time.time()

        render_pixels()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    run()
