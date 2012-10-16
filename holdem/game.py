from holdem.different import *
from copy import deepcopy

class Game(object):
    """
    Implementation of game abstraction.
    """
    def __init__(self, players, table, diler):
        self.players = players
        self.diler = diler
        self.banks = []
        self.sbl = table.sbl
        self.bbl = table.bbl
        self.but_pos = table.but_pos
        self.game_info = {
            'cards': [], # Contains list of cards opened by diler
                        # for each round.
            'moves': [], # Contains list of rounds. Each round - list of laps.
                        # Each lap - list of moves.
            'sbl': self.sbl, # Small blind value
            'bbl': self.bbl, # Big blind value
            'but_pos': self.but_pos, # Button position
             # Info about bankrolls before game started
            'bankrolls': dict([(player.plid, player.bankroll)\
                               for player in players])
            }
   
    def play_game(self):
        """Implementation of game flow"""
        # Give each player two cards
        for player in self.players:
            player.cards = self.diler.give_two_cards()

        self.banks.append({'value': 0, 'players': None})
        # Start a rounds of bets
        for round_no in range(4):
            self.game_info['moves'].append([[]])
            self.game_info['cards'].append([])
            if round_no == 1:
                self.game_info['cards'][round_no] = self.diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                self.game_info['cards'][round_no] = self.diler.give_card()
            lap_no = 0
            while True:
                self.game_info['moves'][round_no].append([[]])
                allins = []
                for player in self.players:
                    move = player.make_move(self.game_info)
                    self.game_info['moves'][round_no][lap_no].append(move)
                    bet = move.value
                    if move.dec_type == DecisionType.FOLD:
                        self.players.remove(player)
                    # Handling a case when player went all-in
                    elif player.bankroll == 0:
                        self.banks[-1]['players'] = \
                        [player.plid for player in self.players]
                        self.banks.append({'value': 0, 'players': None})
                        allins.append(bet)
 
                    if len(allins) > 0:
                        diff = 0
                        for i, allin in enumerate(allins):
                            diff = allin['bet'] - diff
                            self.banks[i]['value'] += diff 
                            bet -= diff
                            player.bankroll -= diff
                                
                        self.banks[-1]['value'] += bet
                        player.bankroll -= bet

                if self.__round_finished__(self.game_info, len(allins)):
                    break
                lap_no += 1
                self.game_info[round_no]['laps'].append([])
    
            if len(self.players) < 2:
                break
            
            for bank in self.banks:
                bank['players'] = list(set(bank['players']) & \
                                       set(self.players))
                for player in bank['players']:
                    player.bankroll += bank['value'] / \
                                       len(bank['players'])

    def __round_finished__(self, lap, allins_cnt):
        """
        Returns true if all players made equal bets, false otherwise.
        """
        flap = self.__remove_folds__(lap)
        # Returns False if some players haven't made their bets 
        if len(flap) < len(self.players) - allins_cnt:
            return False 

        first_move = flap[0]
        for move in flap:
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
