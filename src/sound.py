import math
import os
import pygame

import helpers

pygame.mixer.init()

MUSIC_ON = 1
SOUNDS_ON = 1

def getFreeChannel():
	k = pygame.mixer.find_channel()
	if k is None:
		print('ERROR: Out of sound channels.')
		channels = pygame.mixer.get_num_channels()
		print('You have ' + str(channels) + 'channels, and all are in use.')
		print('Commence bad error handling.')
		stop
	return k


#List of default volumes.
#Sounds not in this list change volume.
normVolume = .25
soundVolumes = {}

def playSound(name,volume=None,loops=0):
	#Play a single sound effect.
	if SOUNDS_ON:
		if volume is None:
			volume = soundVolumes[name]

		sound = helpers.loadWAV(os.path.join('data','sounds',name))
		sound.set_volume(volume)
		sound.play(loops)


class Sound:
	#Basic.
	def __init__(self,name):
		self.sound = helpers.loadOGG(os.path.join('data','sounds',name))
		self.done = 0

	def compute(self):
		self.done = not self.sound.get_num_channels()

	def die(self):
		if self.loops:
			self.sound.stop()

	def play(self,vol=.5,loops=0):
		if SOUNDS_ON:
			self.loops = loops
			self.sound.set_volume(vol)
			self.sound.play(loops)
