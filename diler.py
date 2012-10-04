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

	def best_combination(self, cards):
		"""Returns a list of 5 cards that form best combination"""
		
	def __check_straight_flash__(self, cards):
		"""Returns a list of 5 cards from given list that form streat flash or None otherwise"""

	def __check_four_of_kind__(self, cards):
		"""Returns a list of 5 cards from given list that form four of a kind or None otherwise"""

	def __check_full_house__(self, cards):
		"""Returns a list of 5 cards from given list that form full house or None otherwise"""

	def __check_flush__(self, cards):
		"""Returns a list of 5 cards from given list that form flush or None otherwise"""

	def __check_straight__(self, cards):
		"""Returns a list of 5 cards from given list that form straight or None otherwise"""

	def __check_three_of_kind__(self, cards):
		"""Returns a list of 5 cards from given list that form straight or None otherwise"""

	def __check_two_pair__(self, cards):
		"""Returns a list of 5 cards from given list that form two pair or None otherwise"""

	def __check_pair__(self, cards):
		"""Returns a list of 5 cards from given list that form pair or None otherwise"""

	def __check_high_card__(self, cards):
		"""Returns a list of 5 cards from given list that form high card"""

	def __same_suit__(self, cards):
		"""Returns a sorted list of lists of cards with same suit"""

	def __same_rank__(self, cards):
		"""Returns a sorted list of lists of cards with same rank""" 
