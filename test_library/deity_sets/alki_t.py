import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Alki_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Alki,
		# deity_rules.Alki.major,
		# deity_rules.Alki.minor,
		# deity_rules.Alki.negative,
		deity_rules.Alki.other,
	]
	
	# Destroy at least one non-Alki temple this turn
	def test_major(self):
		return
		
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		w._cities = {
			0: city.City({"id":0,"name":"City 1","population":75000,"team":0}),
			1: city.City({"id":1,"name":"City 2","population":75000,"team":0}),
			2: city.City({"id":2,"name":"City 3","population":40000,"team":0}),
			
			3: city.City({"id":0,"name":"City 1","population":75000,"team":1}),
			4: city.City({"id":1,"name":"City 2","population":75000,"team":1}),
			5: city.City({"id":2,"name":"City 3","population":40000,"team":1}),
		}
		
		w.mass_get_checker.add("mass_get_city_buildings")
		w.mass_get_checker.add("mass_get_team_deities")
		
		w.teams()[0].deities = {w.deities_lookup()['Alki']}
		w.teams()[1].deities = {w.deities_lookup()['Trchkithin']}
		
		# Put some temples in
		w._cities[0].buildings = {}
		w._cities[0].buildings_amount = {w.buildings_lookup()['Temple']:1,w.buildings_lookup()['Expanded university']:1}
		
		deity_instance = deity_rules.Alki(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		return
		
		# Basic failure
		w = dummy_world()
		t = w.teams()[0]
		
		deity_instance = deity_rules.Alki(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	# Kill at least one non-Alki chosen this turn
	def test_minor(self):
		return
		
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		deity_instance = deity_rules.Alki(w)
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
		
		deity_instance = deity_rules.Alki(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	# End the turn with less temples than you started it with
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
		# w._cities = {
		# 	0: city.City({"id":0,"name":"City 1","population":40000}),
		# 	1: city.City({"id":1,"name":"City 2","population":40000}),
		# }
		# 
		# w._cities[0].buildings = {}
		# w._cities[0].buildings_amount = {w.buildings_lookup()['Expanded temple']:1}
		# 
		# w._cities[1].buildings = {}
		# w._cities[1].buildings_amount = {w.buildings_lookup()['Temple']:1}
		# 
		# deity_instance = deity_rules.Alki(w)
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
		# deity_instance = deity_rules.Alki(w)
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
