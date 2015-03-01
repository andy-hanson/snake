import math
import pygame
import random #For tongue animation

import helpers
import vector

class Snake():
	def __init__(self,main):
		self.main = main

		self.bodyColor = (0,32,0)

		self.minBodyWidth = 26*self.main.sizeMult#24*self.main.sizeMult
		self.bodyWidthGain = .5*self.main.sizeMult
		self.minLength = 180*self.main.sizeMult
		self.lengthGain = 180*self.main.sizeMult#120*self.main.sizeMult
		self.minVel = 3*self.main.sizeMult #Start maxVel
		self.levelMinVelPlus = .5*self.main.sizeMult #This much more per level
		self.maxVelGain = .125*self.main.sizeMult#0.25*self.main.sizeMult
		self.direction = 0
		self.speed = [self.minVel,0] #Head movement as a vector.

		self.minPointDist = self.minVel*1 #Head must be this far away from last point to make a new point. Try to keep a multiple of self.vel. Smaller is smoother but slower.

		self.maxTurnAmount = math.pi/16#math.pi/12 #Maximum direction change for each new point (not per frame)

		self.normalHeadImage = helpers.loadPNG('head-normal')
		self.normalHeadShadow = helpers.loadPNG('head-normal-shadow')
		self.deadHeadImage = helpers.loadPNG('head-dead') #Same shadow
		self.numTongueHeadImages = 2 #Images act as an alternate head
		self.tongueHeadImages = []
		for n in range(self.numTongueHeadImages):
			self.tongueHeadImages.append(helpers.loadPNG('head-tongue-' + str(n)))
		self.tongueHeadShadows = []
		for n in range(self.numTongueHeadImages):
			self.tongueHeadShadows.append(helpers.loadPNG('head-tongue-' + str(n) + '-shadow'))
		self.tongueImageIndex = 0

		#Tongue animation
		self.minTimeTillTongue = 40
		self.maxTimeTillTongue = 120
		self.timeTillTongue = self.minTimeTillTongue
		self.minTongueTime = 4
		self.maxTongueTime = 8
		self.tongueTime = 0

		self.segmentImage = helpers.loadPNG('body-segment')
		self.segmentShadowImage = helpers.loadPNG('body-segment-shadow')
		self.tailImage = helpers.loadPNG('tail')
		self.tailShadow = helpers.loadPNG('tail-shadow')
		self.tailSizeMult = 2



	def compute(self):
		#Set this frame's velocity.
		'''minR = 1#.5 #Minimum fraction of maxVel to use
		moreSpeedThresh = 1#.5#Beyond this point in joy rad, speed up.
		if self.main.joy.rad > moreSpeedThresh:
			#Go a little faster than normal.
			relR = (self.main.joy.rad - moreSpeedThresh)/(1 - moreSpeedThresh) #Range [0,1]
			relR = relR**2
			r = relR * (1 - minR) + minR
		else:
			r = minR
		self.vel = self.maxVel*r'''
		self.vel = self.maxVel
		try:
			self.speed = vector.setLength(self.speed,self.vel)
		except TypeError:
			self.speed = (self.vel*math.cos(self.direction),self.vel*math.cos(self.direction))


		self.points[0] = vector.add(self.points[0],self.speed) #Move your head. Tail will be moved later.


		#Move Tail (maybe)
		#Only move tail if you're too long.
		if self.length < self.findLength(): #If desired length < actual length:
			direction = vector.direc(self.points[len(self.points)-1],self.points[len(self.points)-2]) #From tail to one after tail.
			if direction == [0,0]: #The tail is on top of another point, so remove the tail. The other point is the new tail.
				print('wtf')
				self.points.remove(self.points[len(self.points)-1])
			else:
				self.points[len(self.points)-1] = vector.add(self.points[len(self.points)-1],vector.mult(direction,self.vel)) #Move the tail.
				newDirection = vector.direc(self.points[len(self.points)-1],self.points[len(self.points)-2])
				give = math.pi/2
				if newDirection == [0,0] or abs(vector.angDiff(newDirection,direction)) > give:
					#newDirection != direction: #The tail passed through a point while moving, so remove it. The other point is the new tail.
					self.points.remove(self.points[len(self.points)-1])
					'''print('remove')
					print(direction)
					print(newDirection)
					print()'''


		#Change Direction (maybe)

		#Calculate the distance the head has travelled since the last point.
		dist = math.hypot(self.points[0][0] - self.points[1][0], self.points[0][1] - self.points[1][1])
		#Only allow a new point if the head has travelled far enough.
		if dist >= self.minPointDist:

			if self.main.joy.rad != 0:
				ang = self.main.joy.ang
				if helpers.angleDiff(ang,self.direction) > self.maxTurnAmount:#abs(ang - self.direction) > self.maxTurnAmount:
					if helpers.angleSide(ang,self.direction) == 'left':#If it looks like they're trying to turn left:
						ang = self.direction + self.maxTurnAmount
					else: #If it looks like they're trying to turn right:
						ang = self.direction - self.maxTurnAmount
				self.setDirection(ang)

			else:
				self.makeNewPoint()


		#Check to see if the head circle collides with any lines.
		for line in self.findLinesNoHead():
			if self.headCircle.collideLine(line)[0]:
				self.die()

		#Also check if you're outside the boundary.
		if self.headCircle.x < 0 or self.headCircle.x > self.main.FIELD_WIDTH or self.headCircle.y < 0 or self.headCircle.y > self.main.FIELD_HEIGHT:
			self.die()


		#Update head
		self.headCircle.update(self.points[0])
		self.headShadowCircle.update(vector.add(self.points[0],self.main.shadowOffset))
		self.findImage()


	def draw(self,surface):
		bodySegmentImage = pygame.transform.smoothscale(self.segmentImage,helpers.roundPoint(self.bodyWidth*self.main.sizeMult,self.bodyWidth*self.main.sizeMult))
		bodySegmentShadowImage = pygame.transform.smoothscale(self.segmentShadowImage,helpers.roundPoint(self.bodyWidth*self.main.sizeMult,self.bodyWidth*self.main.sizeMult))

		shadowSurface = surface.copy()
		shadowSurface.set_alpha(self.main.SHADOW_AMOUNT)

		#Draw shadow first
		for line in self.findLines():
			point = (int(round(line[1][0])),int(round(line[1][1]))) #Don't worry about first point, head covers it.
			point = vector.add(point,self.main.shadowOffset)
			if line[1] == self.points[len(self.points)-1]:
				#The last one is the tail.
				tailShadow = pygame.transform.smoothscale(self.tailShadow, \
													helpers.roundPoint(self.bodyWidth*self.tailSizeMult*self.main.sizeMult,self.bodyWidth*self.tailSizeMult*self.main.sizeMult))
				ang = helpers.lineAngle(line)
				rotated = pygame.transform.rotozoom(tailShadow,180/math.pi*ang,1)
				shadowSurface.blit(rotated,rotated.get_rect(center=point))

			else:
				shadowSurface.blit(bodySegmentShadowImage,bodySegmentShadowImage.get_rect(center=point))

		self.headShadowCircle.draw(shadowSurface)

		surface.blit(shadowSurface,(0,0))


		for line in self.findLines():
			#pygame.draw.line(surface,self.bodyColor,line[0],line[1],int(round(self.bodyWidth+2)))
			#Circles for smoothness
			point = (int(round(line[1][0])),int(round(line[1][1]))) #Don't worry about first point, head covers it.
			if line[1] == self.points[len(self.points)-1]:
				#The last one is the tail.
				tailImage = pygame.transform.smoothscale(self.tailImage, \
													helpers.roundPoint(self.bodyWidth*self.tailSizeMult*self.main.sizeMult,self.bodyWidth*self.tailSizeMult*self.main.sizeMult))
				ang = helpers.lineAngle(line)
				rotated = pygame.transform.rotozoom(tailImage,180/math.pi*ang,1)
				surface.blit(rotated,rotated.get_rect(center=point))
			else:
				surface.blit(bodySegmentImage,bodySegmentImage.get_rect(center=point))
			#circleRad = int(round(self.bodyWidth/2)) #Just happens to look best this way.
			#pygame.draw.circle(surface,self.bodyColor,point,circleRad)



		self.headCircle.draw(surface)

		#Next part is unnecessary, shows where turning and head/tail points are
		'''b = 128
		for point in self.points:
			pygame.draw.circle(surface,(b,b,b),(int(point[0]),int(point[1])),5)'''

	def reset(self,level):
		self.maxVel = self.minVel + self.levelMinVelPlus*level
		self.vel = self.minVel

		self.bodyWidth = self.minBodyWidth
		self.length = self.minLength

		try:
			if self.headCircle.x < 0 or self.headCircle.x > self.main.FIELD_WIDTH or self.headCircle.y < 0 or self.headCircle.y > self.main.FIELD_HEIGHT:
				#Died by going out of boundary - restart in center.
				self.points = [[20*self.main.sizeMult,self.main.FIELD_HEIGHT/2]]
				self.speed = [self.vel,0]
				self.direction = 0
			else:
				self.points = [self.points[0]] #Removing all other points

		except AttributeError:
			#Level 0, haven't defined points yet
			self.points = [[20*self.main.sizeMult,self.main.FIELD_HEIGHT/2]]
			#Each entry is [x,y]. points[0] is head, last one is tail.
		self.points.append(vector.add(self.points[0],self.speed))



		self.headCircle = helpers.Circle(0,0,self.bodyWidth,self.normalHeadImage)
		self.headShadowCircle = helpers.Circle(0,0,self.bodyWidth,self.normalHeadShadow)
		self.headSizeMult = 4*self.main.sizeMult#3 #Is this many times self.width

		self.findImage() #for head


	def die(self):
		headSize = int(round(self.bodyWidth*self.headSizeMult))
		image = pygame.transform.smoothscale(self.deadHeadImage,(headSize,headSize))
		image = pygame.transform.rotozoom(image,-180/math.pi*self.direction,1)
		self.headCircle.image = image
		self.main.draw()
		pygame.time.wait(1000)
		self.main.lose()

	def findImage(self):
		'''For head.'''
		#Tongue randomly flicks.
		if self.timeTillTongue:
			self.timeTillTongue -= 1
			if self.timeTillTongue == 0:
				self.tongueTime = random.randint(self.minTongueTime,self.maxTongueTime)
			image = self.normalHeadImage
			shadowImage = self.normalHeadShadow

		else:
			self.tongueTime -= 1
			if self.tongueTime == 0:
				self.timeTillTongue = random.randint(self.minTimeTillTongue,self.maxTimeTillTongue)
			self.tongueImageIndex += 1
			if self.tongueImageIndex == self.numTongueHeadImages:
				self.tongueImageIndex = 0
			image = self.tongueHeadImages[self.tongueImageIndex]
			shadowImage = self.tongueHeadShadows[self.tongueImageIndex]

		headSize = int(round(self.bodyWidth*self.headSizeMult))
		thisHeadImage = pygame.transform.smoothscale(image,(headSize,headSize))
		headImage = pygame.transform.rotozoom(thisHeadImage,-180/math.pi*self.direction,1)
		self.headCircle.image = headImage

		thisHeadShadow = pygame.transform.smoothscale(shadowImage,(headSize,headSize))
		headShadow = pygame.transform.rotozoom(thisHeadShadow,-180/math.pi*self.direction,1)
		self.headShadowCircle.image = headShadow

	def findLength(self):
		length = 0
		for line in self.findLines():
			length += math.hypot(line[1][0]-line[0][0],line[1][1]-line[0][1])
		return length

	def getApple(self):
		self.length += self.lengthGain
		self.maxVel += self.maxVelGain
		self.bodyWidth += self.bodyWidthGain
		self.minPointDist = self.vel*1
		self.main.scorer.getPoints(1)

	def setDirection(self,angle):
		if 1:#angle != self.direction:
			v = [math.cos(angle),math.sin(angle)]
			self.speed = vector.mult(v,self.vel)
			self.makeNewPoint()
			self.direction = angle

	def makeNewPoint(self):
		self.points.insert(0,self.points[0]) #A new point will now be the head. Originally the head and old point are the same.

	def findLines(self):
		i = 0
		while i < len(self.points) - 1:
			i += 1
			yield (self.points[i-1],self.points[i])

	def findLinesNoHead(self):
		#Like above but without the head line.
		i = 8#int(self.headCircle.rad/self.minPointDist) + 2 #Just barely enough that normal movement won't be a collision.
		while i < len(self.points) - 1:
			i += 1
			yield (self.points[i-1],self.points[i])

