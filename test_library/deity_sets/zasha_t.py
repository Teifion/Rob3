import unittest
from pages import common
from classes import world
from classes import team, city, stat
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Zasha_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Zasha,
		# deity_rules.Zasha.major,
		# deity_rules.Zasha.minor,
		# deity_rules.Zasha.negative
		deity_rules.Zasha.other,
	]
	
	def test_major(self):
		return
		
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		deity_instance = deity_rules.Zasha(w)
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
		
		deity_instance = deity_rules.Zasha(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
	def test_minor(self):
		return
		
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		deity_instance = deity_rules.Zasha(w)
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
		
		deity_instance = deity_rules.Zasha(w)
		deity_instance.minor(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
	
	def test_negative(self):
		return
		
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		
		deity_instance = deity_rules.Zasha(w)
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
		
		deity_instance = deity_rules.Zasha(w)
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
	
	

