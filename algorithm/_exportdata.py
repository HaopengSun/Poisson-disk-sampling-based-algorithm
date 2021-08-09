import csv, json

#export CSV file containing positions and radius of particles
def exportdata(Circles):
	with open('position.csv', 'w', newline='') as new_file:
		csv_writer = csv.writer(new_file)
		csv_writer.writerow(['Xcoordination', 'Ycoordination', 'radius'])
		for i in range(len(Circles)):
			csv_writer.writerow([Circles[i].x, Circles[i].y, Circles[i].r])
		print('export csv file')