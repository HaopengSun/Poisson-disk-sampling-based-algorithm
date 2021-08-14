import random, math

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