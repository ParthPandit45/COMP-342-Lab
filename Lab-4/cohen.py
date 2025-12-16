import sys
import math

try:
	import glfw
except Exception:
	print("Missing dependency: glfw. Install with: pip install glfw")
	raise

try:
	from OpenGL.GL import (
		glClearColor, glClear, GL_COLOR_BUFFER_BIT,
		glBegin, glEnd, glVertex2f, glColor3f,
		GL_LINES, GL_LINE_LOOP
	)
	from OpenGL.GLU import gluOrtho2D
	from OpenGL.GL import glMatrixMode, GL_PROJECTION, glLoadIdentity
except Exception:
	print("Missing dependency: PyOpenGL. Install with: pip install PyOpenGL")
	raise


# Region codes for Cohen–Sutherland
INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def compute_out_code(x, y, xmin, ymin, xmax, ymax):
	code = INSIDE
	if x < xmin:
		code |= LEFT
	elif x > xmax:
		code |= RIGHT
	if y < ymin:
		code |= BOTTOM
	elif y > ymax:
		code |= TOP
	return code


def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax, verbose=True):
	out_code1 = compute_out_code(x1, y1, xmin, ymin, xmax, ymax)
	out_code2 = compute_out_code(x2, y2, xmin, ymin, xmax, ymax)

	if verbose:
		print(f"Initial line: P1=({x1:.2f},{y1:.2f}) P2=({x2:.2f},{y2:.2f})")
		print(f"Window: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")
		print(f"OutCodes: P1={out_code1:04b} P2={out_code2:04b}")

	accept = False

	while True:
		if (out_code1 | out_code2) == 0:
			# Both inside
			accept = True
			if verbose:
				print("Trivial accept: both points inside.")
			break
		elif (out_code1 & out_code2) != 0:
			# Share an outside zone -> outside
			if verbose:
				print("Trivial reject: both points share outside region.")
			break
		else:
			# At least one point outside; select it
			out_code_out = out_code1 if out_code1 != 0 else out_code2

			if verbose:
				print(f"Processing outCode={out_code_out:04b}")

			# Compute intersection with boundary
			if out_code_out & TOP:
				x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
				y = ymax
				boundary = "TOP"
			elif out_code_out & BOTTOM:
				x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
				y = ymin
				boundary = "BOTTOM"
			elif out_code_out & RIGHT:
				y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
				x = xmax
				boundary = "RIGHT"
			else:  # LEFT
				y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
				x = xmin
				boundary = "LEFT"

			if verbose:
				print(f"Intersect with {boundary}: ({x:.2f},{y:.2f})")

			# Replace the outside point and update its out code
			if out_code_out == out_code1:
				x1, y1 = x, y
				out_code1 = compute_out_code(x1, y1, xmin, ymin, xmax, ymax)
				if verbose:
					print(f"Update P1 -> ({x1:.2f},{y1:.2f}), outCode={out_code1:04b}")
			else:
				x2, y2 = x, y
				out_code2 = compute_out_code(x2, y2, xmin, ymin, xmax, ymax)
				if verbose:
					print(f"Update P2 -> ({x2:.2f},{y2:.2f}), outCode={out_code2:04b}")

	if accept and verbose:
		print(f"Accepted clipped segment: P1=({x1:.2f},{y1:.2f}) P2=({x2:.2f},{y2:.2f})")
	elif verbose:
		print("Rejected: no visible portion inside window.")

	return accept, (x1, y1, x2, y2)


def draw_line(x1, y1, x2, y2, r, g, b):
	glColor3f(r, g, b)
	glBegin(GL_LINES)
	glVertex2f(x1, y1)
	glVertex2f(x2, y2)
	glEnd()


def draw_rect(xmin, ymin, xmax, ymax, r=1.0, g=1.0, b=1.0):
	glColor3f(r, g, b)
	glBegin(GL_LINE_LOOP)
	glVertex2f(xmin, ymin)
	glVertex2f(xmax, ymin)
	glVertex2f(xmax, ymax)
	glVertex2f(xmin, ymax)
	glEnd()


def main():
	if not glfw.init():
		print("Failed to initialize GLFW")
		sys.exit(1)

	width, height = 800, 600
	window = glfw.create_window(width, height, "Cohen–Sutherland (PyOpenGL + GLFW)", None, None)
	if not window:
		glfw.terminate()
		print("Failed to create window")
		sys.exit(1)

	glfw.make_context_current(window)

	# Set a simple orthographic 2D projection matching window pixels
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, width, 0, height)

	glClearColor(0.1, 0.1, 0.12, 1.0)

	# Define a clipping window and a test line
	xmin, ymin, xmax, ymax = 200, 150, 600, 450
	# Line deliberately extending outside bounds
	x1, y1 = 100, 500
	x2, y2 = 700, 100

	# Run clipping once and print computations
	accept, clipped = cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax, verbose=True)

	# Render loop (short and sweet): just show the window until closed
	while not glfw.window_should_close(window):
		glClear(GL_COLOR_BUFFER_BIT)

		# Draw clip window (white)
		draw_rect(xmin, ymin, xmax, ymax, 1.0, 1.0, 1.0)

		# Draw original line (red)
		draw_line(x1, y1, x2, y2, 1.0, 0.2, 0.2)

		# Draw clipped line if accepted (green)
		if accept:
			cx1, cy1, cx2, cy2 = clipped
			draw_line(cx1, cy1, cx2, cy2, 0.2, 1.0, 0.4)

		glfw.swap_buffers(window)
		glfw.poll_events()

	glfw.terminate()


if __name__ == "__main__":
	main()

