import unittest
from rules import sad_rules, map_data
from functions import trade_f
from classes import city

class Trade_functions (unittest.TestCase):
	test_targets = [
		trade_f.make_supply_change_query
	]
	
	def test_make_supply_change_query(self):
		vals = (
			(1, 1, ["UPDATE cities SET supply_good = 1 WHERE id = 1;"]),
			(9, 5, ["UPDATE cities SET supply_good = 5 WHERE id = 9;"]),
		)
		
		for city, res, expected in vals:
			self.assertEqual(expected, trade_f.make_supply_change_query(city, res))