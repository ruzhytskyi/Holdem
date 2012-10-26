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
    
    def test___calculate_pots__(self):
        m1 = {
                 'plid': 1,
                 'decision': Decision(DecisionType.CHECK, 0)
             }
        m2 = {
                'plid': 2,
                'decision': Decision(DecisionType.BET, 10)
             }
        m3 = {
                'plid': 3,
                'decision': Decision(DecisionType.RAISE, 30)
             }
        m4 = {
                'plid': 1,
                'decision': Decision(DecisionType.ALLIN, 20)
             }
        m5 = {
                'plid': 2,
                'decision': Decision(DecisionType.CALL, 20)
             }
        game_info = {'moves': []}
        game_info['moves'].append([m1, m2, m3, m4, m5])
        m1 = {
                'plid': 2,
                'decision': Decision(DecisionType.BET, 50)
             }
        m2 = {
                'plid': 3,
                'decision': Decision(DecisionType.ALLIN, 30)
             }
        game_info['moves'].append([m1, m2])
        pots = self.game.__calculate_pots__(game_info)
        print pots


if __name__ == '__main__':
    unittest.main()
