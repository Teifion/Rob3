import unittest
from pages import common
from classes import world
from classes import team, city, stat, squad, unit
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Azmodius_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Azmodius,
		deity_rules.Azmodius.major,
		deity_rules.Azmodius.minor,
		deity_rules.Azmodius.negative,
		deity_rules.Azmodius.other,
	]
	
	#	Major: You have no mages
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._squads = {
			0:	squad.Squad({
				"name":		"Mages",
				"unit":		1,
				"amount":	0,
			}),
			1:	squad.Squad({
				"name": 	"Not mages",
				"unit":		30,
				"amount":	1000,
			}),
			2:	squad.Squad({
				"name": 	"More mages",
				"unit":		31,
				"amount":	0,
			})
		}
		w._units = {
			30:	unit.Unit({}),
			31:	unit.Unit({}),
		}
		
		w._units[30].equipment = [1]
		w._units[31].equipment = [1, w.equipment_lookup()['High tier magic']]
		
		deity_instance = deity_rules.Azmodius(w)
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
		
		w._squads = {
			0:	squad.Squad({
				"name":		"Mages",
				"unit":		1,
				"amount":	0,
			}),
			1:	squad.Squad({
				"name": 	"Not mages",
				"unit":		30,
				"amount":	1000,
			}),
			2:	squad.Squad({
				"name": 	"More mages",
				"unit":		31,
				"amount":	1000,
			})
		}
		w._units = {
			30:	unit.Unit({}),
			31:	unit.Unit({}),
		}
		
		w._units[30].equipment = [1]
		w._units[31].equipment = [1, w.equipment_lookup()['High tier magic']]
		
		deity_instance = deity_rules.Azmodius(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: Your army is at least 20% the size of your population (yes it's the same as Agashn)
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		t.population = 5000
		w._squads = {
			0:	squad.Squad({
				"amount":	1000,
				"team":		0,
			}),
			1:	squad.Squad({
				"amount":	2000,
				"team":		0,
			}),
		}
		
		deity_instance = deity_rules.Azmodius(w)
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
		
		t.population = 40000
		w._squads = {
			0:	squad.Squad({
				"amount":	1000,
				"team":		0,
			}),
			1:	squad.Squad({
				"amount":	2000,
				"team":		0,
			}),
		}
		
		deity_instance = deity_rules.Azmodius(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: A city within 150 units of one of yours has an expanded or specialised academy
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"team":0,"name":"City 1","population":75000,"x":1000,"y":1000}),
			1: city.City({"id":1,"team":1,"name":"City 2","population":75000,"x":1000,"y":1100}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['University']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['Castle']:1}
		
		deity_instance = deity_rules.Azmodius(w)
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
			0: city.City({"id":0,"team":0,"name":"City 1","population":75000,"x":1000,"y":1000}),
			1: city.City({"id":1,"team":1,"name":"City 2","population":75000,"x":1000,"y":1100}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['University']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['Expanded academy']:1}
		
		deity_instance = deity_rules.Azmodius(w)
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

