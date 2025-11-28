import glfw
from OpenGL.GL import *
import time
import random

WIN_W, WIN_H = 900, 550
plot_buffer = []


def dda_line(x0, y0, x1, y1):
    """Generates points on a line using DDA."""
    dx, dy = x1 - x0, y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        yield round(x0), round(y0)
        return

    sx, sy = dx / steps, dy / steps
    x, y = x0, y0

    for i in range(steps + 1):
        rx, ry = round(x), round(y)
        print(f"[{i:03}] ({x:7.3f},{y:7.3f}) → ({rx},{ry})")
        yield rx, ry
        x += sx
        y += sy


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5)

    # Draw points
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.5, 0.2)
    for px, py in plot_buffer:
        glVertex2i(px, py)
    glEnd()

    # Draw connecting lines
    glBegin(GL_LINE_STRIP)
    glColor3f(0.2, 0.9, 1.0)
    for px, py in plot_buffer:
        glVertex2i(px, py)
    glEnd()


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIN_W, 0, WIN_H, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.08, 0.08, 0.10, 1)


def run():
    global plot_buffer

    if not glfw.init():
        raise RuntimeError("GLFW init fail")
    win = glfw.create_window(WIN_W, WIN_H, "Random Line Graph (DDA)", None, None)
    if not win:
        glfw.terminate()
        raise RuntimeError("Window fail")

    glfw.make_context_current(win)
    setup_projection()

    # Generate random dataset
    n_points = 15
    margin = 50
    x_spacing = (WIN_W - 2*margin) / (n_points - 1)
    data = [random.randint(100, WIN_H - 100) for _ in range(n_points)]

    print("\n### DDA LINE GRAPH LOG ###")
    print("Idx | (x0,y0) → (x1,y1) | points generated")

    # Create generator for all line segments
    line_gens = []
    for i in range(n_points - 1):
        x0, y0 = margin + i * x_spacing, data[i]
        x1, y1 = margin + (i + 1) * x_spacing, data[i + 1]
        gen = dda_line(x0, y0, x1, y1)
        line_gens.append(gen)

    last_time = time.time()
    curr_gen_idx = 0

    while not glfw.window_should_close(win):
        glfw.poll_events()

        if time.time() - last_time >= 0.002:  # faster animation
            if curr_gen_idx < len(line_gens):
                try:
                    plot_buffer.append(next(line_gens[curr_gen_idx]))
                except StopIteration:
                    curr_gen_idx += 1
            last_time = time.time()

        render()
        glfw.swap_buffers(win)

    glfw.terminate()


if __name__ == "__main__":
    run()
