import unittest
from classes import res_dict
from orders import construction_o
from test_library import orders_t_lib
from rules import map_data

class Construction_orders(unittest.TestCase):
	test_targets = [
		construction_o.Construction_block,
		construction_o.building_order
	]
	
	def test_basic_construction(self):
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
	
	def test_multiple_buildings(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = """Build University at City0
Build University at City1
Build University at City2
Build University at City3
Build University at City4""",
			),

			"results": [
				"City0 is 25% of the way through it's University",
				"City1 is 50% of the way through it's University",
				"City2 is 75% of the way through it's University",
				"City3 is 100% of the way through it's University",
				"University could not be built at City4 because you have reached the limit allowed in one city",
			],

			"queries":			[
				'-- Building University at City0 for team:1',
				'UPDATE city_buildings SET completion = 50 WHERE city = 100 AND building = 21;',
				'-- Building University at City1 for team:1',
				'UPDATE city_buildings SET completion = 100 WHERE city = 101 AND building = 21;',
				'-- Building University at City2 for team:1',
				'UPDATE city_buildings SET completion = 150 WHERE city = 102 AND building = 21;',
				'-- Building University at City3 for team:1',
				'UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = 103 AND building = 21;',
			],
			
			
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[w.teams_lookup()['Numericals']].resources = res_dict.Res_dict("Materials:50")
		orders_t_lib.test_orders(self, data)
	
	def test_with_stone_buildings(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = """Build University at City0
Build 25k Walls at City1""",
			),
			
			"results": [
				"City0 is 50% of the way through it's University",
				"City1 is 33% of the way through it's 25k Walls",
			],
			
			"queries":			[
				'-- Building University at City0 for team:1',
				'UPDATE city_buildings SET completion = 100 WHERE city = 100 AND building = 21;',
				'-- Building 25k Walls at City1 for team:1',
				'UPDATE city_buildings SET completion = 100 WHERE city = 101 AND building = 0;',
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[w.teams_lookup()['Numericals']].resources = res_dict.Res_dict("Materials:50,Stone:1")
		orders_t_lib.test_orders(self, data)
	
	def test_without_stone_buildings(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = """Build University at City0
Build 25k Walls at City1""",
			),
			
			"results": [
				"City0 is 25% of the way through it's University",
				"Build 25k Walls at City1 - [neg]Too expensive (5 Materials, 1 Stone)[/neg]",
			],
			
			"queries":			[
				'-- Building University at City0 for team:1',
				'UPDATE city_buildings SET completion = 50 WHERE city = 100 AND building = 21;',
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[w.teams_lookup()['Numericals']].resources = res_dict.Res_dict("Materials:50,Stone:0")
		orders_t_lib.test_orders(self, data)
	
	
	def test_upgrading_buildings(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = """Build 25k Fortifications at City0
Build 25k Fortifications at City1
Build 25k Fortifications at City2""",
			),
			
			"results": [
				"25k Fortifications could not be built at City0 because the required building (25k Walls) is not complete there",
				"City1 is 33% of the way through it's 25k Fortifications",
				"City2 is 100% of the way through it's 25k Fortifications",
			],
			
			"queries": [
				"-- Building 25k Fortifications at City1 for team:1",
				"UPDATE city_buildings SET completion = 100 WHERE city = 101 AND building = 1;",
				"-- Building 25k Fortifications at City2 for team:1",
				"UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = 102 AND building = 1;",
				"DELETE FROM city_buildings WHERE city = 102 AND building = 0;",
			],
			
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		w._teams[w.teams_lookup()['Numericals']].resources = res_dict.Res_dict("Materials:50,Stone:1")
		w._cities[w.cities_lookup()['City0']].buildings[w.buildings_lookup()['25k Walls']] = 100
		w._cities[w.cities_lookup()['City0']].buildings_amount[w.buildings_lookup()['25k Walls']] = 0
		
		w._cities[w.cities_lookup()['City1']].buildings_amount[w.buildings_lookup()['25k Walls']] = 1
		
		w._cities[w.cities_lookup()['City2']].buildings_amount[w.buildings_lookup()['25k Walls']] = 1
		w._cities[w.cities_lookup()['City2']].buildings[w.buildings_lookup()['25k Fortifications']] = 200
		
		orders_t_lib.test_orders(self, data)
		
	
	def test_swamp_terrain(self):
		w = orders_t_lib.dummy_world()
		data = {
			"block": construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['SArkalians'],
				title_name = "Construction",
				content = """Build 25k Walls at Durandalbad
Build castle at Durandalbad""",
			),
			
			"results": [
				"25k Walls could not be built at Durandalbad because Durandalbad is on a swamp",
				"Castle could not be built at Durandalbad because Durandalbad is on a swamp",
			],
			
			"queries":			[],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		w._cities[w.cities_lookup()['Durandalbad']].terrain = map_data.terrain.index("swamp")
		
		data['block'].the_world._teams[w.teams_lookup()['SArkalians']].resources = res_dict.Res_dict("Materials:10")
		orders_t_lib.test_orders(self, data)


class Construction_orders_debug (unittest.TestCase):
	"""Checks each function returns some sort of debug upon failure"""
	test_targets = []
	
	def test_build_limit(self):
		w = orders_t_lib.dummy_world()
		b = construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = "!Build University at City4")
		
		b.setup()
		b.execute()
		self.assertGreater(len(b.debug), 1)
	
	def test_upgrade_requirements(self):
		w = orders_t_lib.dummy_world()
		b = construction_o.Construction_block(
				the_world = w,
				team = w.teams_lookup()['Numericals'],
				title_name = "Construction",
				content = "!Build Expanded University at City0")
		
		b.setup()
		b.execute()
		self.assertGreater(len(b.debug), 1)