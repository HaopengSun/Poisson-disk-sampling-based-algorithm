def filter_particles(Circles, maxi, mini = 0):
	power2D = 2
	volume = 0
	pi = 3.1415926
	for i in range(len(Circles)):
		if mini <= Circles[i].r < maxi:
			volume += pi * Circles[i].r ** power2D
	return volume

def particleSieve(Circles, sieve_number, real_volumes, maximums, roundRadius):
	volumes = []

	for _ in range(sieve_number):
		volumes.append(0)
		real_volumes.append(0)

	volumes_reverse = []
	for i in range(len(maximums)):
		if i == 0:
			volume_sieve = filter_particles(Circles, maximums[i], roundRadius[i])
		elif (i != len(maximums) - 1):
			volume_sieve = filter_particles(Circles, roundRadius[i - 1], roundRadius[i])
		else:
			volume_sieve = filter_particles(Circles, roundRadius[i - 1])
		volumes_reverse.append(volume_sieve)
	volumes = volumes_reverse[::-1]

	return volumes