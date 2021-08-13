import random, math, csv, json
import numpy as np
import _distance2d
import _random_vector_function
import _Circle
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
maximums = [400, 189, 133, 79, 39, 33, 19, 11, 7, 3]
roundRadius = [190, 134, 80, 40, 34, 20, 12, 8, 4, 3]

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
gridnumbers = cols * rows

# calculate the number of cell used for void filling
cols1 = math.floor(width / w1)
rows1 = math.floor(height / w1)
gridnumbers1 = cols1 * rows1
grid1 = np.zeros(gridnumbers1)
volumes = []
real_volumes = []
finers = []

# users should input the parameters of the soil in the first place
target_void_ratio = 0.8
sieves = ['10-4.75', '4.75-3.35', '3.35-2', '2-1', '1-0.85', '0.85-0.5', '0.5-0.3', '0.3-0.2', '0.2-0.1', '<0.1']
soil_distributions = [1, 0.95, 0.93, 0.9, 0.68, 0.44, 0.20, 0.08, 0.02, 0.005]
ideal_distributions = [0.05, 0.02, 0.03, 0.22, 0.24, 0.24, 0.12, 0.06, 0.015, 0.005]
sieve_number = len(sieves)

density = 0.001631

volume = width * height
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

	# enlarge the particles
	_generateParticle.generateCircles_p(ranges[0], (maximums[0] - 2), Circles)

	print('poisson disk sampling', occupation_poisson)


# adjust the volume to ensure it is within the acceptable scope
def poisson(r):
	setup_poisson(gridnumbers, cols, rows)
	if _adjustment.surpass_volume_poisson(1.02, Circles, ideal_volumes):
		while _adjustment.surpass_volume_poisson(1.02, Circles, ideal_volumes) and _adjustment.stop_recursion(Circles, roundRadius):
			_adjustment.adjust_radius(-1, Circles, roundRadius)
		if not _adjustment.surpass_volume_poisson(1, Circles, ideal_volumes):
			_adjustment.adjust_radius(1, Circles, roundRadius)
	elif not _adjustment.surpass_volume_poisson(1, Circles, ideal_volumes):
		_adjustment.remove_particles(maximums[0], roundRadius[0], Circles)
		r = r - 10
		poisson(r)

def fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum):

	gridnum = list(range(0, gridnumbers1))

	#remove the fully filled cells
	_remove_grid.remove_cells(roundRadius, Circles, w1, grid1, cols1, rows1)

	# the loop will stop if the mass of this round of infilling reaches the target or it runs out of void grids
	# the size of divided grids is 5, which can normally covers all round of infilling
	while totalvolume < ideal_volume and len(gridnum) > 0:
		#randomly select a void grid and try to add particles
		q = np.random.randint(len(gridnum))

		# decide the particle radius
		if roundRadius != maximum:
			n = _radii.radii(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, w1, width, height)
		else:
			n = _single_radius.single_radius(gridnum[q], roundRadius, rangeRadius, maximum, Circles, cols1, w1, width, height)

		# insert the particle in the canvas
		if n is False:
			gridnum.remove(gridnum[q])
		else:
			grid1[q] = 1
			totalvolume = totalvolume + math.floor(3.1415926 * n * n)
			occupation = occupation + 1
			gridnum.remove(gridnum[q])
	
	if len(gridnum) == 0:
		print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)

	# adjust the volume of particles
	# print(maximum > roundRadius, totalvolume > ideal_volume * 1.02, not _mini_radius.particles_mini(maximums[roundOfInfilling], roundRadius, Circles))
	if maximum > roundRadius and totalvolume > ideal_volume * 1.02 and not _mini_radius.particles_mini(maximums[roundOfInfilling], roundRadius, Circles):
		maximum -= 1
		_adjustment.remove_particles(maximums[roundOfInfilling], roundRadius, Circles)
		print('volume surpasses the target by 2%', 'round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, 0, 0, ideal_volume, roundRadius, rangeRadius, maximum)
	
	print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)


def result():
	global mass

	volumes = _particle_filter.particleSieve(Circles, sieve_number, real_volumes, maximums, roundRadius)

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

	_print_result.printResult(real_volumes, density, ideal_masses, sieve_number, sieves, finers, ideal_volumes, volumes, voidratio, totalmass, totalvolume)

	# plot the particle size distribution curve
	_plot.plotCurve(finers, soil_distributions, roundRadius, maximums, unit)

main_program()