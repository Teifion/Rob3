import re
from classes import order_block, res_dict
from functions import building_f, wonder_f
from rules import city_rules, map_data

replacements = (
	(re.compile(r'(?i)mundane academy'), 	'university'),
	(re.compile(r'(?i)magical academy'),	'academy'),
	(re.compile(r'(?i)airshipyard'),		'shipyard'),
	(re.compile(r'(?i)academy of runic'),	'academy of runes'),
	(re.compile(r'(?i)fortified walls'),	'fortifications'),
	(re.compile(r'(?i) port'),				'shipyard'),
	
	(re.compile(r'(?i)fortifacations'),		'fortifications'),
	
	# (re.compile(r'(?i)([0-9\.]{1,4}) ?k '),						r'\1k'),
	(re.compile(r'(?i)([0-9\.]{1,4}) fortifications'),			r'\1k Fortifications'),
	(re.compile(r'(?i)([0-9\.]{1,4}) walls'),					r'\1k Walls'),
	
	# (re.compile(r'(?i)Fortifications for ([0-9\.]{1,4})k?'),	r'\1k Fortifications'),
	# (re.compile(r'(?i)Walls for ([0-9\.]{1,4})k?'),				r'\1 walls'),
)


def building_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	building_dict			= the_line.the_world.buildings()
	city_dict				= the_line.the_world.cities()
	
	buildings_lookup		= the_line.the_world.buildings_lookup(lower=True)
	buildings_requirements	= the_line.the_world.building_requirements()
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	
	# DB checks
	#------------------------
	# _find_building
	if groups['building'].lower() not in buildings_lookup:
		if debug:
			results['debug'].append("Failed at _find_building")
		return order_block.fail(results, "there is no building by the name of '%s'" % groups['building'])
	else:
		the_building = building_dict[buildings_lookup[groups['building'].lower()]]
	
	# _find_city
	if groups['city'].lower() not in cities_lookup:
		if debug:
			results['debug'].append("Failed at _find_city")
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['city'])
	else:
		the_city = city_dict[cities_lookup[groups['city'].lower()]]
	
	# _dead_city
	if the_city.dead > 0:
		if debug:
			results['debug'].append("Failed at _dead_city")
		return order_block.fail(results, "there is no living city by the name of '%s' (found id of %d)" % (groups['city'], the_city.id))
	
	# if the_line.the_world._cities[974].buildings != {'0':None}:
	# 	print(the_line.content, the_line.block.team, the_line.block.title_name)
	
	# if the_city.id == 974:
	# 	print("")
	# 	print(the_line.content)
	# 	
	# 	# for k, v in city_dict.items():
	# 	# 	if not v.dead:
	# 	# 		print(v.name, v.buildings)
	# 	
	# 	print("XXYYZZ")
	# 	the_line.the_world.cursor.execute("ROLLBACK")
	# 	the_line.the_world.cursor.execute("ROLLBACK")
	# 	exit()
	
	# Rule checks
	#------------------------
	results = order_block.default_line_results(the_line, "%s could not be built at %s because" % (the_building.name, the_city.name))
	
	# _swamp
	if the_city.terrain == map_data.terrain.index("swamp"):
		if the_building.wall or the_building.name == "Castle":
			if debug:
				results['debug'].append("Failed at _swamp")
			return order_block.fail(results, "%s is on a swamp" % the_city.name)
	
	# _ownership
	if the_city.team != the_line.block.team:
		if debug:
			results['debug'].append("Failed at _ownership")
		return order_block.fail(results, "%s is not your city" % the_city.name)
	
	# _nomadic
	if the_city.nomadic:
		if debug:
			results['debug'].append("Failed at _nomadic")
		return order_block.fail(results, "%s is nomadic" % the_city.name)
	
	amount		= the_city.buildings_amount.get(the_building.id, 0)
	completion	= the_city.buildings.get(the_building.id, 0)
	
	# _wall_points
	if the_building.wall and the_city.wall_points_used >= 1:
		if debug:
			results['debug'].append("Failed at _wall_points")
		return order_block.fail(results, "%s is already constructing a wall this year" % the_city.name)
	
	# _economy_points
	if the_building.economy and the_city.economy_points_used >= 1:
		if debug:
			results['debug'].append("Failed at _economy_points")
		return order_block.fail(results, "%s is already constructing an economic building this year" % the_city.name)
	
	# _building_points
	if not the_building.wall and not the_building.economy and the_city.building_points_used >= 1:
		if debug:
			results['debug'].append("Failed at _building_points")
		return order_block.fail(results, "%s is already constructing a building this year" % the_city.name)
	
	# _build_limit
	if completion == 0 and the_building.limit_per_city > 0:
		instances = amount
		
		# Is it used for an upgrade?
		if the_building.id in buildings_requirements:
			
			for b in buildings_requirements[the_building.id]:
				if b in the_city.buildings_amount:
					instances += the_city.buildings_amount[b]
				
				if b in the_city.buildings and the_city.buildings[b] > 0:
					instances += 1
		
		if instances >= the_building.limit_per_city:
			if debug:
				results['debug'].append("Failed at _build_limit")
			
			return order_block.fail(results, "you have reached the limit allowed in one city")
	
	# _upgrade_requirements
	if completion == 0 and the_building.upgrades > -1:
		if the_city.buildings_amount.get(the_building.upgrades, 0) < 1:
			if debug:
				results['debug'].append("Failed at _upgrade_requirements")
				results['debug'].append("Required {building} (id: {id})".format(
					building=building_dict[the_building.upgrades].name,
					id=the_building.upgrades)
				)
				results['debug'].append("the_city.buildings_amount: %s" % str(the_city.buildings_amount))
				results['debug'].append("the_city.buildings: %s" % str(the_city.buildings))
			
			return order_block.fail(results, "the required building (%s) is not complete there" % building_dict[the_building.upgrades].name)
	
	# Get cost
	results['cost'] = res_dict.Res_dict(the_building.cost_per_turn)
	if completion == 0:
		results['cost'] += res_dict.Res_dict(the_building.cost_up_front)
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability:
		if debug:
			results['debug'].append("Failed at _affordability")
			results['debug'].append("Cost: %s" % str(results['cost']))
			results['debug'].append("Team resources: %s" % str(the_team.resources))
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Check we've got a DB row ready to update
	if completion == 0 and amount == 0:
		the_line.try_query(building_f.check_row_exists(building_id=the_building.id, city_id=the_city.id))
	
	# Completion
	if the_team.resources.get("Stone") > 0:
		new_completion = completion + 100
	else:
		new_completion = completion + 50
	
	new_completion = min(new_completion, the_building.build_time)
	
	# Completion percentage
	completion_percentage = int(100 * (new_completion/the_building.build_time))
	completion_percentage = min(completion_percentage, 100)
	
	# Queries
	results['queries'].append("-- Building %s at %s for team:%d" % (the_building.name, the_city.name, the_team.id))
	results['queries'].extend(building_f.completion_query(the_city, the_building, new_completion))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	# Result
	results['results'].append("%s is %s%% of the way through it's %s" % (the_city.name, completion_percentage, the_building.name))
	
	# Update city points
	if the_building.wall:	the_city.wall_points_used += 1
	else:					the_city.building_points_used += 1	
	
	return order_block.success(results)


def wonder_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	wonder_dict				= the_line.the_world.wonders()
	city_dict				= the_line.the_world.cities()
	
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	
	# DB checks
	#------------------------
	# Can we find the city?
	if groups['assist_city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['wonder_city'])
	else:
		assist_city = city_dict[cities_lookup[groups['assist_city'].lower()]]
	
	# Can we find the city?
	if groups['wonder_city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['wonder_city'])
	else:
		wonder_city = city_dict[cities_lookup[groups['wonder_city'].lower()]]
	
	# Rule checks
	#------------------------
	results = order_block.default_line_results(the_line, "%s could not be assist %s because" % (assist_city.name, wonder_city.name))
	
	# Our cities?
	if assist_city.team != the_team.id:
		return order_block.fail(results, "%s is not your city" % assist_city.name)
	
	if wonder_city.team != the_team.id:
		return order_block.fail(results, "%s is not your city" % wonder_city.name)
	
	# Nomads can't help build
	if assist_city.nomadic:
		return order_block.fail(results, "%s is nomadic" % assist_city.name)
	
	# Dead cities can't build
	if assist_city.dead > 0:
		return order_block.fail(results, "%s is dead" % assist_city.name)
	
	if wonder_city.dead > 0:
		return order_block.fail(results, "%s is dead" % wonder_city.name)
	
	# Check for the wonder
	the_wonder = None
	for w, tw in wonder_dict.items():
		if tw.city == wonder_city.id:
			the_wonder = tw
	
	# Was a wonder found?
	if the_wonder == None:
		return order_block.fail(results, "there is no wonder in %s" % wonder_city.name)
	
	# Is the wonder already completed
	if the_wonder.completed:
		return order_block.fail(results, "%s has already completed it's wonder" % wonder_city.name)
	
	# Does the city have any points left?
	if assist_city.wall_points_used >= 1:
		return order_block.fail(results, "%s has used up it's wall construction point already" % assist_city.name)
	
	if assist_city.building_points_used >= 1:
		return order_block.fail(results, "%s has used up it's normal construction point already" % assist_city.name)
	
	# Get build rate
	build_rate = city_rules.wonder_build_rate(assist_city, wonder_city)
	if the_team.resources.get("Stone") < 1:
		build_rate *= 0.5
	
	if build_rate < 1:
		return order_block.fail(results, "%s is too small or too far away to assist" % assist_city.name)
	
	# Cost
	if the_wonder.completion + build_rate > the_wonder.point_cost:
		build_rate = the_wonder.point_cost - the_wonder.completion
	
	material_per_point = the_wonder.material_cost/the_wonder.point_cost
	results['cost'] = res_dict.Res_dict("Materials:%s" % (material_per_point*build_rate))
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	if not affordability:
		return order_block.fail_cost(results)
	
	
	# INSERTION/UPDATE
	#------------------------
	# First queries are cost
	the_wonder.completion += build_rate
	if the_wonder.completion >= the_wonder.point_cost:
		the_wonder.completed = True
	
	results['queries'].append("-- Wonder %s assisting %s for team:%d" % (assist_city.name, wonder_city.name, the_team.id))
	results['queries'].extend(wonder_f.completion_query(the_wonder.id, the_wonder.completion))
	
	# Work out results
	if the_wonder.completion >= the_wonder.point_cost:
		results['results'].append("%s assisted %s with %s construction points, the wonder is now complete" % (assist_city.name, wonder_city.name, build_rate))
	else:
		results['results'].append("%s assisted %s with %s construction points" % (assist_city.name, wonder_city.name, build_rate))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
		
	# Update city points
	assist_city.wall_points_used		+= 1
	assist_city.building_points_used	+= 1	
	
	return order_block.success(results)
	

class Construction_block (order_block.Order_block):
	background_colour	= "#CCCCCC"
	border_colour		= "#000000"
	
	functions = (
		(re.compile(r'(?i)(Build|Construct) (?P<building>.*?) (at|in) (?P<city>.*?)$'),	
			building_order),
		
		(re.compile(r'(?i)(?P<assist_city>.*?) assist wonder at (?P<wonder_city>.*?)$'),	
			wonder_order),
	)
	
	# def __init__(self):
	# 	super(Construction_block, self).__init__()
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text