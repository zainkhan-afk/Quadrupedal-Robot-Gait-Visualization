import cv2
import numpy as np

class ContactTimingUI:
	def __init__(self):
		self.W = 600
		self.H = 200
		self.slider_height = self.H//4
		self.canvas = np.zeros((self.H, self.W, 3)).astype("uint8")
		self.slider_percentages = [
									[0.5, 0.5, 0.0],
									[0.0, 0.5, 0.5],
									[0.0, 0.5, 0.5],
									[0.5, 0.5, 0.0],
								  ]
		self.slider_percentages = [
									[0.00, 0.25, 0.75],
									[0.25, 0.25, 0.50],
									[0.50, 0.25, 0.25],
									[0.75, 0.25, 0.00],
								  ]
		self.leg_name = ["Front Left", "Front Right", "Rear Left", "Rear Right"]
		self.slider_positions = []
		self.slider_width = 10
		i = 0
		for slider in self.slider_percentages:
			t1 = int(slider[0]*self.W)
			t2 = int(slider[1]*self.W)
			t3 = int(slider[2]*self.W)

			x1 = t1
			x2 = t1+t2
			y = i*(self.slider_height+2)
			row = [[x1, y, (255, 0, 0)], [x2, y, (255, 0, 0)]]
			self.slider_positions.append(row)
			i += 1
		cv2.namedWindow('Contact Timing Control')
		cv2.setMouseCallback('Contact Timing Control', self.mouse_movement)

		self.click_down = [[False, False],[False, False],[False, False],[False, False]]

	def mouse_movement(self, event, x, y, flags, param):
		i = 0
		for row in self.slider_positions:
			pt1, pt2 = row
			if pt1[0]-self.slider_width//2<x<pt1[0]+self.slider_width//2 and pt1[1]<y<pt1[1]+self.slider_height:
				pt1[-1] = (0, 255, 0)
				if event == cv2.EVENT_LBUTTONDOWN:
					self.click_down[i][0] = True
			else:
				pt1[-1] = (255, 0, 0)

			if pt2[0]-self.slider_width//2<x<pt2[0]+self.slider_width//2 and pt2[1]<y<pt2[1]+self.slider_height:
				pt2[-1] = (0, 255, 0)
				if event == cv2.EVENT_LBUTTONDOWN:
					self.click_down[i][1] = True
			else:
				pt2[-1] = (255, 0, 0)

			if self.click_down[i][0]:
				if x < pt2[0]:
					pt1[0] = x
					if pt1[0]<0:
						pt1[0] = 0
				if event == cv2.EVENT_LBUTTONUP:
					self.click_down[i][0] = False
			if self.click_down[i][1]:
				if pt1[0] < x:
					pt2[0] = x
					if pt2[0]>self.W:
						pt2[0] = self.W
				if event == cv2.EVENT_LBUTTONUP:
					self.click_down[i][1] = False


			self.slider_percentages[i][0] = pt1[0]/self.W
			self.slider_percentages[i][1] = (pt2[0] - pt1[0])/self.W
			self.slider_percentages[i][2] = (self.W - pt2[0])/self.W

			i += 1


	def draw_sliders(self):
		self.canvas = np.zeros((self.H, self.W, 3)).astype("uint8")
		i = 0
		for slider in self.slider_percentages:

			t1 = int(slider[0]*self.W)
			t2 = int(slider[1]*self.W)
			t3 = int(slider[2]*self.W)
			
			y = i*(self.slider_height+2)
			cv2.rectangle(self.canvas, (0, y+1), (t1, y+self.slider_height), (255, 255, 255), -1)
			cv2.rectangle(self.canvas, (t1, y+1), (t1+t2, y+self.slider_height), (0, 0, 0), -1)
			cv2.rectangle(self.canvas, (t1+t2, y+1), (t1+t2+t3, y+self.slider_height), (255, 255, 255), -1)

			row = self.slider_positions[i]
			pt1, pt2 = row

			cv2.rectangle(self.canvas, (pt1[0]-self.slider_width//2, pt1[1]), (pt1[0]+self.slider_width//2, pt1[1]+self.slider_height), pt1[2], -1)
			cv2.rectangle(self.canvas, (pt2[0]-self.slider_width//2, pt2[1]), (pt2[0]+self.slider_width//2, pt2[1]+self.slider_height), pt2[2], -1)

			cv2.putText(self.canvas, self.leg_name[i], (self.W//2, y+self.slider_height//2+10), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 2, cv2.LINE_AA)

			i += 1


	def render(self):
		cv2.imshow('Contact Timing Control', self.canvas)


if __name__ == "__main__":
	CT_UI = ContactTimingUI()
	while True:
		CT_UI.draw_sliders()
		CT_UI.render()
		k = cv2.waitKey(30)
		if k == ord("q"):
			break