import unittest
from pages import common
from classes import world
from classes import team, city, stat, squad
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Laegus_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Laegus,
		deity_rules.Laegus.major,
		deity_rules.Laegus.minor,
		# deity_rules.Laegus.negative,
		deity_rules.Laegus.other,
	]
	
	#	Major: Ended the turn with fewer than 100 materials
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		t.stats[common.current_turn()] = stat.Stat({"resources":"Materials:99"})
		
		deity_instance = deity_rules.Laegus(w)
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
		
		t.stats[common.current_turn()] = stat.Stat({"resources":"Materials:200"})
		
		deity_instance = deity_rules.Laegus(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	#	Minor: Army is at least 15% the size of your population (identical to Agashn)
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
		
		deity_instance = deity_rules.Laegus(w)
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
		
		deity_instance = deity_rules.Laegus(w)
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
		# 		w = dummy_world()
		# 		t = w.teams()[0]
		# 		
		# 		deity_instance = deity_rules.Laegus(w)
		# 		deity_instance.negative(t)
		# 		try:
		# 			self.assertEqual(deity_rules.favour_rewards['negative_pos'], deity_instance.favour)
		# 		except Exception as e:
		# 			print("\n")
		# 			print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 			print("")
		# 			raise
		# 		
		# 		# Basic failure
		# 		w = dummy_world()
		# 		t = w.teams()[0]
		# 		
		# 		deity_instance = deity_rules.Laegus(w)
		# 		deity_instance.negative(t)
		# 		try:
		# 			self.assertEqual(deity_rules.favour_rewards['negative_neg'], deity_instance.favour)
		# 		except Exception as e:
		# 			print("\n")
		# 			print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 			print("")
		# 			raise
	
	def test_other(self):
		w = dummy_world()
		t = w.teams()[0]
		deity_instance = deity_rules.Adyl(w)
		deity_instance.other(t)

