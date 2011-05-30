import unittest
import database
from classes import unit, res_dict
from queries import equipment_q
from rules import unit_rules

class Unit_cost(unittest.TestCase):
	test_targets = [
		unit.Unit.get_cost,
		
		unit_rules.disband_cost,
	]
	
	unit_lists = (
		("Untrained arbalest", ["No training", "Arbalest"], (1.5, 6, 0, 0)),
		("Basic arbalest", ["Basic training", "Arbalest"], (2.25, 9, .5625, 2.25)),
		("Standard arbalest", ["Standard training", "Arbalest"], (4, 13, 1, 3.25)),
		("Good arbalest", ["Good training", "Arbalest"], (7.5, 21, 2.25, 6.3)),
		("Exceptional arbalest", ["Exceptional training", "Arbalest"], (11, 29, 3.6, 9.6)),
		("Elite arbalest", ["Elite training", "Arbalest"], (25, 70, 12.5, 35)),
		("Exion Standards", ["Good training", "Mace", "Banded armour suit", "Iron bomb", "Leather suit", "Arquebus"], (18, 33.75, 5.4, 10.125)),
		("Exion Wall Men", ["Repeating crossbow", "Good training"], (5.25, 5.25, 1.575, 1.575)),
		# ("Random test unit", ["short sword", "full plate suit", "elite training", "tower shield", "warhorse"], (5.25, 5.25, 1.575, 1.575)),
		
		("Standard spearmen", ["Standard training", "Spear", "Chainmail jacket", "Large shield"], (3.25, 6.25, 0.8125, 1.5625)),
		("Standard knights", ["Standard training", "Long sword", "Chainmail jacket", "Warhorse"], (9, 15, 2.25, 3.75)),
	)
	
	def test_costs(self):
		cursor = database.get_test_cursor()
		
		# Build lookup dict
		equipment_lookup = {}
		equipment_dict = equipment_q.get_all_equipment(cursor)
		for e, eq in equipment_dict.items():
			equipment_lookup[eq.name.lower()] = eq.id
		
		# Test costs
		for unit_name, equipment_strings, expected_costs in self.unit_lists:
			the_unit = unit.Unit()
			the_unit.name = unit_name
			the_unit.equipment = []
			
			for e in equipment_strings:
				the_unit.equipment.append(equipment_lookup[e.lower()])
			
			actual_costs = the_unit.get_cost(cursor=cursor, equipment_dict=equipment_dict)
			
			try:
				self.assertEqual(expected_costs[0], actual_costs['material_cost'].get("Materials"))
				self.assertEqual(expected_costs[1], actual_costs['iron_cost'].get("Materials"))
				
				self.assertAlmostEqual(expected_costs[2], actual_costs['material_upkeep'].get("Materials"), places=1)
				self.assertAlmostEqual(expected_costs[3], actual_costs['iron_upkeep'].get("Materials"), places=1)
			except Exception as e:
				print("\nFailed with unit: %s" % the_unit.name)
				print("Expected cost: %s" % str(expected_costs))
				print("Actual costs: %s, %s, %s, %s" % (actual_costs['material_cost'], actual_costs['iron_cost'], actual_costs['material_upkeep'], actual_costs['iron_upkeep']))
				
				breakdown = the_unit.get_cost(cursor=cursor, equipment_dict=equipment_dict, breakdown_mode=True)
				print(" - Breakdown - ")
				print("Cost:\n", "\n".join(breakdown['cost']))
				print("")
				print("Upkeep:\n", "\n".join(breakdown['upkeep']))
				
				raise
		
	def test_refund_cost(self):
		vals = (
			("Materials:50", "Materials:-25"),
			("Materials:100", "Materials:-50"),
		)
		
		for cost, answer in vals:
			r_answer = res_dict.Res_dict(answer)
			result = unit_rules.disband_cost(res_dict.Res_dict(cost))
			self.assertEqual(r_answer, result)
		
	
