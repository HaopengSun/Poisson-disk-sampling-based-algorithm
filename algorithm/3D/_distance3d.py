import math
#calculate the distance between two points
def dist(x1, y1, x2, y2, z1, z2):
	distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
	return math.floor(distance)