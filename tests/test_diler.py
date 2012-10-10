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

    def test___same_suit__(self):
        c1 = Card(Rank.THREE, Suit.HEARTS)
        c2 = Card(Rank.THREE, Suit.DIAMONDS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.TWO, Suit.CLUBS)
        c6 = Card(Rank.FIVE, Suit.CLUBS)
        c7 = Card(Rank.JACK, Suit.HEARTS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__same_suit__(cards)
        self.assertSetEqual(set([c3, c4, c5, c6]), set(rcards[0]))
        self.assertSetEqual(set([c1, c7]), set(rcards[1]))
        self.assertSetEqual(set([c2]), set(rcards[2]))

    def test___same_suit__equal_sublists(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.HEARTS)
        c3 = Card(Rank.JACK, Suit.SPADES)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.TWO, Suit.CLUBS)
        c6 = Card(Rank.FIVE, Suit.CLUBS)
        c7 = Card(Rank.THREE, Suit.HEARTS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__same_suit__(cards)

        self.assertSetEqual(set([c4, c5, c6]), set(rcards[0]))
        self.assertSetEqual(set([c1, c2, c7]), set(rcards[1]))
        self.assertSetEqual(set([c3]), set(rcards[2]))

        # Assertions for an order of items in sublists
        self.assertListEqual([c5, c6, c4], rcards[0])
        self.assertListEqual([c7, c2, c1], rcards[1])
        self.assertListEqual([c3], rcards[2])

    def test___check_straight__ace(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.SPADES)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.TWO, Suit.CLUBS)
        c6 = Card(Rank.FIVE, Suit.CLUBS)
        c7 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_straight__(cards)
        self.assertEqual(len(rcards), 5)
        self.assertSetEqual(set(rcards), set([c2, c4, c5, c6, c7]))

    def test___check_straight__five_cards(self):
        c1 = Card(Rank.FOUR, Suit.CLUBS)
        c2 = Card(Rank.SIX, Suit.SPADES)
        c3 = Card(Rank.TWO, Suit.CLUBS)
        c4 = Card(Rank.FIVE, Suit.HEARTS)
        c5 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5]
        rcards = self._diler.__check_straight__(cards)
        self.assertEqual(len(rcards), 5)
        self.assertSetEqual(set(rcards), set([c1, c2, c3, c4, c5]))

    def test___check_straight_flush__positive(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.SIX, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.FIVE, Suit.CLUBS)
        c6 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_straight_flush__(cards)
        self.assertEqual(len(rcards), 5)
        self.assertSetEqual(set(rcards), set([c2, c3, c4, c5, c6]))

    def test___check_straight_flush__positive_wth_ace(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.SPADES)
        c4 = Card(Rank.ACE, Suit.CLUBS)
        c5 = Card(Rank.TWO, Suit.CLUBS)
        c6 = Card(Rank.FIVE, Suit.CLUBS)
        c7 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_straight_flush__(cards)
        self.assertEqual(len(rcards), 5)
        self.assertSetEqual(set(rcards), set([c2, c4, c5, c6, c7]))

    def test___check_straight_flush__negative(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.SIX, Suit.HEARTS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.FIVE, Suit.CLUBS)
        c6 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_straight_flush__(cards)
        self.assertEqual(rcards, None)

    def test___check_straight_flush__negative_not_strght(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.SEVEN, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.FIVE, Suit.CLUBS)
        c6 = Card(Rank.THREE, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_straight_flush__(cards)
        self.assertEqual(rcards, None)

    def test___check_four_of_kind__(self):
        c1 = Card(Rank.JACK, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.JACK, Suit.DIAMONDS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_four_of_kind__(cards)
        self.assertSetEqual(set(rcards), set([c1, c2, c3, c5, c6]))

    def test___check_four_of_kind__negative(self):
        c1 = Card(Rank.THREE, Suit.HEARTS)
        c2 = Card(Rank.FOUR, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.JACK, Suit.DIAMONDS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        c7 = Card(Rank.QUEEN, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_four_of_kind__(cards)
        self.assertEqual(rcards, None)

    def test___check_full_house__(self):
        c1 = Card(Rank.THREE, Suit.HEARTS)
        c2 = Card(Rank.QUEEN, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.JACK, Suit.DIAMONDS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        c7 = Card(Rank.QUEEN, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_full_house__(cards)
        self.assertSetEqual(set(rcards), set([c2, c3, c5, c6, c7]))

    def test___check_full_house__two_thriplets(self):
        c1 = Card(Rank.QUEEN, Suit.HEARTS)
        c2 = Card(Rank.QUEEN, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.JACK, Suit.DIAMONDS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        c7 = Card(Rank.QUEEN, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_full_house__(cards)
        self.assertSetEqual(set(rcards), set([c1, c2, c3, c5, c7]))

    def test___check_flush__(self):
        c1 = Card(Rank.THREE, Suit.CLUBS)
        c2 = Card(Rank.QUEEN, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.CLUBS)
        c4 = Card(Rank.TWO, Suit.CLUBS)
        c5 = Card(Rank.ACE, Suit.CLUBS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        c7 = Card(Rank.KING, Suit.CLUBS)
        cards = [c1, c2, c3, c4, c5, c6, c7]
        rcards = self._diler.__check_flush__(cards)
        self.assertSetEqual(set(rcards), set([c1, c2, c3, c5, c7]))

    def test___check_three_of_kind__(self):
        c1 = Card(Rank.THREE, Suit.CLUBS)
        c2 = Card(Rank.QUEEN, Suit.CLUBS)
        c3 = Card(Rank.JACK, Suit.HEARTS)
        c4 = Card(Rank.JACK, Suit.SPADES)
        c5 = Card(Rank.ACE, Suit.CLUBS)
        c6 = Card(Rank.JACK, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_three_of_kind__(cards)
        self.assertSetEqual(set(rcards), set([c2, c3, c4, c5, c6]))

    def test___check_two_pair__(self):
        c1 = Card(Rank.THREE, Suit.CLUBS)
        c2 = Card(Rank.THREE, Suit.HEARTS)
        c3 = Card(Rank.JACK, Suit.HEARTS)
        c4 = Card(Rank.JACK, Suit.SPADES)
        c5 = Card(Rank.ACE, Suit.CLUBS)
        c6 = Card(Rank.ACE, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_two_pair__(cards)
        self.assertSetEqual(set(rcards), set([c1, c3, c4, c5, c6]))

    def test___check_pair__(self):
        c1 = Card(Rank.THREE, Suit.CLUBS)
        c2 = Card(Rank.THREE, Suit.HEARTS)
        c3 = Card(Rank.JACK, Suit.HEARTS)
        c4 = Card(Rank.JACK, Suit.SPADES)
        c5 = Card(Rank.QUEEN, Suit.CLUBS)
        c6 = Card(Rank.ACE, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_pair__(cards)
        self.assertSetEqual(set(rcards), set([c2, c3, c4, c5, c6]))

    def test___high_card__(self):
        c1 = Card(Rank.THREE, Suit.CLUBS)
        c2 = Card(Rank.THREE, Suit.HEARTS)
        c3 = Card(Rank.JACK, Suit.HEARTS)
        c4 = Card(Rank.JACK, Suit.SPADES)
        c5 = Card(Rank.QUEEN, Suit.CLUBS)
        c6 = Card(Rank.ACE, Suit.SPADES)
        cards = [c1, c2, c3, c4, c5, c6]
        rcards = self._diler.__check_high_card__(cards)
        self.assertSetEqual(set(rcards), set([c1, c3, c4, c5, c6]))

if __name__ == '__main__':
    unittest.main()
