import glfw
from OpenGL.GL import *
import time

# Window dimensions
WIN_WIDTH = 900
WIN_HEIGHT = 550

# Store plotted DDA pixels
plot_buffer = []

def generate_dda_points(xs, ys, xe, ye):
    """
    DDA algorithm rewritten:
    Produces (rounded_x, rounded_y, raw_x, raw_y)
    """
    delta_x = xe - xs
    delta_y = ye - ys

    total_steps = int(max(abs(delta_x), abs(delta_y)))
    if total_steps == 0:
        yield xs, ys, xs, ys
        return

    step_x = delta_x / total_steps
    step_y = delta_y / total_steps

    fx, fy = xs, ys

    for index in range(total_steps + 1):
        rx, ry = round(fx), round(fy)

        # ★ Terminal computation output (distinct format)
        print(f"[{index:03d}]  raw=({fx:7.3f},{fy:7.3f})  →  pixel=({rx},{ry})")

        yield rx, ry, fx, fy

        fx += step_x
        fy += step_y


def render_pixels():
    glClear(GL_COLOR_BUFFER_BIT)

    glPointSize(7)
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
        raise RuntimeError("Failed to init GLFW runtime")

    window = glfw.create_window(WIN_WIDTH, WIN_HEIGHT,"DDA Visualizer", None, None)
    
    if not window:
        glfw.terminate()
        raise RuntimeError("Could not allocate window")

    glfw.make_context_current(window)
    setup_projection()

    print("\n### DDA COMPUTATION LOG ###\n")
    print("Idx |     raw floats (x,y)     →    rasterized pixel (x,y)")
    print("--------------------------------------------------------------")

    dda_stream = generate_dda_points(80, 90, 820, 430)

    last_tick = time.time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        now = time.time()
        if now - last_tick >= 0.006:
            try:
                px, py, _, _ = next(dda_stream)
                plot_buffer.append((px, py))
            except StopIteration:
                pass

            last_tick = now
        render_pixels()
        glfw.swap_buffers(window)
    glfw.terminate()
if __name__ == "__main__":
    run()
