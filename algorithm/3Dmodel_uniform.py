import random, math, csv, json
import numpy as np

# one unit in the program presents 0.05mm and actual size of canvas is 40mm * 40mm
unit = 0.05

# the dimension of 3D canvas
width = 800
height = 800
depth = 800

# active list used in the generation of points with Poisson Disk Sampling
active = []
pi = 3.1415926

# the minimum distance between points with Poisson Disk distribution
# it is set as a quarter of the canvas length and then adjusted automatically to ensure the volume 
# of particles with Poisson Disk distribution is within the acceptable range
r = width / 4
k = 30
root = 2 ** 0.5
w = r / root

# cell size of 5 unit * 5 unit can locate void space for minimum circles with radius which is set to be 2
w1 = 5

# the maximum value of the radius range for the particle insertion round
maximums = [95, 47, 23, 11, 5]
# the minimum value of the radius range for the particle insertion round
roundRadius = [48, 24, 12, 6, 2]

# the range of the adjcent particles is to reduce the reseach field and the running time
ranges = []
for maximum in maximums:
	ranges.append(maximum + maximums[0])

grid = []
Circles = []
growing = []
occupation_poisson = 0

# set cells
cols = math.floor(width / w)
rows = math.floor(height / w)
depths = math.floor(depth / w)
gridnumbers = cols * rows * depths

# sett sub-cells
cols1 = math.floor(width / w1)
rows1 = math.floor(height / w1)
depths1 = math.floor(depth / w1)
gridnumbers1 = cols1 * rows1 * depths1
grid1 = list(range(0, gridnumbers1))
void_grid = []
volumes = []
real_volumes = []
masses = []
differences = []
finers = []

#users should input the parameters of the soil in the first place
target_void_ratio = 5
sieves = ['4.75-2.36', '2.36-1.18', '1.18-0.6', '0.6-0.3', '0.3-0.15']
soil_distributions = [1, 0.92, 0.82, 0.58, 0.14]
ideal_distributions = [0.08, 0.10, 0.24, 0.44, 0.14]
sieve_number = len(sieves)

# density of Sand = 0.001631 g/mm³
density = 0.001631

volume = depth * width * height
ideal_totalmass = (volume / (target_void_ratio + 1))

# the ideal volume for each sieve
ideal_volumes = []
ideal_masses = []
for ideal_distribution in ideal_distributions:
	ideal_volume = math.floor(ideal_totalmass * ideal_distribution)
	ideal_volumes.append(ideal_volume)
	ideal_mass = ideal_volume * density * unit ** 3
	ideal_masses.append(ideal_mass)

def main_program():
	# the generation of the points with Poisson Disk Sampling distribution
	poisson(r)
	# generate the remaining round of particles insertion
	for i in range(len(sieves)):
		fill_the_void(i, 0, 0, ideal_volumes[i], roundRadius[i], ranges[i], maximums[i])
	# calculate the statistic results, the particle size distribution and the void ratio
	list_particles()
	# export CSV file which contains the positions and radii of particles
	exportdata()

# 'Sphere' or 'Circle' object
class Circle:
	def __init__(self, x, y, z, r):
		self.x = x
		self.y = y
		self.z = z
		self.r = r
		self.g = True
	
	def grow(self):
		if self.g is True:
			self.r = self.r + 1
	
	def edge(self):
		if ((self.x + self.r) > width) or ((self.x - self.r) < 0) or ((self.y + self.r) > height) or ((self.y - self.r) < 0) or ((self.z + self.r) > depth) or ((self.z - self.r) < 0):
			self.g = None
		return self.g

def setup_poisson():
	
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
	global occupation_poisson
	while len(active) > 0:
		check = np.random.randint(0, len(active))
		found = None
		for n in range(k):
			s = random_vector_function(r, math.floor(r * 1.5))
			sample = []
			for i in range(0, len(s)):
				sample.append(s[i] + active[check][i])

			gcol = math.floor(sample[0] / w)
			grow = math.floor(sample[1] / w)
			gdepth = math.floor(sample[2] / w)
			ggrid = gdepth + gcol * depths + grow * cols * depths

			if gcol > -1 and grow > -1 and gdepth > -1 and gcol < cols and grow < rows and gdepth < depths:
				ok = True
				#check distance between selected point and points in the around grids
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
									d = dist(grid[index][0], grid[index][1], grid[index][2], sample[0], sample[1], sample[2])
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
			if (grid[i][0] < width - 48) and (grid[i][0] > 48) and (grid[i][1] < height - 48) and (grid[i][1] > 48) and (grid[i][2] < depth - 48) and (grid[i][2] > 48):
				Circles.append(Circle(grid[i][0], grid[i][1], grid[i][2], 48))
				occupation_poisson = occupation_poisson + 1
	generateCircles_poisson(ranges[0], maximums[0])

	print('poisson disk sampling', occupation_poisson)

# decide the radii for the particles with Poisson Disk Sampling
def generateCircles_poisson(mindis, maxi):
	for k in range(len(Circles)):
		if Circles[k].g is True:
			growing.append([Circles[k].x, Circles[k].y, Circles[k].z])

	while len(growing) > 0:
		for i in range(len(Circles)):
			if Circles[i].g is True:
				if Circles[i].r > maxi:
					Circles[i].g = None
					growing.remove([Circles[i].x, Circles[i].y, Circles[i].z])
					break
				elif Circles[i].edge() is None:
					growing.remove([Circles[i].x, Circles[i].y, Circles[i].z])
					break
				else:
					for j in range(len(Circles)):
						if (j != i) and ((Circles[i].x - mindis) < Circles[j].x < (Circles[i].x + mindis)) and ((Circles[i].y - mindis) < Circles[j].y < (Circles[i].y + mindis)) and ((Circles[i].z - mindis) < Circles[j].z < (Circles[i].z + mindis)):
							dis = dist(Circles[i].x, Circles[i].y, Circles[i].z, Circles[j].x, Circles[j].y, Circles[j].z)
							if dis < (Circles[i].r + Circles[j].r - 1):
								Circles[i].g = None
								growing.remove([Circles[i].x, Circles[i].y, Circles[i].z])
								break
			Circles[i].grow()

# check whether the volume of particles of Poisson Disk distirbution surpasses the target by 2% or reaches the target
def surpass_volume_poisson(multiplication):
	volume_poisson = 0
	for i in range(len(Circles)):
		volume_poisson += 4 / 3 * pi * Circles[i].r ** 3
	surpass_percentage = (volume_poisson - ideal_volumes[0]) / ideal_volumes[0]
	print('volume', volume_poisson, 'target volume', ideal_volumes[0], 'percentage', surpass_percentage)
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

# remove the particles and rerun the particle insertion function
def remove_particles(maximum_radius, minimum_radius):
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r < maximum_radius:
			Circles.remove(circle)

# adjust the volume to ensure it is within the acceptable scope using the minimum distance
def poisson(r):
	setup_poisson()
	if surpass_volume_poisson(1.02):
		print('volume surpasses the target by more than 2%, the algorithm shrinks the radius')
		while surpass_volume_poisson(1.02) and stop_recursion():
			adjust_radius(-1)
		if not surpass_volume_poisson(1):
			adjust_radius(1)
	elif not surpass_volume_poisson(1):
		print("volume does not reach the target")
		remove_particles(maximums[0], roundRadius[0])
		r = r - 10
		poisson(r)

# omit cells which are fully covered by big spherical particles
# they will not be checked by the next round of particle insertion
def remove_cells(roundRadius):
	for i in range(len(Circles)):
		col_sub = math.floor(Circles[i].x / w1)
		row_sub = math.floor(Circles[i].y / w1)
		depth_sub = math.floor(Circles[i].z / w1)
		if Circles[i].r > w1:
			range_circles = math.ceil((Circles[i].r + 2) / w1)
			nums = list(range(-range_circles, range_circles + 1))
			num1s = list(range(-range_circles, range_circles + 1))
			num2s = list(range(-range_circles, range_circles+ 1))
			for num in nums:
				for num1 in num1s:
					for num2 in num2s:
						if 0 <= col_sub + num1 < cols1 and 0 <= row_sub + num < rows1 and 0 <= depth_sub + num2 < depths1:
							index = (col_sub + num1) * depths1 + (row_sub + num) * cols1 * depths1 + (depth_sub + num2)
							y_grid = math.floor(index / cols1 / depths1)
							x_grid = math.floor((index - y_grid * cols1 * depths1) / depths1)
							z_grid = index - x_grid * depths1 - y_grid * cols1 * depths1
							y1 = y_grid * w1
							x1 = x_grid * w1 
							z1 = z_grid * w1  
							# distances of the eight corners of the cell and the particle center
							d1 = dist(x1, y1, z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d2 = dist((x1 + w1), y1, z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d3 = dist(x1, (y1 + w1), z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d4 = dist(x1, y1, (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d5 = dist((x1 + w1), (y1 + w1), z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d6 = dist(x1, (y1 + w1), (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d7 = dist((x1 + w1), y1, (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d8 = dist((x1 + w1), (y1 + w1), (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							distance_around = [d1, d2, d3, d4, d5, d6, d7, d8]
							distance_around.sort()
							distance_max = distance_around[6]
							# if the maximum distance is smaller than the particle radius plus the minimun value of the radius range for the next round
							# mark this cell as minus one
							if distance_max <= Circles[i].r + roundRadius:
								grid1[index] = -1
		else:
			# if the particle radius is smaller than the cell size, this cell will be marked as occupied directly
			index = col_sub * depths1 + row_sub * cols1 * depths1 + depth_sub
			grid1[index] = -1
	print("filter the non-filled cells")

def fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum):

	# reset the sub-cell
	grid1 = list(range(0, gridnumbers1))

	# eliminate the filly covered cells
	remove_cells(roundRadius)

	# conclude an array of the numbers of all non-filled cells
	void_grid = []
	non_filled_cells = 0
	for i in range(gridnumbers1):
		if grid1[i] != -1:
			void_grid.append(grid1[i])
			non_filled_cells = non_filled_cells + 1
	gridnum = void_grid

	# the loop will stop if the mass of this round of infilling reaches the target or it runs out of void grids
	# the size of divided grids is 5, which can normally covers all round of infilling
	while totalvolume < ideal_volume and len(gridnum) > 0:
		#randomly select a void grid and try to add particles
		q = np.random.randint(len(gridnum))

		if roundRadius != maximum:
			n = radii(gridnum[q], roundRadius, rangeRadius, maximum)
		else:
			n = radius_single(gridnum[q], roundRadius, rangeRadius, maximum)

		if n == 0:
			# the randomly selected point inside the non-filled cell is invalid
			gridnum.remove(gridnum[q])
		else:
			grid1[q] = 1
			totalvolume = totalvolume + math.floor((4 / 3) * pi * n ** 3)
			occupation = occupation + 1
			gridnum.remove(gridnum[q]) 
			print(len(gridnum), totalvolume, ideal_volume)
	
	# if the function ends due to running out of all non-filled cells instead of reaching the target
	# the function will rerun in an attemp to add more particles
	if len(gridnum) == 0:
		print('void-filling round:', roundOfInfilling, ', insert:', occupation, 'particles, volume:', totalvolume, ', target volume:', ideal_volume)
		fill_the_void(roundOfInfilling, totalvolume, occupation, ideal_volume, roundRadius, rangeRadius, maximum)
	else:
		print('void-filling round:', roundOfInfilling, ', insert:', occupation, 'particles, volume:', totalvolume, ', target volume:', ideal_volume)

# after a valid point being found successfully
# this function is incharge of deciding the particle radius
def radii(q, initial_radius, range1, maximum1):

	global occupation1
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

    #in the reseaching sphere area with 'range1' radius
	min_around = []
	if valid is True:
		for j in range(len(Circles)):
			if ((x - range1) < Circles[j].x < (x + range1)) and ((y - range1) < Circles[j].y < (y + range1)) and ((z - range1) < Circles[j].z < (z + range1)):
				k = dist(x, y, z, Circles[j].x, Circles[j].y, Circles[j].z) - Circles[j].r
				if (k < m):
					valid = None
					break
				else:
					min_around.append(k)
			else:
				min_around.append(maximum1)

    # find the particle radius and add this newly generated particle in the 'Circles' array
	if valid is True:
		min_a = np.amin(min_around)
		if min_a <= min_b:
			if min_a <= maximum1:
				Circles.append(Circle(x, y, z, min_a))
				return min_a
			else:
				Circles.append(Circle(x, y, z, maximum1))
				return maximum1
		elif min_a > min_b:
			if min_b <= maximum1:
				Circles.append(Circle(x, y, z, min_b))
				return min_b
			else:
				Circles.append(Circle(x, y, z, maximum1))
				return maximum1
	else:
		return 0

# to reduce the running time, if the maximum radius and initial radius are equal,
# the function does not need to decide the radius because it is pre-decided by the initial radius
def radius_single(q, initial_radius, range1, maximum1):

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
		return 0


	#in the reseaching sphere area with 'mindis' radius
	if valid is True:
		for j in range(len(Circles)):
			if ((x - range1) < Circles[j].x < (x + range1)) and ((y - range1) < Circles[j].y < (y + range1)) and ((z - range1) < Circles[j].z < (z + range1)):
				k = dist(x, y, z, Circles[j].x, Circles[j].y, Circles[j].z) - Circles[j].r
				if (k < m):
					return 0

    #generate particles:
	Circles.append(Circle(x, y, z, m))
	return m

#generate random 3D vector based on given range of magnitude
def random_vector_function(small, big):
	m = random.randrange(small, big, 1)
	angleXY = random.randrange(360)
	coordinationY = math.sin(angleXY) * m
	k = math.cos(angleXY) * m
	angleZ = random.randrange(360)
	coordinationX = round(math.cos(angleZ) * k)
	coordinationZ = round(math.sin(angleZ) * k)
	return [math.floor(coordinationX), math.floor(coordinationY), math.floor(coordinationZ)]

#calculate the distance between two points
def dist(x1, y1, z1, x2, y2, z2):
	distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
	return math.floor(distance)

#export CSV file containing positions and radius of particles
def exportdata():
	with open('position.csv', 'w', newline='') as new_file:
		csv_writer = csv.writer(new_file)
		csv_writer.writerow(['Xcoordination', 'Ycoordination', 'Zcoordination', 'radius'])
		for i in range(len(Circles)):
			csv_writer.writerow([Circles[i].x, Circles[i].y, Circles[i].z, Circles[i].r])
		print('export csv file')

def list_particles():
	global mass
	for _ in range(sieve_number):
		volumes.append(0)
		real_volumes.append(0)

	for i in range(len(Circles)):
		if Circles[i].r < 6:
			volumes[0] += (4 / 3) * pi * Circles[i].r ** 3
		elif 6 <= Circles[i].r < 12:
			volumes[1] += (4 / 3) * pi * Circles[i].r ** 3
		elif 12 <= Circles[i].r < 24:
			volumes[2] += (4 / 3) * pi * Circles[i].r ** 3
		elif 24 <= Circles[i].r < 48:
			volumes[3] += (4 / 3) * pi * Circles[i].r ** 3
		elif 48 <= Circles[i].r < 95:
			volumes[4] += (4 / 3) * pi * Circles[i].r ** 3

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
				finers[i] += volumes[j]
		finers[i] = round(finers[i] / totalvolume, 4)
	finers.reverse()
	volumes.reverse()
	real_volumes.reverse()

	for volume in real_volumes:
		masses.append(volume * density)
	for i in range(len(masses)):
		differences.append(masses[i] - ideal_masses[i])
	for i in range(sieve_number):
		print('sieve:', sieves[i], 'finer:', finers[i], 'target volume:', ideal_volumes[i], 'volume:', volumes[i], 'mass:', masses[i], 'target mass:', ideal_masses[i])
	print('void ratio:', voidratio,'totalmass:', totalmass, 'totalvolume', totalvolume)

main_program()

