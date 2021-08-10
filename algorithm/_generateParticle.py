#particles of "Poisson Disk Sampling" are growing
def generateCircles_p(mindis, maxi, Circles):
	growing = []
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
							dis = _distance2d.dist(Circles[i].x, Circles[i].y, Circles[j].x, Circles[j].y)
							if dis < (Circles[i].r + Circles[j].r):
								Circles[i].g = None
								growing.remove([Circles[i].x, Circles[i].y])
								break
			Circles[i].grow()