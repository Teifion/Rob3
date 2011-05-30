import re
import math
from classes import order_block, res_dict
from queries import mapper_q
from functions import city_f, path_f
from rules import map_data, map_resources
from lists import resource_list

# replacements = (
# 	(re.compile(r'(?i)mundane academy'), 	'university'),
# 	(re.compile(r'(?i)magical academy'),	'academy'),
# 	(re.compile(r'(?i)airshipyard'),		'shipyard'),
# 	(re.compile(r'(?i)academy of runic'),	'academy of runes'),
# 	(re.compile(r'(?i)fortified walls'),	'fortifications'),
# 	(re.compile(r'(?i) port'),				'shipyard'),
# 	
# 	# (re.compile(r'(?i)([0-9\.]{1,4}) ?k '),						r'\1k'),
# 	(re.compile(r'(?i)([0-9\.]{1,4}) fortifications'),			r'\1k Fortifications'),
# 	(re.compile(r'(?i)([0-9\.]{1,4}) walls'),					r'\1k Walls'),
# 	
# 	# (re.compile(r'(?i)Fortifications for ([0-9\.]{1,4})k?'),	r'\1k Fortifications'),
# 	# (re.compile(r'(?i)Walls for ([0-9\.]{1,4})k?'),				r'\1 walls'),
# )

def prospective_founding_order(the_line, groups, debug=False):
	results = founding_order(the_line, groups, debug)
	if not the_line.block.msn_order:
		return order_block.fail(results, "Command not valid in live mode")
	
	results['queries'] = []
	results['cost'] = ""
	
	if results['success']:
		# X and Y
		x, y = groups['location'].split(',')
		x = int(x.strip())
		y = int(y.strip())
		
		# Header
		results['results'] = ["[b]Founded '%s' successfully[/b]" % groups['city_name']]
		
		# Terrain
		terrain = mapper_q.get_terrain(the_line.the_world.cursor, x, y)
		results['results'].append("Terrain: %s" % map_data.terrain[terrain].title())
		
		# Supplies
		supplies = []
		icon_size = map_data.map_image_size(int(groups['size']))/4
		for r, rx, ry in map_resources.data_list:
			dist = path_f.pythagoras((rx, ry), (x, y))
			if dist < icon_size:
				supplies.append(r)
		
		if len(supplies) > 1:
			results['results'].append("Supplies: %s" % ", ".join([resource_list.data_dict[s].name for s in supplies]))
		elif len(supplies) == 1:
			results['results'].append("Supply: %s" % ", ".join([resource_list.data_dict[s].name for s in supplies]))
		
		return results
	else:
		return results
	

def founding_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	all_cities				= the_line.the_world.cities()
	city_dict				= the_line.the_world.cities_from_team(the_line.block.team)
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	team_dict				= the_line.the_world.teams()
	
	dead_city = -1
	
	# Handles
	new_city_name = groups['city_name']
	supply_list_s = groups['city_list']
	size = int(groups['size'].replace(',', ''))
	if groups['city_type'] != None:
		city_type = groups['city_type'].lower().strip()
	else:
		city_type = None
	
	is_port, is_nomadic = False, False
	
	if city_type == "port":
		is_port = True
	elif city_type == "nomadic":
		is_nomadic = True
	
	# Get the location from the string
	try:
		x, y = groups['location'].split(',')
		x = int(x.strip())
		y = int(y.strip())
		terrain = mapper_q.get_terrain(the_line.the_world.cursor, x, y)
		
	except Exception as e:
		return order_block.fail(results, "%s was not founded because trying to read the location produced an error: %s" % (groups['city_name'], e.args[0]))
	
	# Rule checks
	#------------------------
	results = order_block.default_line_results(the_line, "%s could not be founded at %s because" % (new_city_name, str((x, y))))
	
	# You can't build on water!
	if map_data.terrain[terrain] in ('water', 'lake', 'XYZ_1', 'XYZ_2', 'XYZ_3'):
		return order_block.fail(results, "you cannot build on that terrain (%s)" % map_data.terrain[terrain])
	
	# Does it already exist?
	if new_city_name.lower() in cities_lookup:
		existing_city = all_cities[cities_lookup[new_city_name.lower()]]
		
		try:
			if not existing_city.dead:
				return order_block.fail(results, "%s already exists (controlled by %s)" % (new_city_name, team_dict[existing_city.team].name))
			else:
				# Currently all dead cities need a GM to act
				return order_block.fail(results, "%s already exists as a dead city, contact Teifion to to fix it (ID:%d)" % (new_city_name, cities_lookup[new_city_name.lower()]))
				
				
				if all_cities[cities_lookup[new_city_name.lower()]].team == the_team.id:
					dead_city = cities_lookup[new_city_name.lower()]
				else:
					return order_block.fail(results, "%s already exists as a dead city, contact Teifion to to fix it (ID:%d)" % (new_city_name, cities_lookup[new_city_name.lower()]))
		except Exception as e:
			print(new_city_name.lower())
			raise
	
	# Is it allowed to be a port?
	if is_port:
		if map_data.terrain[terrain] != "shore":
			is_port = False
			if mapper_q.get_terrain(the_line.the_world.cursor, x-10, y-10) == 0: is_port = True
			if mapper_q.get_terrain(the_line.the_world.cursor, x-10, y) == 0: is_port = True
			if mapper_q.get_terrain(the_line.the_world.cursor, x-10, y+10) == 0: is_port = True
			
			if mapper_q.get_terrain(the_line.the_world.cursor, x, y-10) == 0: is_port = True
			if mapper_q.get_terrain(the_line.the_world.cursor, x, y+10) == 0: is_port = True
			
			if mapper_q.get_terrain(the_line.the_world.cursor, x+10, y-10) == 0: is_port = True
			if mapper_q.get_terrain(the_line.the_world.cursor, x+10, y) == 0: is_port = True
			if mapper_q.get_terrain(the_line.the_world.cursor, x+10, y+10) == 0: is_port = True
		
		if not is_port:
			return order_block.fail(results, "%s that is not next to the sea" % str((x, y)))
	
	# Supply list
	supply_dict_raw = {}
	if supply_list_s != None:
		supply_list_s = supply_list_s.split(",")
		for s in supply_list_s:
			sls = s.lower().strip()
			if sls in cities_lookup:
				supply_dict_raw[cities_lookup[sls]] = 9999999
	else:
		for c in city_dict.keys():
			supply_dict_raw[c] = 9999999
	
	# print("")
	# print(supply_dict_raw)
	
	if debug:
		results['debug'].append("First pass:")
	
	# # Now we check each of the cities in the supply list
	new_city_continent = path_f.get_continent(the_line.the_world.cursor, (x, y))
	supply_dict = {}
	for c in supply_dict_raw.keys():
		if c not in city_dict:
			if debug:
				results['debug'].append("City ID %d was not in city_dict" % c)
			return order_block.fail(results, "One or more of the cities used as a source were not valid (ID: %d)" % c)

		the_city = city_dict[c]
		if the_city.dead > 0: continue
		
		if new_city_continent != path_f.get_continent(the_line.the_world.cursor, (the_city.x, the_city.y)):
			if not is_port or not the_city.port:
				if len(supply_dict_raw) == 1:
					if debug:
						results['debug'].append("Continent of target: %s" % new_city_continent)
						results['debug'].append("Continent of supply: %s" % path_f.get_continent(the_line.the_world.cursor, (the_city.x, the_city.y)))
						
					if not the_city.port and not is_port:
						return order_block.fail(results, "the city you supplied is on another contintent and neither this city nor the new one are a port")
					elif not the_city.port:
						return order_block.fail(results, "the city you supplied is on another contintent and the existing city is not a port")
					elif not is_port:
						return order_block.fail(results, "the city you supplied is on another contintent and the new city is not a port")
					else:
						raise Exception("No handle")	
				
				if not is_port:
					if debug:
						results['debug'].append("Skipped %s due to the new city being on another landmass and not a port" % (city_dict[c].name))
				elif not the_city.port:
					if debug:
						results['debug'].append("Skipped %s due to it not being a port" % (city_dict[c].name))
				
				# We need both to be a port if they're on different landmasses
				continue
			
			path_data = path_f.path(the_line.the_world.cursor, [(the_city.x, the_city.y), (x, y)],
				move_speed="Sailing", move_type="Sail")
			supply_dict[c] = path_data.time_cost
			if debug:
				results['debug'].append("Added %s to dict with %s (sailing)" % (city_dict[c].name, int(path_data.time_cost)))
			
		else:# Same continent
			path_data = path_f.path(the_line.the_world.cursor, [(the_city.x, the_city.y), (x, y)],
				move_speed="Colonists", move_type="Colonists")
			supply_dict[c] = path_data.time_cost
			if debug:
				results['debug'].append("Added %s to dict with %s (walking)" % (city_dict[c].name, int(path_data.time_cost)))
		
		# Work out if it's in range
		if supply_dict[c] > 182:# 6 months
			if debug:
				results['debug'].append("Removed %s from dict with, it took %s" % (city_dict[c].name, int(supply_dict[c])))
			del(supply_dict[c])
	
	if debug:
		results['debug'].append("\nCities in range:")
		for k, v in supply_dict.items():
			results['debug'].append("%s has %s to offer (travel time %s)" % (city_dict[k].name, city_dict[k].population, int(v)))
		
		# results['debug'].append("")
	
	cities_changed = True
	while cities_changed:
		if len(supply_dict) < 1:
			if groups['city_list'] == None:
				return order_block.fail(results, "the cities able to reach the new location were too far away or not large enough")
			else:
				return order_block.fail(results, "the cities able to reach the new location from the list provided were too far away or not large enough")
		
		cities_to_delete	= []
		cities_changed		= False
		
		city_count			= len(supply_dict)
		amount_per_city		= math.ceil(size/city_count)
		
		for c in supply_dict.keys():
			# Check the city size
			if city_dict[c].population < amount_per_city:
				# if debug: print("deleted %s (%s) pop:%s < %s" % (c, city_dict[c].name, supply_dict[c], amount_per_city))
				cities_to_delete.append(c)
				cities_changed = True
		
		for c in cities_to_delete:
			del(supply_dict[c])
	
	# Get cost
	results['cost'] = res_dict.Res_dict("Materials:%s" % (size/1000))
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability and "Materials" not in the_team.overbudget:
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Queries
	results['queries'].append("-- Founding %s at %s for team:%d" % (new_city_name, str((x, y)), the_team.id))
	if dead_city > 1: results['queries'].extend(city_f.make_remove_dead_city_query(dead_city))
	results['queries'].extend(city_f.make_founding_query(
		the_team.id, new_city_name, (x, y), is_port, is_nomadic, size, supply_dict.keys())
	)
	
	# Apply cost
	for c in supply_dict.keys():
		city_dict[c].population -= (size/len(supply_dict))
	
	the_team.resources -= results['cost'].discrete()
	
	# Result
	results['results'].append("%s was successfully founded at %s at a size of %s" % (new_city_name, str((x, y)), size))
	
	return order_block.success(results)

class Founding_block (order_block.Order_block):
	background_colour	= "#EEEEFF"
	border_colour		= "#0000AA"
	
	functions = (
		(re.compile(r'(?i)\?(?P<city_name>.*?) \((?P<location>.*?)\) ?(?P<city_type>port|nomadic)? (?P<size>[0-9,]*)(?P<city_list> .*?)?$'),
			prospective_founding_order),
		
		(re.compile(r'(?i)(?P<city_name>.*?) \((?P<location>.*?)\) ?(?P<city_type>port|nomadic)? (?P<size>[0-9,]*)(?P<city_list> .*?)?$'),
			founding_order),
	)
	
	def __init__(self):
		super(Founding_block, self).__init__()
	
	# def common_mistakes(self, text):
	# 	"""Removes common spelling mistakes"""
	# 	for regex, replacement in replacements:
	# 		text = regex.sub(replacement, text)		
	# 	
	# 	return text