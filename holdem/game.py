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
        self.table.on_game_started()
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
        will_move = self.players[:]

        # Start a rounds of bets
        for round_no in range(4):
            self.game_info['moves'].append([])
            self.game_info['cards'].append([])
            if round_no == 1:
                self.game_info['cards'][round_no] = self.diler.give_three_cards()
            elif round_no == 2 or round_no == 3:
                self.game_info['cards'][round_no] = [self.diler.give_card()]
    
            # Show cards handed out by diler
            self.table.display_cards(self.game_info)

            while len(will_move) != 0:
                player = will_move.pop(0) 

                if player not in allins:
                    self.table.display_move_start()
                    # Show player's move
                    move = player.make_move(self.game_info)
                    self.table.display_move(move)
                else: 
                    continue

                self.game_info['moves'][round_no].append(move)
                bet = move['decision'].value
                player.bankroll -= bet
                if move['decision'].dec_type == DecisionType.FOLD:
                    folds.append(player)
                    continue
                # Handling a case when player went all-in
                elif move['decision'].dec_type == DecisionType.ALLINLOWER:
                    allins.append(player)
                    continue
                elif move['decision'].dec_type == DecisionType.RAISE:
                    will_move.extend(made_move)
                    made_move = [player]
                elif move['decision'].dec_type == DecisionType.ALLINRAISE:
                    allins.append(player)
                    will_move.extend(made_move)
                    made_move = []
                    continue
                else:
                    made_move.append(player)

                # Checking end of game: if only one player left in game
                if len(made_move) == 0 and len(allins) == 0 \
                        and len(will_move) == 1:
                    made_move.append(will_move.pop(player))
                    break

                # Handle big blind bet: add player to moves queue
                if round_no == 0 and len(self.game_info['moves'][0]) == 2:
                    will_move.extend(made_move)
                    made_move = []

                                
            # Checking end of game condition: if only one player in next round
            if len(made_move) == 1 and len(allins) == 0:
                break
            
            # Checking if there are allin players
            if len(made_move) < 2 and len(allins) > 0:
                continue

            # Players who made move in this round will move in next round
            if round_no != 3:
                will_move = made_move[:]
                made_move = []
        
        finalists = made_move[:] + allins
        # Determine winners
        fin_ids = [fn.plid for fn in finalists]
        pots = self.__calculate_pots__(self.game_info)

        # Share pots among winners
        for pot in pots:
            cand_ids = list(set(pot['plids']) & set(fin_ids))
            candidates = [self.__player_by_id__(pid) for pid in cand_ids] 
            winner_combs = self.__determine_winners__(self.game_info, candidates)
            winner_ids = [wc[0] for wc in winner_combs]
            for plid in winner_ids:
                amount = round(pot['value']/len(winner_ids))
                comb = dict(winner_combs)[plid]
                self.__player_by_id__(plid).bankroll += amount 
                self.table.announce_win(plid, comb, amount)

    def __player_by_id__(self, plid):
        """
        Returns a player instance given it's id.
        """
        return filter(lambda pl: True if pl.plid == plid \
                                        else False, self.players)[0] 

    def __determine_winners__(self, game_info, candidates):
        """
        Returns a list of winners ids.
        """
        cards_on_table = []
        # Form a list of cards handed out by diler
        for cards in game_info['cards']:
            cards_on_table.extend(cards)
        # Making list of tuples with players ids and their best combinations
        pl_combs = [(pl.plid, self.diler.best_comb(cards_on_table + pl.cards)) \
                    for pl in candidates]
        # Defining sorting function for list of tuples mentioned above
        sort_func = lambda comb1, comb2: \
                        self.diler.compare_combs(comb1[1], comb2[1])
        # Sort list of tuples mentioned above, preparing to determine winners
        pl_combs.sort(cmp = sort_func, reverse = True)
        winner_combs = []
        # Determing winners ids
        for comb in pl_combs:
            if self.diler.compare_combs(comb[1], pl_combs[0][1]) == 0:
                winner_combs.append(comb)

        return winner_combs

    def __calculate_pots__(self, game_info):
        """
        Returns list of pots with values and player ids illegible to share them
        """
        shares = {}
        for mround in game_info['moves']:
            for move in mround:
                if move['plid'] not in shares.keys():
                    shares[move['plid']] = move['decision'].value
                else:
                    shares[move['plid']] += move['decision'].value

        lshares = shares.items()
        lshares.sort(key = lambda el: el[1])
        pots = []
        for i, share in enumerate(lshares):
            pot = {}
            pot['value'] = share[1]*(len(lshares) - i) 
            pot['plids'] = [sh[0] for sh in lshares[i:]]
            for j in range(i + 1, len(lshares)):
                lshares[j] = (lshares[j][0], lshares[j][1] - share[1])
            pots.append(pot)
        return pots
            
