import unittest

from deripy.algo.profit import OptionPositionProfit, AssetPositionProfit, Commission


class TestOptionPositionProfit(unittest.TestCase):
    def setUp(self):
        self.opp = OptionPositionProfit(
            st=1_000,
            k=1_200,
            premium=150,
            commission=Commission(long=0.00103, short=0.00103),
        )

    def test_profit(self):
        self.assertEqual(self.opp.long_call, -150.15)
        self.assertEqual(self.opp.short_call, 149.85)
        self.assertEqual(self.opp.long_put, 49.85)
        self.assertEqual(self.opp.short_put,  -50.15)
