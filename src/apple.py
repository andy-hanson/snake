import pygame

import graphics
import helpers
import movement
import vector

class AppleManager:
	def __init__(self,main):
		self.main = main

		self.numApples = 3
		self.apples = []

		self.level = 0


		self.appleImage = helpers.loadPNG('apple')

	def compute(self):
		if len(self.apples) < self.numApples:
			self.addNewImploder()#self.createRandomApple()

		i = 0
		while i < len(self.apples):
			a = self.apples[i]
			if isinstance(a,graphics.ImplodingImage):
				if a.time == a.maxTime - 1:
					self.apples.remove(a)
					i -= 1
					self.createRandomApple(a.x,a.y)
			elif a.dead:
				self.apples.remove(a)
				i -= 1
			i += 1

	def addNewImploder(self):
		tab = 50*self.main.sizeMult
		x = helpers.randomInRange(tab,self.main.FIELD_WIDTH-tab)
		y = helpers.randomInRange(tab,self.main.FIELD_HEIGHT-tab)

		rad = int(round(16*self.main.sizeMult))
		i = graphics.ImplodingImage(self.main,x,y,self.appleImage,rad*8,rad*2)

		self.apples.append(i)
		self.main.get(i)

	def createRandomApple(self,x,y):
		apple = Apple(self.main,self,x,y)
		self.main.get(apple)
		if self.level == 1:
			self.main.get(movement.BounceAround(self.main,apple,3))
		if self.level == 2:
			self.main.get(movement.BounceAround(self.main,apple,6))
		self.apples.append(apple)

	def draw(self,surface):
		pass

	def reset(self, level):
		#New level
		self.level = level

class Apple:
	def __init__(self,main,manager,x,y):
		self.main = main
		self.dead = 0
		self.manager = manager
		self.x = x
		self.y = y
		rad = int(round(16*self.main.sizeMult))
		image = helpers.loadPNG('apple')
		image = pygame.transform.smoothscale(image,(rad*2,rad*2))
		self.circle = helpers.Circle(self.x,self.y,rad,image)
		shadow = helpers.loadPNG('apple-shadow')
		shadow = pygame.transform.smoothscale(shadow,(rad*2,rad*2))
		shadow = helpers.multAlpha(shadow,.25)
		self.shadowCircle = helpers.Circle(self.x,self.y,rad,shadow)

	def compute(self):
		if self.main.snake.headCircle.collideCircle(self.circle):
			self.main.snake.getApple()
			helpers.playSound('eat')
			self.dead = 1

		self.circle.update(self.x,self.y)
		shadowPos = vector.add((self.x,self.y),self.main.shadowOffset)
		self.shadowCircle.update(shadowPos)

	def draw(self,surface):
		self.shadowCircle.draw(surface)
		self.circle.draw(surface)
