import re
import math
from classes import order_block, res_dict
from queries import mapper_q
from functions import city_f, path_f
from rules import map_data

def relocation_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	city_dict				= the_line.the_world.cities_from_team(the_line.block.team)
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	all_cities		= the_line.the_world.cities()
	city_dict		= the_line.the_world.cities_from_team(the_line.block.team)
	the_team		= the_line.the_world.teams()[the_line.block.team]
	
	groups['from_city'] = groups['from_city'].strip()
	groups['to_city'] = groups['to_city'].strip()
	
	# Can we find the city?
	if groups['from_city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['from_city'])
	else:
		from_city = all_cities[cities_lookup[groups['from_city'].lower()]]
	
	if groups['to_city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['to_city'])
	else:
		to_city = all_cities[cities_lookup[groups['to_city'].lower()]]
	
	# Target
	try:
		amount = int(groups['amount'].replace(',', ''))
	except Exception as e:
		return order_block.fail(results, "there was an error trying to interpret the number '%s'. error: %s" % (groups['amount'], e.args[0]))
	
	# Type
	if groups['type'].lower() == "civilians":
		move_type = "Civilians"
	elif groups['type'].lower() == "slaves":
		move_type = "Slaves"
	
	# Default result
	results = order_block.default_line_results(the_line, "%s %s could not be moved from %s to %s because" % (amount, move_type, from_city.name, to_city.name))
	
	# Strip out all cities too far away, you can only travel for 12 months
	from_loc	= (from_city.x, from_city.y)
	to_loc		= (to_city.x, to_city.y)
	journey = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=[from_loc, to_loc],
		move_speed="Colonists",
		move_type="Colonists"
	)
	
	# _journey.time_cost
	if journey.time_cost > 365:
		if debug:
			results['debug'].append("Failed at _journey.time_cost")
		return order_block.fail(results, "the time required to move between them is too long (%d days)" % journey.time_cost)
	
	# Cost
	results['cost'] = res_dict.Res_dict("Materials:%s" % (amount/1000))
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	if not affordability:
		return order_block.fail_cost(results)
	
	# Are we going overseas?
	# if mapper_f.get_tile_continent(from_loc) != mapper_f.get_tile_continent(to_loc):
	# 	transport_capacity = team_f.team_sea_transport_capacity(block.team)
	# 	trips_allowed = math.floor(365/float(journey_time))
	# 	
	# 	if (amount > transport_capacity) and (amount*2 > transport_capacity * trips_allowed):
	# 		results	= "%s could not be relocated from %s to %s amount of overseas transport available is too small" % (amount, the_from_city.city_name, the_to_city.city_name)
	# 		return results, queries, order_cost
	
	# _city_size
	if move_type == "Civilians":
		if from_city.population < amount:
			if debug:
				results['debug'].append("Failed at _city_size_civilians")
				results['debug'].append("Population: %s" % from_city.population)
				results['debug'].append("Slaves: %s" % from_city.slaves)
				results['debug'].append("Amount: %s" % amount)
			return order_block.fail(results, "the city is not big enough to send that many civilians")
		
		from_city.population -= amount
		to_city.population += amount
	elif move_type == "Slaves":
		if from_city.slaves < amount:
			if debug:
				results['debug'].append("Failed at _city_size_slaves")
				results['debug'].append("Population: %s" % from_city.population)
				results['debug'].append("Slaves: %s" % from_city.slaves)
				results['debug'].append("Amount: %s" % amount)
			return order_block.fail(results, "the city is not big enough to send that many slaves")
		
		from_city.slaves -= amount
		to_city.slaves += amount
	
	results['queries'].extend(city_f.make_relocation_query(from_city.id, to_city.id, amount, move_type))
	results['results'].append("%s %s were successfully moved from %s to %s" % (amount, move_type, from_city.name, to_city.name))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	return order_block.success(results)

class Relocation_block (order_block.Order_block):
	background_colour	= "#EEFFEE"
	border_colour		= "#00AA00"
	
	functions = (
		(re.compile(r'(?i)Relocate (?P<amount>[0-9,]*) (?P<type>civilians|slaves) from (?P<from_city>.*?) to (?P<to_city>.*?)$'),
			relocation_order),
	)
	
	def __init__(self):
		super(Relocation_block, self).__init__()
	
	# def common_mistakes(self, text):
	# 	"""Removes common spelling mistakes"""
	# 	for regex, replacement in replacements:
	# 		text = regex.sub(replacement, text)		
	# 	
	# 	return text