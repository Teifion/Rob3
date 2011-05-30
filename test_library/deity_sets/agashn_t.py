import unittest
from pages import common
from classes import world
from classes import team, city, stat, squad
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Agashn_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Agashn,
		deity_rules.Agashn.major,
		deity_rules.Agashn.minor,
		deity_rules.Agashn.negative,
		deity_rules.Agashn.other,
	]
	
	#	Major: Above average land control
	def test_major(self):
		# Basic success
		w = dummy_world()
		for i, t in w.teams().items(): t.stats[common.current_turn()] = stat.Stat({"land_controlled":50})
		t = w.teams()[0]
		t.stats[common.current_turn()] = stat.Stat({"land_controlled":100})
		
		deity_instance = deity_rules.Agashn(w)
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
		for i, t in w.teams().items(): t.stats[common.current_turn()] = stat.Stat({"land_controlled":50})
		t = w.teams()[0]
		t.stats[common.current_turn()] = stat.Stat({"land_controlled":30})
		
		deity_instance = deity_rules.Agashn(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: Army is at least 15% the size of your population	
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
		
		deity_instance = deity_rules.Agashn(w)
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
		
		deity_instance = deity_rules.Agashn(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Negative: End the turn with fewer cities than you started with
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		t.stats[common.current_turn()] = stat.Stat({"city_count":10})
		t.stats[common.current_turn()-1] = stat.Stat({"city_count":5})
		
		deity_instance = deity_rules.Agashn(w)
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
		
		t.stats[common.current_turn()] = stat.Stat({"city_count":3})
		t.stats[common.current_turn()-1] = stat.Stat({"city_count":5})
		
		deity_instance = deity_rules.Agashn(w)
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
	

