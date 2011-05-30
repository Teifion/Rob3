import unittest
from pages import common
from classes import world
from classes import team, city, stat, operative, squad
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Ssai_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Ssai,
		deity_rules.Ssai.major,
		deity_rules.Ssai.minor,
		deity_rules.Ssai.negative,
		deity_rules.Ssai.other,
	]
	
	#	Major: Must have an operative within every nation that has a city within 1000 units of one of yours
	def test_major(self):
		# Basic success
		w = dummy_world()
		w._teams = {0:w._teams[0],1:w._teams[1]}# Slim it down because we use borders
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Their team"],
				"x":			120,
				"y":			120,
			}),
		}
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"city":			w.cities_lookup()["Second city"]
			}),
		}
		w._relations = {
			0:
			{
				1:{"border":team.border_states.index("Closed")},
			},
		}
		
		deity_instance = deity_rules.Ssai(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Basic failure
		w = dummy_world()
		w._teams = {0:w._teams[0],1:w._teams[1]}# Slim it down because we use borders
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Their team"],
				"x":			120,
				"y":			120,
			}),
		}
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"city":			w.cities_lookup()["First city"]
			}),
		}
		w._relations = {
			0:
			{
				1:{"border":team.border_states.index("Closed")},
			},
		}
		
		deity_instance = deity_rules.Ssai(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: At least 1 operative per 1000 troops
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"size":			10,
			}),
		}
		w._squads =  {
			0:	squad.Squad({
				"name":			"Our squad",
				"team":			w.teams_lookup()["Our team"],
				"amount":		1000,
			}),
		}
		deity_instance = deity_rules.Ssai(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Basic failure
		w = dummy_world()
		t = w.teams()[0]
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"size":			1,
			}),
		}
		w._squads =  {
			0:	squad.Squad({
				"name":			"Our squad",
				"team":			w.teams_lookup()["Our team"],
				"amount":		2000,
			}),
		}
		deity_instance = deity_rules.Ssai(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: A non-allied city within 100 units of one of yours is over 2 years old and is not infiltrated
	def test_negative(self):
		# Basic success
		w = dummy_world()
		w._teams = {0:w._teams[0],1:w._teams[1]}# Slim it down because we use borders
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Their team"],
				"x":			120,
				"y":			120,
				"founded":		common.current_turn(),
			}),
		}
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"city":			w.cities_lookup()["First city"]
			}),
		}
		w._relations = {
			0:
			{
				1:{"border":team.border_states.index("Closed")},
			},
		}
		
		deity_instance = deity_rules.Ssai(w)
		deity_instance.negative(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['negative_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Basic failure
		w = dummy_world()
		w._teams = {0:w._teams[0],1:w._teams[1]}# Slim it down because we use borders
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Their team"],
				"x":			120,
				"y":			120,
				"founded":		common.current_turn()-10,
			}),
		}
		w._operatives =  {
			0:	operative.Operative({
				"name":			"Our cell",
				"team":			w.teams_lookup()["Our team"],
				"city":			w.cities_lookup()["First city"]
			}),
		}
		w._relations = {
			0:
			{
				1:{"border":team.border_states.index("Closed")},
			},
		}
		
		deity_instance = deity_rules.Ssai(w)
		deity_instance.negative(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['negative_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
			
	def test_other(self):
		w = dummy_world()
		t = w.teams()[0]
		deity_instance = deity_rules.Adyl(w)
		deity_instance.other(t)
