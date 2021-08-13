import random, math

#generate random 3D vector based on given range of magnitude
def random_vector_function(small, big):
	m = random.randrange(small, big, 1)
	angleXY = random.randrange(360)
	coordinationY = math.sin(angleXY) * m
	coordinationX = math.cos(angleXY) * m
	return [math.floor(coordinationX), math.floor(coordinationY)]