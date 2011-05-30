from pages import common
import unittest
from functions import team_f
from test_library import orders_t_lib
from classes import res_dict, world

class Add_deity(unittest.TestCase):
	test_targets = [team_f.add_deity]
	
	known_values = (
		(1, 1, "INSERT INTO team_deities (team, deity) values (1, 1);"),
		(3, 16, "INSERT INTO team_deities (team, deity) values (3, 16);"),
	)
	
	def test_known(self):
		for team_id, deity_id, answer in self.known_values:
			result = team_f.add_deity(team_id, deity_id)
			self.assertEqual(result, answer)
	
	fail_values = (
		([1], 1, TypeError),
		(1, [1], TypeError),
	)
	
	def test_fail(self):
		for team_id, deity_id, answer in self.fail_values:
			self.assertRaises(answer, team_f.add_deity, team_id, deity_id)

class Remove_deity(unittest.TestCase):
	test_targets = [team_f.remove_deity]
	
	known_values = (
		(1, 1, "DELETE FROM team_deities WHERE team = 1 AND deity = 1;"),
		(50, 100, "DELETE FROM team_deities WHERE team = 50 AND deity = 100;"),
	)
	
	def test_known(self):
		for team_id, deity_id, answer in self.known_values:
			result = team_f.remove_deity(team_id, deity_id)       
			self.assertEqual(result, answer)
	
	fail_values = (
		([1], 1, TypeError),
		(1, [1], TypeError),
	)
	
	def test_fail(self):
		for team_id, deity_id, answer in self.fail_values:
			self.assertRaises(answer, team_f.remove_deity, team_id, deity_id)

class Get_hash (unittest.TestCase):
	test_targets = [team_f.team_hash]
	
	known_values = (
		("Greymin", 50, "30f4ac4a20dad5dc033129819ed9758c"),
		("Shefair", 50, "b7b936d34bf3880963e897176bdbb6c2"),
		("", 50, "021e517df83c9c39c1c9ea0e8ed088d9"),
		("Bobb", 50, "84dc624dbf8a54f540ad69cd16ff8578"),
	)
	
	def test_known(self):
		for name, turn, hashstr in self.known_values:
			self.assertEqual(team_f.team_hash(name, turn), hashstr)
			
class Start_script_tester (unittest.TestCase):
	test_targets = [
		team_f.produce_resources,
		team_f.grow_cities,
	]
	w = orders_t_lib.dummy_world()
	
	def test_produce_resources(self):
		vals = (
			(0, [
				'UPDATE team_resources SET amount = 34.8528137424 WHERE team = 0 AND resource = 0;',
				'UPDATE team_resources SET amount = 60.0 WHERE team = 0 AND resource = 1;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 2;',
				'UPDATE team_resources SET amount = 50 WHERE team = 0 AND resource = 3;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 4;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 5;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 6;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 7;',
				'UPDATE team_resources SET amount = 0.0 WHERE team = 0 AND resource = 8;',
				'UPDATE team_resources SET amount = 0.0 WHERE team = 0 AND resource = 9;',
				'UPDATE team_resources SET amount = 0.0 WHERE team = 0 AND resource = 10;',
				'UPDATE team_resources SET amount = 0.0 WHERE team = 0 AND resource = 11;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 12;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 13;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 14;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 15;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 16;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 17;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 18;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 19;',
				'UPDATE team_resources SET amount = 0 WHERE team = 0 AND resource = 20;',
			]),
		)
		
		self.w.mass_get_checker.add("mass_get_city_buildings")
		for team_id, expected in vals:
			self.assertEqual(team_f.produce_resources(self.w, self.w._teams[team_id]), expected)
	
	
	def test_grow_cities(self):
		vals = (
			(0, [
				'-- Growing city 0, old pop: 30000, old slave: 10000, new pop, 31200, rate: 1, constant: 0',
				'UPDATE cities SET population = 31200 WHERE id = 0;',
				'UPDATE cities SET dead = %d WHERE id = 1;' % common.current_turn()
			]),
		)
		
		for team_id, expected in vals:
			self.w._teams[team_id].resources = res_dict.Res_dict("Food:10000")
			self.assertEqual(team_f.grow_cities(self.w, self.w._teams[team_id]), expected)


@unittest.skip("Skip")
class Start_script_exception_tester (unittest.TestCase):
	def test_get_upkeep(self):
		import database
		
		w = world.World(database.get_cursor())
		for team_id, the_team in w.active_teams().items():
			team_f.get_upkeep(the_team, w)
			
		