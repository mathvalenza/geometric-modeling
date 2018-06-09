import pygame

BACKGROUND_COLOR = (10, 10, 10)
POINT_COLOR = (200, 200, 200)

def main():
	print ("opa")

	x = y = 0
	running = 1
	screen = pygame.display.set_mode((1200, 600))
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
			pygame.draw.circle(screen, POINT_COLOR, event.pos, 4)
			print(clicked_points)
		elif event.type == pygame.KEYDOWN:
			if chr(event.key) == "p" and len(clicked_points) == 5:
				draw_polygon(screen, clicked_points)
			elif chr(event.key) == "b" and len(clicked_points) == 5:
				print ("draw bezier")
				curve = draw_bezier(screen, clicked_points)
				curves.append(curve)
				c0_points = clicked_points[:]
				clicked_points = []
			elif chr(event.key) == "s" and len(clicked_points) == 5:
				print ("draw b-spline (bezier 2)")
				curve = draw_bezier(screen, clicked_points)
				curves.append(curve)
				c1_points = clicked_points[:]
				clicked_points = []
			elif chr(event.key) == "0" and len(curves) == 2:
				c1_points = do_c0(screen, c0_points, c1_points, curves)
			elif chr(event.key) == "1" and len(curves) == 2:
				do_c1(screen, c0_points, c1_points, curves)
		pygame.display.flip()

def draw_polygon(screen, clicked_points):
	pygame.draw.lines(screen, POINT_COLOR, False, clicked_points, 1)

def draw_bezier(screen, clicked_points):
	precision = 0.001
	t = 0.0

	c1 = []

	while (t < 1):
		point = bezier_function(t, clicked_points)
		c1.append(point)
		pygame.draw.circle(screen, POINT_COLOR, point, 2)
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
		pygame.draw.circle(screen, POINT_COLOR, point, 2)
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

# 	if (t == 0):
# 		x = (-1*(1)**3 + 3*(1)**2 - 3*(1) + 1)/6*B0[0] + (-1*3*(1)**3 + 3*(1)**2 + 3*(1) + 1)/6*B2[0] + (1)**3/6*B3[0] + 0
# 		y = (-1*(1)**3 + 3*(1)**2 - 3*(1) + 1)/6*B0[1] + (-1*3*(1)**3 + 3*(1)**2 + 3*(1) + 1)/6*B2[1] + (1)**3/6*B3[1] + 0
# 	elif (t == 1):
# 		x = 0 + (3*t**3 - 6*t**2 + 4)/6*B1[0] + (-1*3*t**3 + 3*t**2 + 3*t + 1)/6*B2[0] + t**3/6*B3[0]
# 		y = 0 + (3*t**3 - 6*t**2 + 4)/6*B1[1] + (-1*3*t**3 + 3*t**2 + 3*t + 1)/6*B2[1] + t**3/6*B3[1]
# 	else:
# 		x = (-1*t**3 + 3*t**2 - 3*t + 1)/6*B0[0] + (3*t**3 - 6*t**2 + 4)/6*B1[0] + (-1*3*t**3 + 3*t**2 + 3*t + 1)/6*B2[0] + t**3/6*B3[0]


# 		y = (-1*t**3 + 3*t**2 - 3*t + 1)/6*B0[0] + (3*t**3 - 6*t**2 + 4)/6*B1[1] + (-1*3*t**3 + 3*t**2 + 3*t + 1)/6*B2[1] + t**3/6*B3[1]

# 	return int(x), int(y)

def do_c0(screen, c0_points, c1_points, curves):
	c0 = curves[0]
	c1 = curves[1]
	p0, p1 = c0[0], c1[0]

	b = c1_points[0]
	a = c0_points[-1]

	x_diff = b[0] - a[0]
	y_diff = b[1] - a[1]

	new_points = []

	for x, y in c1_points:
		x -= x_diff
		y -= y_diff

		new_points.append((x, y))

	draw_clicked_points(screen, new_points)
	draw_bezier(screen, new_points)

	return new_points

def do_c1(screen, c0_points, c1_points, curves):
	c0 = curves[0]
	c1 = curves[1]
	p0, p1 = c0[0], c1[0]

	commom_point = c0_points[-1]
	last_c0 = c0_points[-2]
	first_c1 = c1_points[1]

	x_diff = commom_point[0] - last_c0[0]
	y_diff = commom_point[1] - last_c0[1]

	new_points = c1_points[:]

	print ("first_c1: ", first_c1)
	print ("commom_point: ", commom_point)
	print ("last_c0: ", last_c0)

	print ("x_diff: ", x_diff)
	print ("y_diff: ", y_diff)

	# first_c1[0] = last_c0[0] - x_diff
	# first_c1[1] = last_c0[1] - y_diff

	first_c1 = (commom_point[0] + x_diff, commom_point[1] + y_diff)

	print("c1_points: ", c1_points)

	new_points[1] = first_c1

	print ("new_points: ", new_points)

	draw_clicked_points(screen, new_points)
	draw_bezier(screen, new_points)


def draw_clicked_points(screen, clicked_points):
	for point in clicked_points:
		pygame.draw.circle(screen, POINT_COLOR, point, 4)

main()