import unittest
from rules import spell_rules
from data_classes import spell
from test_library.orders_t_lib import Dead_cursor
from classes import res_dict

# Dead_cursor = orders_t_lib.Dead_cursor

class Spell_cost_rules(unittest.TestCase):
	test_targets = [spell_rules.cost_for_this_level, spell_rules.cost_for_next_level, spell_rules.cost_to_get_to_level]
	
	def test_cost_for_this_level(self):
		vals = (
			(spell.Spell({"tier":spell.tiers.index("Mid"),"category":spell.categories.index("Light")}), 5, 0, "Materials:9.5,Spell Points:85"),
		)
		
		for the_Spell, level, completed, answer in vals:
			result = spell_rules.cost_for_this_level(Dead_cursor(), the_Spell, level, completed, in_spell_points=True)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)
	
	def test_cost_for_next_level(self):
		vals = (
			(spell.Spell({"tier":spell.tiers.index("Mid"),"category":spell.categories.index("Light")}), 5, 0, "Materials:11,Spell Points:100"),
			(spell.Spell({"tier":spell.tiers.index("Mid"),"category":spell.categories.index("Light")}), 5, 50, "Materials:11,Spell Points:50"),
		)
		
		for the_Spell, level, completed, answer in vals:
			result = spell_rules.cost_for_next_level(Dead_cursor(), the_Spell, level, completed, in_spell_points=True)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)
	
	def test_cost_to_get_to_level(self):
		vals = (
			(spell.Spell({"tier":spell.tiers.index("Mid"),"category":spell.categories.index("Light")}), 5, "Materials:32.5,Spell Points:275"),
		)
		
		for the_Spell, level, answer in vals:
			result = spell_rules.cost_to_get_to_level(Dead_cursor(), the_Spell, level, in_spell_points=True)
			
			r_answer = res_dict.Res_dict(answer)
			
			self.assertEqual(result, r_answer)