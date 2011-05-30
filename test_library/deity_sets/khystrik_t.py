import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Khystrik_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Khystrik,
		deity_rules.Khystrik.major,
		deity_rules.Khystrik.minor,
		deity_rules.Khystrik.negative,
		deity_rules.Khystrik.other,
	]
	
	#	Major: All cities are nomadic
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"name":"City 1", "nomadic":True}),
			1: city.City({"name":"City 2", "nomadic":True}),
			2: city.City({"name":"City 3", "nomadic":True}),
			3: city.City({"name":"City 4", "nomadic":True}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
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
			0: city.City({"name":"City 1", "nomadic":True}),
			1: city.City({"name":"City 2", "nomadic":True}),
			2: city.City({"name":"City 3", "nomadic":True}),
			3: city.City({"name":"City 4", "nomadic":False}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: None of your cities are within 40 map units of each other
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"name":"City 1", "x":100, "y":100}),
			1: city.City({"name":"City 2", "x":100, "y":150}),
			2: city.City({"name":"City 3", "x":100, "y":200}),
			3: city.City({"name":"City 4", "x":100, "y":250}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
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
			0: city.City({"name":"City 1", "x":100, "y":100}),
			1: city.City({"name":"City 2", "x":100, "y":110}),
			2: city.City({"name":"City 3", "x":100, "y":200}),
			3: city.City({"name":"City 4", "x":100, "y":250}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: None of your cities are nomadic
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"name":"City 1", "nomadic":True}),
			1: city.City({"name":"City 2", "nomadic":True}),
			2: city.City({"name":"City 3", "nomadic":True}),
			3: city.City({"name":"City 4", "nomadic":False}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
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
			0: city.City({"name":"City 1", "nomadic":False}),
			1: city.City({"name":"City 2", "nomadic":False}),
			2: city.City({"name":"City 3", "nomadic":False}),
			3: city.City({"name":"City 4", "nomadic":False}),
		}
		
		deity_instance = deity_rules.Khystrik(w)
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

