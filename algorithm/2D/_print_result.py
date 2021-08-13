def printResult(real_volumes, density, ideal_masses, sieve_number, sieves, finers, ideal_volumes, volumes, voidratio, totalmass, totalvolume):

	masses = []
	differences = []

	for volume in real_volumes:
		masses.append(volume * density)
	for i in range(len(masses)):
		differences.append(masses[i] - ideal_masses[i])
	for i in range(sieve_number):
		print('sieve:', sieves[i], 'finer:', finers[i], 'ideal volumes:', ideal_volumes[i], 'volume:', volumes[i], 'ideal mass:', ideal_masses[i], 'mass:', masses[i], 'difference:', differences[i])
	print('void ratio:', voidratio,'totalmass:', totalmass, 'totalvolume', totalvolume)