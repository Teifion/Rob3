import unittest
from pages import common
from classes import world
from classes import team, city, stat, unit
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Adyl_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Adyl,
		deity_rules.Adyl.major,
		# deity_rules.Adyl.minor,
		deity_rules.Adyl.negative,
		deity_rules.Adyl.other,
	]
	
	#	Major: All cities of 30k or more must are walled
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	10000,
			}),
		}
		w._cities[0].walls = [0]
		w._cities[1].walls = []
		
		deity_instance = deity_rules.Adyl(w)
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
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	10000,
			}),
		}
		w._cities[0].walls = []
		w._cities[1].walls = [0]
		
		deity_instance = deity_rules.Adyl(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: Participated in a war
	def test_minor(self):
		"""
		Currently no way to actually test this as it uses campaign_f.team_campaign_count which
		runs a query right away, it doesn't go through the world
		"""
		pass
		# # Basic success
		# w = dummy_world()
		# t = w.teams()[0]
		# 
		# deity_instance = deity_rules.Adyl(w)
		# deity_instance.minor(t)
		# try:
		# 	self.assertEqual(deity_rules.favour_rewards['minor_pos'], deity_instance.favour)
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
		# deity_instance = deity_rules.Adyl(w)
		# deity_instance.minor(t)
		# try:
		# 	self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		# except Exception as e:
		# 	print("\n")
		# 	print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 	print("")
		# 	raise
	
	#	Negative: Posses any troops with training below normal
	def test_negative(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	10000,
			}),
		}
		w._cities[0].walls = [0]
		w._cities[1].walls = []
		
		deity_instance = deity_rules.Adyl(w)
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
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
			1:	city.City({
				"name":			"Second city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	10000,
			}),
		}
		w._cities[0].walls = []
		w._cities[1].walls = [0]
		
		deity_instance = deity_rules.Adyl(w)
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
	
