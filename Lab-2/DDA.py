from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, math

# DDA.py
# Requires: PyOpenGL, PyOpenGL_accelerate (optional)
# Run: python DDA.py


# Window
WIN_W, WIN_H = 900, 500

# DDA endpoints (left panel coordinates)
X0, Y0 = 60.0, 60.0
X1, Y1 = 420.0, 380.0

# Animation control
points = []  # list of tuples (x, y, rx, ry) where rx,ry are rounded pixel coords
current_step = 0
delay_ms = 50  # animation delay per step

def compute_dda(x0, y0, x1, y1):
    pts = []
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        rx, ry = int(round(x0)), int(round(y0))
        pts.append((x0, y0, rx, ry))
        return pts
    xi = dx / steps
    yi = dy / steps
    x, y = x0, y0
    for i in range(steps + 1):
        rx, ry = int(round(x)), int(round(y))
        pts.append((x, y, rx, ry))
        x += xi
        y += yi
    return pts

def draw_text(x, y, text, color=(1,1,1)):
    glColor3f(*color)
    # Use glWindowPos2i for predictable placement in pixel coords
    try:
        glWindowPos2i(int(x), int(y))
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    except Exception:
        # Fallback to raster pos (older contexts)
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def draw_left_panel():
    # Draw axes/background
    left_w = WIN_W * 0.5
    glColor3f(0.06, 0.06, 0.06)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(left_w, 0)
    glVertex2f(left_w, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    # Draw grid lines for reference
    glColor3f(0.12, 0.12, 0.12)
    glLineWidth(1)
    glBegin(GL_LINES)
    step = 20
    for gx in range(0, int(left_w)+1, step):
        glVertex2f(gx, 0); glVertex2f(gx, WIN_H)
    for gy in range(0, WIN_H+1, step):
        glVertex2f(0, gy); glVertex2f(left_w, gy)
    glEnd()

    # Draw the ideal continuous line (for reference)
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(X0, Y0)
    glVertex2f(X1, Y1)
    glEnd()

    # Draw computed pixels up to current_step
    glPointSize(6)
    glBegin(GL_POINTS)
    for i, (x, y, rx, ry) in enumerate(points[:current_step]):
        # color: earlier points bluish, current point yellow
        if i == current_step - 1:
            glColor3f(1.0, 0.85, 0.2)
        else:
            t = i / max(1, len(points)-1)
            glColor3f(0.2 + 0.6*t, 0.4, 1.0 - 0.6*t)
        glVertex2f(x, y)
    glEnd()

    # Draw start/end markers
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 0.0)  # start green
    glVertex2f(X0, Y0)
    glColor3f(1.0, 0.0, 0.0)  # end red
    glVertex2f(X1, Y1)
    glEnd()

    # Labels
    draw_text(8, WIN_H - 18, "DDA Animation (left):")
    draw_text(8, WIN_H - 36, f"Start: ({X0:.1f}, {Y0:.1f})  End: ({X1:.1f}, {Y1:.1f})")
    draw_text(8, WIN_H - 54, "Points shown as they are computed step-by-step.")

def draw_right_panel():
    # Right panel background
    x0 = int(WIN_W * 0.5)
    glColor3f(0.03, 0.03, 0.03)
    glBegin(GL_QUADS)
    glVertex2f(x0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(x0, WIN_H)
    glEnd()

    # Title
    draw_text(x0 + 12, WIN_H - 22, "DDA Computation (right):", (0.9, 0.9, 0.9))
    # Column headers
    draw_text(x0 + 12, WIN_H - 44, "i    x (float)      y (float)     round(x)  round(y)", (0.8, 0.8, 0.8))

    # Print the computations; most recent at top
    max_lines = 18
    start_index = 0
    total = len(points)
    # show first lines downwards; if many points, scroll to show current
    if total > max_lines:
        start_index = max(0, current_step - max_lines)
    y = WIN_H - 66
    for i in range(start_index, min(total, start_index + max_lines)):
        x, y_f, rx, ry = points[i][0], points[i][1], points[i][2], points[i][3]
        txt = f"{i:3d}  {x:10.4f}   {y_f:10.4f}     {rx:6d}   {ry:6d}"
        color = (0.9, 0.9, 0.9)
        if i == current_step - 1:
            color = (1.0, 0.9, 0.3)
        draw_text(WIN_W * 0.5 + 12, y - (i - start_index) * 18, txt, color)

    # Controls/help
    draw_text(WIN_W * 0.5 + 12, 18, "Controls: R - restart, Esc/Q - quit", (0.7, 0.7, 0.7))

def display():
    glClearColor(0.02, 0.02, 0.02, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # 0..WIN_W, 0..WIN_H coordinate system (bottom-left origin)
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_left_panel()
    draw_right_panel()

    glutSwapBuffers()

def timer(fps=delay_ms):
    global current_step
    if current_step < len(points):
        current_step += 1
    glutTimerFunc(fps, lambda x=0: timer(fps), 0)
    glutPostRedisplay()

def keyboard(key, x, y):
    global current_step, points
    k = key.decode("utf-8")
    if k in ('\x1b', 'q', 'Q'):  # ESC or q
        sys.exit(0)
    if k in ('r', 'R'):
        current_step = 0

def reshape(w, h):
    global WIN_W, WIN_H
    WIN_W, WIN_H = w, h
    glViewport(0, 0, w, h)

def main():
    global points, current_step
    points = compute_dda(X0, Y0, X1, Y1)
    current_step = 0

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"DDA Line Drawing - Animation and Computation")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    # start timer-based animation
    glutTimerFunc(delay_ms, lambda x=0: timer(delay_ms), 0)

    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

    glutMainLoop()

if __name__ == "__main__":
    main()