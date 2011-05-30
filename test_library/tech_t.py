import unittest
from rules import tech_rules
from data_classes import tech
from test_library.orders_t_lib import Dead_cursor
from classes import res_dict

# Dead_cursor = orders_t_lib.Dead_cursor

class Tech_cost_rules(unittest.TestCase):
	test_targets = [tech_rules.cost_for_this_level, tech_rules.cost_for_next_level, tech_rules.cost_to_get_to_level]
	
	def test_cost_for_this_level(self):
		vals = (
			(tech.Tech({"base_cost":"Materials:10","extra_cost":"Materials:10,Tech points:100"}), 5, 100, "Materials:60,Tech Points:400"),
		)
		
		for the_tech, level, completed, answer in vals:
			result = tech_rules.cost_for_this_level(Dead_cursor(), the_tech, level, completed)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)
	
	def test_cost_for_next_level(self):
		vals = (
			(tech.Tech({"base_cost":"Materials:10","extra_cost":"Materials:10,Tech points:100"}), 5, 100, "Materials:70,Tech Points:500"),
		)
		
		for the_tech, level, completed, answer in vals:
			result = tech_rules.cost_for_next_level(Dead_cursor(), the_tech, level, completed)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)
	
	def test_cost_to_get_to_level(self):
		vals = (
			(tech.Tech({"base_cost":"Materials:10","extra_cost":"Materials:10,Tech points:100"}), 5, "Materials:200,Tech Points:1500"),
		)
		
		for the_tech, level, answer in vals:
			result = tech_rules.cost_to_get_to_level(Dead_cursor(), the_tech, level)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)