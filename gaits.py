import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

class Trot:
	def __init__(self):
		num_traj_pts = 20
		deg = 0
		delta_deg = 180/num_traj_pts

		self.step_length = 0.1
		self.step_height = 0.1

		self.x = []
		self.z = []

		for i in range(num_traj_pts+1):
			val =  np.cos(deg*np.pi/180)*self.step_length 
			self.x.append(val)
			val =  -0.3 + np.sin(deg*np.pi/180)*self.step_height 
			self.z.append(val)
			deg += delta_deg

		self.x.reverse()
		delta = 2*self.step_length / len(self.x)
		temp_x = list(np.clip(np.arange(-self.step_length, self.step_length+delta, delta), -self.step_length, self.step_length))[2:-2]
		temp_x.reverse()
		self.x = self.x + temp_x
		self.y = [0.077476]*len(self.x)
		self.z = self.z + [-0.3]*len(temp_x)

		# plt.scatter(self.x, self.z)
		# plt.show()

		# self.z = [-0.3]*len(self.x)
		# self.z = list(np.linspace(-0.3, -0.2, num_vert_steps))+[-0.2]*len(temp1) + list(np.linspace(-0.2, -0.3, num_vert_steps)) + [-0.3]*len(temp1)


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