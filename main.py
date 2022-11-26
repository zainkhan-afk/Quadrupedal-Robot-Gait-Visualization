from cvrenderer.cvrenderer.scene import Scene
from cvrenderer.cvrenderer.shapes.joint import Joint
from cvrenderer.cvrenderer.camera import Camera
from quadruped import Quadruped

import numpy as np

scene_width = 700
scene_height = 700

scene = Scene(width = scene_width, height = scene_height, save_as_video = False)

quadruped = Quadruped()

camera = Camera(x = 0, y = 0, z = 5, 
				cx = scene_width//2, cy = scene_height//2, 
				width = scene_width, height = scene_height,
				x_rot = np.pi/6, z_rot = -np.pi/4,
				fov_x = 30, fov_y = 30)
# camera = Camera(x = 0, y = 0, z = 2, 
# 				cx = scene_width//2, cy = scene_height//2, 
# 				width = scene_width, height = scene_height,
# 				x_rot = 0, z_rot =2*np.pi/2,
# 				fov_x = 60, fov_y = 60)

scene.add_camera(camera)
scene.add_axis(size = 25, scaler=0.15)
scene.add_stick_figure(quadruped)

ang = 0
rot_axis = 0
camera_x = 0
camera_y = 0
camera_z = 7
quadruped.stand_up()
while True:
	quadruped.walk()
	# if rot_axis == 0:
	# 	quadruped.rotate_body(x_rot = np.pi/9*np.sin(ang))
	# if rot_axis == 1:
	# 	quadruped.rotate_body(y_rot = np.pi/9*np.sin(ang))
	# if rot_axis == 2:
	# 	quadruped.rotate_body(z_rot = np.pi/9*np.sin(ang))
	scene.move_axis(delta_x = -quadruped.robot_translation)
	# camera.rotate(x_rot = np.pi/6, y_rot = 0, z_rot = ang)
	ang += 0.025
	if ang>2*np.pi:
		ang = 0
		rot_axis += 1

	if rot_axis == 3:
		rot_axis = 0
	k = scene.render_scene()
	if k == ord("q"):
		break