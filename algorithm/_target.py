import math

def targetVolumes(ideal_distributions, ideal_totalmass):
	ideal_volumes = []
	for ideal_distribution in ideal_distributions:
		ideal_volume = math.floor(ideal_totalmass * ideal_distribution)
		ideal_volumes.append(ideal_volume)
	return ideal_volumes

def targetMasses(ideal_distributions, ideal_totalmass, density, unit):
	ideal_masses = []
	for ideal_distribution in ideal_distributions:
		ideal_volume = math.floor(ideal_totalmass * ideal_distribution)
		ideal_mass = ideal_volume * density * unit ** 2
		ideal_masses.append(ideal_mass)
	return ideal_masses