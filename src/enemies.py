import graphics
import helpers
import math
import pygame
import random

class ArrowManager:
	def __init__(self,main):
		self.main = main

	def compute(self):
		if random.random() < self.arrowChance:
			#Randomly choose a side of the bounding square, and a position on that side.
			if random.random() < 0.5:
				if random.random() < 0.5:
					#Left side
					x = 0
					direction = 0
				else:
					#Right side
					x = self.main.FIELD_WIDTH-1
					direction = math.pi
				y = random.randint(0,self.main.FIELD_HEIGHT-1)
			else:
				x = random.randint(0,self.main.FIELD_WIDTH-1)
				if random.random() < 0.5:
					#Top side
					y = 0
					direction = math.pi/2
				else:
					#Bottom side
					y = self.main.FIELD_HEIGHT-1
					direction = 3*math.pi/2
			self.main.get(Arrow(self.main,x,y,direction,self.speed))

	def draw(self,surface):
		pass

	def reset(self,level):
		self.arrowChance = (level-2)*1.0/60
		self.speed = level*self.main.sizeMult

class Arrow:
	def __init__(self,main,x,y,direction,speed):
		self.main = main
		self.xVel = speed*math.cos(direction)
		self.yVel = speed*math.sin(direction)
		self.size = 40*self.main.sizeMult

		self.originalImage = helpers.loadPNG('arrow')
		self.spin = 0
		self.spinSpeed = 2 #Degrees
		self.scale = self.size/self.originalImage.get_width()
		self.circle = helpers.Circle(x,y,self.size/2,pygame.transform.rotozoom(self.originalImage,self.spin,self.scale))

		self.timeTillLaunch = 60 #Waits a second before moving.

	def compute(self):
		if self.timeTillLaunch == 0:
			self.circle.x += self.xVel
			self.circle.y += self.yVel
			if self.circle.collideCircle(self.main.snake.headCircle):
				self.main.snake.die()
			for line in self.main.snake.findLines():
				if self.circle.collideLine(line)[0]:
					self.xVel *= -1
					self.yVel *= -1
			#If it hits another arrow, they both die.
			for o in self.main.objects:
				if isinstance(o,Arrow) and o is not self:
					if self.circle.collideCircle(o.circle):
						self.dead = 1
						o.dead = 1
						startWidth = self.size
						endWidth = self.size*4
						time = 20
						self.main.get(graphics.ExpandingImage(self.main,self.circle.x,self.circle.y,self.originalImage,startWidth,endWidth,time))
						self.main.get(graphics.ExpandingImage(self.main,o.circle.x,o.circle.y,o.originalImage,startWidth,endWidth,time))
			if self.circle.x + self.size < 0 or self.circle.x - self.size > self.main.FIELD_WIDTH or \
			   self.circle.y + self.size < 0 or self.circle.y - self.size > self.main.FIELD_HEIGHT:
				self.dead = 1

			self.spin += self.spinSpeed
			self.circle.image = pygame.transform.rotozoom(self.originalImage,self.spin,self.scale)

		else:
			self.timeTillLaunch -= 1

	def draw(self,surface):
		if self.timeTillLaunch == 0 or random.random() < .5: #Blinking at startup
			self.circle.draw(surface)
