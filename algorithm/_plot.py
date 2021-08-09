import matplotlib.pyplot as plt

def plotCurve(finers, soil_distributions, roundRadius, maximums, unit):
	finers.append(0)
	soil_distributions.append(0)
	roundRadius.insert(0, maximums[0])

	real_radius = []
	for radius in roundRadius:
		real_radius.append(radius * unit)

	plt.title("Particle-size distribution")
	plt.plot(real_radius, finers, linestyle = 'dashed', label='2D model')
	plt.plot(real_radius, soil_distributions, linestyle = 'dotted', label='target soil data')
	plt.xscale('log',base=10)
	plt.xlabel("particle size")
	plt.ylabel("finer percent")
	plt.legend()
	plt.show()
	print(finers, soil_distributions, roundRadius)