import glfw
from OpenGL.GL import *
import numpy as np
import time

WIN_W, WIN_H = 800, 600

def draw_square(vertices):
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.4, 0.0)   # Orange
    for v in vertices.T:
        glVertex2f(v[0], v[1])
    glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIN_W, WIN_H, "2D Scaling Homogeneous", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Initial vertices (homogeneous)
    square_vertices = np.array([
        [-0.2,  0.2,  0.2, -0.2],
        [ 0.2,  0.2, -0.2, -0.2],
        [ 1.0,  1.0,  1.0,  1.0]
    ], dtype=float)

    # Scaling factors (modify if needed)
    sx = 1.002    # Slightly >1 for smooth expansion
    sy = 1.002

    # Scaling matrix
    scaling_matrix = np.array([
        [sx,  0,  0],
        [0,  sy,  0],
        [0,   0,  1]
    ], dtype=float)

    # -----------------------------------------
    # PRINT ONLY INITIAL VALUES
    # -----------------------------------------
    print("\n=== INITIAL COORDINATES (x,y) ===")
    for i in range(4):
        print(f"Vertex {i+1}: ({square_vertices[0, i]:.3f}, {square_vertices[1, i]:.3f})")

    print("\n=== INITIAL SCALING MATRIX ===")
    print(scaling_matrix)
    print("\nAnimation running...\n")
    # -----------------------------------------

    # Animation loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Apply scaling
        square_vertices = np.dot(scaling_matrix, square_vertices)

        # Draw scaled square
        draw_square(square_vertices)

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()


if __name__ == "__main__":
    main()
