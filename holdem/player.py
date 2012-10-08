from random import randint
from different import Desicion

class Player(object):
	def __init__(self, name, cash_amount):
		self.name = name
		self.cash_amount = cache_amount

	def make_decision(self, game_info):
		r = randint(5)
		if r == 0:
			return Decision(DTYPE.FOLD, 0)
		else:
			return Decision(DTYPE.BET, r)
			
	def choose_sit(self, available_sits):
		"""Returns a sit number chosen by player"""
		return available_sits[randint(len(available_sits))]
				
	def make_buyin(max_buyin):
		"""Returns a buyin sum chosen by player"""
		buyin = max(max_buyin, cash_amount)
		cash_amount -= buyin
		return buyin

	def receive_surplus(value):
		"""Increase players cash amount when player leaves a game"""
		cash_amount += value
