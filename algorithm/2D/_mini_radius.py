def particles_mini(maximum_radius, minimum_radius, Circles):
	for circle in Circles:
		if circle.r >= minimum_radius and circle.r <= maximum_radius:
			if circle.r != minimum_radius:
				return False
	return True