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
        self.game_info = {
            'cards': [], # Contains list of cards opened by diler
                        # for each round.
            'moves': [], # Contains list of rounds. Each round - list of laps.
                        # Each lap - list of moves.
            'sb': self.sb, # Small blind value
            'bb': self.bb, # Big blind value
            'but_pos': self.but_pos, # Button position
             # Info about bankrolls before game started
            'bankrolls': dict([(player.plid, player.bankroll)\
                               for player in players])
            }
   
    def play_game(self):
        """Implementation of game flow"""
        # Give each player two cards
        for player in players:
            player.cards = diler.give_two_cards()

        bank_no = 0
        self.banks.append({'value': 0, 'players': None})
        # Start a rounds of bets
        for round_no in range(4)
            game_info['moves'].append([[]])
            game_info['cards'].append([])
            if round_no == 1:
                game_info['cards'][round_no] = diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                game_info['cards'][round_no] = diler.give_card()
            lap_no = 0
            while True:
                game_info['moves'][round_no].append([[]])
                allins = []
                for player in players:
                    move = player.make_move(game_info)
                    game_info['moves'][round_no][lap_no].append(move)
                    bet = move.value
                    if move.dec_type == DecisionType.FOLD:
                        self.players.remove(player)
                    # Handling a case when player went all-in
                    elif player.bankroll == 0:
                        self.banks[-1]['players'] = \
                        [player.plid for player in players]
                        self.banks.append({'value': 0, 'players': None})
                        self.allins.append(bet)
 
                    if len(allins) > 0:
                        diff = 0
                        for i, allin in enumerate(self.allins):
                            diff = allin['bet'] - diff
                            banks[i]['value'] += diff 
                            bet -= diff
                            player.bankroll -= diff
                                
                        self.banks[-1]['value'] += bet
                        player.bankroll -= bet

                if __round_finished__(game_info):
                    break
                lap_no += 1
                game_info[round_no]['laps'].append([])
    
            if len(self.players) < 2:
                break
            
            for bank in banks:
                bank['players'] = list(set(bank['players']) & \
                                       set(players))
                for player in bank['players']:
                    player.bankroll += bank['value'] / \
                                       len(bank['players'])

    def __round_finished__(self, lap, allins_cnt):
        """
        Returns true if all players made equal bets, false otherwise.
        """
        flap = remove_folds(lap)
        # Returns False if some players haven't made their bets 
        if len(flap) < len(self.players) - allins_cnt:
            return False 

        first_move = flap[0]
        for i, move in enumerate(flap, 1):
            if move['decision'].value != first_move['decision'].value:
                return False
        return True
            
    def __remove_folds__(self, lap):
        """
        Removes moves with "fold" type from moves list.
        Returns resulting lap info.
        """
        clap = deepcopy(lap)
        for move in clap:
            if move['decision'].des_type == DecisionType.FOLD:
                clap.remove(move)
        return clap 

