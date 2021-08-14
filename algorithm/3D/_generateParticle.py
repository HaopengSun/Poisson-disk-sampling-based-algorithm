import _distance3d

#particles of "Poisson Disk Sampling" are growing
def generateCircles_p(mindis, maxi, Circles):
	growing = []

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
							dis = _distance3d.dist(Circles[i].x, Circles[i].y, Circles[i].z, Circles[j].x, Circles[j].y, Circles[j].z)
							if dis < (Circles[i].r + Circles[j].r - 1):
								Circles[i].g = None
								growing.remove([Circles[i].x, Circles[i].y, Circles[i].z])
								break
			Circles[i].grow()