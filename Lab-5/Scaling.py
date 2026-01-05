import glfw, time
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

WIN_W, WIN_H = 800, 600

def draw_cube():
    vertices = [
        (-0.2, -0.2,  0.2), ( 0.2, -0.2,  0.2), ( 0.2,  0.2,  0.2), (-0.2,  0.2,  0.2),
        (-0.2, -0.2, -0.2), (-0.2,  0.2, -0.2), ( 0.2,  0.2, -0.2), ( 0.2, -0.2, -0.2)
    ]
    faces = [
        (0,1,2,3), (4,5,6,7), (4,0,3,5), (7,6,2,1), (5,3,2,6), (4,7,1,0)
    ]
    colors = [(0,1,0), (1,0,0), (0,0,1), (1,1,0), (0,1,1), (1,0,1)]
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3f(*colors[i])
        for v in face:
            glVertex3f(*vertices[v])
    glEnd()

def main():
    if not glfw.init(): return
    win = glfw.create_window(WIN_W, WIN_H, "3D Scaling Homogeneous", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIN_W/WIN_H, 0.1, 10)
    glMatrixMode(GL_MODELVIEW)

    pos = np.array([[0.0], [0.0], [-3.0], [1.0]], float)
    scale_factor = 1.0

    print("Starting Position:\n", pos)

    while not glfw.window_should_close(win):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLoadIdentity()
        gluLookAt(0,0,0, 0,0,-3, 0,1,0)
        scale_factor += 0.005
        glTranslatef(pos[0,0], pos[1,0], pos[2,0])
        glScalef(scale_factor, scale_factor, scale_factor)
        draw_cube()
        glfw.swap_buffers(win)
        glfw.poll_events()
        time.sleep(0.01)
    glfw.terminate()

if __name__ == "__main__":
    main()