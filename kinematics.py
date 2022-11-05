import numpy as np

class Kinematics:
	def __init__(self):
		self.l1 = 0.077476
		self.l2 = 0.2115
		self.l3 = 0.2

	def IK(self, x, y, z):
		A = np.sqrt(z**2 + y**2)
		alpha2 = np.arcsin(self.l1/A)
		alpha1 = np.pi - (np.pi/2 + alpha2)

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
		theta2 = np.arctan2(z_, x_) - np.arctan2(self.l3*np.sin(theta3),(self.l2 + self.l3*np.cos(theta3)))+np.pi/2

		return theta1, theta2, theta3