from random import randint
from different import Desicion

class Player(object):
	def __init__(self, name):
		self.name = name
		self.bankroll = bankroll

	def make_decision(self, game_info):
		r = randint(5)
		if r == 0:
			return Decision(DTYPE.FOLD, 0)
		else:
			return Decision(DTYPE.BET, r)
			
				
