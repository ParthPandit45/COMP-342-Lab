import glfw
from OpenGL.GL import *
import numpy as np
import time

WIN_W, WIN_H = 800, 600

def draw_square(vertices, color=(0.0, 1.0, 0.3)):
    """Draw square using column-wise homogeneous vertices"""
    glBegin(GL_QUADS)
    glColor3f(*color)
    for v in vertices.T:
        glVertex2f(v[0], v[1])
    glEnd()

def print_reflection_info(title, original, matrix, transformed):
    print("\n==============================")
    print(" " + title)
    print("==============================")

    print("\nInitial Coordinates:")
    for i in range(4):
        print(f"V{i+1}: ({original[0, i]:.3f}, {original[1, i]:.3f})")

    print("\nReflection Matrix:")
    print(matrix)

    print("\nTransformed Coordinates:")
    for i in range(4):
        print(f"V{i+1}: ({transformed[0, i]:.3f}, {transformed[1, i]:.3f})")

def interpolate_vertices(start, end, t):
    """Linear interpolation of vertices for smooth animation"""
    return (1 - t) * start + t * end

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIN_W, WIN_H, "Reflection Animations", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # Initial square in homogeneous coordinates
    square = np.array([
        [-0.2,  0.2,  0.2, -0.2],
        [ 0.2,  0.2, -0.2, -0.2],
        [ 1.0,  1.0,  1.0,  1.0]
    ], dtype=float)

    # Reflection matrices
    reflections = {
        "Reflection About X-Axis": np.array([[1, 0, 0],
                                             [0,-1, 0],
                                             [0, 0, 1]], dtype=float),
        "Reflection About Y-Axis": np.array([[-1,0,0],
                                             [ 0,1,0],
                                             [ 0,0,1]], dtype=float),
        "Reflection About Origin": np.array([[-1,0,0],
                                             [ 0,-1,0],
                                             [ 0,0,1]], dtype=float)
    }

    # Loop through each reflection
    for title, matrix in reflections.items():
        transformed = matrix @ square
        print_reflection_info(title, square, matrix, transformed)

        # Animate mirror-drop (t: 0 -> 1)
        frames = 60
        for i in range(frames + 1):
            t = i / frames
            current_vertices = interpolate_vertices(square, transformed, t)

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            draw_square(current_vertices)
            glfw.swap_buffers(window)
            glfw.poll_events()
            time.sleep(0.01)  # adjust speed

        # Pause briefly after each reflection
        time.sleep(0.5)

    # Keep the last reflected square visible for a while
    time.sleep(1)
    glfw.terminate()

if __name__ == "__main__":
    main()
