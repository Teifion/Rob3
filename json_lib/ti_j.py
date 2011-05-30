import json
import math
from pages import common
from classes import world, team, operative, player, power
from functions import stat_f, path_f, team_f
from lists import resource_list
from queries import spy_report_q, mapper_q, operative_q
import traceback
from rules import deity_rules
from rules import tech_rules, spell_rules, team_rules, unit_rules, map_data, city_rules

def evolutions(the_world, the_team):
	output = {}
	
	evolution_dict = the_world.evolutions()
	the_team.get_evolutions(the_world.cursor)
	
	for evolution_id, evo_level in the_team.evolutions.items():
		the_evo = evolution_dict[evolution_id]
		
		if evo_level == 0:
			continue
		
		if the_evo.max_level == 1 and evo_level == 1:
			output[evolution_id] = {
				"evo_id":	the_evo.id,
				"level":	evo_level,
			}
	
	return output

def resources(the_world, the_team):
	output = {
		"current":		{},
		"produce":		{},
		"upkeep":		{},
		"availiable":	{},
	}
	
	# We need to do this to predict them correctly
	team_resources = the_team.get_resources(the_world.cursor, force_requery=False)
	produced_resources, new_resources = team_rules.produce_resources(the_world.cursor, the_team, the_world, force_requery=False)
	
	# Now we repeat this to display the current amounts correctly
	the_team.resources = team_resources
	
	count = -1
	for res_id, the_res in enumerate(resource_list.data_list):
		if res_id not in the_team.resources.value:
			the_team.resources.value[res_id] = 0
		
		# If all of them are 0 then there's no need to show it
		if the_team.resources.value[res_id] == 0:
			if produced_resources.get(res_id) == 0:
				if new_resources.get(res_id) == 0:
					continue
		
		if the_res.name == "Materials":
			upkeep_amount = int(team_f.get_upkeep(the_team, the_world))
			future_amount = int(new_resources.value[res_id]-int(upkeep_amount))
			
		elif the_res.name == "Food":
			upkeep_amount = team_rules.resource_needed(the_world.cursor, "Food", the_team)
			upkeep_amount = round(upkeep_amount, 2)
			future_amount = int(new_resources.value[res_id]-int(upkeep_amount))
			
			upkeep_amount = int(upkeep_amount)
		else:
			upkeep_amount = ""
			future_amount = int(new_resources.value[res_id])
		
		output['current'][res_id]		= int(the_team.resources.value.get(res_id, 0))
		output['produce'][res_id]		= int(produced_resources.value.get(res_id, 0))
		output['upkeep'][res_id]		= upkeep_amount
		output['availiable'][res_id]	= future_amount
	
	return output

def deities(the_world, the_team):
	output = {}
	
	# Possible time saver
	the_team.get_deities(the_world.cursor)
	if len(the_team.deities.items()) == 0:
		return {}
	
	deity_dict		= the_world.deities()
	city_dict		= the_world.cities()
	servant_dict_c	= the_world.servants()
	deity_favour_info = {}
	
	# Get favour
	for deity_id, deity_favour in the_team.deities.items():
		favour_result = deity_rules.calculate_favour(the_world, the_team, deity_id)
		the_team.deities[deity_id] = favour_result[0]
		deity_favour_info[deity_id] = favour_result[1]
	
	# Get temple points
	if the_team.temple_points < 0:
		the_team.temple_points = 0
		for city_id, the_city in city_dict.items():
			if the_city.team != the_team.id: continue
			if the_city.population < 15000: continue
			
			multiplier = int(math.floor(the_city.population / 15000))
			the_team.temple_points += (the_city.get_temple_points(the_world.cursor) * multiplier)
	
	deity_servants = {}
	# Servants
	for deity_id, deity_favour in the_team.deities.items():
		for servant_id, the_servant in servant_dict_c.items():
			if the_servant.deity != deity_id: continue
			
			# Favour
			if deity_favour < the_servant.favour_needed: continue
			
			# Temple points
			if the_team.temple_points < the_servant.temple_points: continue
			
			# Monotheism
			if len(the_team.deities.keys()) > 1 and the_servant.monotheistic: continue
			
			if deity_id not in deity_servants:
				deity_servants[deity_id] = {}
				
			deity_servants[deity_id][the_servant.name] = {
				"name":			the_servant.name,
				"description":	the_servant.description,
				"cost":			the_servant.summon_cost,
				"amount":		the_servant.summon_amount,
			}
	
	for deity_id, deity_favour in the_team.deities.items():
		output[deity_id] = {
			"deity_id":	deity_id,
			"favour":	deity_favour,
			"servants":	deity_servants.get(deity_id, {}),
		}
	
	return output

def units(the_world, the_team):
	unit_dict = the_world.units_from_team(the_team.id)
	special_unit_dict = the_world.units_from_team(0)
	the_team.get_units(the_world.cursor)
	
	output = {}
	
	# Team units
	for u, the_unit in unit_dict.items():
		the_unit.get_cost(the_world=the_world)
		output[u] = {
			"team":				the_unit.team,
			"unit_id":			u,
			"name":				the_unit.name,
			"amount":			the_team.units.get(u, 0),
			"iron cost":		the_unit.costs['iron_cost'].value,
			"material cost":	the_unit.costs['material_cost'].value,
			"iron upkeep":		the_unit.costs['iron_upkeep'].value,
			"material upkeep":	the_unit.costs['material_upkeep'].value,
			"equipment":		the_unit.equipment,
		}
		
	# Special units
	for u, the_unit in special_unit_dict.items():
		the_unit.get_cost(the_world=the_world)
		output[u] = {
			"team":				the_unit.team,
			"unit_id":			u,
			"name":				the_unit.name,
			"amount":			the_team.units.get(u, 0),
			"iron cost":		the_unit.costs['iron_cost'].value,
			"material cost":	the_unit.costs['material_cost'].value,
			"iron upkeep":		the_unit.costs['iron_upkeep'].value,
			"material upkeep":	the_unit.costs['material_upkeep'].value,
			"equipment":		the_unit.equipment,
		}
	
	return output

def armies(the_world, the_team):
	output = {}
	unit_dict = the_world.units()
	army_dict = the_world.armies_from_team(the_team.id)
	city_dict = the_world.cities()
	monster_dict = the_world.monsters()
	
	for a, the_army in army_dict.items():
		if the_army.garrison > 0:
			if the_army.garrison not in city_dict: continue# Skip dead cities
			if city_dict[the_army.garrison].dead == True: continue
		
		# Army squads
		# squad_dict = the_army.get_squads(the_world.cursor)
		squads = {}
		for s, the_squad in the_army.squads.items():
			if the_squad.unit not in unit_dict:
				continue
			
			squads[s] = {
				"squad_id":	s,
				"name":		the_squad.name,
				"unit":		the_squad.unit,
				"size":		the_squad.amount,
			}
		
		output[a] = {
			"army_id":	a,
			"name":		the_army.name,
			"x":		the_army.x,
			"y":		the_army.y,
			"size":		the_army.get_size(the_world.cursor),
			"squads":	squads,
			"monsters":	the_army.monsters,
		}
	
	return output

def operatives(the_world, the_team):
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	operatives_dict	= the_world.operatives_from_team(the_team.id)
	reports_dict = {}
	
	if len(operatives_dict) <= 0 and len(reports_dict) <= 0:
		return {}
	
	# Starting the output
	output = {}
	
	# Caught ops
	caught_ops = operative_q.operatives_caught_in_cities(
		the_world.cursor,
		the_world.cities_from_team(the_team.id),
		since=common.current_turn()-3,
	)
	
	if len(caught_ops) > 0:
		for k, the_op in caught_ops.items():
			output[k] = {
				"op_id":	k,
				"name":		the_op.name,
				"team":		the_op.team,
				"city":		the_op.city,
				"caught":	the_op.died,
			}
	
	for o, the_op in operatives_dict.items():
		output[o] = {
			"op_id":	o,
			"name":		the_op.name,
			"team":		the_op.team,
			"city":		the_op.city,
			"caught":	the_op.died,
			
			"size":				the_op.size,
			"arrival":			the_op.arrival,
			"stealth":			the_op.stealth,
			"observation":		the_op.observation,
			"integration":		the_op.integration,
			"sedition":			the_op.sedition,
			"sabotage":			the_op.sabotage,
			"assassination":	the_op.assassination,
		}
	
	return output

def techs(the_world, the_team):
	output = {}
	
	tech_dict = the_world.techs()
	the_team.get_techs(the_world.cursor)
	
	for tech_id, tech_level in the_team.tech_levels.items():
		if tech_level == 0 and the_team.tech_points[tech_id] < 1:
			continue
		
		output[tech_id] = {
			"tech_id":				tech_id,
			"level":				tech_level,
			"points":				the_team.tech_points[tech_id],
			"points_to_next_level":	tech_rules.cost_for_next_level(the_world.cursor, tech_dict[tech_id], tech_level).get("Tech points")
		}
	
	return output

def spells(the_world, the_team):
	output = {}
	
	spell_dict = the_world.spells()
	the_team.get_spells(the_world.cursor)
	
	for spell_id, spell_level in the_team.spell_levels.items():
		if spell_level == 0 and the_team.spell_points[spell_id] < 1:
			continue
		
		output[spell_id] = {
			"spell_id":				spell_id,
			"level":				spell_level,
			"points":				the_team.spell_points[spell_id],
			"points_to_next_level":	spell_rules.cost_for_next_level(the_world.cursor, spell_dict[spell_level], spell_level, True).get("Spell points"),
		}
	
	return output

def chosen(the_world, the_team):
	player_dict = the_world.players_from_team(the_team.id)
	powers_dict = the_world.powers()
	
	team_powers_list = []
	team_powers_list_names = []
	
	output = {}
	for player_id, the_player in player_dict.items():
		
		powers = {}
		for p in the_player.powers:
			the_power = powers_dict[p]
			
			# Avoid dupes
			if the_power.name not in team_powers_list_names:
				team_powers_list_names.append(the_power.name)
			
			powers[the_power.name] = {
				"power_name":	the_power.name,
				"type":			power.power_types[the_power.type],
				"description":	the_power.description,
			}
		
		output[player_id] = {
			"player_id":	player_id,
			"name":			the_player.name,
			"daemon_level":	player.progressions[the_player.progression],
			"daemon_type":	player.daemon_types[the_player.daemon_type],
			"powers":		powers,
		}
	
	return output

def cities(the_world, the_team):
	city_dict		= the_world.cities_from_team(the_team.id)
	building_dict	= the_world.buildings()
	artefact_dict	= the_world.artefacts()
	wonder_dict		= the_world.wonders()
	
	output = {}
	
	for city_id, the_city in city_dict.items():
		if the_city.dead > 0: continue
		
		artefacts = {}
		buildings = {}
		wonders = {}
		
		# City buildings
		buildings_progress, buildings_amount = the_city.get_buildings(the_world.cursor)
		
		for b, the_building in building_dict.items():
			if b not in buildings_progress and b not in buildings_amount:
				continue
			
			buildings[b] = {
				"building_id":			b,
				"completed":			buildings_amount.get(b, 0),
				"current_progress":		buildings_progress.get(b, 0),
			}
		
		# Artefacts
		for artefact_id, the_artefact in artefact_dict.items():
			if the_artefact.city != city_id: continue
			
			artefacts[the_artefact.name] = {
				"name":			the_artefact.name,
				"description":	the_artefact.description,
			}
		
		# Wonders
		for wonder_id, the_wonder in wonder_dict.items():
			if the_wonder.city != city_id: continue
			
			wonders[the_wonder.name] = {
				"name":				the_wonder.name,
				"description":		the_wonder.description,
				"progress":			the_wonder.completion,
				"needed_points":	the_wonder.point_cost,
				"needed_materials":	the_wonder.material_cost,
			}
		
		# Growth
		growth_rate, growth_constant = city_rules.city_growth_rate(the_world.cursor, the_team, the_city, the_world)
		new_population = int((the_city.population * growth_rate) + growth_constant)
		growth_rate = (growth_rate-1)*100
		
		output[city_id] = {
			"city_id":			city_id,
			"name":				the_city.name,
			"x":				the_city.x,
			"y":				the_city.y,
			
			"terrain":			map_data.terrain[mapper_q.get_terrain(the_world.cursor, the_city.x, the_city.y)].title(),
			"port":				the_city.port,
			"nomadic":			the_city.nomadic,
			
			"population":		the_city.population,
			"new_population":	new_population,
			"growth_rate":		growth_rate,
			"slaves":			the_city.slaves,
			"supply_good":		the_city.supply_good,
			
			"artefacts":		artefacts,
			"wonders":			wonders,
			"buildings":		buildings,
		}
	
	return output

def diplomacy(the_world, the_team):
	team_dict		= the_world.teams()
	relations			= the_world.relations()
	border_history	= the_world.border_history()
	
	# Set a default here to save checking it time and time again later
	output = {}
	
	for ot, other_team in team_dict.items():
		if not other_team.active: continue
		if other_team.hidden: continue
		
		output[ot] = {
			"us_to_them":	relations.get(the_team.id, {}).get(ot, {}).get('border', the_team.default_borders),
		}
		
		# Them to us?
		output[ot]['them_to_us'] = relations.get(ot, {}).get(the_team.id, {}).get('border', team_dict[ot].default_borders)
		
		# Get previous status
		previous_status = border_history.get(ot, {})
		if the_team.id in previous_status:
			output[ot]['previous_them_to_us'] = previous_status[the_team.id]
		else:
			output[ot]['previous_them_to_us'] = previous_status.get(-1, team.default_border_state)
	
	return output


def make_ti(the_world, the_team):
	# Build team stats
	stat_f.build_team_stats(the_world.cursor, the_team, the_world)
	
	# Get some properties
	# the_team.get_population(cursor)
	
	output = {}
	
	output['evolutions']	= evolutions(the_world, the_team)	
	output['resources']		= resources(the_world, the_team)
	output['deities']		= deities(the_world, the_team)
	output['cities']		= cities(the_world, the_team)
	output['units']			= units(the_world, the_team)
	output['armies']		= armies(the_world, the_team)
	output['operatives']	= operatives(the_world, the_team)
	output['techs']			= techs(the_world, the_team)
	output['spells']		= spells(the_world, the_team)
	output['chosen']		= chosen(the_world, the_team)
	output['diplomacy']		= diplomacy(the_world, the_team)
	
	return json.dumps(output)
