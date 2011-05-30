import database
from classes import world, res_dict
from classes import team, city, squad, army, unit
from queries import equipment_q, building_q, deity_q, evolution_q, tech_q, spell_q, artefact_q, wonder_q

# Need some live data for things like buildings etc
temp_cursor = database.get_cursor()
equipment_dict = equipment_q.get_all_equipment(temp_cursor)
building_dict = building_q.get_all_buildings(temp_cursor)
deity_dict = deity_q.get_all_deities(temp_cursor)
evolution_dict = evolution_q.get_all_evolutions(temp_cursor)
spell_dict = spell_q.get_all_spells(temp_cursor)
tech_dict = tech_q.get_all_techs(temp_cursor)
artefact_dict = artefact_q.get_all_artefacts(temp_cursor)
wonder_dict = wonder_q.get_all_wonders(temp_cursor)

def dummy_world():
	w = world.World(Dead_cursor())
	
	#	LISTS
	#------------------------
	w._equipment = equipment_dict
	w._buildings = building_dict
	w._deities = deity_dict
	w._evolutions = evolution_dict
	w._spells = spell_dict
	w._techs = tech_dict
	w._artefacts = artefact_dict
	
	#	TEAMS
	#------------------------
	w._teams = {
		0:	team.Team({
			"name":			"SArkalians",
		}),
		1:	team.Team({
			"name":			"Numericals",
		}),
		2:	team.Team({
			"name":			"Úñíçódéß",
		}),
		
		# Actual teams
		71:	team.Team({
			"name":			"Sharyzen",
		}),
	}
	
	for i, t in w._teams.items():
		t.deities = {}
		t.evolutions = {}
		t.tech_levels = {}
		t.spell_levels = {}
		t.resources = res_dict.Res_dict("Materials:0")
		t.artefacts = []
	
	#	CITIES
	#------------------------
	w._cities =  {
		0:	city.City({
			"name":	"Durandalbad",
			"team":	w.teams_lookup()["SArkalians"],
			"population":	30000,
			"slaves":		10000,
		}),
		
		1:	city.City({
			"name":	"Khfear",
			"team":	w.teams_lookup()["SArkalians"],
		}),
		
		
		100:	city.City({
			"name":	"City0",
			"team":	w.teams_lookup()["Numericals"],
		}),
		
		101:	city.City({
			"name":	"City1",
			"team":	w.teams_lookup()["Numericals"],
		}),
		
		102:	city.City({
			"name":	"City2",
			"team":	w.teams_lookup()["Numericals"],
		}),
		
		103:	city.City({
			"name":	"City3",
			"team":	w.teams_lookup()["Numericals"],
		}),
		
		104:	city.City({
			"name":	"City4",
			"team":	w.teams_lookup()["Numericals"],
		}),
		
		
		200:	city.City({
			"name":	"Úñíçódé",
			"team":	w.teams_lookup()["Úñíçódéß"],
		}),
	}
	
	for i, c in w._cities.items():
		c.artefacts = []
		c.wonders = []
		c.buildings = {}
		c.buildings_amount = {}
	
	#	BUILDINGS
	#------------------------
	w._cities[w.cities_lookup()['City0']].buildings[w.buildings_lookup()['University']] = 0
	w._cities[w.cities_lookup()['City1']].buildings[w.buildings_lookup()['University']] = 50
	w._cities[w.cities_lookup()['City2']].buildings[w.buildings_lookup()['University']] = 100
	w._cities[w.cities_lookup()['City3']].buildings[w.buildings_lookup()['University']] = 150
	w._cities[w.cities_lookup()['City4']].buildings_amount[w.buildings_lookup()['University']] = 1
	
	
	#	Units
	#------------------------
	# Build lookup dict
	equipment_lookup = w.equipment_lookup(lower=True)
	
	w._units =  {
		0:	unit.Unit({
			"name":			"My first unit",
			"team":			w.teams_lookup()["SArkalians"],
			"availiable":	True,
		}),
	}
	
	w._units[0].equipment = [equipment_lookup[e.lower()] for e in ["Good training", "Mace", "Banded armour suit", "Leather suit", "Longbow"]]
	
	
	#	Armies
	#------------------------
	w._armies =  {
		0:	army.Army({
			"name":			"My first army",
			"team":			w.teams_lookup()["SArkalians"],
		}),
		1:	army.Army({
			"name":			"My second army",
			"team":			w.teams_lookup()["SArkalians"],
		}),
	}
	
	#	Squads
	#------------------------
	w._squads =  {
		0:	squad.Squad({
			"name":			"My first squad",
			"team":			w.teams_lookup()["SArkalians"],
			"army":			w.armies_lookup()["My first army"],
			"unit":			w.units_lookup()["My first unit"],
		}),
		
		1:	squad.Squad({
			"name":			"My second squad",
			"team":			w.teams_lookup()["SArkalians"],
			"army":			w.armies_lookup()["My second army"],
			"unit":			w.units_lookup()["My first unit"],
		}),
	}
	
	
	dicts = [w._cities, w._squads, w._armies, w._units, w._teams]
	
	for d in dicts:
		for k, v in d.items(): v.id = k
	
		
	
	
	#	PREP STUFF
	#------------------------
	# """Runs a set of prep functions for orders"""
	# # player_q.mass_get_player_powers(self.cursor, self._players)
	# mapper_q.get_terrain(self.cursor, 0, 0)
	# 
	# self.teams()
	# # team_q.mass_get_team_deities(self.cursor, self._teams)
	# team_q.mass_get_team_spells(self.cursor, self._teams)
	# team_q.mass_get_team_techs(self.cursor, self._teams)
	# team_q.mass_get_team_resources(self.cursor, self._teams)
	# team_q.mass_get_team_evolutions(self.cursor, self._teams)
	# 
	# self.buildings()
	# self.cities()
	# city_q.mass_get_city_buildings(self.cursor, self._cities)
	# # city_q.mass_get_city_artefacts(self.cursor, self._cities)
	# # city_q.mass_get_city_wonders(self.cursor, self._cities)
	# 
	# # squad_q.mass_get_squads(self.cursor, self._armies)
	# 
	# unit_q.mass_get_unit_equipment(self.cursor, self._units)
	# 
	for k, v in w._buildings.items():
		if v.upgrades > 0:
			if v.upgrades not in w._building_requirements:
				w._building_requirements[v.upgrades] = []
			
			w._building_requirements[v.upgrades].append(k)
	
	return w


class Dead_cursor (object):
	"""docstring for Dead_cursor"""
	def __init__(self):
		super(Dead_cursor, self).__init__()
		self.log = []
	
	# http://docs.python.org/py3k/library/traceback.html#module-traceback
	def execute(self, *args, **kwargs):
		self.log.append(("execute", args, kwargs))



def test_orders(tester, data):
	b = data['block']
	b.setup()
	b.execute()
	
	# Check stuff
	if "results" in data and data['results'] != []:
		compare_results(b, tester, data['results'], b.results)
	
	if "queries" in data and data['queries'] != []:
		compare_queries(b, tester, data['queries'], b.queries)
	

def compare_results(block, tester, correct_results, actual_results):
	# Delete the title line, if we want to compare the cost we can do so
	del(actual_results[0])
	
	# Test size
	try:
		tester.assertEqual(len(correct_results), len(actual_results))
	except Exception as e:
		print("")
		print("Length of correct results: %d" % len(correct_results))
		print("\n".join(["\t%s" % r for r in correct_results]))
		
		print("Length of actual results: %d" % len(actual_results))
		print("\n".join(["\t%s" % r for r in actual_results]))
		
		raise
	
	# Test content
	for i, cr in enumerate(correct_results):
		ar = actual_results[i]
		
		try:
			tester.assertEqual(cr, ar)
		except Exception as e:
			print("")
			
			if len(block.debug) > 1:
				print("Debug: %s" % "\n".join(block.debug))
			
			raise

def compare_queries(block, tester, correct_queries, actual_queries):
	# Delete the first line, it should be a comment
	# del(actual_queries[0])
	
	# Test size
	try:
		tester.assertEqual(len(correct_queries), len(actual_queries))
	except Exception as e:
		print("")
		print("Length of correct queries: %d" % len(correct_queries))
		print("Length of actual queries: %d" % len(actual_queries))
		
		raise
	
	# Test content
	for i, cq in enumerate(correct_queries):
		aq = actual_queries[i]
		
		try:
			tester.assertEqual(cq, aq)
		except Exception as e:
			print("")
			
			raise