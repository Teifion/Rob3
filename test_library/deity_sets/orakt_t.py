import unittest
from pages import common
from classes import world
from classes import team, city, stat, unit, squad, army, res_dict
from rules import deity_rules
from test_library.deity_sets import deity_t_lib

dummy_world = deity_t_lib.dummy_world

class Orakt_favour_tester(unittest.TestCase):
	test_targets = [
		deity_rules.Orakt,
		deity_rules.Orakt.major,
		# deity_rules.Orakt.minor,
		# deity_rules.Orakt.negative,
		deity_rules.Orakt.other,
	]
	
	#	Major: Upkeep is at least 25% of your income
	def test_major(self):
		# Basic success
		w = dummy_world()
		t = w.teams()[0]
		t.resources = res_dict.Res_dict("Iron:1")
		w._units = {
			0:	unit.Unit({
				"name":	"First unit",
			}),
		}
		w._units[0].costs = {
			"material_cost":	res_dict.Res_dict("Materials:10"),
			"iron_cost":		res_dict.Res_dict("Materials:10"),
			"material_upkeep":	res_dict.Res_dict("Materials:10"),
			"iron_upkeep":		res_dict.Res_dict("Materials:10"),
		}
		# t.evolutions = {}
		w._armies = {
			0:	army.Army({
				"name":	"First army",
			})
		}
		w._squads = {
			0:	squad.Squad({
				"name":	"First squad",
				"unit":	0,
				"army":	0,
				"amount":	4000,
			})
		}
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
		}
		for k, v in w._cities.items():
			v.id = k
			v.artefacts = []
			v.buildings, v.buildings_amount = {}, {}
		
		w.mass_get_checker.add("mass_get_city_buildings")
		deity_instance = deity_rules.Orakt(w)
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
		t.resources = res_dict.Res_dict("Iron:1")
		w._units = {
			0:	unit.Unit({
				"name":	"First unit",
			}),
		}
		w._units[0].costs = {
			"material_cost":	res_dict.Res_dict("Materials:10"),
			"iron_cost":		res_dict.Res_dict("Materials:10"),
			"material_upkeep":	res_dict.Res_dict("Materials:10"),
			"iron_upkeep":		res_dict.Res_dict("Materials:10"),
		}
		w._armies = {
			0:	army.Army({
				"name":	"First army",
			})
		}
		w._squads = {
			0:	squad.Squad({
				"name":	"First squad",
				"unit":	0,
				"army":	0,
				"amount":	1000,
			})
		}
		w._cities =  {
			0:	city.City({
				"name":			"First city",
				"team":			w.teams_lookup()["Our team"],
				"x":			100,
				"y":			100,
				"population":	50000,
			}),
		}
		for k, v in w._cities.items():
			v.id = k
			v.artefacts = []
			v.buildings, v.buildings_amount = {}, {}
		
		w.mass_get_checker.add("mass_get_city_buildings")
		deity_instance = deity_rules.Orakt(w)
		deity_instance.major(t)
		try:
			self.assertEqual(deity_rules.favour_rewards['major_neg'], deity_instance.favour)
		except Exception as e:
			print("\n")
			print(common.html_to_terminal("\n".join(deity_instance.info)))
			print("")
			raise
		
	#	Minor: Participated in at least 3 wars this turn
	def test_minor(self):
		"""
		Currently no way to actually test this as it uses campaign_f.team_campaign_count which
		runs a query right away, it doesn't go through the world
		"""
		pass
		# Basic success
		# w = dummy_world()
		# t = w.teams()[0]
		# 
		# deity_instance = deity_rules.Orakt(w)
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
		# deity_instance = deity_rules.Orakt(w)
		# deity_instance.minor(t)
		# try:
		# 	self.assertEqual(deity_rules.favour_rewards['minor_neg'], deity_instance.favour)
		# except Exception as e:
		# 	print("\n")
		# 	print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 	print("")
		# 	raise
	
	#	Negative: Participated in 0 wars
	def ttest_negative(self):
		"""
		Currently no way to actually test this as it uses campaign_f.team_campaign_count which
		runs a query right away, it doesn't go through the world
		"""
		pass
		# # Basic success
		# 	w = dummy_world()
		# 	t = w.teams()[0]
		# 	
		# 	deity_instance = deity_rules.Orakt(w)
		# 	deity_instance.negative(t)
		# 	try:
		# 		self.assertEqual(deity_rules.favour_rewards['negative_pos'], deity_instance.favour)
		# 	except Exception as e:
		# 		print("\n")
		# 		print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 		print("")
		# 		raise
		# 	
		# 	# Basic failure
		# 	w = dummy_world()
		# 	t = w.teams()[0]
		# 	
		# 	deity_instance = deity_rules.Orakt(w)
		# 	deity_instance.negative(t)
		# 	try:
		# 		self.assertEqual(deity_rules.favour_rewards['negative_neg'], deity_instance.favour)
		# 	except Exception as e:
		# 		print("\n")
		# 		print(common.html_to_terminal("\n".join(deity_instance.info)))
		# 		print("")
		# 		raise
	
	def test_other(self):
		w = dummy_world()
		t = w.teams()[0]
		deity_instance = deity_rules.Adyl(w)
		deity_instance.other(t)
