import glfw, time
from OpenGL.GL import *
from OpenGL.GLU import *

WIN_W, WIN_H = 800, 600

def draw_cube():
    # Define cube vertices (small size for clarity)
    vertices = [
        (-0.2, -0.2,  0.2), ( 0.2, -0.2,  0.2), ( 0.2,  0.2,  0.2), (-0.2,  0.2,  0.2),
        (-0.2, -0.2, -0.2), (-0.2,  0.2, -0.2), ( 0.2,  0.2, -0.2), ( 0.2, -0.2, -0.2)
    ]
    # Define faces
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
    win = glfw.create_window(WIN_W, WIN_H, "Animated Perspective Projection with Cube", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glViewport(0, 0, WIN_W, WIN_H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Perspective projection: makes distant objects appear smaller
    gluPerspective(45, WIN_W/WIN_H, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)

    z_pos = -2.0  # Starting position
    direction = -0.01  # Movement speed and direction

    while not glfw.window_should_close(win):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLoadIdentity()
        gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)

        # Animate the cube moving back and forth
        glPushMatrix()
        glTranslatef(0, 0, z_pos)
        draw_cube()
        glPopMatrix()

        # Update position for animation
        z_pos += direction
        if z_pos <= -6.0 or z_pos >= -2.0:
            direction = -direction  # Reverse direction at boundaries

        # This animation demonstrates perspective projection:
        # - As the cube moves farther (more negative z), it appears smaller
        # - When closer, it appears larger
        # - This shows how perspective makes distant objects look reduced in size

        glfw.swap_buffers(win)
        glfw.poll_events()
        time.sleep(0.02)  # Control animation speed
    glfw.terminate()

if __name__ == "__main__":
    main()
