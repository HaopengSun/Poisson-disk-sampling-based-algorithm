pi = 3.1415926

# the radii of particles with Poisson Disk distribution are equal of the minimum value in the radius range of the largest sieve
def stop_recursion(Circles, roundRadius):
	for i in range(len(Circles)):
		if Circles[i].r > roundRadius[0]:
			return True
	return False

# adjust the volume by adding or minusing the radius by one unit
def adjust_radius(addminus, Circles, roundRadius):
	for i in range(len(Circles)):
		if Circles[i].r > roundRadius[0]:
			Circles[i].r += addminus

def remove_particles(maximum_radius, minimum_radius, Circles):
	remove_particle = []
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r <= maximum_radius:
			remove_particle.append(circle)
	for circle in remove_particle:
		Circles.remove(circle)

# check whether the volume of particles of Poisson Disk distirbution surpasses the target by 2% or reaches the target
def surpass_volume_poisson(multiplication, Circles, ideal_volumes):
	volume_poisson = 0
	for i in range(len(Circles)):
		volume_poisson += pi * Circles[i].r ** 2
	print('volume of Poisson Disk particles', volume_poisson, 'target volume',ideal_volumes[0])
	if volume_poisson > (ideal_volumes[0] * multiplication):
		return True
	return False