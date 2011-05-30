import database
import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Arl_favour_tester(unittest.TestCase):
	test_targets = [
		# These are covered by extension of the other tests
		# deity_rules.calculate_favour,
		deity_rules.Deity,
		deity_rules.Deity.major,
		deity_rules.Deity.minor,
		deity_rules.Deity.negative,
		deity_rules.Deity.other,
		
		deity_rules.Arl,
		deity_rules.Arl.major,
		deity_rules.Arl.minor,
		deity_rules.Arl.negative,
		deity_rules.Arl.other,
	]
	
	# Takes some time to run, leave it off for now
	def test_calculate_favour(self):
		return
		
		self.test_targets.append(deity_rules.calculate_favour)
		
		# Basically to make sure it runs under live data
		w = world.World(database.get_cursor())
		for t, the_team in w.teams().items():
			the_team.get_deities(w.cursor)
			for deity_id, the_deity in w.deities().items():
				deity_rules.calculate_favour(w, the_team, the_deity.name)
				deity_rules.calculate_favour(w, the_team, deity_id)
	
	#	Major: End the turn with at least 1 more city than you started it with
	def test_major(self):
		# Test for basic success
		w = dummy_world()
		t = w.teams()[0]
		t.stats[common.current_turn()] = stat.Stat({"city_count":10})
		t.stats[common.current_turn()-1] = stat.Stat({"city_count":5})
		
		deity_instance = deity_rules.Arl(w)
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
		t.stats[common.current_turn()] = stat.Stat({"city_count":3})
		t.stats[common.current_turn()-1] = stat.Stat({"city_count":8})
		
		deity_instance = deity_rules.Arl(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	
	#	Minor: All of your cities are within 100 units of another nation's city
	def test_minor(self):
		# Test for basic success
		w = dummy_world()
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
		
		deity_instance = deity_rules.Arl(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Test for basic failure
		w = dummy_world()
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
				"x":	250,
				"y":	250,
			}),
		}
		
		deity_instance = deity_rules.Arl(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	
	#	Negative: At least as many civilians as last turn
	def test_negative(self):
		# Test for basic success
		w = dummy_world()
		t = w.teams()[0]
		t.stats[common.current_turn()] = stat.Stat({"population":10})
		t.stats[common.current_turn()-1] = stat.Stat({"population":5})
		
		deity_instance = deity_rules.Arl(w)
		deity_instance.negative(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['negative_pos'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
		# Test for basic failure
		w = dummy_world()
		t = w.teams()[0]
		t.stats[common.current_turn()] = stat.Stat({"population":6})
		t.stats[common.current_turn()-1] = stat.Stat({"population":19})
		
		deity_instance = deity_rules.Arl(w)
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

