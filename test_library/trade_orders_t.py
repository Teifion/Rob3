import unittest
from classes import res_dict
from orders import construction_o
from test_library import orders_t_lib
from rules import map_data

class Trade_orders(unittest.TestCase):
	test_targets = [
		# construction_o.Construction_block,
		# construction_o.building_order
	]
	
	def ttest_basic_construction(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['SArkalians'],
				title_name = "Construction",
				content = """Build University at Durandalbad
Build University at Durandalbad""",
			),
			
			"results": [
				"Durandalbad is 25% of the way through it's University",
				"University could not be built at Durandalbad because Durandalbad is already constructing a building this year",
			],
			
			"queries":			[
				'-- Building University at Durandalbad for team:0',
				'UPDATE city_buildings SET completion = 50 WHERE city = 0 AND building = 21;'
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[w.teams_lookup()['SArkalians']].resources = res_dict.Res_dict("Materials:10")
		orders_t_lib.test_orders(self, data)

# class Construction_orders_debug (unittest.TestCase):
# 	"""Checks each function returns some sort of debug upon failure"""
# 	test_targets = []
# 	
# 	def test_build_limit(self):
# 		w = orders_t_lib.dummy_world()
# 		b = construction_o.Construction_block(
# 				the_world = w,
# 				team = w.teams_lookup()['Numericals'],
# 				title_name = "Construction",
# 				content = "!Build University at City4")
# 		
# 		b.setup()
# 		b.execute()
# 		self.assertGreater(len(b.debug), 1)
# 	
# 	def test_upgrade_requirements(self):
# 		w = orders_t_lib.dummy_world()
# 		b = construction_o.Construction_block(
# 				the_world = w,
# 				team = w.teams_lookup()['Numericals'],
# 				title_name = "Construction",
# 				content = "!Build Expanded University at City0")
# 		
# 		b.setup()
# 		b.execute()
# 		self.assertGreater(len(b.debug), 1)