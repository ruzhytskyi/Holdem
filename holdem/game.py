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
        # Start a rounds of bets
        for round_no in range(4):
            print self.game_info['moves']
            self.game_info['moves'].append([])
            print self.game_info['moves']
            self.game_info['cards'].append([])
            if round_no == 1:
                self.game_info['cards'][round_no] = self.diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                self.game_info['cards'][round_no] = self.diler.give_card()
            lap_no = 0
    
            # Show cards handed out by diler
            self.table.display_cards(self.game_info)

            if len([player for player in self.players \
                                if player.bankroll != 0]) < 2:
                continue

            while True:
                self.game_info['moves'][round_no].append([])
                allins = []
                allin_ids = set([])
                # Position in list where removed items will be copied
                # to be deleted later
                pos = 0
                for i, player in enumerate(self.players):
                    if player.plid not in allin_ids:
                        move = player.make_move(self.game_info)
                    else: 
                        continue
                    # Show player's move
                    # self.table.display_move(self.game_info)
                    self.game_info['moves'][round_no][lap_no].append(move)
                    bet = move['decision'].value
                    player.bankroll -= bet
                    if move['decision'].dec_type == DecisionType.FOLD:
                        self.players.insert(pos, self.players.pop(i))
                        continue
                    # Handling a case when player went all-in
                    if player.bankroll == 0:
                        current_bank['player_ids'] = \
                            [player.plid for player in self.players[pos:]]
                        self.banks[round_no].append(deepcopy(current_bank))
                        current_bank = {'value': 0, 'player_ids': None}
                        allins.append(bet)
                        allin_ids.add(player.plid)
                    # Handle multiple banks situation (one or more allins) 
                    if len(allins) > 0:
                        diff = 0
                        for i, allin in enumerate(allins):
                            diff = allin - diff
                            self.banks[round_no][i]['value'] += diff 
                            bet -= diff
                                
                    current_bank['value'] += bet

                # Remove previously moved items from beginning of the list
                del(self.players[:pos])

                # Checking end of round condition
                if self.__round_finished__(allins, self.game_info['moves'][-1], len(allins)):
                    break
                lap_no += 1
    
            # Checking end of game condition
            if len(self.players) == 1:
                break

        # Finalize current bank and add it to banks list
        current_bank['player_ids'] = \
            [player.plid for player in self.players]
        self.banks[round_no].append(deepcopy(current_bank))
        
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
        

    def __round_finished__(self, allins, laps, allins_cnt):
        """
        Returns true if all players made equal bets, false otherwise.
        """
        flap = self.__remove_folds__(laps[-1])
        # Returns False if some players haven't made their bets 
        if len(flap) < len(self.players) - allins_cnt:
            return False 

        # Calculate cumulative bets
        cum_bets = self.__cum_bets__(laps)
 
        ethval = 0
        for plid, val in cum_bets.items():
            if plid not in allins:
                ethval = val
        print cum_bet
                
        for plid, val in cum_bets.items():
            if plid not in allins and val != ethval:
                return False
        return True
    
    def __cum_bets__(self, laps):
        """
        Returns a dictionary with sums of all bets for each player
        """
        cum_bet = {}
        for lap in laps:
            flap = self.__remove_folds__(lap)
            for move in flap:
                if cum_bet.has_key(move['plid']):
                    cum_bet[move['plid']] += move['decision'].value
                else:
                    cum_bet[move['plid']] = move['decision'].value
        return cum_bet
       
    def __remove_folds__(self, lap):
        """
        Removes moves with "fold" type from moves list.
        Returns resulting lap info.
        """
        pos = 0
        clap = deepcopy(lap)
        for i, move in enumerate(clap):
            if move['decision'].dec_type == DecisionType.FOLD:
                clap.insert(pos, clap.pop(i))
                pos += 1
        del(clap[:pos])
        return clap 
