from cvrenderer.cvrenderer.shapes.line import Line
from cvrenderer.cvrenderer.shapes.rectangle import Rectangle
from cvrenderer.cvrenderer.scene import Scene
from cvrenderer.cvrenderer.shapes.joint import Joint
import numpy as np

from kinematics import Kinematics

class Quadruped:
	def __init__(self, x = 0, y = 0, z = 0,
					   x_rot = 0, y_rot = 0, 
					   z_rot = 0):
		# Shape.__init__(self, x, y, z, x_rot, y_rot, z_rot)

		self.name = "QUADRUPED"
		self.body_w = 0.099328
		self.body_l = 0.392
		self.l1 = 0.077476
		self.l2 = 0.2115
		self.l3 = 0.2

		self.kine_model = Kinematics()


		self.body = Rectangle(x=0, y=0, z=0.3, w=self.body_w, l=self.body_l, thickness=2)
		
		self.fr_hip = Line(x = self.body_w/2+self.l1/2, y = self.body_l/2, z = 0.3, y_rot = np.pi/2, length = self.l1, thickness=2)
		self.fr_knee = Line(x = self.body_w/2+self.l1, y = self.body_l/2, z = 0.3-self.l2/2, length = self.l2, thickness=2)
		self.fr_calf = Line(x = self.body_w/2+self.l1, y = self.body_l/2, z = 0.3-(self.l3/2+self.l2), length = self.l3, thickness=2)

		self.fl_hip = Line(x = -(self.body_w/2+self.l1/2), y = self.body_l/2, z = 0.3, y_rot = np.pi/2, length = self.l1, thickness=2)
		self.fl_knee = Line(x = -(self.body_w/2+self.l1), y = self.body_l/2, z = 0.3-self.l2/2, length = self.l2, thickness=2)
		self.fl_calf = Line(x = -(self.body_w/2+self.l1), y = self.body_l/2, z = 0.3-(self.l3/2+self.l2), length = self.l3, thickness=2)

		self.rr_hip = Line(x = self.body_w/2+self.l1/2, y = -self.body_l/2, z = 0.3, y_rot = np.pi/2, length = self.l1, thickness=2)
		self.rr_knee = Line(x = self.body_w/2+self.l1, y = -self.body_l/2, z = 0.3-self.l2/2, length = self.l2, thickness=2)
		self.rr_calf = Line(x = self.body_w/2+self.l1, y = -self.body_l/2, z = 0.3-(self.l3/2+self.l2), length = self.l3, thickness=2)

		self.rl_hip = Line(x = -(self.body_w/2+self.l1/2), y = -self.body_l/2, z = 0.3, y_rot = np.pi/2, length = self.l1, thickness=2)
		self.rl_knee = Line(x = -(self.body_w/2+self.l1), y = -self.body_l/2, z = 0.3-self.l2/2, length = self.l2, thickness=2)
		self.rl_calf = Line(x = -(self.body_w/2+self.l1), y = -self.body_l/2, z = 0.3-(self.l3/2+self.l2), length = self.l3, thickness=2)

		self.shapes = [self.body, 
						self.fr_hip, self.fr_knee, self.fr_calf,
						self.fl_hip, self.fl_knee, self.fl_calf,
						self.rr_hip, self.rr_knee, self.rr_calf,
						self.rl_hip, self.rl_knee, self.rl_calf
						]

		self.fr_j1 = Joint(x = self.body_w/2, y =self.body_l/2, z = 0.3, axis = [0, 1, 0], parent = self.body, child = self.fr_hip)
		self.fr_j2 = Joint(x = self.body_w/2+self.l1, y =self.body_l/2, z = 0.3, axis = [1, 0, 0], parent = self.fr_hip, child = self.fr_knee)
		self.fr_j3 = Joint(x = self.body_w/2+self.l1, y =self.body_l/2, z = 0.3-self.l2, axis = [1, 0, 0], parent = self.fr_knee, child = self.fr_calf)

		self.fl_j1 = Joint(x = -self.body_w/2, y =self.body_l/2, z = 0.3, axis = [0, 1, 0], parent = self.body, child = self.fl_hip)
		self.fl_j2 = Joint(x = -(self.body_w/2+self.l1), y =self.body_l/2, z = 0.3, axis = [1, 0, 0], parent = self.fl_hip, child = self.fl_knee)
		self.fl_j3 = Joint(x = -(self.body_w/2+self.l1), y =self.body_l/2, z = 0.3-self.l2, axis = [1, 0, 0], parent = self.fl_knee, child = self.fl_calf)

		self.rr_j1 = Joint(x = self.body_w/2, y =-self.body_l/2, z = 0.3, axis = [0, 1, 0], parent = self.body, child = self.rr_hip)
		self.rr_j2 = Joint(x = self.body_w/2+self.l1, y =-self.body_l/2, z = 0.3, axis = [1, 0, 0], parent = self.rr_hip, child = self.rr_knee)
		self.rr_j3 = Joint(x = self.body_w/2+self.l1, y =-self.body_l/2, z = 0.3-self.l2, axis = [1, 0, 0], parent = self.rr_knee, child = self.rr_calf)

		self.rl_j1 = Joint(x = -self.body_w/2, y =-self.body_l/2, z = 0.3, axis = [0, 1, 0], parent = self.body, child = self.rl_hip)
		self.rl_j2 = Joint(x = -(self.body_w/2+self.l1), y =-self.body_l/2, z = 0.3, axis = [1, 0, 0], parent = self.rl_hip, child = self.rl_knee)
		self.rl_j3 = Joint(x = -(self.body_w/2+self.l1), y =-self.body_l/2, z = 0.3-self.l2, axis = [1, 0, 0], parent = self.rl_knee, child = self.rl_calf)

		self.joints = [
						self.fr_j1, self.fr_j2, self.fr_j3,
						self.fl_j1, self.fl_j2, self.fl_j3,
						self.rr_j1, self.rr_j2, self.rr_j3,
						self.rl_j1, self.rl_j2, self.rl_j3
						]
	def rotate_body(self, ang):
		self.body.rotate(0, 0, ang)
		# self.move_joints()

	def stand_up(self):
		th1, th2, th3 = self.kine_model.IK(0, self.l1, -0.3)
		angles = [
					th1, th2, th3,
					th1, th2, th3,
					th1, th2, th3,
					th1, th2, th3
				]
		self.move_joints(angles)

	def move_joints(self, angles):
		i = 0
		for ang in angles:
			self.joints[i].set_joint_position(ang)
			i += 1
