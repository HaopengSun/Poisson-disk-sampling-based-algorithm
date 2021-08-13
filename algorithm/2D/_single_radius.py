import _distance2d
import _Circle
import math
import numpy as np

# for the last round of infilling, because there is only one possibility, generating particles with radius 2
# the program simplifies the process of "adding particles"
def single_radius(q, initial_radius, range1, maximum1, Circles, cols1, w1, width, height):

	valid = True
	yaxis = math.floor(q / cols1)
	xaxis = math.floor(q - yaxis * cols1)

	w_use = w1
	x = np.random.randint(math.floor(xaxis * w_use), math.floor((xaxis + 1) * w_use))
	y = np.random.randint(math.floor(yaxis * w_use), math.floor((yaxis + 1) * w_use))

    #if the randomly selected point in the void grid is too close to borders, it will be deleted.
	m = initial_radius
	min_boundary = [x, y, (width - x), (height - y)]
	min_b = np.amin(min_boundary)
	if min_b < m:
		valid = None

    #in the reseaching sphere area with 'mindis' radius
	min_around = []
	if valid is True:
		for j in range(len(Circles)):
			if ((x - range1) < Circles[j].x < (x + range1)) or ((y - range1) < Circles[j].y < (y + range1)):
				k = _distance2d.dist(x, y, Circles[j].x, Circles[j].y) - Circles[j].r
				if (k <  m):
					valid = None
					break

    #generate particles
	if valid is True:
		Circles.append(_Circle.Circle(x, y, maximum1, width, height))
		return maximum1

	return False