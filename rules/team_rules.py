import math

from queries import evolution_q, team_q
from lists import resource_list
from classes import res_dict
import classes
import rules

def _food_needed_modifier(the_world, the_team):
	modifier = 1
	
	# Check evos
	team_evolutions = the_team.get_evolutions(the_world.cursor)
	evo_id = the_world.evolutions_lookup()["Metabolic Efficiency"]
	
	if evo_id in team_evolutions:
		evo_level = team_evolutions[evo_id]
		
		if evo_level > 0:
			modifier *= (1 - (evo_level * 0.05))
		elif evo_level < 0:
			modifier *= (1 + (evo_level * 0.1))
	
	# Take it down
	modifier = modifier/1000
	
	return modifier

def resource_needed(cursor, resource_name, the_team, the_world=None):
	# Erronous values
	if resource_name != "Food":
		raise Exception("No handler for %s" % resource_name)
	
	if the_world == None:
		from classes import world
		the_world = world.World(cursor)
	
	# Sizes
	population	= the_team.get_population(cursor)
	slaves		= the_team.get_slaves(cursor)
	military	= team_q.get_unit_category_size(cursor, the_team.id, 0, 100)
	
	total_size = population + slaves + military
	
	total_size *= _food_needed_modifier(the_world, the_team)
	
	return total_size

def Materials(cursor, the_team, the_world=None, one_city_id=-1):
	from rules import city_rules
	if the_world == None: the_world = classes.world.World(cursor)
	
	our_cities			= the_world.cities_from_team(the_team.id)
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	techs_lookup		= the_world.techs_lookup()
	artefacts_lookup	= the_world.artefacts_lookup()
	
	result = 0
	
	for city_id, the_city in our_cities.items():
		if the_city.dead > 0: continue
		
		if one_city_id > 0 and one_city_id != city_id: continue
		
		# Basic production
		size_small	= (the_city.population + the_city.slaves)/1000
		city_result	= math.sqrt(size_small * size_small * 4.5) - 25
		
		# Nomads are losers, they produce half
		if the_city.nomadic:
			city_result /= 2
		
		# buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		# if buildings_lookup['Hospital'] in buildings_amount:		small_size -= 10
		
		# Deities
		team_deities = the_team.get_deities(cursor)
		
		# Arl gives a 10% bonus
		if deities_lookup['Arl'] in team_deities:
			arl_points = team_deities[deities_lookup['Arl']]
			if city_result > 0:
				city_result *= (1+(arl_points*0.1))
			else:
				city_result *= (1-(arl_points*0.1))
		
		# Trchkithin gives each city 7.5 more materials
		if deities_lookup['Trchkithin'] in team_deities:
			trch_points = team_deities[deities_lookup['Trchkithin']]
			city_result += (trch_points*7.5)
		
		# Economy tech
		team_techs = the_team.get_techs(cursor)[0]
		
		if techs_lookup['Economy'] in team_techs:
			if not the_city.nomadic:
				if city_result > 0:
					city_result *= (1+(team_techs[techs_lookup['Economy']]*0.025))
				else:
					city_result *= (1-(team_techs[techs_lookup['Economy']]*0.025))
		
		# Economy evo
		team_evolutions = the_team.get_evolutions(cursor)
		if evolutions_lookup['Affinity for Economics'] in team_evolutions:
			if city_result > 0:
				city_result *= (1+(team_evolutions[evolutions_lookup['Affinity for Economics']]*0.05))
			else:
				city_result *= (1-(team_evolutions[evolutions_lookup['Affinity for Economics']]*0.05))
		
		# Reethmine artefact
		if artefacts_lookup['Reethmine'] in the_city.get_artefacts(cursor):
			if city_result > 0:
				city_result *= 3.0
			else:
				city_result *= 0.33
		
		# Swarm statue
		if artefacts_lookup['Swarm statue'] in the_team.get_artefacts(cursor):
			city_result = max(city_result, 0)
		
		# Breakdown
		# print("%s: %s" % (the_city.name, city_result))
		
		# Overlap
		city_result *= rules.city_rules.overlap(the_city.overlap)
		
		# Nomadic, can't be negative
		if the_city.nomadic:
			city_result = max(city_result, 0)
		
		result += city_result
	
	return result

def Food(cursor, the_team, the_world=None, one_city_id=-1):
	from rules import city_rules
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	# buildings_lookup	= the_world.buildings_lookup()
	techs_lookup		= the_world.techs_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		if one_city_id > 0 and one_city_id != city_id: continue
		
		# Basic production
		city_size	= (the_city.population + the_city.slaves)
		
		city_result = min(city_size * 1.5, 75000)
		
		if city_size > 50000:
			city_size -= 50000
			
			for i in range(1, 11):
				if city_size > 5000:
					city_size -= 5000
					
					# Produces less and less
					city_result += (7500 - (i * 750))
		
		# Is the city built on a food supply?
		if resource_list.data_dict_n['Fertile lands'] in the_city.supplies:
			city_result *= 2
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		# if buildings_lookup['Hospital'] in buildings_amount:		small_size -= 10
		
		# Adyl gives a 10% bonus
		team_deities = the_team.get_deities(cursor)
		if deities_lookup['Adyl'] in team_deities:
			adyl_points = team_deities[deities_lookup['Adyl']]
			city_result *= (1+(adyl_points*0.1))
		
		# Farming tech
		team_techs = the_team.get_techs(cursor)[0]
		
		if techs_lookup['Farming'] in team_techs:
			if the_city.nomadic == 0:
				city_result *= (1+(team_techs[techs_lookup['Farming']]*0.025))
		
		# Farming evo
		team_evolutions = the_team.get_evolutions(cursor)
		
		if evolutions_lookup['Affinity for the land'] in team_evolutions:
			city_result *= (1+(team_evolutions[evolutions_lookup['Affinity for the land']]*0.05))
		
		# Overlap
		city_result *= rules.city_rules.overlap(the_city.overlap)
		the_city.surplus_food = city_result
		
		# Food is measured at 1 unit per 1k people
		result += city_result/1000.0
	
	return result

def Tech_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	# techs_lookup		= the_world.techs_lookup()
	result = 0
	
	sub_total = 0
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['University'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['University']] * 50)
		
		if buildings_lookup['Expanded university'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Expanded university']] * 100)
		
		# What about a partially completed uni?
		if buildings_lookup['Expanded university'] in buildings_completion:
			if buildings_completion[buildings_lookup['Expanded university']] > 0:
				city_result += 50
		
		# Ldura gives a 10% bonus
		team_deities = the_team.get_deities(cursor)
		if deities_lookup['Ldura'] in team_deities:
			# OLD DEITY
			# ldura_points = the_city.get_temple_points() * team_deities[deities_lookup['Ldura']]
			# city_result *= (1+(ldura_points*0.1))
			
			# NEW DEITY
			ldura_points = team_deities[deities_lookup['Ldura']]
			city_result *= (1+(ldura_points*0.1))
		
		# Tech affinity
		team_evolutions = the_team.get_evolutions(cursor)
		if evolutions_lookup['Technological affinity'] in team_evolutions:
			city_result *= (1+(team_evolutions[evolutions_lookup['Technological affinity']]*0.1))
		
		result += city_result
		
		# Breakdown
		# sub_total += city_result
		# print("%s: %s (%s)<br />" % (the_city.name, city_result, sub_total))
	
	return result

def Spell_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	# evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	# techs_lookup		= the_world.techs_lookup()
	result = 50# Each team gets 50 right away
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy']] * 50)
		
		if buildings_lookup['Expanded academy'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Expanded academy']] * 100)
		
		# Specifics
		city_result += buildings_amount.get(buildings_lookup['Academy of Light'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Dark'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Abjuration'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Destruction'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Daemonic'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Necromancy'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Enchantment'], 0) * 50
		city_result += buildings_amount.get(buildings_lookup['Academy of Alchemy'], 0) * 50
		
		# Partially completed expandeds
		if buildings_lookup['Expanded academy'] in buildings_completion:
			if buildings_completion[buildings_lookup['Expanded academy']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Light'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Light']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Dark'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Dark']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Abjuration'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Abjuration']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Destruction'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Destruction']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Daemonic'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Daemonic']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Necromancy'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Necromancy']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Enchantment'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Enchantment']] > 0:
				city_result += 50
		
		if buildings_lookup['Academy of Alchemy'] in buildings_completion:
			if buildings_completion[buildings_lookup['Academy of Alchemy']] > 0:
				city_result += 50
		
		# Ldura gives a 10% bonus
		team_deities = the_team.get_deities(cursor)
		if deities_lookup['Ldura'] in team_deities:
			# OLD DEITY
			# ldura_points = the_city.get_temple_points() * team_deities[deities_lookup['Ldura']]
			# city_result *= (1+(ldura_points*0.1))
			
			# NEW DEITY
			ldura_points = team_deities[deities_lookup['Ldura']]
			city_result *= (1+(ldura_points*0.1))
		
		# Breakdown
		# print "%s: %s<br />" % (the_city.name, city_result)
		
		result += city_result
	
	return result

def Ship_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	techs_lookup		= the_world.techs_lookup()
	artefacts_lookup	= the_world.artefacts_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		if the_city.port != 1: continue
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Shipyard'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Shipyard']] * 100)
		
		if buildings_lookup['Expanded shipyard'] in buildings_amount:
			if buildings_amount[buildings_lookup['Expanded shipyard']] > 0:
				city_result += 100
		
		if buildings_lookup['Expanded shipyard'] in buildings_completion:
			city_result += (buildings_amount[buildings_lookup['Expanded shipyard']] * 200)
		
		# Farming tech
		team_techs = the_team.get_techs(cursor)[0]
		
		if techs_lookup['Shipbuilding'] in team_techs:
			if the_city.nomadic == 0:
				city_result *= (1+(team_techs[techs_lookup['Shipbuilding']]*0.1))
		
		# Timberfell artefact
		if artefacts_lookup['Timberfell'] in the_city.get_artefacts(cursor):
			city_result += 500
		
		# print the_city.name, "&nbsp;", city_result, "<br />"
		result += city_result
		
	
	return result

def Airship_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	techs_lookup		= the_world.techs_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		if the_city.port == 1: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Shipyard'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Shipyard']] * 100)
		
		if buildings_lookup['Expanded shipyard'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Expanded shipyard']] * 200)
		
		if buildings_lookup['Expanded shipyard'] in buildings_completion:
			if buildings_completion[buildings_lookup['Expanded shipyard']] > 0:
				city_result += 100
		
		# Farming tech
		team_techs = the_team.get_techs(cursor)[0]
		
		if techs_lookup['Shipbuilding'] in team_techs:
			if the_city.nomadic == 0:
				city_result *= (1+(team_techs[techs_lookup['Shipbuilding']]*0.1))
		
		result += city_result
	
	return result


def Iron(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict		= the_world.cities_from_team(the_team.id)
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.dead > 0: continue
		
		city_result = 0
		
		if resource_list.data_dict_n['Iron'] in the_city.supplies:
			city_result = 1
		
		result += city_result
	
	
	return result

def Stone(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		if resource_list.data_dict_n['Stone'] in the_city.supplies:
			city_result = 1
		
		result += city_result
	
	return result

def Wood(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		if resource_list.data_dict_n['Wood'] in the_city.supplies:
			city_result = 1
		
		result += city_result
	
	return result


#	Specific spell types
#------------------------
def Light_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Light'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Light']] * 100)
		
		result += city_result
	
	return result

def Dark_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Dark'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Dark']] * 100)
		
		result += city_result
	
	return result

def Abjuration_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Abjuration'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Abjuration']] * 100)
		
		result += city_result
	
	return result

def Destruction_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Destruction'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Destruction']] * 100)
		
		result += city_result
	
	return result

def Daemonic_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Daemonic'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Daemonic']] * 100)
		
		result += city_result
	
	return result

def Necromancy_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Necromancy'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Necromancy']] * 100)
		
		result += city_result
	
	return result


def Alchemy_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Alchemy'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Alchemy']] * 100)
		
		result += city_result
	
	return result


def Enchantment_points(cursor, the_team, the_world=None):
	if the_world == None: the_world = classes.world.World(cursor)
	
	city_dict			= the_world.cities()
	buildings_lookup	= the_world.buildings_lookup()
	result = 0
	
	for city_id, the_city in city_dict.items():
		if the_city.team != the_team.id: continue
		if the_city.dead > 0: continue
		
		city_result = 0
		
		buildings_completion, buildings_amount = the_city.get_buildings(cursor)
		
		# No buildings boost material production
		if buildings_lookup['Academy of Enchantment'] in buildings_amount:
			city_result += (buildings_amount[buildings_lookup['Academy of Enchantment']] * 100)
		
		result += city_result
	
	return result

# Used for things that are not actually resources
def return_none(cursor, the_team, the_world=None):
	return 0
 
resource_functions = {
	"Materials":			Materials,
	"Food":					Food,
	"Tech points":			Tech_points,
	"Spell points":			Spell_points,
	"Ship points":			Ship_points,
	
	"Iron":					Iron,
	"Stone":				Stone,
	"Wood":					Wood,
	
	"Fertile lands":		return_none,
	"Giant hill":			return_none,
	"Natural harbour":		return_none,
	"Gateway to Enkhingi":	return_none,
	
	"Light points":			Light_points,
	"Dark points":			Dark_points,
	"Abjuration points":	Abjuration_points,
	"Destruction points":	Destruction_points,
	"Daemonic points":		Daemonic_points,
	"Necromancy points":	Necromancy_points,
	"Alchemy points":		Alchemy_points,
	"Enchantment points":	Enchantment_points,
	
	"Balloon points":		Airship_points,
}

def produce_resources(cursor, the_team, the_world=None, force_requery=False):
	"""Returns a Res_dict of the current resources, resources produced and the two added together"""
	produced_resources	= res_dict.Res_dict()
	new_resources		= res_dict.Res_dict(the_team.get_resources(cursor).value)# Set to their current resources for adding purposes
	
	# For each resource type
	for resource_id, the_resource in resource_list.data_dict.items():
		if the_resource.name in resource_functions:
			value = resource_functions[the_resource.name](cursor, the_team, the_world)
			
			# Reset or add?
			if the_resource.reset:
				produced_resources.set(resource_id, value)
				new_resources.set(resource_id, value)	
			else:
				produced_resources.set(resource_id, value)
				new_resources += ("%s:%s" % (the_resource.name, value))
		
		else: raise Exception("No function to handle resource type '%s'" % the_resource.name)
	
	return produced_resources, new_resources


def alter_upkeep(cursor, the_team, upkeep_cost, the_world=None):
	"""Alters the team upkeep as needed"""
	if the_world == None:
		affinity_for_war = evolution_q.get_one_evolution(cursor, "Affinity for war")
	else:
		affinity_for_war = the_world.evolutions()[the_world.evolutions_lookup()['Affinity for war']]
	
	# Affinity for war evo
	team_evolutions = the_team.get_evolutions(cursor)
	
	multiplier = 1
	if affinity_for_war.id in team_evolutions:
		level = team_evolutions[affinity_for_war.id]
		if level > 0:
			multiplier = (1-(level*0.05))
		else:
			multiplier = (1+(level*0.1))
	
	return upkeep_cost * multiplier

def nation_morale(cursor, the_team, the_world=None):
	if the_world == None:
		try:
			the_world = classes.world.World(cursor)
		except Exception as e:
			try:
				from classes import world
				the_world = world.World(cursor)
			except Exception as e:
				raise
	
	
	evolutions_lookup = the_world.evolutions_lookup()
	
	# Get resources
	team_res = the_team.get_resources(cursor)
	
	score = 100
	
	# Materials
	material_amount = int(team_res.get("Materials"))
	
	if material_amount < 0:
		if material_amount < -200:	score = 25
		else:						score = 65
	else:							score = 100
	
	# Food
	food_amount = int(team_res.get("Food"))
	needed = resource_needed(cursor, "Food", the_team)
	food_ratio = round(food_amount/float(needed), 2)
	
	food_score = (food_ratio-1) * 50
	score = score + food_score
	
	# Evos
	team_evolutions = the_team.get_evolutions(cursor)
	
	if evolutions_lookup["Morale"] in team_evolutions:
		morale_evo = team_evolutions[evolutions_lookup["Morale"]]
		if morale_evo > 0:
			score *= (1 + (morale_evo/10.0))
		elif morale_evo < 0:
			score *= (1 - (morale_evo/5.0))
	
	return score

def define_nation_morale(score):
	if score < 25:
		return "Almost anarchy"
	elif score < 50:
		return "Appaling"
	elif score < 75:
		return "Bad"
	elif score < 95:
		return "Poor"
	elif score < 105:
		return "Neutral"
	elif score < 125:
		return "Good"
	elif score < 150:
		return "Very good"
	else:
		return "Amazing"


