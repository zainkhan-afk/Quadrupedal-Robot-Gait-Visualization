import numpy as np

class Trot:
	def __init__(self):
		delta = 0.01
		num_vert_steps = 25
		temp1 = list(np.arange(-0.1, 0.1+delta, delta))
		temp2 = sorted(list(np.arange(-0.1, 0.1+delta, delta)), reverse=True)
		self.x = [-0.1]*num_vert_steps + temp1 + [0.1]*num_vert_steps + temp2
		self.y = [0.077476]*len(self.x)
		self.z = list(np.linspace(-0.3, -0.2, num_vert_steps))+[-0.2]*len(temp1) + list(np.linspace(-0.2, -0.3, num_vert_steps)) + [-0.3]*len(temp1)


	def get_leg_positions(self, i):
		leg_idx1 = i + len(self.x)//4
		leg_idx2 = i + 3*len(self.x)//4

		if leg_idx1>=len(self.x):
			leg_idx1 = leg_idx1 - len(self.x)

		if leg_idx2>=len(self.x):
			leg_idx2 = leg_idx2 - len(self.x)

		fl_x = self.x[leg_idx1]
		fl_y = self.y[leg_idx1]
		fl_z = self.z[leg_idx1]

		fr_x = self.x[leg_idx2]
		fr_y = self.y[leg_idx2]
		fr_z = self.z[leg_idx2]

		rl_x = self.x[leg_idx2]
		rl_y = self.y[leg_idx2]
		rl_z = self.z[leg_idx2]


		rr_x = self.x[leg_idx1]
		rr_y = self.y[leg_idx1]
		rr_z = self.z[leg_idx1]

		all_leg_positions = [
							[fl_x, fl_y, fl_z],
							[fr_x, fr_y, fr_z],
							[rl_x, rl_y, rl_z],
							[rr_x, rr_y, rr_z],
							]
		i += 1
		if i>=len(self.x):
			i = 0
		return all_leg_positions, i