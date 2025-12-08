import glfw
from OpenGL.GL import *
import numpy as np
import time

# Window size
WIN_W, WIN_H = 800, 600

def draw_square():
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)  # Green color
    glVertex2f(-0.2, 0.2)
    glVertex2f(0.2, 0.2)
    glVertex2f(0.2, -0.2)
    glVertex2f(-0.2, -0.2)
    glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIN_W, WIN_H, "2D Translation Homogeneous", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Starting position in homogeneous coordinates
    start_pos = np.array([[ -0.8 ],
                          [ -0.8 ],
                          [ 1.0 ]], dtype=float)

    # Translation factor as a homogeneous matrix
    translation_factor = np.array([[ 1, 0, 0.002 ],
                                   [ 0, 1, 0.0015 ],
                                   [ 0, 0, 1 ]], dtype=float)

    print("Starting Position (homogeneous):\n", start_pos)
    print("Translation Factor (homogeneous matrix):\n", translation_factor)

    # Current position
    current_pos = start_pos.copy()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Apply translation using the homogeneous matrix
        current_pos = np.dot(translation_factor, current_pos)

        # Draw square at current position
        glTranslatef(current_pos[0, 0], current_pos[1, 0], 0.0)
        draw_square()

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()

if __name__ == "__main__":
    main()
