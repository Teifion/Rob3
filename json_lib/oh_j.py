import json
from queries import building_q, deity_q, equipment_q, evolution_q, spell_q, tech_q, player_q, team_q
from lists import resource_list
from classes import res_dict
from data_classes import evolution, spell
from rules import sad_rules

def buildings(cursor):
	output = {}
	id_list = []
	has_up_list = set()
	
	building_dict = building_q.get_all_buildings(cursor)
	for b, the_building in building_dict.items():
		if not the_building.public: continue
		
		if the_building.upgrades > 0:
			has_up_list.add(the_building.upgrades)
		
		id_list.append(b)
		output[b] =  {
			"building_id":		b,
			"name":				the_building.name,
			"build_time":		the_building.build_time,
			"upgrades":			the_building.upgrades,
			"has_upgrade":		the_building.has_upgrade,
			"wall":				the_building.wall,
			"economy":			the_building.economy,
			"needs_port":		the_building.needs_port,
			# "cost_per_turn":	res_dict.Res_dict(the_building.cost_per_turn).value,
			# "cost_up_front":	res_dict.Res_dict(the_building.cost_up_front).value,
			# "upkeep":			res_dict.Res_dict(the_building.upkeep).value,
			"limit_per_city":	the_building.limit_per_city,
		}
	
	return "buildings = %s; building_list = %s; building_has_up = %s;" % (json.dumps(output), id_list, list(has_up_list))

def spells(cursor):
	output = {}
	id_list = []
	
	spell_dict = spell_q.get_all_spells(cursor)
	for s, the_spell in spell_dict.items():
		
		id_list.append(s)
		output[s] =  {
			"spell_id":		s,
			"name":			the_spell.name,
			"tier":			the_spell.tier,
			"max_level":	the_spell.max_level,
			"category":		spell.categories[the_spell.category],
			# "cooldown":		the_spell.cooldown,
			# "cast_time":	the_spell.cast_time,
			"tradable":		the_spell.tradable,
		}
	
	return "spells = %s; spell_list = %s;" % (json.dumps(output), id_list)

def techs(cursor):
	output = {}
	id_list = []
	
	tech_dict = tech_q.get_all_techs(cursor)
	for t, the_tech in tech_dict.items():
		
		id_list.append(t)
		output[t] =  {
			"tech_id":		t,
			"name":			the_tech.name,
			# "base_cost":	res_dict.Res_dict(the_tech.base_cost).value,
			# "extra_cost":	res_dict.Res_dict(the_tech.extra_cost).value,
			"max_level":	the_tech.max_level,
			"category":		the_tech.category,
			"tradable":		the_tech.tradable,
		}
	
	return "techs = %s; tech_list = %s;" % (json.dumps(output), id_list)

def resources(cursor):
	output = {}
	id_list = []
	
	for r, resource in enumerate(resource_list.data_list):
		id_list.append(r)
		output[r] =  {
			"resource_id":	r,
			"name":			resource.name,
			"type":			resource.type,
			"category":		resource.category,
			"tradable":		resource.tradable,
			"reset":		resource.reset,
			"map_supply":	resource.map_supply,
		}

	return "resources = %s; resource_list = %s;" % (json.dumps(output), id_list)

def teams(cursor):
	output = {}
	id_list = []
	
	team_dict = team_q.get_all_teams(cursor)
	
	for t, the_team in team_dict.items():
		id_list.append(t)
		output[t] =  {
			"team_id":		t,
			"name":			the_team.name,
			"ir":			the_team.ir,
			"join_turn":	the_team.join_turn,
		}
	
	return "teams = %s; team_list = %s;" % (json.dumps(output), id_list)

def supply_demand(cursor):
	output = {}
	id_list = []
	
	for i, g in enumerate(sad_rules.res_list):
		id_list.append(i)
		output[i] = g
	
	return "supplies = %s; supply_list = %s;" % (json.dumps(output), id_list)


def get_data(cursor):
	return """
	{buildings}
	{spells}
	{techs}
	{resources}
	{teams}
	{supply_demand}
	""".format(
		buildings = buildings(cursor),
		spells = spells(cursor),
		techs = techs(cursor),
		resources = resources(cursor),
		teams = teams(cursor),
		supply_demand = supply_demand(cursor),
	)