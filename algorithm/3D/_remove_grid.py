import math
import _distance3d

# omit cells which are fully covered by big spherical particles
def remove_cells(roundRadius, Circles, w1, grid1, cols1, rows1, depths1):
	for i in range(len(Circles)):
		col_sub = math.floor(Circles[i].x / w1)
		row_sub = math.floor(Circles[i].y / w1)
		depth_sub = math.floor(Circles[i].z / w1)
		if Circles[i].r > w1:
			range_circles = math.ceil((Circles[i].r + 2) / w1)
			nums = list(range(-range_circles, range_circles + 1))
			num1s = list(range(-range_circles, range_circles + 1))
			num2s = list(range(-range_circles, range_circles+ 1))
			for num in nums:
				for num1 in num1s:
					for num2 in num2s:
						if 0 <= col_sub + num1 < cols1 and 0 <= row_sub + num < rows1 and 0 <= depth_sub + num2 < depths1:
							index = (col_sub + num1) * depths1 + (row_sub + num) * cols1 * depths1 + (depth_sub + num2)
							y_grid = math.floor(index / cols1 / depths1)
							x_grid = math.floor((index - y_grid * cols1 * depths1) / depths1)
							z_grid = index - x_grid * depths1 - y_grid * cols1 * depths1
							y1 = y_grid * w1
							x1 = x_grid * w1 
							z1 = z_grid * w1  
							# distances of the eight corners of the cell and the particle center
							d1 = _distance3d.dist(x1, y1, z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d2 = _distance3d.dist((x1 + w1), y1, z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d3 = _distance3d.dist(x1, (y1 + w1), z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d4 = _distance3d.dist(x1, y1, (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d5 = _distance3d.dist((x1 + w1), (y1 + w1), z1, Circles[i].x, Circles[i].y, Circles[i].z)
							d6 = _distance3d.dist(x1, (y1 + w1), (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d7 = _distance3d.dist((x1 + w1), y1, (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							d8 = _distance3d.dist((x1 + w1), (y1 + w1), (z1 + w1), Circles[i].x, Circles[i].y, Circles[i].z)
							distance_around = [d1, d2, d3, d4, d5, d6, d7, d8]
							distance_around.sort()
							distance_max = distance_around[6]
							# if the maximum distance is smaller than the particle radius plus the minimun value of the radius range for the next round
							# mark this cell as minus one
							if distance_max <= Circles[i].r + roundRadius:
								grid1[index] = -1
		else:
			# if the particle radius is smaller than the cell size, this cell will be marked as occupied directly
			index = col_sub * depths1 + row_sub * cols1 * depths1 + depth_sub
			grid1[index] = -1
	print("filter the non-filled cells")