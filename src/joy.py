import math
import os
import pygame

import helpers

class Joystick:
	def __init__(self):
		#NO BUTTONS IN THIS GAME
		pygame.joystick.init()
		numJoys = pygame.joystick.get_count()

		self.configuration = {
			'LEFT': pygame.K_LEFT,
			'RIGHT': pygame.K_RIGHT,
			'UP': pygame.K_UP,
			'DOWN': pygame.K_DOWN
		}

		self.keyboardMode = 0
		if numJoys == 0:
			print('There are no joysticks available. Keyboard mode will be used.')
			print('This will negatively affect your play experience.')
			print('You can try closing the game and inserting a joystick.')
			print('Or, use the arrow keys.')
			self.keyboardMode = 1
		else:
			if numJoys >= 2:
				joyI = input('There are ' + str(numJoys) + ' joysticks on the system. Input index for your joystick choice (starts at 0). ')
			else:
				print('A joystick has been detected on your system and will be used for control.')
				joyI = 0
			self.joystick = pygame.joystick.Joystick(joyI)
			self.joystick.init()


			self.numButtons = self.joystick.get_numbuttons()
			if self.numButtons <  8:
				print('OOPS! Joystick has too few (<8) buttons. Switching to keyboard control.')
				self.keyboardMode = 1

			self.buttons = [0]*self.numButtons

		self.x = 0
		self.y = 0
		self.rad = 0


	def compute(self):
		#ANALOG MOVEMENT
		if self.keyboardMode:
			#You can only simulate the analog control. Rad will always be 1, and there are only 8 directions.
			xComponent = 0
			yComponent = 0
			keys = pygame.key.get_pressed()
			if keys[self.configuration['LEFT']]:
				xComponent -= 1
			if keys[self.configuration['RIGHT']]:
				xComponent += 1
			if keys[self.configuration['UP']]:
				yComponent -= 1
			if keys[self.configuration['DOWN']]:
				yComponent += 1


			if xComponent or yComponent:
				self.rad = 1
			else:
				self.rad = 0
			self.ang = math.atan2(yComponent,xComponent)
			self.x = self.rad*math.cos(self.ang)
			self.y = self.rad*math.sin(self.ang)



		else: #JOYSTICK MODE
			self.x = self.joystick.get_axis(0)
			self.y = self.joystick.get_axis(1)
			self.rad = math.hypot(self.x,self.y)
			self.rad = helpers.limitToRange(self.rad,0,1)
			self.ang = math.atan2(self.y,self.x)
			self.x = self.rad*math.cos(self.ang)
			self.y = self.rad*math.sin(self.ang)
			#'clicks' to middle
			tab = .25#.12
			if -tab < self.x < tab:
				self.x = 0
			if -tab < self.y < tab:
				self.y = 0


			self.rad = math.hypot(self.x,self.y)
			self.ang = math.atan2(self.y,self.x)


	def draw(self,surface):
		pass



