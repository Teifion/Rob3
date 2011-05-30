import unittest
from rules import sad_rules, map_data
from functions import trade_f, sad_f
from classes import city, team
from test_library.deity_sets import deity_t_lib
from rules import sad_rules

dummy_world = deity_t_lib.dummy_world

"""
	A -- B -- C
	  \     /
	   \   /
         D

A can get to C through B or D
"""


class SAD_loop (unittest.TestCase):
	def ttest_loop_1(self):
		w = dummy_world()
		
		city_dict = {
			0:	city.City({
				"name":	"City A",
			}),
			1:	city.City({
				"name":	"City B",
			}),
			2:	city.City({
				"name":	"City C",
			}),
			3:	city.City({
				"name":	"City D",
			}),
		}
		
		for k, v in city_dict.items():
			v.id = k
			v.team = k
			v.goods = {r:0 for r in sad_rules.res_list}
			v.wealth = 100
		
		# City connections
		city_dict[0].connections = {1: 50, 3: 80}
		city_dict[1].connections = {0: 50, 2: 50}
		city_dict[2].connections = {1: 50, 3: 80}
		city_dict[3].connections = {0: 80, 2: 80}
		
		# Goods
		city_dict[0].goods['Grain'] = -100
		city_dict[2].goods['Grain'] = 110
		
		# city_dict[0].goods['Wool'] = -100
		# city_dict[1].goods['Wool'] = 100
		
		team_dict = {
			0:	team.Team({
				"name":	"Team A",
			}),
			1:	team.Team({
				"name":	"Team B",
			}),
			2:	team.Team({
				"name":	"Team C",
			}),
			3:	team.Team({
				"name":	"Team D",
			}),
		}
		
		for k, v in team_dict.items():
			v.techs = {}
		
		#	Relations
		#------------------------
		w._relations = {
			0: {
				1: {'visitor': 1, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 10},
				2: {'visitor': 2, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 10},
				3: {'visitor': 3, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 10},
			},
			1: {
				0: {'visitor': 0, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 10},
				2: {'visitor': 2, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 10},
				3: {'visitor': 3, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 10},
			},
			2: {
				1: {'visitor': 1, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 8},
				0: {'visitor': 0, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 10},
				3: {'visitor': 3, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			3: {
				1: {'visitor': 1, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 10},
				2: {'visitor': 2, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 10},
				0: {'visitor': 0, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 10},
			},
		}
		
		w._cities = city_dict
		
		w.mass_get_checker.add("mass_get_team_techs")
		w.mass_get_checker.add("mass_get_team_deities")
		w.mass_get_checker.add("mass_get_team_evolutions")
		
		# Build caches
		w.tax_cache = {}
		for t1 in team_dict.keys():
			for t2 in team_dict.keys():
				if t1 == t2:
					w.tax_cache[(t1, t2)] = 0
				else:
					w.tax_cache[(t1, t2)] = w.get_taxes(t1, t2)
		
		# Build a distance cache, K1 going to K2
		w.distance_cache = {}
		for k1, c1 in city_dict.items():
			for k2, c2 in city_dict.items():
				if k1 == k2:
					w.distance_cache[(k1, k2)] = 0
				else:
					if k2 in c1.connections:
						w.distance_cache[(k1, k2)] = (1 + (sad_rules.distance_percentage * c1.connections[k2]/100))
		
		# Now for some testing, lets make sure we're getting the right buys/sells from the first loop
		sad_f.find_buys(w, city_dict, verbose=False)
		
		self.assertEqual(
			[('Grain', [2, 1, 0], 84.09097218016095)],
			city_dict[2].sells,
		)
	
	def test_loop_2(self):
		w = dummy_world()
		
		city_dict = {
			0:	city.City({
				"name":	"City A",
			}),
			1:	city.City({
				"name":	"City B",
			}),
			2:	city.City({
				"name":	"City C",
			}),
			3:	city.City({
				"name":	"City D",
			}),
		}
		
		for k, v in city_dict.items():
			v.id = k
			v.team = k
			v.goods = {r:0 for r in sad_rules.res_list}
			v.wealth = 300
		
		# City connections
		city_dict[0].connections = {1: 50, 3: 80}
		city_dict[1].connections = {0: 50, 2: 50}
		city_dict[2].connections = {1: 50, 3: 80}
		city_dict[3].connections = {0: 80, 2: 80}
		
		# Goods
		city_dict[0].goods['Grain'] = -100
		city_dict[3].goods['Grain'] = -100
		city_dict[2].goods['Grain'] = 150
		
		# city_dict[0].goods['Wool'] = -100
		# city_dict[1].goods['Wool'] = 100
		
		team_dict = {
			0:	team.Team({
				"name":	"Team A",
			}),
			1:	team.Team({
				"name":	"Team B",
			}),
			2:	team.Team({
				"name":	"Team C",
			}),
			3:	team.Team({
				"name":	"Team D",
			}),
		}
		
		for k, v in team_dict.items():
			v.techs = {}
		
		#	Relations
		#------------------------
		w._relations = {
			0: {
				1: {'visitor': 1, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			1: {
				0: {'visitor': 0, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			2: {
				1: {'visitor': 1, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 8},
				0: {'visitor': 0, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			3: {
				1: {'visitor': 1, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
				0: {'visitor': 0, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
			},
		}
		
		w._cities = city_dict
		
		w.mass_get_checker.add("mass_get_team_techs")
		w.mass_get_checker.add("mass_get_team_deities")
		w.mass_get_checker.add("mass_get_team_evolutions")
		
		# Build caches
		w.tax_cache = {}
		for t1 in team_dict.keys():
			for t2 in team_dict.keys():
				if t1 == t2:
					w.tax_cache[(t1, t2)] = 0
				else:
					w.tax_cache[(t1, t2)] = w.get_taxes(t1, t2)
		
		# Build a distance cache, K1 going to K2
		w.distance_cache = {}
		for k1, c1 in city_dict.items():
			for k2, c2 in city_dict.items():
				if k1 == k2:
					w.distance_cache[(k1, k2)] = 0
				else:
					if k2 in c1.connections:
						w.distance_cache[(k1, k2)] = (1 + (sad_rules.distance_percentage * c1.connections[k2]/100))
		
		# Now for some testing, lets make sure we're getting the right buys/sells from the first loop
		sad_f.find_buys(w, city_dict, verbose=False)
		sad_f.approve_buys(w, city_dict, verbose=False)
		
		self.assertEqual(
			[
				('Grain', [2, 1, 0], 100),
				('Grain', [2, 3], 50)
			],
			city_dict[2].sells,
		)
		
		# Now we need to actually execute the buys
		sad_f.execute_buys(w, city_dict, verbose=False)
		
		# Now make sure the goods/wealth are correct
		self.assertAlmostEqual(city_dict[0].wealth, 183.24, places=2)
		self.assertAlmostEqual(city_dict[1].wealth, 308.64, places=2)
		self.assertAlmostEqual(city_dict[2].wealth, 464.0, places=2)
		self.assertAlmostEqual(city_dict[3].wealth, 243.96, places=2)
		
		# City A has -15 grain because it couldn't afford the full 100, City C started with 110 so has +25 grain
		self.assertAlmostEqual(city_dict[0].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[1].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[2].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[3].goods['Grain'], -50, places=2)


	def test_loop_3(self):
		w = dummy_world()

		city_dict = {
			0:	city.City({"name":	"City A",}),
			1:	city.City({"name":	"City B",}),
			2:	city.City({"name":	"City C",}),
			3:	city.City({"name":	"City D",}),
			4:	city.City({"name":	"City E",}),
			5:	city.City({"name":	"City F",}),
			6:	city.City({"name":	"City G",}),
			7:	city.City({"name":	"City H",}),
		}
		
		for k, v in city_dict.items():
			v.id = k
			v.team = k
			v.goods = {r:0 for r in sad_rules.res_list}
			v.wealth = 300

		# City connections
		city_dict[0].connections = {1: 50, 3: 80}
		city_dict[1].connections = {0: 50, 2: 50}
		city_dict[2].connections = {1: 50, 3: 80}
		city_dict[3].connections = {0: 80, 2: 80}

		# Goods
		city_dict[0].goods['Grain'] = -100
		city_dict[3].goods['Grain'] = -100
		city_dict[2].goods['Grain'] = 150

		# city_dict[0].goods['Wool'] = -100
		# city_dict[1].goods['Wool'] = 100

		team_dict = {
			0:	team.Team({
				"name":	"Team A",
			}),
			1:	team.Team({
				"name":	"Team B",
			}),
			2:	team.Team({
				"name":	"Team C",
			}),
			3:	team.Team({
				"name":	"Team D",
			}),
		}

		for k, v in team_dict.items():
			v.techs = {}

		#	Relations
		#------------------------
		w._relations = {
			0: {
				1: {'visitor': 1, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 0, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			1: {
				0: {'visitor': 0, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 1, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			2: {
				1: {'visitor': 1, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 8},
				0: {'visitor': 0, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 8},
				3: {'visitor': 3, 'host': 2, 'border': team.border_states.index('Open'), 'taxes': 12},
			},
			3: {
				1: {'visitor': 1, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
				2: {'visitor': 2, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
				0: {'visitor': 0, 'host': 3, 'border': team.border_states.index('Open'), 'taxes': 8},
			},
		}

		w._cities = city_dict

		w.mass_get_checker.add("mass_get_team_techs")
		w.mass_get_checker.add("mass_get_team_deities")
		w.mass_get_checker.add("mass_get_team_evolutions")

		# Build caches
		w.tax_cache = {}
		for t1 in team_dict.keys():
			for t2 in team_dict.keys():
				if t1 == t2:
					w.tax_cache[(t1, t2)] = 0
				else:
					w.tax_cache[(t1, t2)] = w.get_taxes(t1, t2)

		# Build a distance cache, K1 going to K2
		w.distance_cache = {}
		for k1, c1 in city_dict.items():
			for k2, c2 in city_dict.items():
				if k1 == k2:
					w.distance_cache[(k1, k2)] = 0
				else:
					if k2 in c1.connections:
						w.distance_cache[(k1, k2)] = (1 + (sad_rules.distance_percentage * c1.connections[k2]/100))

		# Now for some testing, lets make sure we're getting the right buys/sells from the first loop
		sad_f.find_buys(w, city_dict, verbose=False)
		sad_f.approve_buys(w, city_dict, verbose=False)

		self.assertEqual(
			[
				('Grain', [2, 1, 0], 100),
				('Grain', [2, 3], 50)
			],
			city_dict[2].sells,
		)

		# Now we need to actually execute the buys
		sad_f.execute_buys(w, city_dict, verbose=False)

		# Now make sure the goods/wealth are correct
		self.assertAlmostEqual(city_dict[0].wealth, 183.24, places=2)
		self.assertAlmostEqual(city_dict[1].wealth, 308.64, places=2)
		self.assertAlmostEqual(city_dict[2].wealth, 464.0, places=2)
		self.assertAlmostEqual(city_dict[3].wealth, 243.96, places=2)

		# City A has -15 grain because it couldn't afford the full 100, City C started with 110 so has +25 grain
		self.assertAlmostEqual(city_dict[0].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[1].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[2].goods['Grain'], 0, places=2)
		self.assertAlmostEqual(city_dict[3].goods['Grain'], -50, places=2)		
		


class Basic_functions (unittest.TestCase):
	test_targets = [
		sad_rules.trade_distance,
		sad_rules.reverse_trade_distance,
		sad_rules.tech_bonus,
		sad_rules.distance_from_equator
	]
	
	def test_trade_distances(self):
		self.assertAlmostEqual(12.59, sad_rules.trade_distance(10), places=2)
		self.assertAlmostEqual(42.15, sad_rules.trade_distance(30), places=2)
		self.assertAlmostEqual(57.85, sad_rules.trade_distance(40), places=2)
		self.assertAlmostEqual(141.15, sad_rules.trade_distance(90), places=2)
	
	def test_trade_distances_reverse(self):
		for i in range(0, 100):
			self.assertAlmostEqual(i, sad_rules.reverse_trade_distance(sad_rules.trade_distance(i)), places=5)
		
	def test_tech_bonus(self):
		vals = (
			#L	B	A
			(0, 100, 1),
			(10, 10, 2),
			(2, 5, 1.1),
		)
		
		for level, bonus, expected_answer in vals:
			actual_answer = sad_rules.tech_bonus(level, bonus)
			self.assertEqual(expected_answer, actual_answer)
	
	def test_distance_from_equator(self):
		vals = (
			#y, Ans
			(0,		2000),
			(500,	1500),
			(1000,	1000),
			(1500,	500),
			(2000,	0),
			(2500,	500),
			(3000,	1000),
			(3500,	1500),
			(4000,	2000),
		)
		
		for y, expected_answer in vals:
			actual_answer = sad_rules.distance_from_equator(y)
			self.assertEqual(expected_answer, actual_answer)
			

class Dict_entries(unittest.TestCase):
	test_targets = []
	
	# Tests that we are creating supply/demand values for each resource
	
	def test_supply(self):
		for r in sad_rules.res_list:
			self.assertIn(r, sad_rules.supply)
	
	def test_demand(self):
		for r in sad_rules.res_list:
			self.assertIn(r, sad_rules.demand)
	
	def test_terrain_factors(self):
		for r in sad_rules.res_list:
			self.assertIn(r, sad_rules._terrain_factor_s)
			self.assertIn(r, sad_rules._terrain_factor_d)
			
			try:
				self.assertEqual(len(sad_rules._terrain_factor_s[r]), len(map_data.terrain))
			except Exception as e:
				print("")
				print("r = %s" % r)
				print("")
				raise
			
			
			try:
				self.assertEqual(len(sad_rules._terrain_factor_d[r]), len(map_data.terrain))
			except Exception as e:
				print("")
				print("r = %s" % r)
				print("")
				raise

class Function_args(unittest.TestCase):
	test_targets = []
	
	dummy_city = city.City({"x":100, "y":100,"population":10000})
	dummy_city.supplies = []
	dummy_city.turn_history = {}
	
	def ttest_supply(self):
		for k, v in sad_rules.supply.items():
			v(city = self.dummy_city, techs = {})
		
	def ttest_demand(self):
		for k, v in sad_rules.demand.items():
			v(city = self.dummy_city, techs = {})

class Supply_results(unittest.TestCase):
	test_targets = [
		sad_rules.supply['Grain'],
	]
	
	normal_city = city.City({"name":"normal_city", "x":100, "y":100,"population":10000})
	normal_city.supplies = []
	normal_city.turn_history = {}
	
	# Grain
	grain_set = (
		(normal_city, map_data.terrain.index("water"), {}, 0),
		(normal_city, map_data.terrain.index("lowlands"), {}, 6.84),
	)
	def ttest_grain(self):
		for the_city, terrain, techs, expected_answer in self.grain_set:
			the_city.terrain = terrain
			actual_answer = sad_rules.supply['Grain'](city=the_city, techs=techs)
			
			try:
				self.assertAlmostEqual(actual_answer, expected_answer, places=2)
			except Exception as e:
				print("")
				print("City: %s" % the_city.name)
				print("")
				raise


class Demand_results(unittest.TestCase):
	test_targets = []
	pass