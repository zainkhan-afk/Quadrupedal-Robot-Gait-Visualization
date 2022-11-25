import numpy as np
import cv2


def leg_IK(x, y, length):
	angle2 = np.arccos((x**2  + y**2 - length**2 - length**2)/(2*length*length))
	angle1 = np.arctan2(y, x) - np.arctan2((length*np.sin(angle2)),(length+length*np.cos(angle2)))
	return angle1+np.pi, angle2

def body_IK(x, y, body_length, angle):
	R = get_R(angle, degrees = False)
	T_rot = np.append(R, np.array([[0,0]]).T, axis = 1)
	T_rot = np.append(T_rot, np.array([[0,0,1]]), axis=0)
	T_rot = get_inverse_transformation(T_rot)
	leg_origins = np.array([
							[-body_length, 0],
							[ body_length, 0],
							])
	p_L_ee = np.array([
						[x],
						[y],
						[1]
					])
	
	out_positions = []
	for leg_origin in leg_origins:
		T_B_L_n = np.array([
						[1, 0, leg_origin[0] ],
						[0, 1, leg_origin[1] ],
						[0, 0,             1 ]
					])
		p_B_ee_n = T_B_L_n@p_L_ee
		p_B_ee_n = T_rot@p_B_ee_n

		T_L_B_n = get_inverse_transformation(T_B_L_n)

		p_L_ee_n = T_L_B_n@p_B_ee_n
		out_positions.append([p_L_ee_n.T[0, 0], p_L_ee_n.T[0, 1]])

	return out_positions

class Leg:
	def __init__(self, x, y, length = 50):
		self.x = x
		self.y = y
		self.length = length

		R1 = get_R(90)
		R2 = get_R(0)
		self.o1 = np.array([
							[self.x, self.y]
							])
		self.o2 = np.array([
							[self.length, 0] 
							])

		self.pts = np.array([
							[0,           0, 1],
							[self.length, 0, 1],
							])

		self.T1 = np.append(R1, self.o1.T, axis = 1)
		self.T1 = np.append(self.T1, np.array([[0,0,1]]), axis=0)

		self.T2 = np.append(R2, self.o2.T, axis = 1)
		self.T2 = np.append(self.T2, np.array([[0,0,1]]), axis=0)

	def draw(self, canvas, T_b_l):
		pts = self.T1@self.pts.T
		pts = (T_b_l@pts).astype("int").T

		cv2.line(canvas, pts[0,:2], pts[1,:2], (255, 0, 0), 2)

		pts = self.T1@self.T2@self.pts.T
		pts = (T_b_l@pts).astype("int").T

		cv2.line(canvas, pts[0,:2], pts[1,:2], (0, 0, 255), 2)

	def move_leg(self, x, y):
		angle1, angle2 = leg_IK(x, y, self.length)
		self.rotate(angle1, angle2, degrees = False)

	def rotate(self, angle1, angle2, degrees = True):
		R1 = get_R(angle1, degrees)
		R2 = get_R(angle2, degrees)
		self.T1 = np.append(R1, self.o1.T, axis = 1)
		self.T1 = np.append(self.T1, np.array([[0,0,1]]), axis=0)

		self.T2 = np.append(R2, self.o2.T, axis = 1)
		self.T2 = np.append(self.T2, np.array([[0,0,1]]), axis=0)

class Robot:
	def __init__(self, x, y, angle):
		self.x 	 = x
		self.y   = y
		R   = get_R(angle)
		self.w   = 50
		self.h   = 10
		self.o   = np.array([
							[self.x, self.y]
							])
		self.pts = np.array([
							[-self.w, -self.h, 1],
							[ self.w, -self.h, 1],
							[ self.w,  self.h, 1],
							[-self.w,  self.h, 1],
							])

		self.leg1  = Leg(x= self.w, y=0)
		self.leg2  = Leg(x=-self.w, y=0)
		
		self.T = np.append(R, self.o.T, axis = 1)
		self.T = np.append(self.T, np.array([[0,0,1]]), axis=0)


	def draw(self, canvas):
		pts = (self.T@self.pts.T).astype("int").T
		for i in range(len(pts)-1):
			pt1 = pts[i,:2]
			pt2 = pts[i+1,:2]
			cv2.line(canvas, pt1, pt2, (0, 255, 0), 2)
		cv2.line(canvas, pts[0,:2], pts[-1,:2], (0, 255, 0), 2)

		self.leg1.draw(canvas, self.T)
		self.leg2.draw(canvas, self.T)

	def stand_up(self):
		self.leg1.move_leg(0, -60)
		self.leg2.move_leg(0, -60)

	def rotate(self, angle, degrees = False):
		R = get_R(angle, degrees)
		self.T = np.append(R, self.o.T, axis = 1)
		self.T = np.append(self.T, np.array([[0,0,1]]), axis=0)
		positions = body_IK(0, -60, self.w, angle)

		self.leg1.move_leg(positions[0][0], positions[0][1])
		self.leg2.move_leg(positions[1][0], positions[1][1])

def get_R(ang, degrees = True):
	if degrees:
		ang = ang/180*np.pi
	R = np.array([
		[np.cos(ang), -np.sin(ang)],
		[np.sin(ang),  np.cos(ang)]
		])
	return R

def get_inverse_transformation(T):
	R = T[0:2, 0:2]
	trans = T[:-1, -1][:, np.newaxis]

	new_R = np.linalg.inv(R)
	new_trans = -new_R@trans

	T = np.append(new_R, new_trans, axis = 1)
	T = np.append(T, np.array([[0, 0, 1]]), axis = 0)

	return T


W = 600
H = 600
robot = Robot(W//2, H//2, 0)

ang = 0
while True:
	canvas = (np.ones((W, H, 3))*255).astype("uint8")
	cv2.line(canvas, (0, H//2+60), (W, H//2+60), (0, 0, 0), 2)
	robot.draw(canvas)
	# robot.stand_up()
	robot.rotate(np.pi/12*np.sin(ang), degrees = False)
	ang += 0.1

	if ang>np.pi*2:
		ang = 0

	cv2.imshow("canvas", canvas)
	k = cv2.waitKey(30)
	if k == ord("q"):
		break