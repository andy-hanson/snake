import pygame
import random

import helpers

class Background:
	def __init__(self,main):
		self.main = main
		self.drawPriority = -2
		#bg = random.randint(0,2)
		#self.image = helpers.loadPNG('bg' + str(bg))

	def compute(self):
		pass

	def draw(self,surface):
		surface.blit(self.image,(0,0))

	def reset(self,level):
		self.image = helpers.loadPNG('bg' + str(level%3))
		self.image = pygame.transform.smoothscale(self.image,(self.main.FIELD_WIDTH,self.main.FIELD_HEIGHT))
		self.image.convert() #No alpha
		self.image.set_alpha(64)


class ExpandingImage:
	def __init__(self,main,x,y,img,startWidth=None,endWidth=None,time=80):
		self.main = main
		self.x = x
		self.y = y
		self.image = img
		if startWidth is None:
			self.startWidth = img.get_width()
			self.endWidth = img.get_width()*8
		else:
			self.startWidth = startWidth
			self.endWidth = endWidth


		self.maxTime = time
		self.time = 0

	def compute(self):
		self.time += 1
		if self.time == self.maxTime:
			self.dead = 1

		self.alpha = 255 * (1 - self.time/self.maxTime)

	def draw(self,surface):
		minRad = self.startWidth
		maxRad = self.endWidth
		thisWidth = minRad + (maxRad-minRad)*self.time/self.maxTime
		thisHeight = thisWidth*self.image.get_height()/self.image.get_width()
		scaledImage = pygame.transform.smoothscale(self.image,helpers.roundPoint(thisWidth,thisHeight))

		minX = self.x - thisWidth/2
		minY = self.y - thisHeight/2
		#If: Can't take a subsurface if it doesn't intersect at all!
		if minX < surface.get_width() and minY < surface.get_height() and minX + thisWidth > 0 and minY + thisHeight > 0:
			if minX < 0:
				width = thisWidth/2 + minX
				minX = 0
			else:
				width = thisWidth
			if minY < 0:
				height = thisHeight + minY
				minY = 0
			else:
				height = thisHeight
			if minX + width >= surface.get_width():
				width = surface.get_width() - minX
			if minY + height >= surface.get_height():
				height = surface.get_height() - minY

			tempSurface = surface.subsurface(pygame.Rect(minX,minY,width,height)).copy() #A buffer that is the appropriate size.

			if minX == 0:
				blitX = width - thisWidth
			else:
				blitX = 0
			if minY == 0:
				blitY = height - thisHeight
			else:
				blitY = 0
			tempSurface.blit(scaledImage,(blitX,blitY))
			a = self.alpha
			tempSurface.set_alpha(a)

			surface.blit(tempSurface,(minX,minY))

class ImplodingImage:
	def __init__(self,main,x,y,img,startWidth=None,endWidth=None,time=12):
		self.main = main
		self.dead = 0
		self.x = x
		self.y = y
		self.image = img
		if startWidth is None:
			self.startWidth = img.get_width()*8
			self.endWidth = img.get_width()
		else:
			self.startWidth = startWidth
			self.endWidth = endWidth

		self.maxTime = time
		self.time = 0

	def compute(self):
		self.time += 1
		if self.time == self.maxTime:
			self.dead = 1

		self.alpha = 255 * (self.time/self.maxTime)

	def draw(self,surface):
		minRad = self.startWidth
		maxRad = self.endWidth
		thisWidth = minRad + (maxRad-minRad)*self.time/self.maxTime
		thisHeight = thisWidth*self.image.get_height()/self.image.get_width()
		scaledImage = pygame.transform.smoothscale(self.image,helpers.roundPoint(thisWidth,thisHeight))

		minX = self.x - thisWidth/2
		minY = self.y - thisHeight/2
		#If: Can't take a subsurface if it doesn't intersect at all!
		if minX < surface.get_width() and minY < surface.get_height() and minX + thisWidth > 0 and minY + thisHeight > 0:
			if minX < 0:
				width = thisWidth/2 + minX
				minX = 0
			else:
				width = thisWidth
			if minY < 0:
				height = thisHeight + minY
				minY = 0
			else:
				height = thisHeight
			if minX + width >= surface.get_width():
				width = surface.get_width() - minX
			if minY + height >= surface.get_height():
				height = surface.get_height() - minY

			tempSurface = surface.subsurface(pygame.Rect(minX,minY,width,height)).copy()

			if minX == 0:
				blitX = width - thisWidth
			else:
				blitX = 0
			if minY == 0:
				blitY = height - thisHeight
			else:
				blitY = 0
			tempSurface.blit(scaledImage,(blitX,blitY))
			a = self.alpha
			tempSurface.set_alpha(a)

			surface.blit(tempSurface,(minX,minY))
