class Sphere:
	def __init__(self, x, y, z, r, width, height, depth):
		self.x = x
		self.y = y
		self.r = r
		self.z = z
		self.width = width
		self.height = height
		self.depth = depth
		self.g = True
	
	def grow(self):
		if self.g is True:
			self.r = self.r + 1
	
	def edge(self):
		if ((self.x + self.r) > self.width) or ((self.x - self.r) < 0) or ((self.y + self.r) > self.height) or ((self.y - self.r) < 0) or ((self.z + self.r) > self.depth) or ((self.z - self.r) < 0):
			self.g = None
		return self.g