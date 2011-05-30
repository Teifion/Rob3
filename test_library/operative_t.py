import unittest
from rules import operative_rules
from classes import operative

def empty_city(x, y, pop):
	return city.City({"x":x,"y":y,"population":pop})

class Operative_rule_functions(unittest.TestCase):
	test_targets = [operative_rules.get_cost, operative_rules.get_reinforce_cost]
	
	def test_get_cost(self):
		vals = (
			({"Stealth":1, "Integration":1, "Sedition":1, "Sabotage":1, "Assassination":1, "Observation":1, "Size":1}, 5),
			({"Stealth":5, "Integration":1, "Sedition":1, "Sabotage":1, "Assassination":1, "Observation":1, "Size":1}, 9),
			({"Stealth":5, "Integration":1, "Sedition":1, "Sabotage":1, "Assassination":1, "Observation":1, "Size":2}, 18),
		)
		
		for data, expected in vals:
			r = operative_rules.get_cost(data).get("Materials")
			r2 = operative_rules.get_cost(**data).get("Materials")
			
			self.assertEqual(r, r2)
			self.assertEqual(expected, r)
	
	def test_get_reinforce(self):
		vals = (
			(operative.Operative({"stealth":1, "integration":1, "sedition":1, "sabotage":1, "assassination":1, "observation":1, "size":1}), 1, 5),
			(operative.Operative({"stealth":1, "integration":1, "sedition":1, "sabotage":1, "assassination":1, "observation":1, "size":1}), 5, 25),
			(operative.Operative({"stealth":5, "integration":1, "sedition":1, "sabotage":1, "assassination":1, "observation":1, "size":1}), 1, 9),
		)
		
		for the_op, amount, expected in vals:
			r = operative_rules.get_reinforce_cost(the_op, amount).get("Materials")
			self.assertEqual(expected, r)
		
	
