import pygame

import graphics
import helpers

class Scorer:
	def __init__(self,main):
		self.main = main
		self.smallFontSize = int(round(80*self.main.sizeMult))
		self.largeFontSize = int(round(640*self.main.sizeMult))
		self.font = helpers.loadFont('pokemon',self.smallFontSize)
		self.largeFont = helpers.loadFont('pokemon',self.largeFontSize)
		self.color = (255,255,255)

	def compute(self):
		pass

	def getPoints(self,amount):
		self.score += amount

		t = self.largeFont.render(str(self.score),1,self.color)
		x = self.main.FIELD_WIDTH/2
		y = t.get_height()/2*self.smallFontSize/self.largeFontSize
		startWidth = t.get_width()*self.smallFontSize/self.largeFontSize
		endWidth = t.get_width()
		time = 40
		self.main.get(graphics.ExpandingImage(self.main,x,y,t,startWidth,endWidth,time))


	def draw(self,surface):
		t = self.font.render(str(self.score),1,self.color)
		surface.blit(t,t.get_rect(centerx=self.main.FIELD_WIDTH/2,y=0))

	def reset(self,level):
		#New level
		try:
			self.score = level*self.main.levelManager.NEW_LEVEL_SCORE #In case of reset; otherwise does nothing.
		except AttributeError:
			self.score = 0 #No levelManager yet
