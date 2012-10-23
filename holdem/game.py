from holdem.different import *
from copy import deepcopy

class Game(object):
    """
    Implementation of game abstraction.
    """
    def __init__(self, table):
        self.table = table
        self.players = table.players
        self.diler = table.diler
        self.banks = []
        self.sbl = table.sbl
        self.bbl = table.bbl
        self.sits = table.sits
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
                               for player in self.players])
            }
   
    def play_game(self):
        """Implementation of game flow"""
        # Sort players accroding to button position
        func = lambda player: player.sit if player.sit > self.but_pos \
                                            else player.sit + len(self.sits)
        self.players.sort(key = func)
        # Give each player two cards
        for player in self.players:
            player.cards = self.diler.give_two_cards()

        current_bank = {'value': 0, 'player_ids': None}

        folds = []
        allins = []
        made_move = []
        will_move = self.players

        # Start a rounds of bets
        for round_no in range(4):
            self.game_info['moves'].append([])
            self.game_info['cards'].append([])
            if round_no == 1:
                self.game_info['cards'][round_no] = self.diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                self.game_info['cards'][round_no] = self.diler.give_card()
    
            # Show cards handed out by diler
            self.table.display_cards(self.game_info)

            if len([player for player in self.players \
                                if player.bankroll != 0]) < 2:
                continue

            while len(will_move) != 0:
                player = will_move.pop(0) 
                if player not in allins:
                    move = player.make_move(self.game_info, self.__cum_bets__)
                else: 
                    continue
                # Show player's move
                # self.table.display_move(self.game_info)
                self.game_info['moves'][round_no].append(move)
                bet = move['decision'].value
                player.bankroll -= bet
                if move['decision'].dec_type == DecisionType.FOLD:
                    folds.append(player)
                    continue
                # Handling a case when player went all-in
                elif move['decision'].dec_type == DecisionType.ALLIN
                    allins.append(player)
                    continue
                elif move['decision'].dec_type == DecisionType.RAISE
                    will_move.extend(made_move)
                elif move['decision'].dec_type == DecisionType.RAISEALLIN
                    allins.append(player)
                    will_move.extend(made_move)
                    continue

                made_move.append(player)
                                
            # Checking end of game condition
            if len(made_move) == 1:
                break

        # Determine winners
        winner_ids = self.__determine_winners__()

        for round_no in range(3):
            for bank in self.banks[round_no]:
                # Filter out players that haven't finished a game
                bank['player_ids'] = list(set(bank['player_ids']) & \
                                       set(winner_ids))
                
                # Share bank among winners
                for player_id in bank['player_ids']:
                    self.__player_by_id__(player_id).bankroll \
                        += bank['value'] / len(bank['player_ids'])

    def __player_by_id__(self, plid):
        """
        Returns a player instance given it's id.
        """
        return filter(lambda pl: True if pl.plid == plid \
                                        else False, self.players)[0] 

    def __determine_winners__(self):
        """
        Returns a list of winners ids.
        """
        cards_on_table = []
        # Form a list of cards handed out by diler
        for cards in self.game_info['cards']:
            cards_on_table.extend(cards)
        # Making list of tuples with players ids and their best combinations
        pl_combs = [(pl.plid, self.diler.best_comb(cards_on_table + pl.cards)) \
                    for pl in self.players]
        # Defining sorting function for list of tuples mentioned above
        sort_func = lambda comb1, comb2: \
                        self.diler.compare_combs(comb1[1], comb2[1])
        # Sort list of tuples mentioned above, preparing to determine winners
        pl_combs.sort(cmp = sort_func, reverse = True)
        winners_ids = []
        # Determing winners ids
        for comb in pl_combs:
            if self.diler.compare_combs(comb[1], pl_combs[0][1]) == 0:
                winners_ids.append(comb[0])

        return winners_ids

    def __calculate_banks__(self, game_info):
        """
        Returns list of banks with values and player ids sharing them
        """
        banks = [{}]
        for moves_round in game_info['moves']:
            for move in moves_round:
                if move['decision'].dec_type == DecisionType.FOLD and \
                        move['plid'] in  
                 
        
