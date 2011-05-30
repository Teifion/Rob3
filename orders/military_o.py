import math
import re
from classes import order_block, res_dict, unit
from functions import army_f, squad_f, city_f, unit_f
from queries import squad_q, army_q, unit_q
from rules import unit_rules, military_rules

replacements = (
	(re.compile(r'(?i)(High|Mid|Low) mage'), 	r'\1 tier mage'),
	(re.compile(r'(?i)(High|Mid|Low) tier mages'),	r'\1 tier mage'),
	
	# With the new lookup method this probably isn't needed
	# (re.compile(r'Garrison'), 'garrison'),
)

def create_army_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	the_team		= the_line.the_world.teams()[the_line.block.team]
	
	# # Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		# return order_block.fail(results, "could not find an army by the name of '%s'" % (groups['army']))
		pass
		the_army = None
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	x, y = int(groups['x']), int(groups['y'])
	
	# Check to see if the army exists
	if the_army == None:
		# Input a new army
		army_id = army_q.create_empty_army(the_line.the_world.cursor, groups['army'], the_line.block.team, groups['x'], groups['y'])
		
		# Update caches
		army_dict[army_id] = army_q.get_one_army(the_line.the_world.cursor, army_id)
		the_army = army_dict[army_id]
		the_line.the_world._armies_lookup_from_team[the_team.id][the_army.name.lower()] = army_id
	
	# Right, time to run recruitment
	results['results'].append("Created the army %s at %s" % (the_army.name, str((the_army.x, the_army.y))))
	results['line_cache'] = {"army":the_army.id}
	return order_block.success(results)

def select_army_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	armies_lookup = the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		army_id = armies_lookup[groups['army'].lower()]
	
	results['results'].append("Selected '%s'" % (groups['army']))
	results['line_cache'] = {"army":army_id}
	return order_block.success(results)
	
def relocate_army_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	new_location = (int(groups['x']), int(groups['y']))
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	results['queries'].extend(army_f.make_relocation_query(the_army.id, new_location))
	results['results'] = ["%s relocated to %s" % (the_army.name, str(new_location))]
	return order_block.success(results)

def rename_army_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	# Default result
	results = order_block.default_line_results(the_line, "%s could not be renamed to %s because" % (the_army.name, groups['new_name']))
	
	# Lets check this army doesn't exist already
	if groups['new_name'].lower() in armies_lookup:
		return order_block.fail(results, "an army called %s already exists" % groups['new_name'])
	
	# Ensure they're not trying to make a garrison
	if "garrison" in groups['new_name'].lower():
		return order_block.fail(results, "it sounds like you are trying to make a garrison, these are created automatically")
	
	results['queries'].extend(army_f.make_rename_query(the_army.id, groups['new_name']))
	results['results'].append("%s renamed to %s" % (the_army.name, groups['new_name']))
	
	return order_block.success(results)

def delete_army_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	# Default result
	results = order_block.default_line_results(the_line, "%s could not be deleted because" % (the_army.name))
	
	# More handles
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(the_army.id)# We're not gonna use this the normal way
	
	# Are the squads in it empty?
	for squad_name, squad_id in squads_lookup.items():
		results['queries'].extend(squad_f.make_delete_query(squad_id))
		
		if squad_dict[squad_id].amount > 0:
			return order_block.fail(results, "one of it's squads (%s) is not empty" % squad_dict[squad_id].name)
	
	results['queries'].extend(army_f.make_delete_query(the_army.id))
	results['results'].append("The army '%s' was deleted" % the_army.name)
	
	return order_block.success(results)

def create_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "could not find an army by the name of '%s'" % (groups['army']))
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(the_army.id)
	
	# Can we find the squad?
	if groups['squad'].lower() not in squads_lookup:
		the_squad = None
	else:
		the_squad = squad_dict[squads_lookup[groups['squad'].lower()]]
	
	# Check amount
	try:
		amount = int(groups['amount'])
	except Exception as e:
		return order_block.fail(results, "the amount '%s' could not be converted into a number" % groups['amount'])
	
	# Unit type
	unit_dict			= the_line.the_world.units()
	units_lookup		= the_line.the_world.units_lookup_from_team(the_line.block.team)
	all_units_lookup	= the_line.the_world.units_lookup_from_team(0)
	
	if groups['unit'].lower() not in units_lookup:
		if groups['unit'].lower() not in all_units_lookup:
			return order_block.fail(results, "no unit by the name of '%s' could be found" % (groups['unit']))
		else:
			the_unit = unit_dict[all_units_lookup[groups['unit'].lower()]]
	else:
		the_unit = unit_dict[units_lookup[groups['unit'].lower()]]
	
	# Check to see if the squad exists
	if the_squad == None:
		# Input a new squad
		squad_id = squad_q.create_empty_squad(the_line.the_world.cursor, groups['squad'], the_army.id, the_unit.id, the_line.block.team)
		
		# Update caches
		squad_dict[squad_id] = squad_q.get_one_squad(the_line.the_world.cursor, squad_id)
		the_squad = squad_dict[squad_id]
		if the_army.id not in the_line.the_world._squads_lookup_from_army:
			the_line.the_world._squads_lookup_from_army[the_army.id] = {}
		the_line.the_world._squads_lookup_from_army[the_army.id][the_squad.name.lower()] = squad_id
		# the_line.the_world.squads_lookup_from_army(the_army.id)# We're not gonna use this the normal way
	else:
		if the_squad.unit != the_unit.id:
			return order_block.fail(results, "the squad %s in %s already exists with a unit type of %s" % (the_squad.name, the_army.name, unit_dict[the_squad.unit].name))
	
	# If no amount then it's a template
	if amount == 0:
		results['input_response'] = "Created empty squad %s in %s of type %s" % (groups['squad'], groups['army'], groups['unit'])
		return results
	
	# Right, time to run recruitment
	return _recruit(the_line, the_squad, the_army, amount, debug)

def select_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	# Check we have an army to select from
	army_id = -1
	if "army" in the_line.block.line_cache:
		army_id = the_line.block.line_cache["army"]
	
	if army_id < 1:
		return order_block.fail(results, "No army has been selected so no squad can be found")
	
	# Cache it for the next line
	results['line_cache'] = {"army":army_id}
	
	the_army		= the_line.the_world.armies()[army_id]
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(army_id)
	
	# Can we find the squad?
	if groups['squad'].lower() not in squads_lookup:
		return order_block.fail(results, "there is no squad by the name of '%s' in %s" % (groups['squad'], the_army.name))
	else:
		the_squad = squad_dict[squads_lookup[groups['squad'].lower()]]
	
	# Check amount
	try:
		amount = int(groups['amount'])
	except Exception as e:
		return order_block.fail(results, "the amount '%s' could not be converted into a number" % groups['amount'])
	
	if amount < 0:
		groups['amount'] = str(-amount)
		return disband_squad_order(the_line, groups, debug=debug)
	
	# Right, time to run recruitment
	results = _recruit(the_line, the_squad, the_army, amount, debug)
	results['line_cache'] = {"army":army_id}
	return results


def _recruit(the_line, the_squad, the_army, amount, debug):
	# if not debug:
	# 	raise Exception("No debug")
	
	results = order_block.default_line_results(the_line)
	results['base_failure'] = "The squad %s into %s could not be recruited to because " % (the_squad.name, the_army.name)
	
	# Check amount
	if amount < 1:
		return order_block.fail(results, "a number smaller than 1 was supplied" % groups['amount'])
	
	# Handles
	city_dict		= the_line.the_world.cities_from_team(the_line.block.team)
	unit_dict		= the_line.the_world.units()
	the_team		= the_line.the_world.teams()[the_line.block.team]
	
	the_unit = unit_dict[the_squad.unit]
	
	#	AVAILABLE
	#------------------------
	if not the_unit.available:
		return order_block.fail(results, "the unit (%s) or it's equipment is not available" % (the_unit.name))
	
	# _distance_from_base
	if the_army.distance > military_rules.non_recruitment_distance:
		pass
		# if debug:
		# 	results['debug'].append("Failed at _distance_from_base")
		# return order_block.fail(results, "the distance from the base of operations of this army is too large")
	
	#	COST
	#------------------------
	if the_team.resources.get("Iron") > 0:
		# results['cost'] = the_unit.get_cost(the_world=the_line.the_world)['iron_cost']
		results['cost'] = the_unit.get_cost(the_world=the_line.the_world)['material_cost']
	else:
		results['cost'] = the_unit.get_cost(the_world=the_line.the_world)['iron_cost']
		# results['cost'] = the_unit.get_cost(the_world=the_line.the_world)['material_cost']
	
	if unit.categories[the_unit.type_cat] != "Ship" and \
		unit.categories[the_unit.type_cat] != "Airship":
		results['cost'] *= (amount/1000)
	else:
		results['cost'] *= amount
	
	man_amount = amount * the_unit.crew
	
	# Some units can get special reductions
	results['cost'] = unit_rules.unit_cost_override(the_line.the_world, the_unit, results['cost'], the_team)
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability and "Materials" not in the_team.overbudget:
		return order_block.fail_cost(results)
	
	#	INSERTION/UPDATE
	#------------------------
	# If there's no city defined, make sure the cities are all big enough
	supply_dict = {}
	for c_id, c in city_dict.items():
		if c.population > 5000:
			supply_dict[c_id] = True
			
			# if debug:
			# 	results['debug'].append("Added %s to supply dict with a population of %s" % (c.name, c.population))
	
	# Now to make sure no city will drop below a certain size
	# _supply_dict
	cities_changed = True
	if debug:
		results['debug'].append("Initial supply dict %s" % supply_dict)
	
	while cities_changed:
		if len(supply_dict) < 1:
			if debug:
				results['debug'].append("Failed at _supply_dict")
			return order_block.fail(results, "no cities could supply the required population")
		
		cities_to_delete	= []
		cities_changed		= False
		
		city_count			= len(supply_dict)
		amount_per_city		= math.ceil(amount/city_count)
		
		for c in supply_dict.keys():
			# Check the city size
			if city_dict[c].population < amount_per_city:
				if debug:
					results['debug'].append("Remvoing %s from supply_dict because it's too small" % c)
				cities_to_delete.append(c)
				cities_changed = True
		
		for c in cities_to_delete:
			del(supply_dict[c])
	
	# First queries are cost
	results['queries'].append("-- Unit: %s %s" % (amount, the_unit.name))
	results['queries'].extend(squad_f.make_reinforcement_query(the_squad.id, amount))
	results['queries'].extend(city_f.make_recruitment_queries(man_amount, supply_dict.keys()))
	
	# Apply cost(s)
	the_team.resources -= results['cost'].discrete()
	for c in supply_dict.keys():
		city_dict[c].population -= amount/len(supply_dict)
	
	# Rules final call and returning of values
	if man_amount != amount:
		results['results'].append("Recruited %s %s (%s men) into %s in %s" % (amount, the_unit.name, man_amount, the_squad.name, the_army.name))
	else:
		results['results'].append("Recruited %s %s into %s in %s" % (amount, the_unit.name, the_squad.name, the_army.name))
	
	return order_block.success(results)

def delete_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	# More handles
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(the_army.id)
	
	# Can we find the squad?
	if groups['squad'].lower() not in squads_lookup:
		return order_block.fail(results, "there is no squad by the name of '%s' in '%s'" % (groups['squad'], the_army.name))
	else:
		the_squad = squad_dict[squads_lookup[groups['squad'].lower()]]
	
	# Default result
	results = order_block.default_line_results(the_line, "%s could not be deleted from %s because" % (the_squad.name, the_army.name))
	
	# Is the squad empty?
	if the_squad.amount > 0:
		return order_block.fail(results, "%s still has %s men in it" % (the_squad.name, the_squad.amount))
	
	results['queries'].extend(squad_f.make_delete_query(the_squad.id))
	results['results'].append("The squad '%s' was deleted" % the_squad.name)
	
	return order_block.success(results)

def disband_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	# Check we have an army to select from
	if "army" in the_line.block.line_cache:
		army_id = the_line.block.line_cache["army"]
		the_army = the_line.the_world.armies()[army_id]
	else:
		return order_block.fail(results, "No army has been selected so no squad can be selected")
	
	# More handles
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(army_id)
	
	try:
		amount = int(groups['amount'])
	except Exception as e:
		return order_block.fail(results, "the value '%s' could not be converted to an integer, how it got this far is beyond me" % (groups['amount']))
	
	# Can we find the squad?
	if groups['squad'].lower() not in squads_lookup:
		return order_block.fail(results, "there is no squad by the name of '%s' in '%s'" % (groups['squad'], the_army.name))
	else:
		the_squad = squad_dict[squads_lookup[groups['squad'].lower()]]
	
	# Default line
	results = order_block.default_line_results(the_line, "%s could not be disbanded from %s in %s because" % (groups['amount'], the_squad.name, the_army.name))
	
	# Check amount
	if amount < 1:
		return order_block.fail(results, "an ammount less than 1 was given")
	
	# Bounds enforcement
	amount = min(amount, the_squad.amount)
	
	# Handles/Aliases
	city_dict	= the_line.the_world.cities_from_team(the_line.block.team)
	the_unit	= the_line.the_world.units()[the_squad.unit]
	the_team	= the_line.the_world.teams()[the_line.block.team]
	
	#	SITUATIONAL
	#------------------------
	# Dead cities can't be the target, set it to no city instead
	city_list = []
	for c, the_city in city_dict.items():
		if the_city.dead < 1:
			city_list.append(c)
	
	# Cost
	results['cost'] = the_unit.get_cost(the_world=the_line.the_world)['material_cost']
	
	if unit.categories[the_unit.type_cat] != "Ship" and \
		unit.categories[the_unit.type_cat] != "Airship":
		results['cost'] *= amount/1000
	else:
		results['cost'] *= amount
	
	# Apply unit_rules to it
	results['cost'] = unit_rules.disband_cost(results['cost'])
		
	# First queries are cost
	results['queries'].append("-- Disbanding: %s %s" % (amount, the_unit.name))
	results['queries'].extend(squad_f.make_disband_query(amount=amount, squad_id=the_squad.id))
	results['queries'].extend(city_f.make_disbanding_queries(amount, city_list))
	results['results'].append("Disbanded %s of %s in %s" % (amount, the_squad.name, the_army.name))
	
	# Update squad
	the_squad.amount -= amount
	if the_squad.amount == 0:
		results['queries'].append("-- Deleting as a result of 0 size")
		results['queries'].extend(squad_f.make_delete_query(the_squad.id))
	
	the_team.resources -= results['cost'].discrete()
	results['line_cache'] = {"army":the_army.id}
	return order_block.success(results)

def rename_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	
	# Can we find the army?
	if groups['army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of '%s'" % groups['army'])
	else:
		the_army = army_dict[armies_lookup[groups['army'].lower()]]
	
	# More handles
	squad_dict		= the_line.the_world.squads()
	squads_lookup	= the_line.the_world.squads_lookup_from_army(the_army.id)
	
	# Can we find the army?
	if groups['squad'].lower() not in squads_lookup:
		return order_block.fail(results, "there is no squad by the name of '%s' in %s" % (groups['squad'], the_army.name))
	else:
		the_squad = squad_dict[squads_lookup[groups['squad'].lower()]]
	
	results['queries'].extend(squad_f.make_rename_query(the_squad.id, groups['new_name']))
	results['results'].append("%s renamed to %s" % (the_squad.name, groups['new_name']))
	
	return order_block.success(results)

def move_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	# Handles
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	the_team		= the_line.the_world.teams()[the_line.block.team]
	
	# Check we have an army to take from
	if groups['current_army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of %s" % (groups['current_army']))
	else:
		current_army = army_dict[armies_lookup[groups['current_army'].lower()]]
	
	# Check we have an army to send to
	if groups['new_army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of %s" % (groups['new_army']))
	else:
		new_army = army_dict[armies_lookup[groups['new_army'].lower()]]
	
	# Now to find squads
	squad_dict				= the_line.the_world.squads()
	current_squads_lookup	= the_line.the_world.squads_lookup_from_army(current_army.id)
	new_squads_lookup		= the_line.the_world.squads_lookup_from_army(new_army.id)
	
	# Check we have a squad to take from
	if groups['squad'].lower() not in current_squads_lookup:
		return order_block.fail(results, "there is no army by the squad of %s in %s" % (groups['squad'], groups['current_army']))
	else:
		current_squad = squad_dict[current_squads_lookup[groups['squad'].lower()]]
	
	# Does a squad of this name already exist in the other army?
	if groups['squad'].lower() in new_squads_lookup:
		return split_squad_order(the_line, {
			"first_army":	groups['current_army'],
			"second_army":	groups['new_army'],
			"first_squad":	groups['squad'],
			"second_squad":	groups['squad'],
			"amount":		current_squad.amount,
		})
	
	# Run it!
	results = order_block.default_line_results(the_line, "The squad %s from %s could not be moved to %s because" % (current_squad.name, current_army.name, new_army.name))
	
	results['queries'].append("-- Moving squad '%s' (ID:%d) from army '%s' (ID:%d) to army '%s' (ID:%d)" % (
		current_squad.name,
		current_squad.id,
		
		current_army.name,
		current_army.id,
		
		new_army.name,
		new_army.id,
	))
	results['queries'].extend(squad_f.make_squad_move_query(current_squad.id, new_army.id))
	results['results'] = ["%s moved from %s to %s" % (current_squad.name, current_army.name, new_army.name)]
	
	return order_block.success(results)

def split_squad_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	# Handles
	army_dict		= the_line.the_world.armies()
	armies_lookup	= the_line.the_world.armies_lookup_from_team(the_line.block.team)
	the_team		= the_line.the_world.teams()[the_line.block.team]
	
	groups['second_army'] = groups['second_army'].strip()
	
	# First army
	if groups['first_army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of %s (first army)" % (groups['first_army']))
	else:
		first_army = army_dict[armies_lookup[groups['first_army'].lower()]]
	
	# Second army
	if groups['second_army'].lower() not in armies_lookup:
		return order_block.fail(results, "there is no army by the name of %s (second army)" % (groups['second_army']))
	else:
		second_army = army_dict[armies_lookup[groups['second_army'].lower()]]
	
	# Now to find squads
	squad_dict						= the_line.the_world.squads()
	first_current_squads_lookup		= the_line.the_world.squads_lookup_from_army(first_army.id)
	second_current_squads_lookup	= the_line.the_world.squads_lookup_from_army(second_army.id)
	
	# First squad
	if groups['first_squad'].lower() not in first_current_squads_lookup:
		return order_block.fail(results, "there is no squad by the name of %s in %s" % (groups['first_squad'], first_army.name))
	else:
		first_squad = squad_dict[first_current_squads_lookup[groups['first_squad'].lower()]]
	
	# Second squad
	if groups['second_squad'].lower() not in second_current_squads_lookup:
		return order_block.fail(results, "there is no squad by the name of %s in %s" % (groups['second_squad'], second_army.name))
	else:
		second_squad = squad_dict[second_current_squads_lookup[groups['second_squad'].lower()]]
	
	# Amount
	try:
		amount = int(groups['amount'])
	except Exception as e:
		return order_block.fail(results, "the amount '%s' could not be converted into a number" % groups['amount'])
	
	# Default results
	results = order_block.default_line_results(the_line, "%s men from %s (%s) could not be sent to %s (%s) because" % (amount, first_squad.name, first_army.name, second_squad.name, second_army.name))
	
	unit_dict		= the_line.the_world.units()
	
	# Are they the same type? If not then we can't combine them
	if first_squad.unit != second_squad.unit:
		return order_block.fail(results, "they are from different types of units")
	
	# Is squad 1 big enough?
	amount = min(amount, first_squad.amount)
	
	results['queries'].extend(squad_f.make_split_queries(first_squad.id, second_squad.id, amount))
	results['results'].append("%s men were moved from %s to %s" % (amount, first_squad.name, second_squad.name))
	
	return order_block.success(results)


def add_equipment_order(the_line, groups, debug=False):
	return _equipment_order("add", the_line, groups)
	
def remove_equipment_order(the_line, groups, debug=False):
	return _equipment_order("remove", the_line, groups)
		
def new_equipment_order(the_line, groups, debug=False):
	return _equipment_order("new", the_line, groups)

def _equipment_order(otype, the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	# Handles
	unit_dict			= the_line.the_world.units()
	units_lookup		= the_line.the_world.units_lookup_from_team(the_line.block.team)
	squad_dict			= the_line.the_world.squads_from_team(the_line.block.team)
	
	equipment_dict		= the_line.the_world.equipment()
	equipment_lookup	= the_line.the_world.equipment_lookup(lower=True)
	
	the_team			= the_line.the_world.teams()[the_line.block.team]
	
	# Find unit
	if groups['unit'].lower() not in units_lookup:
		return order_block.fail(results, "you have no unit type of %s" % (groups['unit']))
	else:
		the_unit = unit_dict[units_lookup[groups['unit'].lower()]]
	
	# Now get equipment
	equipment_list = []
	equipment_list_s = groups['item_list'].split(",")
	for e in equipment_list_s:
		els = e.lower().strip()
		if els in equipment_lookup:
			new_equipment = equipment_lookup[els]
			if equipment_dict[new_equipment].public:
				equipment_list.append(new_equipment)
	
	# Make sure we actually have equipment
	if len(equipment_list) < 0:
		return order_block.fail(results, "none of the equipment listed was able to be found")
	
	# Amount
	amount = 0
	for squad_id, the_squad in squad_dict.items():
		if the_squad.unit == the_unit.id:
			amount += the_squad.amount
	
	# Refund
	refund = the_unit.get_cost(the_world=the_line.the_world)['material_cost'] * (amount/1000)/2
	
	# Now to update the unit entry
	if otype == "add":
		for e in equipment_list:
			the_unit.equipment.append(e)
		
	elif otype == "remove":
		new_equip = []
		for e in the_unit.equipment:
			if e not in equipment_list:
				new_equip.append(e)
		
		the_unit.equipment = new_equip
		
	elif otype == "new":
		the_unit.equipment = equipment_list
		
	else:
		raise Exception("Unknown otype '%s'" % otype)
	
	if the_team.resources.get("Iron") > 0:
		new_cost = the_unit.get_cost(the_world=the_line.the_world, force_requery=True)['material_cost'] * (amount/1000)
	else:
		new_cost = the_unit.get_cost(the_world=the_line.the_world, force_requery=True)['iron_cost'] * (amount/1000)
	
	# print("")
	# print(the_unit.name)
	# print(str(refund))
	# print(str(new_cost))
	# print("")
	
	# Apply unit_rules to it
	results['cost'] = new_cost - refund
		
	# First queries are cost
	results['queries'].append("-- Changing equipment: %s, %s: %s" % (the_unit.name, otype, groups['item_list']))
	results['queries'].extend(unit_f.replace_equipment(the_unit.id, the_unit.equipment))
	
	# Results
	equip_string = [equipment_dict[e].name for e in the_unit.equipment]
	results['results'].append("Changed the equipment of %s to %s" % (the_unit.name, ", ".join(equip_string)))
	
	the_team.resources -= results['cost'].discrete()
	return order_block.success(results)

def confirm_new_unit_order(the_line, groups, debug=False):
	return new_unit_order(the_line, groups, debug=debug, confirm=True)

def new_unit_order(the_line, groups, debug=False, confirm=False):
	from checks import military_check
	
	results = order_block.default_line_results(the_line)
	
	# Handles
	unit_dict			= the_line.the_world.units()
	units_lookup		= the_line.the_world.units_lookup_from_team(the_line.block.team)
	squad_dict			= the_line.the_world.squads_from_team(the_line.block.team)
	
	equipment_dict		= the_line.the_world.equipment()
	equipment_lookup	= the_line.the_world.equipment_lookup(lower=True)
	
	the_team			= the_line.the_world.teams()[the_line.block.team]
	
	# Make sure unit does not already exist
	# _check_exists
	if groups['unit_name'].lower() in units_lookup:
		if debug:
			results['debug'].append("Failed at _check_exists")
			results['debug'].append("Exists with unit id: %d" % units_lookup[groups['unit_name'].lower()])
		return order_block.fail(results, "you already have a unit type by the name %s" % (groups['unit_name']))
	
	# Now get equipment
	equipment_list = []
	equipment_list_s = groups['item_list'].split(",")
	for e in equipment_list_s:
		els = e.lower().strip()
		if els in equipment_lookup:
			new_equipment = equipment_lookup[els]
			if equipment_dict[new_equipment].public:
				equipment_list.append(new_equipment)
	
	# Make sure we actually have equipment
	# _empty_equipment_list
	if len(equipment_list) < 1:
		if debug:
			results['debug'].append("Failed at _empty_equipment_list")
		return order_block.fail(results, "none of the equipment listed was able to be found")
	
	# Add unit info to the dictionary, only if confirming it
	if confirm:
		temp_unit = unit.Unit()
		temp_unit.name = groups['unit_name']
		temp_unit.equipment.extend(equipment_list)
		c = temp_unit.get_cost(cursor=None, the_world=the_line.the_world, equipment_dict=None, breakdown_mode=False, force_requery=False)
		
		# We need to actually add the unit + equipment
		unit_id = unit_f.new_unit(the_line.the_world.cursor, the_line.block.team, groups['unit_name'], "", 0, equipment_list)
		
		# Now to add it to the dictionaries
		unit_dict[unit_id] = unit_q.get_one_unit(the_line.the_world.cursor, unit_id)
		the_unit = unit_dict[unit_id]
		the_unit.id = unit_id
		
		units_lookup[the_unit.name.lower()] = unit_id
		
		military_check.check_available(the_line.the_world.cursor, verbose=False)
		
		equip_string = [equipment_dict[e].name for e in temp_unit.equipment]
		results['results'].append("Created new unit: %s" % temp_unit.name)
		results['results'].append("Equipment list: %s" % ", ".join(equip_string))
		results['results'].append("Cost: (%s/%s) (%s/%s)" % (
			c['material_cost'].get('Materials'),
			c['iron_cost'].get('Materials'),
			c['material_upkeep'].get('Materials'),
			c['iron_upkeep'].get('Materials'),
		))
		results['results'].append("This unit has been added successfully, even if in a Rob request")
		results['results'].append("")
		
		# Queries
		# results['queries'].append("-- Changing equipment: %s, %s: %s" % (the_unit.name, otype, groups['item_list']))
		# results['queries'].extend(unit_f.replace_equipment(the_unit.id, the_unit.equipment))
		
		return order_block.success(results)
		
	else:
		temp_unit = unit.Unit()
		temp_unit.name = groups['unit_name']
		temp_unit.equipment.extend(equipment_list)
		
		c = temp_unit.get_cost(cursor=None, the_world=the_line.the_world, equipment_dict=None, breakdown_mode=False, force_requery=False)
		
		equip_string = [equipment_dict[e].name for e in temp_unit.equipment]
		results['results'].append("Template for new unit: %s" % temp_unit.name)
		results['results'].append("Equipment list: %s" % ", ".join(equip_string))
		results['results'].append("Cost: (%s/%s) (%s/%s)" % (
			c['material_cost'].get('Materials'),
			c['iron_cost'].get('Materials'),
			c['material_upkeep'].get('Materials'),
			c['iron_upkeep'].get('Materials'),
		))
		results['results'].append("This unit has not yet been added, you must repeat this order with 'New unit' switched with 'Confirm new unit'")
		results['results'].append("")
		
		return order_block.success(results)

class Military_block (order_block.Order_block):
	background_colour	= "#FFEEBB"
	border_colour		= "#AA7700"
	
	functions = (
		(re.compile(r"(?i)^(?:Create|New) (?:army|fleet|navy|airforce|airfleet): ?(?P<army>[^,<>]*), ?(?P<x>-?[0-9]+)(?:,| |, )(?P<y>-?[0-9]+)$"),
			create_army_order),
		
		(re.compile(r"(?i)^(?:Select) (?:army|fleet|navy|airforce|airfleet): (?P<army>[^,<>]*)$"),
			select_army_order),
		
		(re.compile(r"(?i)^(?:Relocate army): ?(?P<army>[^,<>]*), ?(?P<x>-?[0-9]+)(?:,| |, )(?P<y>-?[0-9]+)$"),
			relocate_army_order),
		(re.compile(r"(?i)^(?:Rename army): ?(?P<army>[^,<>]*), ?(?P<new_name>[^,<>]*)$"),
			rename_army_order),
		(re.compile(r"(?i)^(?:Delete army): ?(?P<army>[^,<>]*)$"),
			delete_army_order),
		
		(re.compile(r"(?i)^(?:Create|New) squad: ?(?P<squad>[a-z -_#0-9]+), ?(?P<amount>[0-9]+), ?(?P<unit>[0-9a-z \-']+), ?(?P<army>[^,<>]*)$"),
			create_squad_order),
		(re.compile(r"(?i)^(?:Reinforce squad|Select squad): ?(?P<squad>[^,<>]*), ?(?P<amount>-?[0-9]*)"),
			select_squad_order),
		(re.compile(r"(?i)^(?:Delete squad): ?(?P<squad>[a-z -_#0-9]+) from (?P<army>[^,<>]*)$"),
			delete_squad_order),
		(re.compile(r"(?i)^(?:Disband squad): ?(?P<squad>[a-z -_#0-9]+), ?(?P<amount>[0-9]*)$"),
			disband_squad_order),
		
		(re.compile(r"(?i)^(?:Rename squad): ?(?P<squad>[a-z -_#0-9]*) in (?P<army>[^,<>]*), ?(?P<new_name>[a-z -_#0-9]*)$"),
			rename_squad_order),
		(re.compile(r"(?i)^(?:Move squad): ?(?P<squad>[a-z -_#0-9]+) from (?P<current_army>[^,<>]*) to (?P<new_army>[^,<>]*)$"),
			move_squad_order),
		
		(re.compile(r"(?i)^(?:Split squad): ?(?P<amount>[0-9]*) from ?(?P<first_squad>[a-z -_#0-9]+) in ?(?P<first_army>[^,<>]*) to ?(?P<second_squad>[a-z -_#0-9]+) in ?(?P<second_army>[^,<>]*)$"),
			split_squad_order),
		
		# Equipment
		(re.compile(r"(?i)^(?:Add equipment): ?(?P<unit>[^,]*), (?P<item_list>.*?)$"),
			add_equipment_order),
		
		(re.compile(r"(?i)^(?:Remove equipment): ?(?P<unit>[^,]*), (?P<item_list>.*?)$"),
			remove_equipment_order),
			
		(re.compile(r"(?i)^(?:New equipment): ?(?P<unit>[^,]*), (?P<item_list>.*?)$"),
			new_equipment_order),
		
		# New unit
		(re.compile(r"(?i)^(?:New unit): ?(?P<unit_name>[^,]*), (?P<item_list>.*?)$"),
			new_unit_order),
		
		(re.compile(r"(?i)^(?:Confirm new unit): ?(?P<unit_name>[^,]*), (?P<item_list>.*?)$"),
			confirm_new_unit_order),
	)
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text
	
