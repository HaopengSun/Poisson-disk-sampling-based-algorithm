import random, math, csv, json
import numpy as np
import _distance3d
import _random_vector_function
import _Sphere
import _exportdata
import _radii
import _single_radius
import _remove_grid
import _adjustment
import _mini_radius
import _plot
import _particle_filter
import _print_result
import _generateParticle
import _target

# set unit size and canvas size
unit = 0.025
width = 2400
height = 2400
depth = 2400
pi = 3.1415926

# minimum distance of points with Poisson Disk disktribution
r = width / 2
k = 30
root = 2 ** 0.5
w = r / root
active = []

# cell size for void filling process
w1 = 8

# Particle size distribution
maximums = [450, 399, 319, 79, 11, 9, 7, 5, 4]
roundRadius = [400, 320, 80, 12, 10, 8, 6, 5, 4]

# calculate the range where the void filling process searches
ranges = []
for maximum in maximums:
	ranges.append(maximum + maximums[0])

grid = []
grid1 = []
Circles = []
occupation_poisson = 0

# calculate the number of cells used for the generation of points with Poisson Disk distribution
cols = math.floor(width / w)
rows = math.floor(height / w)
depths = math.floor(depth / w)
gridnumbers = cols * rows * depths

# calculate the number of cell used for void filling
cols1 = math.floor(width / w1)
rows1 = math.floor(height / w1)
depths1 = math.floor(depth / w1)
gridnumbers1 = cols1 * rows1 * depths1
grid1 = np.zeros(gridnumbers1)
volumes = []
real_volumes = []
finers = []

#users should input the parameters of the soil in the first place
target_void_ratio = 0.55
sieves = ['10.5-10', '10-8', '8-2', '2-0.3', '0.3-0.25', '0.25-0.2', '0.2-0.15', '0.15-0.125', '0.125-0.1']
soil_distributions = [1, 0.83, 0.52, 0.15, 0.15, 0.06, 0.035, 0.015, 0.005]
ideal_distributions = [0.17, 0.31, 0.37, 0, 0.09, 0.025, 0.02, 0.01, 0.005]
sieve_number = len(sieves)

density = 0.001631

volume = depth * width * height
ideal_totalmass = (volume / (target_void_ratio + 1))

# calculate the volume/mass targets
ideal_volumes = _target.targetVolumes(ideal_distributions, ideal_totalmass)
ideal_masses = _target.targetMasses(ideal_distributions, ideal_totalmass, density, unit)

def main_program():
	poisson(r)
	for i in range(len(sieves)):
		if i > 0:
			fill_the_void(i, 0, 0, ideal_volumes[i], roundRadius[i], ranges[i], maximums[i])
	result()
	# _exportdata.exportdata(Circles)

def setup_poisson(gridnumbers, cols, rows):

	for i in range(gridnumbers):
		grid.append(None)

	#randomly select a point in the canvas
	randomx = np.random.randint(0, math.floor(cols * w))
	randomy = np.random.randint(0, math.floor(rows * w))
	randomz = np.random.randint(0, math.floor(depths * w))
	randompoint = [randomx, randomy, randomz]

	#put the point into the grid it located
	gridx = math.floor(randomx / w)
	gridy = math.floor(randomy / w)
	gridz = math.floor(randomz / w)
	grid[gridz + gridx * depths + gridy * cols * depths] = randompoint
	active.append(randompoint)
	point_poisson()

#generate points of Poisson Disk Sampling
def point_poisson():

	min_radius = roundRadius[0]

	global occupation_poisson

	while len(active) > 0:
		check = np.random.randint(0, len(active))
		found = None
		for n in range(k):
			s = _random_vector_function.random_vector_function(r, math.floor(r * 1.5))
			sample = []
			for i in range(0, len(s)):
				sample.append(s[i] + active[check][i])

			gcol = math.floor(sample[0] / w)
			grow = math.floor(sample[1] / w)
			gdepth = math.floor(sample[2] / w)
			ggrid = gdepth + gcol * depths + grow * cols * depths

			if gcol > -1 and grow > -1 and gdepth > -1 and gcol < cols and grow < rows and gdepth < depths:
				ok = True
				# check distances between selected point and points in the around grids
				nums = [-1, 0, 1]
				num1s = [-1, 0, 1]
				num2s = [-1, 0, 1]
				for num in nums:
					for num1 in num1s:
						for num2 in num2s:
							if 0 <= gcol + num1 < cols and 0 <= grow + num < rows and 0 <= gdepth + num2 < depths:
								index = (gcol + num1) * depths + (grow + num) * cols * depths + (gdepth + num2)
								if grid[index] is None:
									pass
								else:
									d = _distance3d.dist(grid[index][0], grid[index][1], grid[index][2], sample[0], sample[1], sample[2])
									if d < r:
										ok = None
				if ok is True:
					found = True
					grid[gdepth + gcol * depths + grow * depths * cols] = sample
					active.append(sample)
					break
		if found is None:
			del active [check : (check + 1)]

	for i in range(len(grid)):
		if grid[i] is None:
			pass
		else:
			#delete points which are too close to the border
			if (grid[i][0] < width - min_radius) and (grid[i][0] > min_radius) and (grid[i][1] < height - min_radius) and (grid[i][1] > min_radius) and (grid[i][2] < depth - min_radius) and (grid[i][2] > min_radius):
				Circles.append(_Sphere.Sphere(grid[i][0], grid[i][1], grid[i][2], min_radius, width, height, depth))
				occupation_poisson = occupation_poisson + 1

	# enlarge the particles
	_generateParticle.generateCircles_p(ranges[0], (maximums[0] - 2), Circles)

	print('poisson disk sampling', occupation_poisson)

def poisson(r):
	gradient = width / 100
	setup_poisson(gridnumbers, cols, rows)
	if _adjustment.surpass_volume_poisson(5, Circles, ideal_volumes):
		# volume surpasses the target by more than 20%, remove the particle and regenerate with a larger minimum radius
		_adjustment.remove_particles(maximums[0], roundRadius[0], Circles)
		if r + gradient < width:
			r = r + gradient
			poisson(r)
	elif _adjustment.surpass_volume_poisson(2, Circles, ideal_volumes):
		# volume surpasses the target by more than 2%, shrink the radius
		while _adjustment.surpass_volume_poisson(1.02, Circles, ideal_volumes) and _adjustment.stop_recursion(Circles, roundRadius):
			_adjustment.adjust_radius(-1, Circles, roundRadius)
		if not _adjustment.surpass_volume_poisson(1, Circles, ideal_volumes):
			_adjustment.adjust_radius(1, Circles, roundRadius)
	elif not _adjustment.surpass_volume_poisson(1, Circles, ideal_volumes):
		# volume does not reach the target, remove the particle and regenerate with a smaller minimum radius
		_adjustment.remove_particles(maximums[0], roundRadius[0], Circles)
		r = r - gradient
		poisson(r)

def fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum):

	gridnum = list(range(0, gridnumbers1))

	# remove the fully filled cells
	_remove_grid.remove_cells(roundRadius, Circles, w1, grid1, cols1, rows1, depths1)

	while totalvolume < ideal_volume and len(gridnum) > 0:
		#randomly select a void grid and try to add particles
		q = np.random.randint(len(gridnum))

		# decide the particle radius
		if roundRadius != maximum:
			n = _radii.radii(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, depths1, w1, width, height, depth)
		else:
			n = _single_radius.single_radius(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, depths1, w1, width, height, depth)

		# insert the particle in the canvas
		if n is False:
			gridnum.remove(gridnum[q])
		else:
			grid1[q] = 1
			totalvolume = totalvolume + math.floor((4 / 3) * pi * n ** 3)
			occupation = occupation + 1
			gridnum.remove(gridnum[q])
	
	if len(gridnum) == 0:
		print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)

	# adjust the volume of particles
	if maximum > roundRadius and totalvolume > ideal_volume * 1.02 and not _mini_radius.particles_mini(maximums[roundOfInfilling], roundRadius, Circles):
		maximum -= 1
		_adjustment.remove_particles(maximums[roundOfInfilling], roundRadius, Circles)
		print('volume surpasses the target by 2%', 'round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, 0, 0, ideal_volume, roundRadius, rangeRadius, maximum)
	
	print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)


def result():

	volumes = _particle_filter.particleSieve(Circles, sieve_number, real_volumes, maximums, roundRadius)

	totalvolume = 0
	real_totalvolume = 0
	for i in range(sieve_number):
		volumes[i] = round(volumes[i], 4)
		totalvolume += volumes[i]
		real_volumes[i] = math.floor(volumes[i]) * unit ** 3
		real_totalvolume += real_volumes[i]
	totalmass = real_totalvolume * density
	voidratio = ((width * height * depth * unit ** 3) - real_totalvolume) / real_totalvolume

	for i in range(sieve_number):
		finers.append(0)
		for j in range(sieve_number):
			if j <= i:
				finers[i] += real_volumes[j]
		finers[i] = round(finers[i] * density / totalmass, 4)
	finers.reverse()
	volumes.reverse()
	real_volumes.reverse()

	_print_result.printResult(real_volumes, density, ideal_masses, sieve_number, sieves, finers, ideal_volumes, volumes, voidratio, totalmass, totalvolume)

	# plot the particle size distribution curve
	_plot.plotCurve(finers, soil_distributions, roundRadius, maximums, unit)

main_program()