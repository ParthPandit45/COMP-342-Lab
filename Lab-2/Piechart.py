import glfw
from OpenGL.GL import *
import math
import time
import random

WIN_W, WIN_H = 800, 600
plot_buffer = []

# Unequal random segments
data = [random.randint(5, 50) for _ in range(6)]
total = sum(data)
angles = [360 * v / total for v in data]  # convert to degrees

# Flashy colors
colors = [
    (1.0, 0.1, 0.2),  # red
    (0.1, 1.0, 0.2),  # green
    (0.2, 0.3, 1.0),  # blue
    (1.0, 0.8, 0.1),  # yellow
    (1.0, 0.2, 1.0),  # magenta
    (0.0, 1.0, 1.0)   # cyan
]


def generate_slice(cx, cy, r, start_angle, end_angle, steps=100):
    """Yield points to animate a pie slice."""
    points = [(cx, cy)]
    for i in range(steps + 1):
        angle = math.radians(start_angle + (end_angle - start_angle) * i / steps)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((round(x), round(y)))
        yield points.copy()


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    for idx, slice_points in enumerate(plot_buffer):
        glColor3f(*colors[idx % len(colors)])
        glBegin(GL_TRIANGLE_FAN)
        for px, py in slice_points:
            glVertex2i(px, py)
        glEnd()


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIN_W, 0, WIN_H, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.08, 0.08, 0.08, 1)


def run():
    global plot_buffer
    if not glfw.init(): raise RuntimeError("GLFW init failed")
    win = glfw.create_window(WIN_W, WIN_H, "Flashy Pie Chart", None, None)
    if not win: glfw.terminate(); raise RuntimeError("Window fail")
    glfw.make_context_current(win)
    setup_projection()

    print("### FLASHY PIE CHART LOG ###")
    print("Slice | Start Angle | End Angle | Data Value")

    # Slice generators
    slice_gens = []
    start = 0
    for idx, a in enumerate(angles):
        end = start + a
        print(f"{idx:3}   | {start:6.2f}     | {end:6.2f}    | {data[idx]}")
        slice_gens.append(generate_slice(WIN_W//2, WIN_H//2, 200, start, end))
        start = end

    plot_buffer = [[] for _ in slice_gens]
    curr_idx = 0
    last_time = time.time()

    while not glfw.window_should_close(win):
        glfw.poll_events()

        if time.time() - last_time >= 0.002:  # faster animation
            if curr_idx < len(slice_gens):
                try:
                    plot_buffer[curr_idx] = next(slice_gens[curr_idx])
                except StopIteration:
                    curr_idx += 1
            last_time = time.time()

        render()
        glfw.swap_buffers(win)

    glfw.terminate()


if __name__ == "__main__":
    run()
