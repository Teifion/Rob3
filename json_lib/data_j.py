import json
from queries import building_q, deity_q, equipment_q, evolution_q, spell_q, tech_q, player_q, team_q
from lists import resource_list
from classes import res_dict
from data_classes import evolution, spell
from rules import sad_rules

def buildings(cursor):
	output = {}
	
	building_dict = building_q.get_all_buildings(cursor)
	for b, the_building in building_dict.items():
		if not the_building.public: continue
		output[b] =  {
			"building_id":		b,
			"name":				the_building.name,
			"build_time":		the_building.build_time,
			"upgrades":			the_building.upgrades,
			"wall":				the_building.wall,
			"economy":			the_building.economy,
			"needs_port":		the_building.needs_port,
			"cost_per_turn":	res_dict.Res_dict(the_building.cost_per_turn).value,
			"cost_up_front":	res_dict.Res_dict(the_building.cost_up_front).value,
			"upkeep":			res_dict.Res_dict(the_building.upkeep).value,
			"limit_per_city":	the_building.limit_per_city,
			"description":		the_building.description,
		}
	
	return json.dumps(output)

def deities(cursor):
	output = {}
	
	deity_dict = deity_q.get_all_deities(cursor)
	for d, the_deity in deity_dict.items():
		output[d] =  {
			"deity_id":		d,
			"name":			the_deity.name,
			"major":		the_deity.major,
			"minor":		the_deity.minor,
			"negative":		the_deity.negative,
			"bonus":		the_deity.bonus,
			"objective":	the_deity.objective,
			"di":			the_deity.di,
			"summary":		the_deity.summary,
			"likes":		the_deity.likes,
			"dislikes":		the_deity.dislikes,
			"hates":		the_deity.hates,
			"backstory":	the_deity.backstory,
			"monotheistic":	the_deity.monotheistic,
		}
	
	return json.dumps(output)

def equipment(cursor):
	output = {}
	
	equipment_dict = equipment_q.get_all_equipment(cursor)
	for e, the_eq in equipment_dict.items():
		if not the_eq.public: continue
		output[e] =  {
			"equipment_id":			e,
			"name":					the_eq.name,
			"cost":					res_dict.Res_dict(the_eq.cost).value,
			"cost_raw":				the_eq.cost,
			"cost_multiplier":		res_dict.Res_dict(the_eq.cost_multiplier).value,
			"cost_multiplier_raw":	the_eq.cost_multiplier,
			"crew":					the_eq.crew,
			"transport":			the_eq.transport,
		}
	
	return json.dumps(output)

def evolutions(cursor):
	output = {}
	
	evolution_dict = evolution_q.get_all_evolutions(cursor)
	for e, the_evo in evolution_dict.items():
		if the_evo.name == "VOID": continue
		output[e] =  {
			"evolution_id":			e,
			"name":					the_evo.name,
			"cost_per_level":		the_evo.cost_per_level,
			"max_level":			the_evo.max_level,
			"min_level":			the_evo.min_level,
			"description":			the_evo.description,
			"category":				evolution.categories[the_evo.category],
		}
	
	return json.dumps(output)

def resources(cursor):
	output = {}
	
	for r, resource in enumerate(resource_list.data_list):
		output[r] =  {
			"resource_id":	r,
			"name":			resource.name,
			"type":			resource.type,
			"category":		resource.category,
			"tradable":		resource.tradable,
			"reset":		resource.reset,
			"map_supply":	resource.map_supply,
		}
	
	return json.dumps(output)

def spells(cursor):
	output = {}
	
	spell_dict = spell_q.get_all_spells(cursor)
	for s, the_spell in spell_dict.items():
		output[s] =  {
			"spell_id":		s,
			"name":			the_spell.name,
			"tier":			the_spell.tier,
			"max_level":	the_spell.max_level,
			"category":		spell.categories[the_spell.category],
			"cooldown":		the_spell.cooldown,
			"cast_time":	the_spell.cast_time,
			"tradable":		the_spell.tradable,
			"description":	the_spell.description,
		}
	
	return json.dumps(output)

def techs(cursor):
	output = {}
	
	tech_dict = tech_q.get_all_techs(cursor)
	for t, the_tech in tech_dict.items():
		output[t] =  {
			"tech_id":		t,
			"name":			the_tech.name,
			"base_cost":	res_dict.Res_dict(the_tech.base_cost).value,
			"extra_cost":	res_dict.Res_dict(the_tech.extra_cost).value,
			"max_level":	the_tech.max_level,
			"category":		the_tech.category,
			"tradable":		the_tech.tradable,
			"description":	the_tech.description,
		}
	
	return json.dumps(output)

def players(cursor):
	output = {}
	
	player_dict = player_q.get_active_players(cursor, turn_count=7)
	for p, the_player in player_dict.items():
		output[p] =  {
			"player_id":	p,
			"name":			the_player.name,
			"ir":			the_player.ir,
			"team":			the_player.team,
			"last_order":	the_player.last_posted,
		}
	
	return json.dumps(output)

def teams(cursor):
	output = {}
	
	team_dict = team_q.get_all_teams(cursor)
	player_dict = player_q.get_active_players(cursor, turn_count=5)
	
	seconds = {}
	for p, the_player in player_dict.items():
		if p != team_dict[the_player.team].leader_id:
			if the_player.team not in seconds:
				seconds[the_player.team] = []
			seconds[the_player.team].append(p)
	
	deities = []
	evolutions = []
	
	for t, the_team in team_dict.items():
		if the_team.dead: continue
		if the_team.not_in_queue: continue
		if the_team.hidden: continue
		if the_team.not_a_team: continue
		
		output[t] =  {
			"team_id":		t,
			"name":			the_team.name,
			"leader":		the_team.leader_id,
			"seconds":		seconds.get(t, []),
			"culture":		the_team.culture_topic,
			"ir":			the_team.ir,
			"join_turn":	the_team.join_turn,
			
			"deities":		list(the_team.get_deities(cursor).keys()),
			"evolutions":	the_team.get_evolutions(cursor),
		}
	
	return json.dumps(output)

def supply_demand(cursor):
	output = {}
	
	for i, g in enumerate(sad_rules.res_list):
		output[i] = g
	
	return json.dumps(output)

handle_dict = {
	'buildings':		buildings,
	'deities':			deities,
	'equipment':		equipment,
	'evolutions':		evolutions,
	'resources':		resources,
	'spells':			spells,
	'techs':			techs,
	'players':			players,
	'teams':			teams,
	'supply_demand':	supply_demand,
}