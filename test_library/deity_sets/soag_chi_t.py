import unittest
from pages import common
from classes import world
from classes import team, city, stat, operative
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Soag_chi_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Soag_chi,
		deity_rules.Soag_chi.major,
		deity_rules.Soag_chi.minor,
		deity_rules.Soag_chi.negative,
		deity_rules.Soag_chi.other,
	]
	
	#	Major: An operative within every non Soag chi city within 100 units of each of yours where your city and their city is at least 3 years old
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		1,
				"founded":	common.current_turn()-1,
				"x":		990,
				"y":		990,
			}),
		}
		
		w._operatives = {
			0:	operative.Operative({
				"id":	0,
				"team":	0,
				"city":	1,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
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
		t = w.teams()[0]
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		1,
				"founded":	common.current_turn()-1,
				"x":		990,
				"y":		990,
			}),
		}
		
		w._operatives = {
			0:	operative.Operative({
				"id":	0,
				"team":	0,
				"city":	2,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: One or more of your cities are within 50 map units of a non-Soag chi follower
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		2,
				"founded":	common.current_turn()-1,
				"x":		900,
				"y":		900,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
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
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		2,
				"founded":	common.current_turn()-1,
				"x":		900,
				"y":		900,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		w._teams[1].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: None of your cities are within 50 map units of a non-Soag chi follower
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		2,
				"founded":	common.current_turn()-1,
				"x":		900,
				"y":		900,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
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
		t = w.teams()[0]
		
		w._cities = {
			0:	city.City({
				"id":		0,
				"name":		"City 1",
				"team":		0,
				"founded":	0,
				"x":		1000,
				"y":		1000,
			}),
			1:	city.City({
				"id":		1,
				"name":		"City 2",
				"team":		1,
				"founded":	common.current_turn()-5,
				"x":		1010,
				"y":		1010,
			}),
			2:	city.City({
				"id":		2,
				"name":		"City 3",
				"team":		2,
				"founded":	common.current_turn()-1,
				"x":		900,
				"y":		900,
			}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Soag chi']]
		w._teams[1].deities = [w.deities_lookup()['Soag chi']]
		
		deity_instance = deity_rules.Soag_chi(w)
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
