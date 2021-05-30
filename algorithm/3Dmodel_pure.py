import random, math, csv, json
import numpy as np

# the dimension of 2D canvas
# one unit in the program presents 0.0125mm and actual size of canvas is 12.5mm * 12.5mm
unit = 0.0125
width = 1000
height = 1000
active = []
pi = 3.1415926

# for the "Poisson Disk Sampling", it is in charge of generating biggest particles with radius from 190 to 95
# this part is still required to adjust manually and there are mainly two parameters to adjust
# minimum distance between points and the maximum radius of circles
r = 400
k = 30
root = 2 ** 0.5
w = r / root

# 5 * 5 grid can roughly locate  minimum circles with radius which is set to be 2
# divide the whole canvan with 5 * 5 grids, because it can roughly contain a minimum circle
w1 = 10

maximums = [95, 47, 23, 11, 5]
roundRadius = [48, 24, 12, 6, 2]

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

#users should input the parameters of the soil in the first place
target_void_ratio = 0.6
sieves = ['4.75-2.36', '2.36-1.18', '1.18-0.6', '0.6-0.3', '0.3-0.15']
soil_distributions = [1, 0.76, 0.70, 0.47, 0.]
ideal_distributions =  [0.24, 0.06, 0.23, 0.18, 0.11, 0.13, 0.03, 0.02]
sieve_number = len(sieves)

# density of  Sand = 0.001631 g/mm³
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
	setup()
	for i in range(len(sieves)):
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

def setup():
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
	poisson()

#generate points of Poisson Disk Sampling
def poisson():

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

	generateCircles_p(ranges[0], maximums[0])

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
							dis = dist(Circles[i].x, Circles[i].y, Circles[j].x, Circles[j].y)
							if dis < (Circles[i].r + Circles[j].r):
								Circles[i].g = None
								growing.remove([Circles[i].x, Circles[i].y])
								break
			Circles[i].grow()

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
	
	if len(gridnum) == 0:
		print('round of infilling:', roundOfInfilling, 'infilling and add:', occupation, totalvolume, ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)
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