import unittest
from functions import building_f
from classes import city
from data_classes import building
from queries import building_q
from rules import building_rules

class Building_function_tests(unittest.TestCase):
	test_targets = [building_f.check_row_exists, building_f.completion_query]
	
	check_row_exists_sets = [
		(1,		1,		"INSERT INTO city_buildings (city, building) values (1, 1);"),
		(100,	31,		"INSERT INTO city_buildings (city, building) values (100, 31);"),
		(999,	400,	"INSERT INTO city_buildings (city, building) values (999, 400);"),
		(-1,	-2,		"INSERT INTO city_buildings (city, building) values (-1, -2);"),
		(1,		100,	"INSERT INTO city_buildings (city, building) values (1, 100);"),
	]
	
	def test_check_row_exists(self):
		for city_id, building_id, expected in self.check_row_exists_sets:
			r = building_f.check_row_exists(city_id=city_id, building_id=building_id)
			self.assertEqual(expected, r)
	
	
	completion_query_sets = [
		# Standard progression
		(1,	(2, 100, 1),	50,	["UPDATE city_buildings SET completion = 50 WHERE city = 1 AND building = 2;",]),
		
		# Complete building, kill upgrade source
		(2,	(3, 100, 2),	100,	[
			"UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = 2 AND building = 3;",
			"DELETE FROM city_buildings WHERE city = 2 AND building = 2;",
		]),
		
		# Ensure we still kill it's source with a building id of 0
		(4,	(5, 100, 0),	100,	[
			"UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = 4 AND building = 5;",
			"DELETE FROM city_buildings WHERE city = 4 AND building = 0;",
		]),
		
		# Complete, but with no upgrade source
		(5,	(7, 100, -1),	100,	[
			"UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = 5 AND building = 7;",
		]),
	]
	def test_completion_query(self):
		for city_id, building_data, new_completion, expected in self.completion_query_sets:
			the_city = city.City(row={"id":city_id})
			the_building = building.Building(row={"id":building_data[0], "build_time":building_data[1], "upgrades":building_data[2]})
			
			r = building_f.completion_query(the_city=the_city, the_building=the_building, new_completion=new_completion)
			self.assertEqual(expected, r)
			
		
	
class Building_rules_tests(unittest.TestCase):
	test_targets = [building_rules.temple_points]
	
	def test_temple_points(self):
		vals = (
			# Temple
			(22,	0),
			(23,	1),
			(24,	0),
			("Temple",	1),
			
			# Expanded temple
			(49,	0),
			(50,	2),
			(51,	0),
			("Expanded temple",	2),
		)
		
		for the_building, expected in vals:
			r = building_rules.temple_points(the_building)
			self.assertEqual(expected, r)
		