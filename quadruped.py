from cvrenderer.cvrenderer.shapes.line import Line
from cvrenderer.cvrenderer.shapes.rectangle import Rectangle
from cvrenderer.cvrenderer.shapes.cube import Cube
from cvrenderer.cvrenderer.scene import Scene
from cvrenderer.cvrenderer.shapes.joint import Joint
import numpy as np

from kinematics import LegKinematicsModel
from gaits import Trot

class Quadruped:
	def __init__(self, x = 0, y = 0, z = 0,
					   x_rot = 0, y_rot = 0, 
					   z_rot = 0):
		# Shape.__init__(self, x, y, z, x_rot, y_rot, z_rot)

		self.body_initial_height = 0.3
		self.robot_x = 0
		self.robot_y = 0
		self.name = "QUADRUPED"
		self.body_w = 0.099328
		self.body_l = 0.392
		self.l1 = 0.077476
		self.l2 = 0.2115
		self.l3 = 0.2

		self.kine_model = LegKinematicsModel()
		self.trot = Trot()
		self.gait_idx = 0

		self.leg_thickness = 5
		self.leg_color = (0, 0, 0)

		self.leg_prev = [None, None, None, None]

		self.body = Cube(x=0, y=0, z=self.body_initial_height, h=self.body_l, w=self.body_w, l=self.body_w/2, thickness=2)
		
		self.fr_hip = Line(x = self.body_w/2+self.l1/2, y = self.body_l/2, z = self.body_initial_height, 
							y_rot = np.pi/2, length = self.l1, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.fr_knee = Line(x = self.body_w/2+self.l1, y = self.body_l/2, z = self.body_initial_height-self.l2/2, 
							length = self.l2, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.fr_calf = Line(x = self.body_w/2+self.l1, y = self.body_l/2, z = self.body_initial_height-(self.l3/2+self.l2), 
							length = self.l3, thickness=self.leg_thickness, color=self.leg_color)

		self.fl_hip = Line(x = -(self.body_w/2+self.l1/2), y = self.body_l/2, z = self.body_initial_height, 
							y_rot = np.pi/2, length = self.l1, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.fl_knee = Line(x = -(self.body_w/2+self.l1), y = self.body_l/2, z = self.body_initial_height-self.l2/2, 
							length = self.l2, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.fl_calf = Line(x = -(self.body_w/2+self.l1), y = self.body_l/2, z = self.body_initial_height-(self.l3/2+self.l2), 
							length = self.l3, thickness=self.leg_thickness, color=self.leg_color)

		self.rr_hip = Line(x = self.body_w/2+self.l1/2, y = -self.body_l/2, z = self.body_initial_height, 
							y_rot = np.pi/2, length = self.l1, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.rr_knee = Line(x = self.body_w/2+self.l1, y = -self.body_l/2, z = self.body_initial_height-self.l2/2, 
							length = self.l2, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.rr_calf = Line(x = self.body_w/2+self.l1, y = -self.body_l/2, z = self.body_initial_height-(self.l3/2+self.l2), 
							length = self.l3, thickness=self.leg_thickness, color=self.leg_color)

		self.rl_hip = Line(x = -(self.body_w/2+self.l1/2), y = -self.body_l/2, z = self.body_initial_height, 
							y_rot = np.pi/2, length = self.l1, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.rl_knee = Line(x = -(self.body_w/2+self.l1), y = -self.body_l/2, z = self.body_initial_height-self.l2/2, 
							length = self.l2, 
							thickness=self.leg_thickness, color=self.leg_color)
		self.rl_calf = Line(x = -(self.body_w/2+self.l1), y = -self.body_l/2, z = self.body_initial_height-(self.l3/2+self.l2), 
							length = self.l3, thickness=self.leg_thickness, color=self.leg_color)

		self.shapes = [self.body, 
						self.fl_hip, self.fl_knee, self.fl_calf,
						self.fr_hip, self.fr_knee, self.fr_calf,
						self.rl_hip, self.rl_knee, self.rl_calf,
						self.rr_hip, self.rr_knee, self.rr_calf
						]

		self.fr_j1 = Joint(x = self.body_w/2, y =self.body_l/2, z = self.body_initial_height, axis = [0, 1, 0], parent = self.body, child = self.fr_hip)
		self.fr_j2 = Joint(x = self.body_w/2+self.l1, y =self.body_l/2, z = self.body_initial_height, axis = [1, 0, 0], parent = self.fr_hip, child = self.fr_knee)
		self.fr_j3 = Joint(x = self.body_w/2+self.l1, y =self.body_l/2, z = self.body_initial_height-self.l2, axis = [1, 0, 0], parent = self.fr_knee, child = self.fr_calf)

		self.fl_j1 = Joint(x = -self.body_w/2, y =self.body_l/2, z = self.body_initial_height, axis = [0, 1, 0], parent = self.body, child = self.fl_hip)
		self.fl_j2 = Joint(x = -(self.body_w/2+self.l1), y =self.body_l/2, z = self.body_initial_height, axis = [1, 0, 0], parent = self.fl_hip, child = self.fl_knee)
		self.fl_j3 = Joint(x = -(self.body_w/2+self.l1), y =self.body_l/2, z = self.body_initial_height-self.l2, axis = [1, 0, 0], parent = self.fl_knee, child = self.fl_calf)

		self.rr_j1 = Joint(x = self.body_w/2, y =-self.body_l/2, z = self.body_initial_height, axis = [0, 1, 0], parent = self.body, child = self.rr_hip)
		self.rr_j2 = Joint(x = self.body_w/2+self.l1, y =-self.body_l/2, z = self.body_initial_height, axis = [1, 0, 0], parent = self.rr_hip, child = self.rr_knee)
		self.rr_j3 = Joint(x = self.body_w/2+self.l1, y =-self.body_l/2, z = self.body_initial_height-self.l2, axis = [1, 0, 0], parent = self.rr_knee, child = self.rr_calf)

		self.rl_j1 = Joint(x = -self.body_w/2, y =-self.body_l/2, z = self.body_initial_height, axis = [0, 1, 0], parent = self.body, child = self.rl_hip)
		self.rl_j2 = Joint(x = -(self.body_w/2+self.l1), y =-self.body_l/2, z = self.body_initial_height, axis = [1, 0, 0], parent = self.rl_hip, child = self.rl_knee)
		self.rl_j3 = Joint(x = -(self.body_w/2+self.l1), y =-self.body_l/2, z = self.body_initial_height-self.l2, axis = [1, 0, 0], parent = self.rl_knee, child = self.rl_calf)

		self.joints = [
						self.fl_j1, self.fl_j2, self.fl_j3,
						self.fr_j1, self.fr_j2, self.fr_j3,
						self.rl_j1, self.rl_j2, self.rl_j3,
						self.rr_j1, self.rr_j2, self.rr_j3
						]
	def rotate_body(self, ang):
		self.body.rotate(0, 0, ang)
		# self.move_joints()

	def stand_up(self):
		th1, th2, th3 = self.kine_model.IK(0, self.l1, -self.body_initial_height)
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

	def walk(self):
		leg_positions, self.gait_idx = self.trot.get_leg_positions(self.gait_idx)
		joint_positions = []

		max_z_height = 0
		y_movement = 0


		idx = 0
		for leg_pos in leg_positions:
			th1, th2, th3 = self.kine_model.IK(leg_pos[0], leg_pos[1], leg_pos[2])
			joint_positions.append(th1)
			joint_positions.append(th2)
			joint_positions.append(th3)

			if leg_pos[2]<max_z_height:
				max_z_height = leg_pos[2]
				y_movement

			if self.leg_prev[idx] is None:
				self.leg_prev[idx] = leg_pos[0]

			diff = leg_pos[0] - self.leg_prev[idx]
			self.leg_prev[idx] = leg_pos[0]
			if diff>0:
				y_movement = diff

			idx += 1

		self.body.translate(0, self.robot_y, -max_z_height)
		self.robot_y += y_movement

		self.move_joints(joint_positions)