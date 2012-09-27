class Diler(object):
	def __init__(self, deck):
		self.deck = deck	

	def give_card(self):
		"""Returns Card object taken from a Deck"""
		return deck.pop_card() 
	
	def give_two_cards(self):
		"""Returns a list of two Card objects"""
		return [deck.pop_card() for i in range(2)]
		
	def give_three_cards(self):
		"""Returns a list of three Card objects"""
		return [deck.pop_card() for i in range(3)]
	
	def verify_move(self, move, history):
		"""Verifies player's move according to given game history. Returns 0 if move is correct and 1 otherwise.""" 
		pass
