import pygame

import apple
import enemies
import graphics
import helpers
import joy
import levelManager
import os
import scorer
import snake
import sound
import vector

class Main:
	def __init__(self):
		k = 600
		self.FIELD_WIDTH = k
		self.FIELD_HEIGHT = k
		self.sizeMult = self.FIELD_WIDTH/800.0
		self.screen = pygame.display.set_mode((self.FIELD_WIDTH,self.FIELD_HEIGHT))
		self.objects = []
		self.clock = pygame.time.Clock()
		self.FPS = 30

		self.SHADOW_AMOUNT = 96
		self.shadowOffset = vector.mult([-10,10],self.sizeMult)

		self.setup()

		self.go()

	def setup(self):
		self.snake = snake.Snake(self)
		self.get(self.snake)

		self.get(apple.AppleManager(self))

		self.get(graphics.Background(self))

		self.joy = joy.Joystick()
		self.scorer = scorer.Scorer(self)
		self.get(self.scorer)

		self.get(enemies.ArrowManager(self))


		self.levelManager = levelManager.LevelManager(self)
		self.get(self.levelManager) #Must be last got, because it tells all others to reset(0).

		pygame.mixer.music.load(os.path.join('data','sounds','theme.ogg'))
		pygame.mixer.music.play(-1)

	def go(self):
		self.done = 0
		self.time = 0
		while not self.done:
			self.compute()
			self.draw()
			self.getInput()
			self.clock.tick(self.FPS)
			self.time += 1
		pygame.quit()

	def draw(self):
		for x in range(-2,3):
			for o in self.objects:
				if o.drawPriority == x:
					o.draw(self.screen)

		pygame.display.flip()
		pygame.display.set_caption('Rhodium Snake August 18 2009 - Framerate ' + str(self.clock.get_fps()) + '/' + str(self.FPS))

	def compute(self):
		self.joy.compute()

		i = 0
		while i < len(self.objects):
			self.objects[i].compute()
			try:
				if self.objects[i].dead:
					del self.objects[i]
					i -= 1
			except AttributeError:
				pass
			i += 1

	def get(self,obj):
		try:
			obj.drawPriority
		except AttributeError:
			obj.drawPriority = 0
		self.objects.append(obj)

	def allObjects(self):
		for o in self.objects:
			yield o

	def getInput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = 1
			'''if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.objects[0].setDirection([0,-1])
				if event.key == pygame.K_LEFT:
					self.objects[0].setDirection([-1,0])
				if event.key == pygame.K_RIGHT:
					self.objects[0].setDirection([1,0])
				if event.key == pygame.K_DOWN:
					self.objects[0].setDirection([0,1])'''

	def lose(self):
		self.levelManager.resetAll() #Restart at beginning of current level.
		#print('GAME OVER')
		#print('SCORE: ' + str(self.scorer.score))
		#self.done = 1

	def win(self):
		self.screen.fill((255,255,255))
		f1 = pygame.font.Font(os.path.join('data','fonts','pokemon.ttf'),int(round(180*self.sizeMult)))
		v = f1.render('Victory!',1,(0,0,0))
		self.screen.blit(v,v.get_rect(centerx=self.FIELD_WIDTH/2,centery=1*self.FIELD_HEIGHT/5))
		v = f1.render('Yummy!',1,(0,0,0))
		self.screen.blit(v,v.get_rect(centerx=self.FIELD_WIDTH/2,centery=2*self.FIELD_HEIGHT/4))
		f2 = pygame.font.Font(os.path.join('data','fonts','pokemon.ttf'),int(round(50*self.sizeMult)))
		v = f2.render('Completed in ' + str(int(round(self.time/self.FPS))) + ' seconds!',1,(0,0,0))
		self.screen.blit(v,v.get_rect(centerx=self.FIELD_WIDTH/2,centery=6*self.FIELD_HEIGHT/8))
		v = f2.render('Close the window to exit.',1,(0,0,0))
		self.screen.blit(v,v.get_rect(centerx=self.FIELD_WIDTH/2,centery=7*self.FIELD_HEIGHT/8))
		pygame.display.flip()

		while not self.done:
			self.getInput()
			self.clock.tick(self.FPS)


m = Main()
