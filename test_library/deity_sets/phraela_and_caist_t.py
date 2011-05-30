import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Phraela_and_Caist_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Phraela_and_Caist,
		deity_rules.Phraela_and_Caist.major,
		deity_rules.Phraela_and_Caist.minor,
		deity_rules.Phraela_and_Caist.negative,
		deity_rules.Phraela_and_Caist.other,
	]
	
	#	Major: All cities are within 100 map units of at least two of your other cities
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":0,"name":"City 2","x":1050,"y":1000}),
			2: city.City({"id":2,"team":0,"name":"City 3","x":1000,"y":1050}),
		}
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
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
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":0,"name":"City 2","x":1050,"y":1000}),
			2: city.City({"id":2,"team":0,"name":"City 3","x":1000,"y":2050}),
		}
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: You have a city within 150 map units of another Phraela and Caist follower or 3 of your own	
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":1,"name":"City 2","x":1050,"y":1000}),
		}
		
		w._teams[1].deities = [w.deities_lookup()['Phraela and Caist']]
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
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
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":1,"name":"City 2","x":1050,"y":1000}),
		}
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: Any of your cities are closer to a non-Phraela and Caist follower than they are to a Phraela and Caist follower or one of your own cities
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":0,"name":"City 2","x":1400,"y":1000}),
			2: city.City({"id":2,"team":1,"name":"City 3","x":2000,"y":1000}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Phraela and Caist']]
		w._teams[1].deities = [w.deities_lookup()['Phraela and Caist']]
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
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
			0: city.City({"id":0,"team":0,"name":"City 1","x":1000,"y":1000}),
			1: city.City({"id":1,"team":0,"name":"City 2","x":1600,"y":1000}),
			2: city.City({"id":2,"team":1,"name":"City 3","x":2000,"y":1000}),
		}
		
		w._teams[0].deities = [w.deities_lookup()['Phraela and Caist']]
		
		deity_instance = deity_rules.Phraela_and_Caist(w)
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
