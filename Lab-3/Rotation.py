import glfw
from OpenGL.GL import *
import numpy as np
import time

WIN_W, WIN_H = 800, 600

def draw_square(vertices):
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 1.0)
    for v in vertices.T:
        glVertex2f(v[0], v[1])
    glEnd()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIN_W, WIN_H, "2D Rotation Homogeneous", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Initial vertices in homogeneous coordinates
    square_vertices = np.array([
        [-0.2,  0.2,  0.2, -0.2],
        [ 0.2,  0.2, -0.2, -0.2],
        [ 1.0,  1.0,  1.0,  1.0]
    ], dtype=float)

    # 1 degree rotation
    theta = np.radians(1)
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)

    # -----------------------------------------
    # PRINT ONLY INITIAL VALUES (once)
    # -----------------------------------------
    print("\n=== INITIAL COORDINATES (x,y) ===")
    for i in range(4):
        print(f"Vertex {i+1}: ({square_vertices[0, i]:.3f}, {square_vertices[1, i]:.3f})")

    print("\n=== INITIAL TRANSFORMATION MATRIX (Rotation) ===")
    print(rotation_matrix)
    print("\nAnimation running...\n")
    # -----------------------------------------

    # Animation loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Rotate square every frame
        square_vertices = np.dot(rotation_matrix, square_vertices)

        # Draw updated square
        draw_square(square_vertices)

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()


if __name__ == "__main__":
    main()
