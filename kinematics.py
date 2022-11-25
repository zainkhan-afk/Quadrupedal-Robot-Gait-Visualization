import numpy as np
from cvrenderer.cvrenderer.utils import *
import matplotlib.pyplot as plt


class LegKinematicsModel:
	def __init__(self):
		self.l1 = 0.077476
		self.l2 = 0.2115
		self.l3 = 0.2

	def IK(self, x, y, z):
		A = np.sqrt(z**2 + y**2)
		alpha2 = np.arcsin(self.l1/A)
		alpha1 = np.pi/2 - alpha2

		alpha3 = np.arctan2(z, y)

		theta1 = alpha1 + alpha3

		thigh_pos = np.array([[0, self.l1*np.cos(theta1), self.l1*np.sin(theta1)]])
		ee_pos = np.array([[x, y, z]])
		thigh_ee = ee_pos - thigh_pos

		R = np.array([
					[1, 0, 0],
					[0, np.cos(theta1), -np.sin(theta1)],
					[0, np.sin(theta1), np.cos(theta1)]
					])
		thigh_ee_ = np.dot(R, thigh_ee.T)

		x_, y_, z_ = thigh_ee[0,0], thigh_ee[0,1], thigh_ee[0,2]
		temp = (x_**2 + z_**2 - self.l2**2 - self.l3**2)/(2*self.l2*self.l3)

		if temp>1:
			temp = 1
		if temp<-1:
			temp = -1

		theta3 = np.arccos(temp)
		theta2 = -np.arctan2(z_, x_) - np.arctan2(self.l3*np.sin(theta3),(self.l2 + self.l3*np.cos(theta3)))

		return theta1, theta2-np.pi/2, theta3

class BodyKinematicsModel:
	def __init__(self):
		self.body_l = 0.099328
		self.body_w = 0.392
		self.leg_origins = np.array([
								[ self.body_w /2,  self.body_l/2, 0], # FL
								[ self.body_w /2, -self.body_l/2, 0], # FR
								[-self.body_w /2,  self.body_l/2, 0], # RL
								[-self.body_w /2, -self.body_l/2, 0]  # RR
								])

		self.T_B_L = []
		for val in self.leg_origins:
			print(val)
			T = np.array([
							[1, 0, 0, val[0]],
							[0, 1, 0, val[1]],
							[0, 0, 1, val[2]],
							[0, 0, 0, 1]
							])
			self.T_B_L.append(T)
	def solve(self, x, y, z, x_rot = 0, y_rot = 0, z_rot = 0):
		pt_L_ee = np.array([
			[x],
			[y],
			[z],
			[1],
			])

		T_rot = get_rotation_matrix(x_rot, y_rot, z_rot)
		T_rot = np.append(T_rot, np.array([[0],[0],[0]]), axis = 1)
		T_rot = np.append(T_rot, np.array([[0, 0, 0, 1]]), axis = 0)
		T_rot = get_inverse_transformation(T_rot)
		
		out_positions = []
		for T_B_L_n in self.T_B_L:
			pt_B_ee_n = T_B_L_n@pt_L_ee
			pt_B_ee_n_corrected = T_rot@pt_B_ee_n

			T_L_B_n = get_inverse_transformation(T_B_L_n)
			pt_L_ee_n_corrected = T_L_B_n@pt_B_ee_n_corrected

			out_positions.append([pt_L_ee_n_corrected.T[0, 0], pt_L_ee_n_corrected.T[0, 1], pt_L_ee_n_corrected.T[0, 2]])

		return out_positions



if __name__ == "__main__":
	BK = BodyKinematicsModel()
	print(BK.body_w, BK.body_l)
	for i in range(-10, 0, 1):
		p1,p2 = BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot = i*np.pi/180)
		x1, y1, z1 = p1
		x2, y2, z2 = p2
		plt.scatter(x1,y1)
		plt.scatter(x2,y2)
	plt.show()
	# BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =           0)[0]
	# BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =     np.pi/2)[0]
	# BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =   3*np.pi/4)[0]
	# BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =     2*np.pi)[0]
	# print(BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =           0)[0])
	# print(BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =     np.pi/2)[0])
	# print(BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =   3*np.pi/4)[0])
	# print(BK.solve(0, 0, -0.3, x_rot = 0, y_rot = 0, z_rot =     2*np.pi)[0])