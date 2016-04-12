import copy
import math
import os
import pygame
import random

def angleDiff(ang1,ang2):
	'''Difference between pi*1.9 and pi*.1 is pi*.2.'''
	while ang2 < ang1:
		ang2 += 2*math.pi
	while ang1 < ang2:
		ang1 += math.pi*2
	return min(ang1 - ang2, abs(ang1 - ang2 - 2*math.pi)) #Take the least of the distances moving left/right around the circle

def angleSide(ang1,ang2):
	'''If ang1 left or right of ang2?'''
	#Test left distance; if >pi, return right
	while ang2 < ang1:
		ang2 += 2*math.pi
	while ang1 < ang2:
		ang1 += 2*math.pi
	leftDistance = ang1 - ang2
	if leftDistance <= math.pi:
		return 'left'
	else:
		return 'right'

def normalAngle(ang):
	#Sets 0<=ang<2pi
	while ang < 0:
		ang += 2*math.pi
	while ang >= 2*math.pi:
		ang -= 2*math.pi
	return ang

def circleOf(obj,num,center,rad,startAng=0):
	l = []
	ang = startAng
	while ang < startAng + math.pi*2:
		o = obj.copy()
		o.realX = center[0] + rad*math.cos(ang)
		o.realY = center[1] + rad*math.sin(ang)
		l.append(o)
		ang += math.pi*2/num
	return l

def changeRectSize(rect,size):
	c = rect.center
	r = rect.move(0,0)
	r.width = size[0]
	r.height = size[1]
	r.center = c
	return r

def containRectInRect(r1,r2):
	#Assumes r1 is smaller than r2
	r = r1.move(0,0)
	moved = 0
	if r.left < r2.left:
		r.left = r2.left
		moved = 1
	elif r.right > r2.right:
		r.right = r2.right
		moved = 1
	if r.top < r2.top:
		r.top = r2.top
		moved = 1
	elif r.bottom > r2.bottom:
		r.bottom = r2.bottom
		moved = 1
	return [r,moved]

def containPointInRect(point,rect):
	p = list(point)
	if p[0] < rect.left:
		p[0] = rect.left
	if p[0] > rect.right:
		p[0] = rect.right
	if p[1] < rect.top:
		p[1] = rect.top
	if p[1] > rect.bottom:
		p[1] = rect.bottom
	return p

def fontRenderLines(font,lines,color,space=0):
	#Centered.
	imgs = []
	maxWidth = 0
	totalHeight = 0
	for line in lines:
		this = font.render(line,1,color)
		imgs.append(this)
		maxWidth = max(maxWidth,this.get_width())
		totalHeight += this.get_height()+space
	totalHeight -= space

	totalImage = pygame.Surface((maxWidth,totalHeight)).convert_alpha()
	totalImage.fill((0,0,0,0))
	blitY = 0
	for img in imgs:
		totalImage.blit(img,img.get_rect(centerx=maxWidth/2.0,top=blitY))
		blitY += img.get_height()
	return totalImage

def lineAngle(l):
	return math.atan2(l[0][1]-l[1][1],l[1][0]-l[0][0])

def lineCollision(line1,line2):
	'''Line format ((x1,y1),(x2,y2)).'''
	m1 = (line1[1][1] - line1[0][1])/float(line1[1][0] - line1[0][0])
	b1 = line1[0][1] - m1*line1[0][0]
	m2 = (line2[1][1] - line2[0][1])/float(line2[1][0] - line2[0][0])
	b2 = line2[0][1] - m2*line2[0][0]

	#Two infinitely long lines with different angles will always collide. Find that point.
	intersectX = (m2 + b2 - b1)/m1
	intersectY = m1*intersectX + b1

	if line1[0][0] < intersectX < line1[1][0]:
		return 1
	else:
		return 0



def loadText(name):
	'''Returns a string of that file. For level loading.'''
	fullname = os.path.join('data',name)
	in_file = open(fullname,'rU')
	text = in_file.read()
	in_file.close()
	text = removeCharFromString(text, '\r')
	return text

def limitToRange(a,b,c):
	if a < b:
		a = b
	if a > c:
		a = c
	return a

def loadFont(name,size):
	pygame.font.init() #Safe to call more than once.
	return pygame.font.Font(os.path.join('data','fonts',name+'.ttf'),size)

def loadOGG(name):
	return pygame.mixer.Sound(name + '.ogg')

def loadWAV(name):
	return pygame.mixer.Sound(name + '.wav')

def loadPNG(name,alpha=1):
	'''Loads a PNG with alpha values. For completely opaque PNGs, use loadImage.'''
	fullname = os.path.join('data','images',name + '.png')
	image = pygame.image.load(fullname)
	if alpha:
		image = image.convert_alpha()
	else:
		image = image.convert()
	return image

def loadWAV(name):
	return pygame.mixer.Sound(os.path.join('data','sounds',name + '.wav'))

def makeList(objs):
	if objs == None:
		return []
	try:
		objs[0]
		#If that works, it's a list
		return objs
	except AttributeError:
		return [objs] #Make it a list.

def moveToRange(subj,size,MIN,MAX):
	#Range is [MIN,MAX]
	while subj < MIN:
		subj += size
	while subj > MAX:
		subj -= size
	if subj < MIN or subj > MAX:
		#print 'move to range FAILED.'
		pass
	return subj

def multAlpha(image,mult):
	'''SLOW!!!'''
	image = image.copy()
	for x in range(image.get_width()):
		for y in range(image.get_height()):
			col = image.get_at((x,y))
			col[3] = int(round(col[3]*mult))
			image.set_at((x,y),col)
	return image

def randomInRange(a,b):
	return a + random.random()*(b-a)

def randomElement(l):
	return l[random.randint(0,len(l)-1)]

def rectCollisionSide(a,b):
	#Where is a in relation to b?
	ang = math.atan2(a.centery-b.centery,a.centerx-b.centerx)
	if ang < 0:
		ang += 2*math.pi
	toCorner = math.atan(float(b.height)/b.width) #The angle from the rect's center to the corner.
	if toCorner < ang <= math.pi-toCorner:
		return 'below'
	elif math.pi-toCorner < ang <= math.pi+toCorner:
		return 'left'
	elif math.pi+toCorner < ang <= 2*math.pi-toCorner:
		return 'above'
	elif 2*math.pi-toCorner < ang or ang <= toCorner:
		return 'right'

def removeCharFromString(string, removechar):
	'''Returns a string that is the original without any removechar'''
	rs = ''
	for character in string:
		if character != removechar:
			rs += character
	return rs

def roundPoint(var0,var1=None): #Also works for size
	if var1:
		return (int(round(var0)),int(round(var1)))
	else:
		return (int(round(var0[0])),int(round(var0[1])))

def sign(num):
	if num < 0:
		return -1
	elif num > 0:
		return 1
	else:
		return 0

def split(string,token='\n'):
	'''Turns a string into a list of strings, breaking it at each \n'''
	r = []
	this = ''
	for char in string:
		if char == token:
			r.append(this)
			this = ''
		else:
			this += char
	if this != '':
		r.append(this)
	return r


def writeToFile(name,text):
	outFile = open(os.path.join('data',name),'w')
	outFile.write(text)
	outFile.close()


class AnimatedImage:
	def __init__(self,main,images,time,rect=None):
		self.images = images

		#Might need to load them.
		for i in xrange(len(self.images)):
			if str(self.images[i]) == self.images[i]: #It's a string:
				self.images[i] = loadPNG(self.images[i])

		self.index = 0
		self.maxTimeTillNext = time
		self.timeTillNext = self.maxTimeTillNext
		self.rect = rect
		if self.rect:
			#Set up so that it can be give straight to main.getObj()
			self.image = self.getImage() #Get an image so it will be picked up by camera.
			self.rect = rect

	def compute(self):
		self.timeTillNext -= 1

		if self.timeTillNext <= 0:
			self.index += 1
			if self.index >= len(self.images):
				self.index = 0
			self.timeTillNext = self.maxTimeTillNext

		if self.rect:
			self.image = self.getImage()

	def getImage(self):
		return self.images[self.index]


class Circle:
	'''Used for collision.'''
	def __init__(self,x,y,rad,image=None):
		self.x = x
		self.y = y
		self.rad = rad
		self.image = image

	def collideCircle(self,other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2) <= self.rad + other.rad

	def collideLine(self,line):
		'''Returns a tuple [Whether there is collision, whether the circle is above or below the line, the vertical distance from the circle to the line]'''
		line = toLine(line)

		#We will determine the distance from the circle to the line.
		#If that distance if less than or equal to the circle's radius, then the circle is touching the line.
		#Now we will determine an mx+b equation for both the line and
		#A line perpendicular to this line which passes through player's center.
		#Output is of type [collision,above,yDiff]
		if line.x1 == line.x2:
			#special case; use different method
			dist = abs(self.x - line.x1)
			touchesSegment = min(line.y1,line.y2) < self.y < max(line.y1,line.y2)
			if dist <= self.rad and touchesSegment:
				above = 0#self.x > line.x1
				return [1,above,0]
			return [0,0,0]

		else:
			m1 = math.tan(line.angle) #The slope of the line
			b1 = line.y1 - m1*line.x1
			m2 = math.tan(line.angle+math.pi/2) #The slope of the line drawing the distance from the line to the circle
			#y = mx + b, know m,x,y
			b2 = self.y - m2*self.x
			#Intersection of 2 lines:
			#y = m1*x + b
			#y = m2*x + b2
			intersectX = (b2 - b1)/(m1 - m2)
			intersectY = m1*intersectX + b1#(b1*m2 + b2*m1)/(m1 - m2)
			dist = math.sqrt((intersectX-self.x)**2 + (intersectY-self.y)**2) #CHECK!
			#But we're only going to collide with it if we touch the line segment.
			lesserX = min(line.x1,line.x2)
			greaterX = max(line.x1,line.x2)
			lesserY = min(line.y1,line.y2)
			greaterY = max(line.y1,line.y2)
			touchesSegment = lesserX <= intersectX <= greaterX and lesserY <= intersectY <= greaterY

			if dist <= self.rad and touchesSegment:
				above = self.y < intersectY #Greater y value means go down
				yToCircle = abs(self.y - (line.y1 + (self.x - line.x1)*m1))
				return [1,above,yToCircle]

			return [0,0,0]

	def draw(self,surface):
		if self.image:
			surface.blit(self.image,(self.x-self.image.get_width()/2,self.y-self.image.get_height()/2))

	def getTop(self):
		return self.y - self.rad
	def getLeft(self):
		return self.x - self.rad
	def getRight(self):
		return self.x + self.rad
	def getBottom(self):
		return self.y + self.rad

	def update(self,var0,var1=None):
		if var1 is not None:
			self.x = var0
			self.y = var1
		else:
			self.x = var0[0]
			self.y = var0[1]

	def __str__(self):
		return 'Circle: ' + str(self.x) + ',' + str(self.y) + ',' + str(self.rad)

class Image:
	def __init__(self,image,rect,drawPriority=0):
		self.image = image
		self.rect = rect
		self.drawPriority = drawPriority

	def compute(self):
		pass

class Line:
	#Not much
	def __init__(self,x1,y1,x2,y2):
		if x1 > x2:
			temp = x1
			x1 = x2
			x2 = temp
			temp = y1
			y1 = y2
			y2 = temp

		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		self.angle = math.atan2(self.y2-self.y1,self.x2-self.x1)

def toLine(k):
	if isinstance(k,Line):
		return k
	else:
		#It's a tuple ((x1,y1),(x2,y2))
		return Line(k[0][0],k[0][1],k[1][0],k[1][1])

class TimedEvent:
	def __init__(self,main,text,time):
		self.main = main
		self.time = time
		self.text = text

	def compute(self):
		self.time -= 1
		if self.time <= 0:
			self.main.runText(self.text)
			self.dead = 1


def loadOGG(name):
	return pygame.mixer.Sound(os.path.join('data','sounds',name + '.ogg'))

def playSound(name):
	sound = loadOGG(name)
	sound.set_volume(1)
	sound.play()
