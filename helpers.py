import numpy as np

def almost_equal(p1, p2, thresh = 1e-5):
	if abs(p1 - p2)<thresh:
		return True
	return False