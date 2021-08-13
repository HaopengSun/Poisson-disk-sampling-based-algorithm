import math
import _distance2d

# omit cells which are fully covered by big spherical particles
# they will not be checked by the next round of particle insertion
def remove_cells(roundRadius, Circles, w1, grid1, cols1, rows1):
	for i in range(len(Circles)):
		col_sub = math.floor(Circles[i].x / w1)
		row_sub = math.floor(Circles[i].y / w1)
		if Circles[i].r > w1:
			range_circles = math.ceil((Circles[i].r + 2) / w1)
			nums = list(range(-range_circles, range_circles + 1))
			num1s = list(range(-range_circles, range_circles + 1))
			for num in nums:
				for num1 in num1s:
					if 0 <= col_sub + num1 < cols1 and 0 <= row_sub + num < rows1:
						index = (col_sub + num1) + (row_sub + num) * cols1
						y_grid = math.floor(index / cols1)
						x_grid = math.floor(index - y_grid * cols1)
						y1 = y_grid * w1
						x1 = x_grid * w1
						# distances of the eight corners of the cell and the particle center
						d1 = _distance2d.dist(x1, y1, Circles[i].x, Circles[i].y)
						d2 = _distance2d.dist((x1 + w1), y1, Circles[i].x, Circles[i].y)
						d3 = _distance2d.dist(x1, (y1 + w1), Circles[i].x, Circles[i].y)
						d4 = _distance2d.dist((x1 + w1), (y1 + w1), Circles[i].x, Circles[i].y)
						distance_around = [d1, d2, d3, d4]
						distance_around.sort()
						distance_max = distance_around[2]
						# if the maximum distance is smaller than the particle radius plus the minimun value of the radius range for the next round
						# mark this cell as minus one
						if distance_max <= Circles[i].r + roundRadius:
							grid1[index] = -1
		else:
			# if the particle radius is smaller than the cell size, this cell will be marked as occupied directly
			index = col_sub + row_sub * cols1
			grid1[index] = -1
	print("filter the non-filled cells")