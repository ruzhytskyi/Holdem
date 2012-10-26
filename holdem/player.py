from random import randint
from holdem.different import Decision
from holdem.different import DecisionType

class Player(object):
    """
    Implementation of player abstraction.
    """
    def __init__(self, name, cash_amount, plid):
        self.name = name
        self.cash_amount = cash_amount
        self.plid = plid

class PlayerAtTable(object):
    """
    Implementation of player at a table abstraction
    """
    def __init__(self, player):
        self.player = player
        self.plid = player.plid
        self.bankroll = 0
        self.is_active = False
        self.cards = []

    def make_move(self, game_info):
        """
        Implementation of player's strategy.
        """
        r = randint(0, 5)
        if r == 0:
            return {'plid': self.player.plid, 
                    'decision': Decision(DecisionType.FOLD, 0)}
        else:
            return {'plid': self.player.plid,
                    'decision': Decision(DecisionType.BET, r)}
            
    def take_sit(self, available_sits):
        """Player chooses a sit among available"""
        self.sit = available_sits[randint(0, len(available_sits) -1 )]
                
    def make_buyin(self, min_buyin):
        """Player makes a buy-in"""
        buyin = max(min_buyin, self.player.cash_amount)
        self.player.cash_amount -= buyin
        self.bankroll += buyin

    def receive_surplus(self, value):
        """Increase players cash amount when player leaves a game"""
        self.player.cash_amount += value
        self.bankroll -= value

    def become_active(self):
        """If active, player joins next game"""
        self.is_active = True

    def become_inactive(self):
        """If inactive, player skips next game"""
        self.is_active = False

class CLIPlayer(Player):
    """
    Implementation of command line interface player
    """
    def __init__(self, player):
        self.player = player
        self.plid = player.plid
        self.bankroll = 0
        self.is_active = False
        self.cards = []

    def make_move(self, game_info):
        """
        Implementation of player's strategy.
        """
        print "Now it is %r players move" % self.plid
        moves = []
        # Making one list for all moves
        for mround in game_info['moves']:
            moves.extend(mround)
        if len(moves) == 0:
            print "Player's move: small blind - %r" %game_info['sbl']
            return {'plid': self.player.plid,
                    'decision': Decision(DecisionType.BET, game_info['sbl'])}
        if len(moves) == 1:
            print "Player's move: big blind - %r" %game_info['bbl']
            return {'plid': self.player.plid,
                    'decision': Decision(DecisionType.RAISE, game_info['bbl'])}
          
        # Last not FOLD and not ALLIN bet
        min_bet = 0
        # Last not FOLD and not ALLIN move
        last_move = None
        for move in reversed(moves):
            if move['decision'].dec_type == DecisionType.FOLD:
                continue
            if move['decision'].dec_type == DecisionType.ALLINLOWER:
                continue
            min_bet = move['decision'].value
            last_move = move
            break 
            
        print "Minimal allowed bet is: %r" % min_bet
        print "Maximum allowed bet is: %r" % self.bankroll
        # Last not FOLD and not ALLIN decision type
        if last_move != None:
            last_dec_type = last_move['decision'].dec_type
        while True:
            print "Make a bet or fold: 'f'."
            bet = raw_input("Please, make a bet: ")
            if bet == 'f':
                return {'plid': self.player.plid,
                        'decision': Decision(DecisionType.FOLD, 0)}

            bet = int(bet) 
            
            if min_bet <= bet <= self.bankroll:
                if bet > 0 and last_move == None:
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.BET, bet)} 
                elif bet == 0 and last_move == None:
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.CHECK, bet)}
                elif bet == min_bet and last_dec_type == DecisionType.CHECK:
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.CHECK, bet)} 
                elif bet == min_bet and last_dec_type != DecisionType.CHECK: 
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.CALL, bet)}
                elif bet < min_bet:
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.ALLINLOWER, bet)}
                elif bet >= min_bet and bet == self.bankroll:
                    return {'plid': self.player.plid,
                            'decision': Decision(DecisionType.ALLINRAISE, bet)}
            else:
                print "You've made a wrong move. Try again."
       
    def take_sit(self, available_sits):
        """Player chooses a sit among available"""
        print "Currently available sits are: %r" % available_sits
        while True:
# For debug purpose
#            sit = raw_input("Please, choose your sit: ")
            sit = available_sits[randint(0, len(available_sits) - 1)]
            if int(sit) in available_sits:
                self.sit = int(sit)
                break
            else:
                print "This sit is not among available."

    def make_buyin(self, min_buyin):
        """Player makes a buy-in"""
        print "Your cash amount is: %r. Min buyin for this table is: %r" \
               % (self.player.cash_amount, min_buyin) 

        while True:
            # buyin = int(raw_input("Please, choose an amount of chips to start with: "))
            buyin = 200
            if min_buyin <= buyin <= self.player.cash_amount:
                self.player.cash_amount -= buyin
                self.bankroll += buyin 
                break
            else:
                print "Your choise doesn't satisfy given constraints"


    def receive_surplus(self, value):
        """Increase players cash amount when player leaves a game"""
        self.player.cash_amount += value
        self.bankroll -= value

    def become_active(self):
        """If active, player joins next game"""
        self.is_active = True

    def become_inactive(self):
        """If inactive, player skips next game"""
        self.is_active = False

