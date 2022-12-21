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


class TimingGait:
	def __init__(self, Tg):
		self.x_fl = []
		self.y_fl = []
		self.z_fl = []

		self.num_pts = 100

		self.Tg = Tg
		self.t = 0
		self.segment_t = [0,0,0,0]
		self.delta_t = self.Tg/self.num_pts

		self.step_length = 0.1
		self.step_height = 0.1

	def calculate_leg_i_position(self, leg_contact_timing):
		'''
		t0___________t1------------t2__________T
		leg_contact_timing: [t1 - t0, t2 - t1, T - t2]
		'''
		leg_t_seg1 = leg_contact_timing[0]*self.Tg
		leg_t_seg2 = leg_t_seg1 + leg_contact_timing[1]*self.Tg
		leg_t_seg3 = leg_t_seg2 + leg_contact_timing[2]*self.Tg


		leg_t_swing = leg_contact_timing[1]*self.Tg
		leg_t_stance= leg_contact_timing[0]*self.Tg + leg_contact_timing[2]*self.Tg

		leg_freq_swing = (1/leg_contact_timing[1]*self.Tg)/4

		y = 0.077476

		if 0 <= self.t < leg_t_seg1: # Leg stance
			seg_t = self.t
			x =  (leg_contact_timing[2]*self.Tg + seg_t)/leg_t_stance*self.step_length*2 - self.step_length
			z = -0.3

		elif leg_t_seg2 <= self.t <= self.Tg: # Leg stance
			seg_t = self.t - leg_t_seg2
			x =  seg_t/leg_t_stance*self.step_length*2 - self.step_length
			z = -0.3

		elif leg_t_seg1 <= self.t < leg_t_seg2: # Leg swinging
			seg_t = self.t - leg_t_seg1
			val =  np.cos(np.pi*leg_freq_swing*seg_t)*self.step_length 
			x = val
			val =  -0.3 + np.sin(np.pi*leg_freq_swing*seg_t)*self.step_height 
			z = val

		return -x, y, z

	def calculate_leg_positions(self, contact_timing_matrix):
		leg_positions = []
		for i in range(4):
			x, y, z = self.calculate_leg_i_position(contact_timing_matrix[i])
			leg_positions.append([x, y, z])

		self.t         += self.delta_t
		if self.t >= self.Tg:
			self.t = 0
			# exit()

		return leg_positions

if __name__ == "__main__":
	contact_timing_matrix = [
								[0.0, 0.5, 0.5],
								[0.5, 0.5, 0.0],
								[0.0, 0.5, 0.5],
								[0.5, 0.5, 0.0]
							]
	tg = TimingGait(1)
	while True:
		tg.calculate_leg_positions(contact_timing_matrix)