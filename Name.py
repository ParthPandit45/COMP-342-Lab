from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1200, 0, 600)  # Wide canvas for spacing

def draw_rect(x, y, width, height, color):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_name():
    glClear(GL_COLOR_BUFFER_BIT)

    # Letter P (Blue)
    draw_rect(50, 100, 40, 400, (0.2, 0.5, 0.9))     # Vertical spine
    draw_rect(90, 460, 100, 40, (0.2, 0.5, 0.9))     # Top horizontal
    draw_rect(90, 300, 100, 40, (0.2, 0.5, 0.9))     # Middle horizontal
    draw_rect(190, 340, 40, 120, (0.2, 0.5, 0.9))    # Right vertical  

   # Letter A (Red)
    draw_rect(250, 100, 40, 360, (0.9, 0.2, 0.2))    # Left vertical bar
    draw_rect(370, 100, 40, 360, (0.9, 0.2, 0.2))    # Right vertical bar
    draw_rect(290, 300, 80, 40, (0.9, 0.2, 0.2))     # Middle horizontal bar
    draw_rect(290, 460, 80, 40, (0.9, 0.2, 0.2))    # Top horizontal bar 

    # Letter R (Green)
    draw_rect(430, 100, 40, 400, (0.2, 0.8, 0.2))    # Left vertical bar
    draw_rect(470, 460, 100, 40, (0.2, 0.8, 0.2))    # Top horizontal bar
    draw_rect(570, 340, 40, 120, (0.2, 0.8, 0.2))   # Right vertical bar
    draw_rect(470, 300, 100, 40, (0.2, 0.8, 0.2))    # Middle horizontal bar
    draw_rect(570, 100, 40, 200, (0.2, 0.8, 0.2))    # Diagonal leg

    # Letter T (Purple)
    draw_rect(630, 460, 160, 40, (0.6, 0.2, 0.8))    # Top horizontal bar
    draw_rect(690, 100, 40, 400, (0.6, 0.2, 0.8))    # Vertical bar

    # Letter H (Orange)
    draw_rect(810, 100, 40, 400, (0.9, 0.5, 0.2))    # Left vertical bar
    draw_rect(930, 100, 40, 400, (0.9, 0.5, 0.2))    # Right vertical bar
    draw_rect(850, 300, 80, 40, (0.9, 0.5, 0.2))     # Middle horizontal bar    

    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1200, 600)
    # glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Parth but with Rectangles")
    init()
    glutDisplayFunc(draw_name)
    glutMainLoop()

if __name__ == "__main__":
    main()