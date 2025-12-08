import glfw, time
from OpenGL.GL import *
import numpy as np

WIN_W, WIN_H = 800, 600

def draw_square(v):
    glBegin(GL_QUADS); glColor3f(0,0.5,1)
    for p in v.T: glVertex2f(p[0],p[1])
    glEnd()

def main():
    if not glfw.init(): return
    win=glfw.create_window(WIN_W,WIN_H,"2D Rotation Homogeneous",None,None)
    if not win: glfw.terminate(); return
    glfw.make_context_current(win)
    glViewport(0,0,WIN_W,WIN_H); glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(-1,1,-1,1,-1,1); glMatrixMode(GL_MODELVIEW)

    square = np.array([[-0.2,0.2,0.2,-0.2],[0.2,0.2,-0.2,-0.2],[1,1,1,1]],float)
    theta = np.radians(1)
    R = np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])

    print("\n=== INITIAL COORDINATES ===")
    for i in range(4): print(f"V{i+1}: ({square[0,i]:.3f},{square[1,i]:.3f})")
    print("\n=== ROTATION MATRIX ===\n", R,"\nAnimation running...\n")

    while not glfw.window_should_close(win):
        glClear(GL_COLOR_BUFFER_BIT); glLoadIdentity()
        square = R @ square
        draw_square(square)
        glfw.swap_buffers(win); glfw.poll_events(); time.sleep(0.01)

    glfw.terminate()

if __name__=="__main__": main()
