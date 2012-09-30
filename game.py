game_history = [round1, round2] # is a list of round_histories
round_history = [lap1, lap2] # is a list of laps during round 
lap_history = [move1, move2] # is a list of moves for one lap
move1 = {
	'player': 'Player1',
	'decision': decision,
}

from copy import deepcopy

class Round(object):
	def __init__(self, ):
		pass

	def start(self):
		"""Starts a round of game."""
		pass
	
	def get_players(self):

class Game(object):
	def __init__(self):
		self.players_num = players_num
		self.button = Button()
		self.players = players
		self.diler = Diler()
	
	def start(self):
		pass

	def preflop(self):
		"""Implementation of preflop round"""
		player_index = 0
		while not self.round_finished(cur_lap_hist, len(players)):
			# Should be refactored according to real player methods
			move = players[player_index].make_move(game_history)
			if self.verify_move(lap_history, move, bb_val):	
				lap_history.append(move)
			
				

	def verify_move(self, lap_history, move, bb_val):
		lap_hist = remove_folds(lap_history)
		if len(lap_hist) > 0:
			return 	move['decision'].value >= \
				lap_hist[-1]['decision'].value and \
				move['decision'].value % bb_val == 0 
		else:
			return True
	
	def game_finished(self, lap_history, players_num):
		return len(remove_folds(lap_history)) == players_num

	def round_finished(self, lap_history, players_num):
		"""Returns true if all players made equal bets, false otherwise."""
		lap_hist = remove_folds(lap_history)
		# Returns False if some players haven't made their bets	
		if len(lap_hist) < players_num:
			return False 

		first_move = lap_hist[0]
		for i, move in enumerate(lap_hist, 1):
			if move['decision'].value != first_move['decision'].value:
				return False
		return True
			
	def remove_folds(self, lap_history):
		"""Removes moves with "fold" type from lap history. Returns resulting lap history."""
		lap_hist = deepcopy(lap_history)
		for move in lap_hist:
			if move['decision'].des_type == DES_TYPE.FOLD:
				lap_hist.remove(move)
		return lap_hist
		

			
