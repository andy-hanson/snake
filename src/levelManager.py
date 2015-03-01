import random
class LevelManager:
	def __init__(self,main):
		self.main = main
		self.level = 0 #EDIT ME
		self.resetAll()
		self.NEW_LEVEL_SCORE = 15
		self.MAX_LEVEL = 6

	def compute(self):
		if self.main.scorer.score >= self.NEW_LEVEL_SCORE*(self.level+1):
			self.level += 1
			if self.level > self.MAX_LEVEL:
				self.main.win()
			else:
				self.resetAll()

	def draw(self, surface):
		pass

	def resetAll(self):
		for o in self.main.allObjects():
			try:
				o.reset(self.level)
			except AttributeError:
				o.dead = 1 #If it doesn't have a special reset command, it is destroyed!
		'''self.main.scorer.reset()
		self.main.appleManager.reset(self.level)'''

	def reset(self,level):
		pass #So I don't delete myself!

