from OpenGL.GL import *
from OpenGL.GLUT import *
import ctypes
import sys

def getRes():
    
    ctypes.windll.user32.SetProcessDPIAware()

    glutInit(sys.argv)

    width = glutGet(GLUT_SCREEN_WIDTH)
    height = glutGet(GLUT_SCREEN_HEIGHT)

    return width, height

if __name__ == "__main__":
    w, h = getRes()
    print(f"Screen resolution: {w} x {h}")
    