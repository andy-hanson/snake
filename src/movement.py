import math
import random

import helpers

class BounceAround:
	def __init__(self,main,obj,speed=None,ang=None):
		'''Only 1 object!'''
		self.main = main
		self.obj = obj
		if ang is None:
			ang = random.random()*2*math.pi
		self.xVel = speed*math.cos(ang)
		self.yVel = speed*math.sin(ang)
		'''self.maxTimeSinceBounce = 4 #Only for off snake (walls are absolute!!!)
		self.timeSinceBounce = 0'''

	def compute(self):
		self.obj.x += self.xVel
		self.obj.y += self.yVel

		self.obj.circle.update(self.obj.x,self.obj.y)

		if self.obj.circle.getLeft() < 0 or self.obj.circle.getRight() >= self.main.FIELD_WIDTH:
			self.xVel *= -1
		elif self.obj.circle.getTop() < 0 or self.obj.circle.getBottom() >= self.main.FIELD_HEIGHT:
			self.yVel *= -1
		'''else:
			if not self.timeSinceBounce:
				for line in self.main.snake.findLines():
					if self.obj.circle.collideLine(line)[0]:
						lineAngle = helpers.normalAngle(helpers.lineAngle(line))
						moveAngle = helpers.normalAngle(math.atan2(self.yVel,self.xVel))
						speed = math.hypot(self.xVel,self.yVel)
						print(lineAngle)
						print(moveAngle)
						print('')
						newAngle = 2*lineAngle-moveAngle
						if moveAngle > lineAngle:
							newAngle += math.pi
						self.xVel = speed*math.cos(newAngle)
						self.yVel = speed*math.sin(newAngle)

						self.timeSinceBounce = self.maxTimeSinceBounce

		if self.timeSinceBounce > 0:
			self.timeSinceBounce -= 1'''


		try:
			if self.obj.dead:
				self.dead = 1
		except AttributeError:
			pass

	def draw(self,surface):
		pass

