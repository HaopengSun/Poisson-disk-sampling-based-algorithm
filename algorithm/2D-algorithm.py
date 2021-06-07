import random, math, csv, json
import numpy as np

# input the parameters
print('Please enter unit size (mm/unit):')
unit = float(input())

print('Please enter canvas width (unit):')
width = int(input())

print('Please enter canvas height (unit):')
height = int(input())

# 4.75, 2.36, 1.18, 0.6, 0.3
print('Please enter sieve sizes (mm):')
sieveSize = input().split(',')
sieves = []

for i in range(len(sieveSize)):
	if i < (len(sieveSize) - 1):
		sieve = sieveSize[i].strip() + '-' + sieveSize[i + 1].strip()
	else:
		sieve = '<' + sieveSize[i].strip()
	sieves.append(sieve)
print('Soil particle size ranges (mm):', sieves)

maximums = []
roundRadius = []
for i in range(len(sieveSize)):
	r = math.ceil(float(sieveSize[i].strip()) / unit)
	if i == 0:
		maximums.append(r)
	elif i == len(sieveSize):
		maximums.append(r)
	else:
		maximums.append(r - 1)
		roundRadius.append(r)
print('Please enter minimum particle radius (unit) (should be an integer greater than 0 and smaller than'+ str(maximums[len(maximums)-1]) +'):')
minimum_radius = int(input())
roundRadius.append(minimum_radius)
print('maximum radius in every sieve:', maximums, 'minimum radius in every sieve:', roundRadius)

soil_distributions = []
ideal_distributions = []
print('Please enter the finer percent:')
finer_percent = input().split(',')
for i in range(len(finer_percent)):
	finer = round(float(finer_percent[i]), 2)
	soil_distributions.append(finer)
	if (i != len(finer_percent) - 1):
		finer1 = round(float(finer_percent[i + 1]), 2)
		ideal_distributions.append(round((finer - finer1), 2))
	else:
		ideal_distributions.append(finer)
print('finer percent:', soil_distributions, 'percent passing for every sieve:', ideal_distributions)

active = []
pi = 3.1415926

# the minimum distance between particles is initially set as the half of the canvas side length
# and then the algorithm will adjust it to ensure the volume of particles in the first sieve is within the acceptable limit
r = 400
k = 30
root = 2 ** 0.5
w = r / root

# divide the whole canvan with 5 * 5 grids, because it can locat the tiny voids to insert the smallest particles
w1 = 5

# only check the particles around the newly-inserted particle
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
occupation8 = 0

# users should input the parameters of the soil in the first place
target_void_ratio = 0.8
# sieves = ['4.75-2.36', '2.36-1.18', '1.18-0.6', '0.6-0.3', '0.3-0.15']
# soil_distributions = [1, 0.92, 0.82, 0.58, 0.14]
# ideal_distributions = [0.08, 0.10, 0.24, 0.44, 0.14]
sieve_number = len(sieves)

# density of Sand = 0.001631 g/mm³
# for mixture soil, the user can add variables for particles with different densities
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
		if i != 0:
			fill_the_void(i, 0, 0, ideal_volumes[i], roundRadius[i], ranges[i], maximums[i])
	list_particles()
	exportdata()

class Circle:
	def __init__(self, x, y, r):
		self.x = x
		self.y = y
		self.r = r
		self.g = True
	
	def grow(self):
		if self.g is True:
			self.r = self.r + 1
	
	def edge(self):
		if ((self.x + self.r) > width) or ((self.x - self.r) < 0) or ((self.y + self.r) > height) or ((self.y - self.r) < 0):
			self.g = None
		return self.g

def setup_poisson():
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
			s = random_vector_function(r, math.floor(r * 2))
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
								d = dist(grid[index][0], grid[index][1], sample[0], sample[1])
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
				Circles.append(Circle(grid[i][0], grid[i][1], roundRadius[0]))
				occupation_poisson = occupation_poisson + 1

	generateCircles_poisson(ranges[0], (maximums[0] - 1))
	print('poisson disk sampling', occupation_poisson)

#particles of "Poisson Disk Sampling" are growing
def generateCircles_poisson(mindis, maxi):
	for k in range(len(Circles)):
		if Circles[k].g is True:
			growing.append([Circles[k].x, Circles[k].y])

	while len(growing) > 0:
		for i in range(len(Circles)):
			if Circles[i].g is True:
				if Circles[i].r >= maxi:
					Circles[i].g = None
					growing.remove([Circles[i].x, Circles[i].y])
					break
				elif Circles[i].edge() is None:
					growing.remove([Circles[i].x, Circles[i].y])
					break
				else:
					for j in range(len(Circles)):
						if (j != i) and ((Circles[i].x - mindis) < Circles[j].x < (Circles[i].x + mindis)) and ((Circles[i].y - mindis) < Circles[j].y < (Circles[i].y + mindis)):
							dis = dist(Circles[i].x, Circles[i].y, Circles[j].x, Circles[j].y)
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
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r < maximum_radius:
			Circles.remove(circle)

# adjust the volume to ensure it is within the acceptable scope
def poisson(r):
	setup_poisson()
	if surpass_volume_poisson(1.02):
		while surpass_volume_poisson(1.02) and stop_recursion():
			adjust_radius(-1)
		if not surpass_volume_poisson(1):
			adjust_radius(1)
	elif not surpass_volume_poisson(1):
		# print("does not reach the target")
		remove_particles(maximums[0], roundRadius[0])
		r = r - 10
		poisson(r)

def fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum):

	gridnum = list(range(0, gridnumbers1))

	for i in range(len(Circles)):
		col_sub = math.floor(Circles[i].x / w1)
		row_sub = math.floor(Circles[i].y / w1)
		numb = col_sub + row_sub * cols1
		grid1[numb] = 1
		gridnum.remove(numb)

	# the loop will stop if the mass of this round of infilling reaches the target or it runs out of void grids
	# the size of divided grids is 5, which can normally covers all round of infilling
	while totalvolume < ideal_volume and len(gridnum) > 0:
		#randomly select a void grid and try to add particles
		q = np.random.randint(len(gridnum))

		if roundRadius != maximum:
			n = radii(gridnum[q], roundRadius, rangeRadius, maximum)
		else:
			n = single_radius(gridnum[q], roundRadius, rangeRadius, maximum)

		if n == 0:
			gridnum.remove(gridnum[q])
		else:
			grid1[q] = 1
			totalvolume = totalvolume + math.floor(3.1415926 * n * n)
			occupation = occupation + 1
			gridnum.remove(gridnum[q])
	
	# if the algorithm checks all non-filled cells but the volume still falls short of the target
	if len(gridnum) == 0:
		print('all non-filled cells checked', 'round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)
	elif totalvolume > ideal_volume * 1.02:
		remove_particles(maximum, roundRadius)
		if (maximum > roundRadius):
			print('volume surpasses the target by 2%', 'round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
			fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, (maximum - 1))
	else:
		print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)

def radii(q, initial_radius, range1, maximum1):

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
				k = dist(x, y, Circles[j].x, Circles[j].y) - Circles[j].r
				if (k < m):
					valid = None
					break
				else:
					min_around.append(k)

    #generate particles
	if valid is True:

		if not min_around:
			min_a = 0
		else:
			min_a = np.amin(min_around)

		if min_a <= min_b:
			if min_a <= maximum1:
				Circles.append(Circle(x, y, min_a))
				return min_a
			else:
				Circles.append(Circle(x, y, maximum1))
				return maximum1
		elif min_a > min_b:
			if min_b <= maximum1:
				Circles.append(Circle(x, y, min_b))
				return min_b
			else:
				Circles.append(Circle(x, y, maximum1))
				return maximum1
	else:
		return 0

# for the last round of infilling, because there is only one possibility, generating particles with radius 2
# the program simplifies the process of "adding particles"
def single_radius(q, initial_radius, range1, maximum1):

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
				k = dist(x, y, Circles[j].x, Circles[j].y) - Circles[j].r
				if (k <  m):
					valid = None
					break

    #generate particles
	if valid is True:
		Circles.append(Circle(x, y, maximum1))
	else:
		return 0

#generate random 3D vector based on given range of magnitude
def random_vector_function(small, big):
	m = random.randrange(small, big, 1)
	angleXY = random.randrange(360)
	coordinationY = math.sin(angleXY) * m
	coordinationX = math.cos(angleXY) * m
	return [math.floor(coordinationX), math.floor(coordinationY)]

#calculate the distance between two points
def dist(x1, y1, x2, y2):
	distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
	return math.floor(distance)

#export CSV file containing positions and radius of particles
def exportdata():
	with open('position.csv', 'w', newline='') as new_file:
		csv_writer = csv.writer(new_file)
		csv_writer.writerow(['Xcoordination', 'Ycoordination', 'radius'])
		for i in range(len(Circles)):
			csv_writer.writerow([Circles[i].x, Circles[i].y, Circles[i].r])
		print('export csv file')

def list_particles():
	global mass
	for _ in range(sieve_number):
		volumes.append(0)
		real_volumes.append(0)

	power2D = 2

	for i in range(len(Circles)):
		if Circles[i].r < 6:
			volumes[0] += pi * Circles[i].r ** power2D
		elif 6 <= Circles[i].r < 12:
			volumes[1] += pi * Circles[i].r ** power2D
		elif 12 <= Circles[i].r < 24:
			volumes[2] += pi * Circles[i].r ** power2D
		elif 24 <= Circles[i].r < 48:
			volumes[3] += pi * Circles[i].r ** power2D
		elif 48 <= Circles[i].r < 95:
			volumes[4] += pi * Circles[i].r ** power2D

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