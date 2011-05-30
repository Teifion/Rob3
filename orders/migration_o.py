import re
import math
from classes import order_block
from queries import mapper_q
from functions import city_f, path_f
from rules import map_data

def migration_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	city_dict		= the_line.the_world.cities_from_team(the_line.block.team)
	cities_lookup	= the_line.the_world.cities_lookup(lower=True)
	
	# Can we find the city?
	if groups['city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['city'])
	else:
		the_city = city_dict[cities_lookup[groups['city'].lower()]]
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Target
	try:
		target = (int(groups['x']), int(groups['y']))
	except Exception as e:
		return order_block.fail(results, "%s was not moved because trying to read the target location produced an error: %s" % (groups['city_name'], e.args[0]))
	
	# Default result
	results = order_block.default_line_results(the_line, "%s could not be moved to %s because" % (the_city.name, str(target)))
	
	# First we check it's on the same continent, if it's not you can't migrate there
	our_continent		= path_f.get_continent(the_line.the_world.cursor, (the_city.x, the_city.y))
	target_continent	= path_f.get_continent(the_line.the_world.cursor, target)
	
	# Before we path, lets check that they can walk there
	if our_continent != target_continent:
		if target_continent == None:# or target_continent == -1:
			return order_block.fail(results, "the target is the ocean")
		else:
			return order_block.fail(results, "the target is on a different island")
	
	terrain = mapper_q.get_terrain(the_line.the_world.cursor, target[0], target[1])
	if map_data.terrain[terrain] in ('lake', 'XYZ_1', 'XYZ_2', 'XYZ_3'):
		return order_block.fail(results, "you cannot migrate to that terrain (%s)" % map_data.terrain[terrain])
	
	# Pathing time!
	journey = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=[(the_city.x, the_city.y), target],
		move_speed="Nomads",
		move_type="Nomads")
	
	# Does this take more than a year?
	travel_time = journey.time_cost
	actual_target = target
	
	current_time = 0
	if journey.time_cost > 365:
		for s in journey.steps:
			if current_time + s['time_cost'] <= 365:
				actual_target = s['tile']
				current_time += s['time_cost']
		
		travel_time = current_time
	
	if actual_target != target:
		results['results'].append("%s migrated to %s, to migrate to %s will take another %s days" % (the_city.name, str(actual_target), str(target), (journey.time_cost - travel_time)))
	else:
		results['results'].append("%s migrated to %s" % (the_city.name, str(target)))
	
	# Get the query to make it happen
	results['queries'].extend(city_f.make_migration_query(the_city.id, actual_target, travel_time))
	
	return order_block.success(results)

class Migration_block (order_block.Order_block):
	background_colour	= "#EEFFEE"
	border_colour		= "#00AA00"
	
	functions = (
		(re.compile(r'(?i)Move (?P<city>.*?) (?:towards|to) (?P<x>-?[0-9]*), ?(?P<y>-?[0-9]*)$'),
			migration_order),
	)
	
	def __init__(self):
		super(Migration_block, self).__init__()
	
	# def common_mistakes(self, text):
	# 	"""Removes common spelling mistakes"""
	# 	for regex, replacement in replacements:
	# 		text = regex.sub(replacement, text)		
	# 	
	# 	return text