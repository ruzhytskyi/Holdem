import unittest
from holdem.game import *
from holdem.table import *
from holdem.diler import *
from holdem.player import *
from holdem.different import *
from copy import deepcopy

class TestGameMethods(unittest.TestCase):

    def setUp(self):
        self.table = Table('tT', 1, 2, 4, 100)
        self.player1 = Player('p1', 300, 1)
        self.player2 = Player('p2', 300, 2)
        self.player3 = Player('p3', 300, 3)
        self.table.add_player(self.player1)
        self.table.add_player(self.player2)
        self.table.add_player(self.player3)
        self.game = Game(self.table) 

    def test___remove_folds__(self):
        move1 = {
            'decision': Decision(DecisionType.BET, 10),
            'plid': 1
        }
        move2 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 2
        }
        move3 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 3
        }

        lap = [move1, move2, move3]
        rlap = self.game.__remove_folds__(lap)
        self.assertEqual(rlap, [move1])
    
    def test___round_finished__positive(self):
        move1 = {
            'decision': Decision(DecisionType.BET, 10),
            'plid': 1
        }
        move2 = {
            'decision': Decision(DecisionType.BET, 10),
            'plid': 2
        }
        move3 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 3
        }

        del(self.game.players[:2])

        lap = [move1, move2, move3]
        allins = set([])
        self.assertTrue(self.game.__round_finished__(allins, lap, 0))

    def test___round_finished__negative(self):
        move1 = {
            'decision': Decision(DecisionType.BET, 10),
            'plid': 1
        }
        move2 = {
            'decision': Decision(DecisionType.BET, 15),
            'plid': 2
        }
        move3 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 3
        }

        del(self.game.players[2:])

        lap = [move1, move2, move3]
        allins = set([2])
        self.assertFalse(self.game.__round_finished__(allins, lap, 0))

    def test___determine_winners__(self):
        c1 = Card(Rank.TWO, Suit.SPADES) 
        c2 = Card(Rank.THREE, Suit.SPADES) 
        c3 = Card(Rank.FOUR, Suit.CLUBS) 
        c4 = Card(Rank.JACK, Suit.SPADES)

        self.game.game_info['cards'] = [[c1, c2, c3], [c4]]

        self.game.players[0].cards = [Card(Rank.ACE, Suit.SPADES),
                                      Card(Rank.FIVE, Suit.HEARTS)]
        self.game.players[1].cards = [Card(Rank.SIX, Suit.HEARTS),
                                      Card(Rank.FIVE, Suit.DIAMONDS)]
        self.game.players[2].cards = [Card(Rank.KING, Suit.SPADES),
                                      Card(Rank.QUEEN, Suit.DIAMONDS)]

        winners_ids = self.game.__determine_winners__()
        self.assertEqual(winners_ids, [1, 2])

    def test___player_by_id__(self):
        self.assertEqual(self.game.__player_by_id__(2), self.game.players[1])

if __name__ == '__main__':
    unittest.main()
