import glfw, time
from OpenGL.GL import *
import numpy as np

WIN_W, WIN_H = 800, 600

def draw_square(v): 
    glBegin(GL_QUADS)
    glColor3f(0,0.5,1)
    for p in v.T: glVertex2f(p[0], p[1])
    glEnd()

def main():
    if not glfw.init(): return
    win = glfw.create_window(WIN_W, WIN_H, "Composite Transform", None, None)
    if not win: glfw.terminate(); return
    glfw.make_context_current(win)
    glViewport(0,0,WIN_W,WIN_H); glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(-1,1,-1,1,-1,1); glMatrixMode(GL_MODELVIEW)

    square = np.array([[-0.2,0.2,0.2,-0.2],[0.2,0.2,-0.2,-0.2],[1,1,1,1]],float)
    S = np.array([[1.5,0,0],[0,0.7,0],[0,0,1]])
    R = np.array([[np.cos(np.radians(30)),-np.sin(np.radians(30)),0],[np.sin(np.radians(30)),np.cos(np.radians(30)),0],[0,0,1]])
    Sh = np.array([[1,0.5,0],[0.3,1,0],[0,0,1]])
    T = np.array([[1,0,0.3],[0,1,0.2],[0,0,1]])
    M = T @ R @ S @ Sh
    transformed = M @ square

    print("\nInitial coords:\n", square[:2].T)
    print("\nComposite matrix:\n", M)
    print("\nTransformed coords:\n", transformed[:2].T)

    for t in np.linspace(0,1,80):
        glClear(GL_COLOR_BUFFER_BIT); glLoadIdentity()
        draw_square((1-t)*square + t*transformed)
        glfw.swap_buffers(win); glfw.poll_events(); time.sleep(0.01)
    time.sleep(1)
    glfw.terminate()

if __name__=="__main__": main()
