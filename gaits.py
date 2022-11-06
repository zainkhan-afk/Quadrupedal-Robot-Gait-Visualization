class Trot:
	def __init__(self):
		self.x1 = [0,   -0.05, -0.1, -0.1, -0.05,   0,  0.05,  0.1,  0.1, 0.05]
		self.y1 = [0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476]
		self.z1 = [-0.3,  -0.3, -0.3, -0.2,  -0.2, -0.2, -0.2, -0.2, -0.3, -0.3]

		self.x2 = [  0,  0.05,  0.1,  0.1, 0.05, 0,   -0.05, -0.1, -0.1, -0.05]
		self.y2 = [0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476, 0.077476]
		self.z2 = [-0.2, -0.2, -0.2, -0.3, -0.3, -0.3,  -0.3, -0.3, -0.2,  -0.2]


	def get_leg_positions(self, i):
		fl_x = self.x1[i]
		fl_y = self.y1[i]
		fl_z = self.z1[i]

		fr_x = self.x2[i]
		fr_y = self.y2[i]
		fr_z = self.z2[i]

		rl_x = self.x1[i]
		rl_y = self.y1[i]
		rl_z = self.z1[i]


		rr_x = self.x2[i]
		rr_y = self.y2[i]
		rr_z = self.z2[i]

		all_leg_positions = [
							[fl_x, fl_y, fl_z],
							[fr_x, fr_y, fr_z],
							[rl_x, rl_y, rl_z],
							[rr_x, rr_y, rr_z],
							]
		i += 1
		if i>=len(self.x1):
			i = 0
		return all_leg_positions, i