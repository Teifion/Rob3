import unittest
from classes import res_dict
from orders import construction_o
from test_library import orders_t_lib
from rules import map_data

class Monster_orders(unittest.TestCase):
	test_targets = [
		
	]
	
	def test_basic_monsters(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['SArkalians'],
				title_name = "Monsters",
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