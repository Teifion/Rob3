import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Ldura_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Ldura,
		deity_rules.Ldura.major,
		deity_rules.Ldura.minor,
		# deity_rules.Ldura.negative,
		deity_rules.Ldura.other,
	]
	
	#	Major: All cities larger than 50k have an expanded university and expanded academy
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"name":"City 1","population":75000}),
			1: city.City({"id":1,"name":"City 2","population":75000}),
			2: city.City({"id":2,"name":"City 3","population":40000}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['Expanded academy']:1,w.buildings_lookup()['Expanded university']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['Expanded university']:1,w.buildings_lookup()['Expanded academy']:1}
		
		deity_instance = deity_rules.Ldura(w)
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
			0: city.City({"id":0,"name":"City 1","population":75000}),
			1: city.City({"id":1,"name":"City 2","population":75000}),
			2: city.City({"id":2,"name":"City 3","population":75000}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['Expanded academy']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['Expanded university']:1}
		
		w._cities[2].buildings = {}
		w._cities[2].buildings_amount = {}
		
		deity_instance = deity_rules.Ldura(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: Every city has a university and an academy before anything else except walls
	def test_minor(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"team":0,"name":"City 1","population":75000}),
			1: city.City({"id":1,"team":0,"name":"City 2","population":75000}),
			2: city.City({"id":2,"team":0,"name":"City 3","population":75000}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['Academy']:1,w.buildings_lookup()['Castle']:1,w.buildings_lookup()['University']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['University']:1}
		
		w._cities[2].buildings = {}
		w._cities[2].buildings_amount = {}
		
		deity_instance = deity_rules.Ldura(w)
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
			0: city.City({"id":0,"team":0,"name":"City 1","population":75000}),
			1: city.City({"id":1,"team":0,"name":"City 2","population":75000}),
			2: city.City({"id":2,"team":0,"name":"City 3","population":75000}),
		}
		
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['Academy']:1,w.buildings_lookup()['Castle']:1,w.buildings_lookup()['University']:1}
		
		w._cities[1].buildings = {}
		w._cities[1].buildings_amount = {w.buildings_lookup()['University']:1}
		
		w._cities[2].buildings = {}
		w._cities[2].buildings_amount = {w.buildings_lookup()['Castle']:1}
		
		deity_instance = deity_rules.Ldura(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: Participated in more than 1 war
	def test_negative(self):
		"""
		Currently no way to actually test this as it uses campaign_f.team_campaign_count which
		runs a query right away, it doesn't go through the world
		"""
		pass
		
		# # Basic success
		# w = dummy_world()
		# t = w.teams()[0]
		# 
		# deity_instance = deity_rules.Ldura(w)
		# deity_instance.negative(t)
		# try:
		# 	self.assertEqual(deity_rules.favour_rewards['negative_pos'], deity_instance.favour)
		# except Exception as e:
		# 	print("\n")
		# 	print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 	print("")
		# 	raise
		# 
		# # Basic failure
		# w = dummy_world()
		# t = w.teams()[0]
		# 
		# deity_instance = deity_rules.Ldura(w)
		# deity_instance.negative(t)
		# try:
		# 	self.assertEqual(deity_rules.favour_rewards['negative_neg'], deity_instance.favour)
		# except Exception as e:
		# 	print("\n")
		# 	print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 	print("")
		# 	raise
	
	def test_other(self):
		w = dummy_world()
		t = w.teams()[0]
		deity_instance = deity_rules.Adyl(w)
		deity_instance.other(t)
