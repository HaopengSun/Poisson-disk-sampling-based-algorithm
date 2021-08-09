import random, math, csv, json
import numpy as np
import _distance2d
import _random_vector_function
import _Circle
import _exportdata
import _radii
import _single_radius
import _remove_grid

# set unit size and canvas size
unit = 0.0125
width = 1000
height = 1000
pi = 3.1415926

# minimum distance of points with Poisson Disk Disktribution
r = width / 2
k = 30
root = 2 ** 0.5
w = r / root
active = []

# cell size for void filling process
w1 = 4

# Particle size distribution
maximums = [190, 94, 67, 23, 15,  11, 5, 3, 2]
roundRadius = [95, 68, 24, 16, 12, 6, 3, 2]

ranges = []
for maximum in maximums:
	ranges.append(maximum + maximums[0])

grid = []
grid1 = []
Circles = []
growing = []
occupation_poisson = 0

cols = math.floor(width / w)
rows = math.floor(height / w)
gridnumbers = cols * rows

cols1 = math.floor(width / w1)
rows1 = math.floor(height / w1)
gridnumbers1 = cols1 * rows1
grid1 = np.zeros(gridnumbers1)
volumes = []
real_volumes = []
masses = []
differences = []
finers = []

#users should input the parameters of the soil in the first place
target_void_ratio = 0.6
sieves = ['4.75-2.36', '2.36-1.7', '1.7-0.6', '0.6-0.4', '0.4-0.3', '0.3-0.15', '0.15-0.075', '<0.074']
soil_distributions = [1, 0.76, 0.7, 0.47, 0.29, 0.18, 0.05, 0.02]
ideal_distributions = [0.24, 0.06, 0.23, 0.18, 0.11, 0.13, 0.03, 0.02]
sieve_number = len(sieves)

density = 0.001631

volume = width * height
ideal_totalmass = (volume / (target_void_ratio + 1))

ideal_volumes = []
ideal_masses = []
for ideal_distribution in ideal_distributions:
	ideal_volume = math.floor(ideal_totalmass * ideal_distribution)
	ideal_volumes.append(ideal_volume)
	ideal_mass = ideal_volume * density * unit ** 2
	ideal_masses.append(ideal_mass)

def main_program():
	poisson(r)
	for i in range(len(sieves)):
		if i > 0:
			fill_the_void(i, 0, 0, ideal_volumes[i], roundRadius[i], ranges[i], maximums[i])
	list_particles()
	# _exportdata.exportdata(Circles)

def setup_poisson(gridnumbers, cols, rows):
	for i in range(gridnumbers):
		grid.append(None)

	#randomly select a point in the canvas
	randomx = np.random.randint(0, math.floor(cols * w))
	randomy = np.random.randint(0, math.floor(rows * w))
	randompoint = [randomx, randomy]

	#put the point into the grid it located
	gridx = math.floor(randomx / w)
	gridy = math.floor(randomy / w)
	grid[gridx + gridy * cols] = randompoint
	active.append(randompoint)
	point_poisson()

#generate points of Poisson Disk Sampling
def point_poisson():

	global occupation_poisson

	while len(active) > 0:
		check = np.random.randint(0, len(active))
		found = None
		for n in range(k):
			s = _random_vector_function.random_vector_function(r, math.floor(r * 2))
			sample = []
			for i in range(0, len(s)):
				sample.append(s[i] + active[check][i])

			gcol = math.floor(sample[0] / w)
			grow = math.floor(sample[1] / w)
			ggrid = gcol + grow * cols

			if gcol > -1 and grow > -1 and gcol < cols and grow < rows:
				ok = True
				#check distance between selected point and points in the around grids
				nums = [-1, 0, 1]
				num1s = [-1, 0, 1]
				for num in nums:
					for num1 in num1s:
						if 0 <= gcol + num1 < cols and 0 <= grow + num < rows:
							index = (gcol + num1) + (grow + num) * cols
							if grid[index] is None:
								pass
							else:
								d = _distance2d.dist(grid[index][0], grid[index][1], sample[0], sample[1])
								if d < r:
									ok = None
				if ok is True:
					found = True
					grid[gcol + grow * cols] = sample
					active.append(sample)
					break
		if found is None:
			del active [check : (check + 1)]

	for i in range(len(grid)):
		if grid[i] is None:
			pass
		else:
			if (grid[i][0] < width - roundRadius[0]) and (grid[i][0] > roundRadius[0]) and (grid[i][1] < height - roundRadius[0]) and (grid[i][1] > roundRadius[0]):
				Circles.append(_Circle.Circle(grid[i][0], grid[i][1], roundRadius[0], width, height))
				occupation_poisson = occupation_poisson + 1

	generateCircles_p(ranges[0], (maximums[0] - 2))

	print('poisson disk sampling', occupation_poisson)

#particles of "Poisson Disk Sampling" are growing
def generateCircles_p(mindis, maxi):
	for k in range(len(Circles)):
		if Circles[k].g is True:
			growing.append([Circles[k].x, Circles[k].y])

	while len(growing) > 0:
		for i in range(len(Circles)):
			if Circles[i].g is True:
				if Circles[i].r > maxi:
					Circles[i].g = None
					growing.remove([Circles[i].x, Circles[i].y])
					break
				elif Circles[i].edge() is None:
					growing.remove([Circles[i].x, Circles[i].y])
					break
				else:
					for j in range(len(Circles)):
						if (j != i) and ((Circles[i].x - mindis) < Circles[j].x < (Circles[i].x + mindis)) and ((Circles[i].y - mindis) < Circles[j].y < (Circles[i].y + mindis)):
							dis = _distance2d.dist(Circles[i].x, Circles[i].y, Circles[j].x, Circles[j].y)
							if dis < (Circles[i].r + Circles[j].r):
								Circles[i].g = None
								growing.remove([Circles[i].x, Circles[i].y])
								break
			Circles[i].grow()


# check whether the volume of particles of Poisson Disk distirbution surpasses the target by 2% or reaches the target
def surpass_volume_poisson(multiplication):
	volume_poisson = 0
	for i in range(len(Circles)):
		volume_poisson += pi * Circles[i].r ** 2
	print('volume of Poisson Disk particles', volume_poisson, 'target volume',ideal_volumes[0])
	if volume_poisson > (ideal_volumes[0] * multiplication):
		return True
	return False

# the radii of particles with Poisson Disk distribution are equal of the minimum value in the radius range of the largest sieve
def stop_recursion():
	for i in range(len(Circles)):
		if Circles[i].r > roundRadius[0]:
			return True
	return False

# adjust the volume by adding or minusing the radius by one unit
def adjust_radius(addminus):
	for i in range(len(Circles)):
		if Circles[i].r > roundRadius[0]:
			Circles[i].r += addminus

def remove_particles(maximum_radius, minimum_radius):
	remove_particle = []
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r <= maximum_radius:
			remove_particle.append(circle)
	for circle in remove_particle:
		Circles.remove(circle)

# adjust the volume to ensure it is within the acceptable scope
def poisson(r):
	setup_poisson(gridnumbers, cols, rows)
	if surpass_volume_poisson(1.02):
		while surpass_volume_poisson(1.02) and stop_recursion():
			adjust_radius(-1)
		if not surpass_volume_poisson(1):
			adjust_radius(1)
	elif not surpass_volume_poisson(1):
		remove_particles(maximums[0], roundRadius[0])
		r = r - 10
		poisson(r)

def particles_mini(maximum_radius, minimum_radius):
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r <= maximum_radius:
			if circle.r != minimum_radius:
				return False
	return True

def fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum):

	gridnum = list(range(0, gridnumbers1))
	_remove_grid.remove_cells(roundRadius, Circles, w1, grid1, cols1, rows1)

	# the loop will stop if the mass of this round of infilling reaches the target or it runs out of void grids
	# the size of divided grids is 5, which can normally covers all round of infilling
	while totalvolume < ideal_volume and len(gridnum) > 0:
		#randomly select a void grid and try to add particles
		q = np.random.randint(len(gridnum))

		if roundRadius != maximum:
			n = _radii.radii(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, w1, width, height)
		else:
			n = _single_radius.single_radius(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, w1, width, height)

		if n == 0:
			gridnum.remove(gridnum[q])
		else:
			grid1[q] = 1
			totalvolume = totalvolume + math.floor(3.1415926 * n * n)
			occupation = occupation + 1
			gridnum.remove(gridnum[q])
	
	if len(gridnum) == 0:
		print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)

	print(maximum > roundRadius, totalvolume > ideal_volume * 1.02, not particles_mini(maximums[roundOfInfilling], roundRadius))
	if maximum > roundRadius and totalvolume > ideal_volume * 1.02 and not particles_mini(maximums[roundOfInfilling], roundRadius):
		maximum -= 1
		remove_particles(maximums[roundOfInfilling], roundRadius)
		print('volume surpasses the target by 2%', 'round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, 0, 0, ideal_volume, roundRadius, rangeRadius, maximum)
	
	print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)


def list_particles():
	global mass
	for _ in range(sieve_number):
		volumes.append(0)
		real_volumes.append(0)

	power2D = 2

	for i in range(len(Circles)):
		if Circles[i].r < 3:
			volumes[0] += pi * Circles[i].r ** power2D
		elif 3 <= Circles[i].r < 6:
			volumes[1] += pi * Circles[i].r ** power2D
		elif 6 <= Circles[i].r < 12:
			volumes[2] += pi * Circles[i].r ** power2D
		elif 12 <= Circles[i].r < 16:
			volumes[3] += pi * Circles[i].r ** power2D
		elif 16 <= Circles[i].r < 24:
			volumes[4] += pi * Circles[i].r ** power2D
		elif 24 <= Circles[i].r < 68:
			volumes[5] += pi * Circles[i].r ** power2D
		elif 68 <= Circles[i].r < 95:
			volumes[6] += pi * Circles[i].r ** power2D
		elif 95 <= Circles[i].r < 190:
			volumes[7] += pi * Circles[i].r ** power2D

	totalvolume = 0
	real_totalvolume = 0
	for i in range(sieve_number):
		volumes[i] = round(volumes[i], 4)
		totalvolume += volumes[i]
		real_volumes[i] = math.floor(volumes[i]) * unit ** 2
		real_totalvolume += real_volumes[i]
	totalmass = real_totalvolume * density
	voidratio = ((width * height * unit ** 2) - real_totalvolume) / real_totalvolume

	for i in range(sieve_number):
		finers.append(0)
		for j in range(sieve_number):
			if j <= i:
				finers[i] += real_volumes[j]
		finers[i] = round(finers[i] * density / totalmass, 4)
	finers.reverse()
	volumes.reverse()
	real_volumes.reverse()

	for volume in real_volumes:
		masses.append(volume * density)
	for i in range(len(masses)):
		differences.append(masses[i] - ideal_masses[i])
	for i in range(sieve_number):
		print('sieve:', sieves[i], 'finer:', finers[i], 'ideal volumes:', ideal_volumes[i], 'volume:', volumes[i], 'ideal mass:', ideal_masses[i], 'mass:', masses[i], 'difference:', differences[i])
	print('void ratio:', voidratio,'totalmass:', totalmass, 'totalvolume', totalvolume)

main_program()