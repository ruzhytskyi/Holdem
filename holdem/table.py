# table_history = [game_history1, game_history2]
# game_history = [round1, round2] # is a list of round_histories
# round_history = [lap1, lap2] # is a list of laps during round 
# lap_history = [move1, move2] # is a list of moves for one lap
# move1 = {
#     'player': 'Player1',
#     'decision': decision,

from copy import deepcopy

class Table(object):
    def __init__(self, name, sb, bb, sits_count, max_buyin):
        self.diler = Diler()
        self.sb = sb
        self.bb = bb 
        self.max_buyin = max_buyin
        self.table_history = []
        self.sits = range(1, sits_count + 1)
        self.players = {}

    def add_player(self, player):
        """Registers player for current table"""
        tplayer = PlayerAtTable(player)
        tplayer.take_sit(__available_sits__())
        tplayer.make_buyin(max_buyin)
        self.players.append(tplayer)
        tplayer.become_active()
        
    def remove_player(self, player):
        """Removes player from current table"""
        pass
        

    def __available_sits__(self):
        """Returns list of sits numbers that are avaialble for players"""
        return list(set(sits) - set(__occupied_sits__()))

    def __occupied_sits__(self):
        """Returns list of sits numbers that are occupied by players"""
        return [player.sit for player in players]

class Game(object):
    def __init__(self, players):
        self.players = players
        self.banks = []
        game_info = {
            'cards': []
            'moves': []
            'sb': self.sb
            'bb': self.bb
            'but_pos': self.but_pos
            'bankrolls': dict([(player.plid, player.bankroll)\
                               for player in players])
            }

   
    def start_game(self):
        self.button_pos = 0
        pass


    def play_game(self):
        """Implementation of game flow"""
        # Give each player two cards
        for player in players:
            player.cards = diler.give_two_cards()

        bank_no = 0
        self.banks.append({'value': 0, 'players': None})
        # Start a rounds of bets
        for round_no in range(4)
            game_info['moves'].append([])
            if round_no == 1:
                game_info[round_no]['cards'] = diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                game_info[round_no]['cards'] = diler.give_card()
	        lap_no = 0
	        while True:
                game_info['moves'][round_no] = []
	            for player in players:
	                move = player.make_move(game_info)
	                game_info[round_no]['laps'][lap_no].append(move)
	                self.banks[bank_no]['value'] += move['decision'].value
	                player.bankroll -= move['decision'].value
                    # Handling a case when player went all-in
                    if player.bankroll == 0:
                        self.banks[bank_no]['players'] = players
                        players.remove[player]
                        self.banks.append({'value': 0, 'players': None})

	            if __round_finished__(game_info):
	                break
	            lap_no += 1
	            game_info[round_no]['laps'].append([])
    
            if __game_finished__(game_info):
                break
            
    def __verify_move__(self, lap_history, move):
        lap_hist = remove_folds(lap_history)
        if len(lap_hist) > 0:
            return  move['decision'].value >= \
                lap_hist[-1]['decision'].value and \
                move['decision'].value % bb_val == 0 
        else:
            return True
    
    def __game_finished__(self, lap_history):
        return len(remove_folds(lap_history)) == __occupied_sits__()

    def __round_finished__(self, lap_history, players_num):
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
            
    def __remove_folds__(self, lap_history):
        """Removes moves with "fold" type from lap history. Returns resulting lap history."""
        lap_hist = deepcopy(lap_history)
        for move in lap_hist:
            if move['decision'].des_type == DES_TYPE.FOLD:
                lap_hist.remove(move)
        return lap_hist

    def __is_allin__(self, lap_history):
        """Returns True if last move in lap_history is all-in"""
        if len(lap_history) == 1 and \
           lap_history[0]['decision'] < self.sb and \
           lap_history[0]['player_id']

