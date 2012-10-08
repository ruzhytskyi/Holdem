table_history = [game_history1, game_history2]
game_history = [round1, round2] # is a list of round_histories
round_history = [lap1, lap2] # is a list of laps during round 
lap_history = [move1, move2] # is a list of moves for one lap
move1 = {
    'player': 'Player1',
    'decision': decision,
}

from copy import deepcopy

class Table(object):
    def __init__(self, name, sb, bb, sits_count, max_buyin):
        self.diler = Diler()
        self.sb = sb
        self.bb = bb 
        self.max_buyin = max_buyin
        self.table_history = []
        self.sits = [{'player': 'empty', 'bankroll': 0, 'is_active': True} for i in range(sits_count)]

    def add_player(self, player):
        """Registers player for current table"""
        sit = player.choose_sit(__available_sits__())
        sits[sit]['player'] = player
        sits[sit]['bankroll'] = player.make_buyin(max_buyin)
        sits[sit]['is_active'] = True
        
    def remove_player(self, player):
        """Removes player from current table"""
        sit = [sits.index(x) for x in sits if x['player'] == player]
        player.receive_surplus(sits[sit]['bankroll'])
        sits[sit]['player'] = 'empty'
        sits[sit]['bankroll'] = 0
        sits[sit]['is_active'] = False

    def __available_sits__(self):
        """Returns list of sits numbers that are avaialble for players"""
        return [sits.index(x) for x in sits if x['player'] == 'empty']  

    def __occupied_sits__(self):
        """Returns list of sits numbers that are occupied by players"""
        return list(set(range(sits_count)) - set(__available_sits__()))
    
    def start_game(self):
        self.button_pos = 0
        pass

    def __preflop__(self):
        """Implementation of preflop round"""
        player_index = 0
        active_sits = [sits.index(x) for x in sits if x['is_active'] == True]
        while not __round_finished__(cur_lap_hist):
            # Should be refactored according to real player methods
            move = players[player_index].make_move(game_history)
            if self.verify_move(lap_history, move, bb_val): 
                lap_history.append(move)
            
    def __verify_move__(self, lap_history, move):
        lap_hist = remove_folds(lap_history)
        if len(lap_hist) > 0:
            return  move['decision'].value >= \
                lap_hist[-1]['decision'].value and \
                move['decision'].value % bb_val == 0 
        else:
            return True
    
    def __game_finished__(self, lap_history):
        return len(remove_folds(lap_history)) == __occupied_sits()__

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
