import glfw
from OpenGL.GL import *
import numpy as np
import time

WIN_W, WIN_H = 800, 600

def draw_square(vertices, color=(0.8, 0.3, 1.0)):
    glBegin(GL_QUADS)
    glColor3f(*color)
    for v in vertices.T:
        glVertex2f(v[0], v[1])
    glEnd()

def print_shear_info(title, original, matrix, transformed):
    print("\n==============================")
    print(" " + title)
    print("==============================")

    print("\nInitial Coordinates:")
    for i in range(4):
        print(f"V{i+1}: ({original[0, i]:.3f}, {original[1, i]:.3f})")

    print("\nShearing Matrix:")
    print(matrix)

    print("\nTransformed Coordinates:")
    for i in range(4):
        print(f"V{i+1}: ({transformed[0, i]:.3f}, {transformed[1, i]:.3f})")

def interpolate_vertices(start, end, t):
    return (1 - t) * start + t * end

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIN_W, WIN_H, "Shearing Animation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Original square
    square = np.array([
        [-0.2,  0.2,  0.2, -0.2],
        [ 0.2,  0.2, -0.2, -0.2],
        [ 1.0,  1.0,  1.0,  1.0]
    ], dtype=float)

    # Shear matrices
    shears = {
        "Shear in X-direction": np.array([[1, 0.5, 0],
                                          [0, 1, 0],
                                          [0, 0, 1]], dtype=float),
        "Shear in Y-direction": np.array([[1, 0, 0],
                                          [0.5, 1, 0],
                                          [0, 0, 1]], dtype=float),
        "Shear in Both X and Y": np.array([[1, 0.5, 0],
                                           [0.5, 1, 0],
                                           [0, 0, 1]], dtype=float)
    }

    for title, matrix in shears.items():
        transformed = matrix @ square
        print_shear_info(title, square, matrix, transformed)

        # Animate smooth shearing
        frames = 60
        for i in range(frames + 1):
            t = i / frames
            current_vertices = interpolate_vertices(square, transformed, t)

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            draw_square(current_vertices)
            glfw.swap_buffers(window)
            glfw.poll_events()
            time.sleep(0.01)

        time.sleep(0.5)

    # Keep last sheared square visible for a moment
    time.sleep(1)
    glfw.terminate()

if __name__ == "__main__":
    main()
