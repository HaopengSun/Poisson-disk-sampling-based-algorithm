import csv, math

maxi_position_x = 0
maxi_position_y = 0
maxi_position_z = 0
total_volume = 284599529

with open('3d-yade-deposted-result.txt', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	for line in csv_reader:
		imput = list()
		for element in line:
			newelement = element.split("\t")
			for i in range(4):
				e = float(newelement[i]) / 0.05
				imput.append(math.ceil(e))

		if (imput[0] + imput[3]) > maxi_position_x:
			maxi_position_x = (imput[0] + imput[3])
		if (imput[1] + imput[3]) > maxi_position_y:
			maxi_position_y = (imput[1] + imput[3])
		if (imput[2] + imput[3]) > maxi_position_z:
			maxi_position_z = (imput[2] + imput[3])
	print(maxi_position_x, maxi_position_y, maxi_position_z, total_volume)
	void_ratio = (maxi_position_x * maxi_position_y * maxi_position_z - total_volume) / total_volume
	print(void_ratio)
