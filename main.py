from cvrenderer.cvrenderer.scene import Scene
from cvrenderer.cvrenderer.shapes.joint import Joint
from cvrenderer.cvrenderer.camera import Camera
from quadruped import Quadruped

import numpy as np

scene_width = 700
scene_height = 700

scene = Scene(width = scene_width, height = scene_height)

quadruped = Quadruped()

camera = Camera(x = 0, y = 0, z = 5, 
				cx = scene_width//2, cy = scene_height//2, 
				fx = 2000, fy = 2000, 
				x_rot = np.pi/6, z_rot = np.pi/3)

scene.add_camera(camera)
scene.add_axis(scaler=0.1)
scene.add_stick_figure(quadruped)

ang = 0
camera_x = 0
camera_y = 0
camera_z = 7
while True:
	quadruped.move_joints(ang)
	# camera.rotate(np.pi/6, 0, ang/2)
	ang += 0.025
	k = scene.render_scene()
	if k == ord("q"):
		break