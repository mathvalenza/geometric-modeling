import pygame
import numpy as np
import math

BACKGROUND_COLOR = (10, 10, 10)
WHITE = (200, 200, 200)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

def main():
	print ("opa")

	x = y = 0
	running = 1
	screen = pygame.display.set_mode((800, 600))
	screen.fill(BACKGROUND_COLOR)
	pygame.display.flip()

	clicked_points = []
	c0_points = []
	c1_points = []
	curves = []
 
	while running:
		event = pygame.event.poll()

		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.MOUSEBUTTONUP:
			clicked_points.append(event.pos)
			pygame.draw.circle(screen, WHITE, event.pos, 4)
		elif event.type == pygame.KEYDOWN:
			if chr(event.key) == "p" and len(clicked_points) == 5:
				draw_polygon(screen, clicked_points)
				# and len(clicked_points) == 5
			elif chr(event.key) == "b" and len(clicked_points) == 5:
				curve = draw_bezier(screen, clicked_points, WHITE)
				curves.append(curve)
				c0_points = clicked_points[:]
				print('C0: ', clicked_points)
				clicked_points = []
			elif chr(event.key) == "s" and len(clicked_points) == 5:
				curve = draw_bezier(screen, clicked_points, WHITE)
				curves.append(curve)
				c1_points = clicked_points[:]
				print('C1: ', clicked_points)
				clicked_points = []
			elif chr(event.key) == "0" and len(curves) == 2:
				c1_points = do_c0(screen, c0_points, c1_points, curves)
				# c1_points = do_c0(screen, c0, c1, curves)
			elif chr(event.key) == "1" and len(curves) == 2:
				c1_points = do_c1(screen, c0_points, c1_points, curves)
				# c1_points = do_c1(screen, c0, c1_points, curves)
			elif chr(event.key) == "2" and len(curves) == 2:
				# do_c1(screen, c0_points, c1_points, curves)
				do_c2(screen, c0_points, c1_points, curves)
		pygame.display.flip()

def draw_polygon(screen, clicked_points):
	pygame.draw.lines(screen, WHITE, False, clicked_points, 1)

def draw_bezier(screen, clicked_points, color):
	precision = 0.001
	t = 0.0

	c1 = []

	while (t < 1):
		point = bezier_function(t, clicked_points)
		c1.append(point)
		pygame.draw.circle(screen, color, point, 2)
		t += precision
		pygame.display.flip()

	return c1

def draw_b_spline(screen, clicked_points):
	precision = 0.001
	t = 0.0

	c1 = []

	while (t < 1):
		point = b_spline_function(t, clicked_points)
		c1.append(point)
		pygame.draw.circle(screen, WHITE, point, 2)
		t += precision
		pygame.display.flip()

	return c1

def bezier_function(t, clicked_points):
	B0 = clicked_points[0]
	B1 = clicked_points[1]
	B2 = clicked_points[2]
	B3 = clicked_points[3]
	B4 = clicked_points[4]

	x = (1 - t)**4*B0[0] + 4*t*(1 - t)**3*B1[0] + 6*t**2*(1 - t)**2*B2[0] + 4*t**3*(1 - t)*B3[0] + t**4*B4[0]

	y = (1 - t)**4*B0[1] + 4*t*(1 - t)**3*B1[1] + 6*t**2*(1 - t)**2*B2[1] + 4*t**3*(1 - t)*B3[1] + t**4*B4[1]

	return int(x), int(y)

# def b_spline_function(t, clicked_points):
# 	B0 = clicked_points[0]
# 	B1 = clicked_points[1]
# 	B2 = clicked_points[2]
# 	B3 = clicked_points[3]


# 	x = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[0] + (3*t**3 - 6*t**2 + 4)*B1[0] + (-1*3*t**3 + 3*t**2 + 3*t + 1)*B2[0] + t**3*B3[0])/6
# 	print (x)
# 	y = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[1] + (3*t**3 - 6*t**2 + 4)*B1[1] + (-1*3*t**3 + 3*t**2 + 3*t + 1)*B2[1] + t**3*B3[1])/6

# 	return int(x), int(y)

# def b_spline_function(t, clicked_points):
# 	B0 = clicked_points[0]
# 	B1 = clicked_points[1]
# 	B2 = clicked_points[2]
# 	B3 = clicked_points[3]
# 	B4 = clicked_points[4]

# 	x = ((1/6)*(t - 0)**3)*B0[0] - ((2/3)*(t - 1)**3)*B1[0] + ((t - 2)**3)*B2[0] - ((2/3)*(t - 3)**3)*B3[0] + ((1/6)*(t - 4)**3)*B4[0] 
# 	y = ((1/6)*(t - 0)**3)*B0[0] - ((2/3)*(t - 1)**3)*B1[0] + ((t - 2)**3)*B2[1] - ((2/3)*(t - 3)**3)*B3[1] + ((1/6)*(t - 4)**3)*B4[1]

# 	print ("x: ", x)

# 	return int(x), int(y)

def b_spline_function(t, clicked_points):
	B0 = clicked_points[0]
	B1 = clicked_points[1]
	B2 = clicked_points[2]
	B3 = clicked_points[3]

	x = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[0] + (3*t**3 - 6*t**2 + 0*t + 4)*B1[0] + (-3*t**3 + 3*t**2 + 3*t + 1)*B2[0] + (t**3)*B3[0]) / 6
	y = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[1] + (3*t**3 - 6*t**2 + 0*t + 4)*B1[1] + (-3*t**3 + 3*t**2 + 3*t + 1)*B2[1] + (t**3)*B3[1]) / 6

	# x = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[0] + (3*t**3 - 6*t**2 + 4)*B1[0] + (-3*t**3 + 3*t**2 + 3*t + 1)*B2[0] + (-3*t**2 + 3*t**2 + 3*t + 1)*B3[0]) / 6
	# y = ((-1*t**3 + 3*t**2 - 3*t + 1)*B0[1] + (3*t**3 - 6*t**2 + 4)*B1[1] + (-3*t**3 + 3*t**2 + 3*t + 1)*B2[1] + (-3*t**2 + 3*t**2 + 3*t + 1)*B3[1]) / 6

	return int(x), int(y)

def do_c0(screen, c0_points, c1_points, curves):
	print('------------------------ DOING C0 ------------------------')

	c0 = curves[0]
	c1 = curves[1]
	p0, p1 = c0[0], c1[0]

	b = curves[1][0]
	a = c0_points[-1]

	x_diff = b[0] - a[0]
	y_diff = b[1] - a[1]

	new_points = []

	for x, y in c1_points:
		x -= x_diff
		y -= y_diff

		new_points.append((x, y))

	draw_clicked_points(screen, new_points, BLUE)
	draw_bezier(screen, new_points, BLUE)

	c0_deritave = bezier_derivate(1, c0_points)
	c1_deritave = bezier_derivate(0, new_points)

	print ('C0 derivate: ', c0_deritave)
	print ('C1 derivate: ', c1_deritave)

	c0_second_derivate = bezier_second_derivate(1, c0_points)
	c1_second_derivate = bezier_second_derivate(0, new_points)

	print ('C0 second derivate: ', math.degrees(c0_second_derivate))
	print ('C1 second derivate: ', math.degrees(c1_second_derivate))

	return new_points

def do_c1(screen, c0_points, c1_points, curves):
	print('------------------------ DOING C1 ------------------------')

	c0 = curves[0]
	c1 = curves[1]
	p0, p1 = c0[0], c1[0]

	commom_point = c0_points[-1]
	last_c0 = c0_points[-2]
	first_c1 = c1_points[1]

	x_diff = commom_point[0] - last_c0[0]
	y_diff = commom_point[1] - last_c0[1]

	new_points = c1_points[:]

	# first_c1[0] = last_c0[0] - x_diff
	# first_c1[1] = last_c0[1] - y_diff

	first_c1 = (commom_point[0] + x_diff, commom_point[1] + y_diff)

	new_points[1] = first_c1

	c0_deritave = bezier_derivate(1, c0_points)
	c1_deritave = bezier_derivate(0, new_points)

	print ('C0 derivate: ', math.degrees(c0_deritave))
	print ('C1 derivate: ', math.degrees(c1_deritave))

	c0_second_derivate = bezier_second_derivate(1, c0_points)
	c1_second_derivate = bezier_second_derivate(0, new_points)

	print ('C0 second derivate: ', math.degrees(c0_second_derivate))
	print ('C1 second derivate: ', math.degrees(c1_second_derivate))


	draw_clicked_points(screen, new_points, GREEN)
	draw_bezier(screen, new_points, GREEN)

	return new_points

def do_c2(screen, c0_points, c1_points, curves):
	print('------------------------ DOING C2 ------------------------')

	new_points = c1_points[:]

	last_c0 = c0_points[-2]
	before_last_c0 = c0_points[-3]

	x_diff = last_c0[0] - before_last_c0[0]
	y_diff = last_c0[1] - before_last_c0[1]

	ref = c1_points[1]

	new_points[2] = (ref[0] + x_diff, ref[1] + y_diff)

	c0_deritave = bezier_derivate(1, c0_points)

	c1_deritave = bezier_derivate(0, new_points)

	print ('C0 derivate: ', math.degrees(c0_deritave))
	print ('C1 derivate: ', math.degrees(c1_deritave))

	c0_second_derivate = bezier_second_derivate(1, c0_points)
	c1_second_derivate = bezier_second_derivate(0, new_points)

	print ('C0 second derivate: ', math.degrees(c0_second_derivate))
	print ('C1 second derivate: ', math.degrees(c1_second_derivate))	

	draw_clicked_points(screen, new_points, RED)
	draw_bezier(screen, new_points, RED)


def bezier_derivate(t, clicked_points):
	B0 = clicked_points[0]
	B1 = clicked_points[1]
	B2 = clicked_points[2]
	B3 = clicked_points[3]
	B4 = clicked_points[4]

	dx = 4*B0[0]*t**3 - 12*B0[0]*t**2 + 12*B0[0]*t - 4*B0[0] - 16*B1[0]*t**3 + 36*B1[0]*t**2 - 24*B1[0]*t + 4*B1[0] + 24*B2[0]*t**3 - 36*B2[0]*t**2 + 12*B2[0]*t - 16*B3[0]*t**3 + 12*B3[0]*t**2 + 4*B4[0]*t**3
	dy = 4*B0[1]*t**3 - 12*B0[1]*t**2 + 12*B0[1]*t - 4*B0[1] - 16*B1[1]*t**3 + 36*B1[1]*t**2 - 24*B1[1]*t + 4*B1[1] + 24*B2[1]*t**3 - 36*B2[1]*t**2 + 12*B2[1]*t - 16*B3[1]*t**3 + 12*B3[1]*t**2 + 4*B4[1]*t**3

	return float(dx/dy)

def bezier_second_derivate(t, clicked_points):
	B0 = clicked_points[0]
	B1 = clicked_points[1]
	B2 = clicked_points[2]
	B3 = clicked_points[3]
	B4 = clicked_points[4]

	dx = 12*t**2*B0[0] - 24*t*B0[0] + 12*B0[0] - 48*t**2*B1[0] + 72*t*B1[0] - 24*B1[0] + 72*t**2*B2[0] - 72*t*B2[0] + 12*B2[0] - 48*t**2*B3[0] + 24*t*B3[0] + 12*t**2*B4[0]
	dy = 12*t**2*B0[1] - 24*t*B0[1] + 12*B0[1] - 48*t**2*B1[1] + 72*t*B1[1] - 24*B1[1] + 72*t**2*B2[1] - 72*t*B2[1] + 12*B2[1] - 48*t**2*B3[1] + 24*t*B3[1] + 12*t**2*B4[1]

	return float(dx/dy)

def b_spline_derivate(point):
	return 0

def draw_tangent(a, point, screen):

	p0 = 200, bezier_tangent(200, a)
	p1 = 400, bezier_tangent(400, a)

	pygame.draw.line(screen, WHITE, p0, p1)

def bezier_tangent(x, a):
	return a*x

def draw_clicked_points(screen, clicked_points, color):
	for point in clicked_points:
		pygame.draw.circle(screen, color, point, 4)
main()