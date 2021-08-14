import _distance3d
import _Sphere
import math
import numpy as np

def radii(q, initial_radius, range1, maximum1, Circles, cols1, depths1, w1, width, height, depth):

	valid = True

	yaxis = math.floor(q / cols1 / depths1)
	xaxis = math.floor((q - yaxis * cols1 * depths1) / depths1)
	zaxis = q - xaxis * depths1 - yaxis * cols1 * depths1

	w_use = w1
	x = np.random.randint(math.floor(xaxis * w_use), math.floor((xaxis + 1) * w_use))
	y = np.random.randint(math.floor(yaxis * w_use), math.floor((yaxis + 1) * w_use))
	z = np.random.randint(math.floor(zaxis * w_use), math.floor((zaxis + 1) * w_use))

    #if the randomly selected point in the void grid is too close to borders, it will be deleted.
	m = initial_radius
	min_boundary = [x, y, z, (width - x), (height - y), (depth - z)]
	min_b = np.amin(min_boundary)
	if min_b < m:
		valid = None

    #in the reseaching sphere area with 'mindis' radius
	min_around = []
	if valid is True:
		for j in range(len(Circles)):
			if ((x - range1) < Circles[j].x < (x + range1)) and ((y - range1) < Circles[j].y < (y + range1)) and ((z - range1) < Circles[j].z < (z + range1)):
				k = _distance3d.dist(x, y, z, Circles[j].x, Circles[j].y, Circles[j].z) - Circles[j].r
				if (k < m):
					valid = None
					break
				else:
					min_around.append(k)
			else:
				min_around.append(maximum1)


    #generate particles
	if valid is True:

		if not min_around:
			min_a = 0
		else:
			min_a = np.amin(min_around)

		if min_a <= min_b:
			if min_a <= maximum1:
				Circles.append(_Sphere.Sphere(x, y, z, min_a, width, height, depth))
				return min_a
			else:
				Circles.append(_Sphere.Sphere(x, y, z, maximum1, width, height, depth))
				return maximum1
		elif min_a > min_b:
			if min_b <= maximum1:
				Circles.append(_Sphere.Sphere(x, y, z, min_b, width, height, depth))
				return min_b
			else:
				Circles.append(_Sphere.Sphere(x, y, z, maximum1, width, height, depth))
				return maximum1
	else:
		return False