from holdem.diler import *
from holdem.different import *
import unittest

class TestDilerMethods(unittest.TestCase):

    def setUp(self):
        self._deck = Deck() 
        self._diler = Diler(self._deck) 

    def test___is_straight__valid_comb(self):
        comb = []
        comb.append(Card(Rank.TWO, Suit.HEARTS))
        comb.append(Card(Rank.SIX, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertTrue(self._diler.__is_straight__(comb))


    def test___is_straight__valid_comb_wth_ace(self):
        comb = []
        comb.append(Card(Rank.TWO, Suit.HEARTS))
        comb.append(Card(Rank.ACE, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertTrue(self._diler.__is_straight__(comb))

    def test___is_straight__inv_comb(self):
        comb = []
        comb.append(Card(Rank.THREE, Suit.HEARTS))
        comb.append(Card(Rank.ACE, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertFalse(self._diler.__is_straight__(comb))

    def test___same_rank__(self):
        c1 = Card(Rank.THREE, Suit.HEARTS)
        c2 = Card(Rank.THREE, Suit.DIAMONDS)
        c3 = Card(Rank.ACE, Suit.DIAMONDS)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.ACE, Suit.SPADES)
        c6 = Card(Rank.ACE, Suit.HEARTS)
        c7 = Card(Rank.JACK, Suit.HEARTS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__same_rank__(cards)
        self.assertSetEqual(set([c3, c4, c5, c6]), set(rcards[0]))
        self.assertSetEqual(set([c1, c2]), set(rcards[1]))
        self.assertSetEqual(set([c7]), set(rcards[2]))

    def test___same_rank__equal_sublists(self):
        c1 = Card(Rank.THREE, Suit.HEARTS)
        c2 = Card(Rank.THREE, Suit.DIAMONDS)
        c3 = Card(Rank.ACE, Suit.DIAMONDS)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.ACE, Suit.SPADES)
        c6 = Card(Rank.QUEEN, Suit.HEARTS)
        c7 = Card(Rank.THREE, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__same_rank__(cards)
        self.assertSetEqual(set([c3, c4, c5]), set(rcards[0]))
        self.assertSetEqual(set([c1, c2, c7]), set(rcards[1]))
        self.assertSetEqual(set([c6]), set(rcards[2]))

    def test___highest_rank__(self):
        c1 = Card(Rank.QUEEN, Suit.CLUBS)
        c2 = Card(Rank.THREE, Suit.DIAMONDS)
        c3 = Card(Rank.ACE, Suit.DIAMONDS)
        cards = [c1, c2, c3]
        self.assertEqual(self._diler.__highest_rank__(cards), Rank.ACE)
        

if __name__ == '__main__':
    unittest.main()
