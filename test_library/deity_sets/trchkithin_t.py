import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Trchkithin_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Trchkithin,
		deity_rules.Trchkithin.major,
		deity_rules.Trchkithin.minor,
		deity_rules.Trchkithin.negative,
		deity_rules.Trchkithin.other,
	]
	
	#	Major: Trchkithin nations control at least 40% of the chosen land
	def test_major(self):
		# Test for basic success
		w = dummy_world()
		t = w.teams()[0]
		w.teams()[0].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[0].stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		w.teams()[12].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[12].stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		w.teams()[1].deities = {w.deities_lookup()['Arl']}
		w.teams()[1].stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
		}
		
		deity_instance = deity_rules.Trchkithin(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Test for basic failure
		w = dummy_world()
		t = w.teams()[0]
		w.teams()[0].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[0].stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		w.teams()[12].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[12].stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		w.teams()[1].deities = {w.deities_lookup()['Arl']}
		w.teams()[1].stats[common.current_turn()] = stat.Stat({"land_controlled":1000})
		
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
		}
		
		deity_instance = deity_rules.Trchkithin(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	
	#	Minor: Your slave count is at least 20% the size of your population
	def test_minor(self):
		# Simple success
		w = dummy_world()
		t = w.teams()[0]
		t.slaves = 1000
		t.population = 3000
		
		deity_instance = deity_rules.Trchkithin(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Simple failure
		w = dummy_world()
		t = w.teams()[0]
		t.slaves = 100
		t.population = 3000
		
		deity_instance = deity_rules.Trchkithin(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	
	#	Negative: A city within 200 map units follows Arl
	def test_negative(self):
		# Basic success
		w = dummy_world()
		w.teams()[0].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[1].deities = {w.deities_lookup()['Arl']}
		
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":	"First city",
				"team":	w.teams_lookup()["Our team"],
				"x":	100,
				"y":	100,
			}),
			
			1:	city.City({
				"name":	"Second city",
				"team":	w.teams_lookup()["Their team"],
				"x":	300,
				"y":	300,
			}),
		}
		
		deity_instance = deity_rules.Trchkithin(w)
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
		w.teams()[0].deities = {w.deities_lookup()['Trchkithin']}
		w.teams()[1].deities = {w.deities_lookup()['Arl']}
		
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":	"First city",
				"team":	w.teams_lookup()["Our team"],
				"x":	100,
				"y":	100,
			}),
			
			1:	city.City({
				"name":	"Second city",
				"team":	w.teams_lookup()["Their team"],
				"x":	140,
				"y":	140,
			}),
		}
		
		deity_instance = deity_rules.Trchkithin(w)
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
	