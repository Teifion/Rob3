import math
import unittest
from pages import common
from classes import world
from classes import team, city, stat, res_dict
from rules import deity_rules
from test_library import orders_t_lib

# Need some live data for things like buildings etc
equipment_dict = orders_t_lib.equipment_dict
building_dict = orders_t_lib.building_dict
deity_dict = orders_t_lib.deity_dict
evolution_dict = orders_t_lib.evolution_dict
spell_dict = orders_t_lib.spell_dict
tech_dict = orders_t_lib.tech_dict
artefact_dict = orders_t_lib.artefact_dict
wonder_dict = orders_t_lib.wonder_dict

Dead_cursor = orders_t_lib.Dead_cursor

# We need a much reduced dummy world from the orders, we need to test much more specific things each time
def dummy_world():
	w = world.World(Dead_cursor())
	
	#	TEAMS
	#------------------------
	w._teams = {
		0:	team.Team({
			"name":			"Our team",
			"active":		True,
		}),
		1:	team.Team({
			"name":			"Their team",
			"active":		True,
		}),
		
		2:	team.Team({
			"name":			"Our first ally",
			"active":		True,
		}),
		3:	team.Team({
			"name":			"Our second ally",
			"active":		True,
		}),
		
		12:	team.Team({
			"name":			"Their first ally",
			"active":		True,
		}),
		13:	team.Team({
			"name":			"Their second ally",
			"active":		True,
		}),
	}
	
	for i, t in w._teams.items():
		t.id = i
		t.deities = {}
		t.evolutions = {}
		t.tech_levels = {}
		t.spell_levels = {}
		t.resources = res_dict.Res_dict("Materials:0")
		t.artefacts = []
		t.wonders = []
	
	#	LISTS
	#------------------------
	w._buildings = building_dict
	w._equipment = equipment_dict
	w._deities = deity_dict
	w._evolutions = evolution_dict
	w._spell = spell_dict
	w._techs = tech_dict
	w._artefacts = artefact_dict
	w._wonders = wonder_dict
	
	# Build an array it'd normally do itself
	for k, v in w._buildings.items():
		if v.upgrades > 0:
			if v.upgrades not in w._building_requirements:
				w._building_requirements[v.upgrades] = []
			
			w._building_requirements[v.upgrades].append(k)
	
	return w


def XYZ():
	#	TEAMS
	#------------------------
	w._teams = {
		0:	team.Team({
			"name":			"Team all",
		}),
		1:	team.Team({
			"name":			"Team arl",
		}),
		2:	team.Team({
			"name":			"Team adyl",
		}),
	}
	
	for k, v in w._teams.items(): v.id = k
	
	#	CITIES
	#------------------------
	w._cities =  {
		0:	city.City({
			"name":	"Durandalbad",
			"team":	w.teams_lookup()["SArkalians"],
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
	
	for k, v in w._cities.items(): v.id = k
	
	#	BUILDINGS
	#------------------------
	w._cities[w.cities_lookup()['City0']].buildings[w.buildings_lookup()['University']] = 0
	w._cities[w.cities_lookup()['City1']].buildings[w.buildings_lookup()['University']] = 50
	w._cities[w.cities_lookup()['City2']].buildings[w.buildings_lookup()['University']] = 100
	w._cities[w.cities_lookup()['City3']].buildings[w.buildings_lookup()['University']] = 150
	w._cities[w.cities_lookup()['City4']].buildings_amount[w.buildings_lookup()['University']] = 1
	
	
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

