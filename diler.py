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
		if len(__same_suit__(cards)[0]) != 5:
			return None
		else:
			

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
		"""Returns a sorted list of sublists of cards with same suit. Cards in sublists doesn't intersect. Resulting list is sorted in decreasing order according to the count of cards with same suit. Sublist with higher card rank is greater than sublist with same cards count, but lower card rank."""
		# Make a dictionary with suit and corredponding lists of cards of this suit
		for card in cards:
			if d.has_key(card.suit) == False:
				d[card.suit] = []
				d[card.suit].append(card)
			else:
				d[card.suit].append(card)
		
		# Make a list of sublists sorted by highest rank in sublist
		l = sorted(d.items(), key = __highest_rank__, reverse = True)
		
		# Make a list of sublists sorted by elements count in sublists.
		# As sorted() preserves original order if two elements are equal,
		# equal sublists will be sorted according to highest rank
		l = sorted(l, key = lambda sl: len(sl), reverse = True)
		return l

	def __same_rank__(self, cards):
		"""Returns a sorted list of sublists of cards with same rank. Cards in sublists doesn't intersect. Resulting list is sorted in decreasing order according to the count of cards with same rank. Sublist with higher card rank is greater than sublist with same cards count, but lower card rank."""
		# Make a dictionary with ranks and corredponding lists of cards of this rank
		for card in cards:
			if d.has_key(card.rank) == False:
				d[card.rank] = []
				d[card.rank].append(card)
			else:
				d[card.rank].append(card)
		
		# Make a list of sublists sorted by highest rank in sublist
		l = sorted(d.items(), key = __highest_rank__, reverse = True)
		
		# Make a list of sublists sorted by elements count in sublists.
		# As sorted() preserves original order if two elements are equal,
		# equal sublists will be sorted according to highest rank
		l = sorted(l, key = lambda sl: len(sl), reverse = True)
		return l

	def __highest_rank__(self, cards):
		"""Returns a highest rank among given cards"""
		return sorted(cards, key = lambda card: card.rank, reverse = True)[0]
