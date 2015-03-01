import math

def add(v1,v2): # [1,2] + [3,4] = [4,6]
	rv = []
	i = 0
	while i < len(v1):
		rv.append(v1[i] + v2[i])
		i += 1
	return rv

def ang(v):
	if v == [0,0]:
		return None
	return math.atan2(v[1],v[0])

def angDiff(v1,v2):
	return ang(v2) - ang(v1)

'''def direc(v1,v2): #The direction from v1 to v2 as another (normalized) vector. Uses the assumption that all angles are multiples of 90 degrees.
	vector = [v2[0] - v1[0],v2[1] - v1[1]]
	if vector[0] > 0:
		return [1,0]
	if vector[0] < 0:
		return [-1,0]
	if vector[1] > 0:
		return [0,1]
	if vector[1] < 0:
		return [0,-1]
	else:
		return [0,0]'''

def direc(v1,v2): #The direction from v1 to v2 as another (normalized) vector.
	vector = [v2[0] - v1[0],v2[1] - v1[1]]
	size = math.hypot(vector[0],vector[1])
	return normalize(vector)

def mult(v1,c): #Scalar
	return [v1[0]*c,v1[1]*c]

def normalize(v):
	size = math.hypot(v[0],v[1])
	if size == 0:
		return [0,0]
	else:
		v[0] /= size
		v[1] /= size
	return v


def setLength(v,length):
	if v == [0,0]:
		raise TypeError
	v = normalize(v)
	return [v[0]*length,v[1]*length]
