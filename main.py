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
				clicked_points = []
				print ("len(curves): ", len(curves))
		
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

def bezier_function(t, clicked_points):
	B0 = clicked_points[0]
	B1 = clicked_points[1]
	B2 = clicked_points[2]
	B3 = clicked_points[3]
	B4 = clicked_points[4]

	print (B0)
	print (B1)
	print (B2)
	print (B3)
	print (B4)

	x = (1 - t)**4*B0[0] + 4*t*(1 - t)**3*B1[0] + 6*t**2*(1 - t)**2*B2[0] + 4*t**3*(1 - t)*B3[0] + t**4*B4[0]
	print ("x: ", x)

	y = (1 - t)**4*B0[1] + 4*t*(1 - t)**3*B1[1] + 6*t**2*(1 - t)**2*B2[1] + 4*t**3*(1 - t)*B3[1] + t**4*B4[1]
	print ("y: ", y)

	return int(x), int(y)

main()