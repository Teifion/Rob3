import re
from classes import order_block, res_dict
from lists import resource_list
from functions import path_f, spell_f, tech_f, trade_f
from rules import sad_rules

replacements = (
	(re.compile(r'(?i)enchantment low'), 	'enchantment (low)'),
	(re.compile(r'(?i)enchantment mid'), 	'enchantment (mid)'),
	(re.compile(r'(?i)enchantment high'), 	'enchantment (high)'),
	(re.compile(r'(?i)enchantment master'), 'enchantment (master)'),
)

def supply_change_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	city_dict		= the_line.the_world.cities()
	cities_lookup	= the_line.the_world.cities_lookup(lower=True)
	
	# _find_city
	if groups['city'].lower() not in cities_lookup:
		if debug:
			results['debug'].append("Failed at _find_city")
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['city'])
	else:
		the_city = city_dict[cities_lookup[groups['city'].lower()]]
	
	# _ownership
	if the_city.team != the_line.block.team:
		if debug:
			results['debug'].append("Failed at _ownership")
		return order_block.fail(results, "%s is not your city" % the_city.name)
	
	# _find_res
	resource_id = -1
	for i, r in enumerate(sad_rules.res_list):
		if r.lower() == groups['res_item'].lower():
			resource_id = i
	
	if resource_id < 0:
		if debug:
			results['debug'].append("Failed at _find_res")
		return order_block.fail(results, "%s is not a valid resource" % groups['res_item'])
	
	# Queries
	results['queries'].append("-- Supply change for %s to %s for team:%d, city:%d" % (
		the_city.name, sad_rules.res_list[resource_id], the_line.block.team, the_city.id))
	results['queries'].extend(trade_f.make_supply_change_query(the_city.id, resource_id))
	
	# Result
	results['results'].append("%s is now producing %s" % (the_city.name, sad_rules.res_list[resource_id]))
	
	# Update city points
	the_city.supply_good = resource_id
	
	return order_block.success(results)
	

def discrete_trade_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	resources_lookup	= resource_list.data_dict_n_l
	resource_dict		= resource_list.data_dict
	teams_lookup		= the_line.the_world.teams_lookup(lower=True)
	
	team_dict			= the_line.the_world.teams()
	the_team			= the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the resource?
	if groups['item_name'].lower() not in resources_lookup:
		raise Exception("Unable to find %s in resource_list.data_dict_n_l.\n\nresource_list.data_dict_n_l = %s" % (groups['item_name'].lower(), resources_lookup))
	else:
		the_resource = resource_dict[resources_lookup[groups['item_name'].lower()]]
	
	# Can we find the team?
	if groups['team_name'].lower() not in teams_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team_name'])
	else:
		target_team = team_dict[teams_lookup[groups['team_name'].lower()]]
	
	# Is it tradable?:
	if not the_resource.tradable:
		raise Exception("%s is not a tradable resource yet is still matched for trade_o.discrete_trade_order" % the_resource.name)
	
	# Are they sending at least 1?
	try:
		amount = float(groups['amount'])
		
		if amount < 1:
			return order_block.fail(results, "you need to send at least 1 unit of %s" % the_resource.name)
	except Exception as e:
		raise Exception("The amount of '%s' cannot be parsed as an integer but was still matched for trade_o.discrete_trade_order")
	
	# Is there a path there?
	path_found = path_f.find_trade_route(the_line.the_world.cursor,
		the_team.id, target_team.id, the_world=the_line.the_world)
	
	if path_found == (-1, -1):
		return order_block.fail(results, "%s %s could not be sent to %s because no trade route between you could be found" % (amount, the_resource.name, target_team.name))
	
	# Can you afford it?
	results['cost'] = res_dict.Res_dict("%s:%s" % (the_resource.name, amount))
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability:
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	target_team.resources += results['cost'].discrete()
	
	# Result
	results['results'].append("%s %s were sent to %s" % (amount, the_resource.name, target_team.name))
	results['foreign_results'][target_team.id] = ["%s %s were sent from %s" % (amount, the_resource.name, the_team.name)]
	results['foreign_costs'][target_team.id] = res_dict.Res_dict("%s:-%s" % (the_resource.name, amount))
	
	return order_block.success(results)


def boolean_trade_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	resources_lookup	= resource_list.data_dict_n_l
	resource_dict		= resource_list.data_dict
	teams_lookup		= the_line.the_world.teams_lookup(lower=True)
	
	team_dict			= the_line.the_world.teams()
	the_team			= the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the resource?
	if groups['item_name'].lower() not in resources_lookup:
		raise Exception("Unable to find %s in resource_list.data_dict_n_l.\n\nresource_list.data_dict_n_l = %s" % (groups['item_name'].lower(), resources_lookup))
	else:
		the_resource = resource_dict[resources_lookup[groups['item_name'].lower()]]
	
	# Can we find the team?
	if groups['team_name'].lower() not in teams_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team_name'])
	else:
		target_team = team_dict[teams_lookup[groups['team_name'].lower()]]
	
	# Is it tradable?:
	if not the_resource.tradable:
		raise Exception("%s is not a tradable resource yet is still matched for trade_o.discrete_trade_order" % the_resource.name)
	
	# Is there a path there?
	path_found = path_f.find_trade_route(the_line.the_world.cursor,
		the_team.id, target_team.id, the_world=the_line.the_world)
	
	if path_found == (-1, -1):
		return order_block.fail(results, "%s could not be sent to %s because no trade route between you could be found" % (the_resource.name, target_team.name))
	
	# Can you afford it?
	if the_team.resources.get(the_resource.name, 0) < 1:
		results['cost'] = res_dict.Res_dict("%s:1" % the_resource.name)
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Apply cost
	target_team.resources.set(the_resource.id, 1)
	
	# Result
	results['results'].append("%s was sent to %s" % (the_resource.name, target_team.name))
	results['foreign_results'][target_team.id] = ["%s was sent from %s" % (the_resource.name, the_team.name)]
	results['foreign_costs'][target_team.id] = res_dict.Res_dict("%s:-1" % the_resource.name)
	
	return order_block.success(results)
	
def tech_trade_order(the_line, groups, debug=False):
	spells_lookup	= the_line.the_world.spells_lookup(lower=True)
	techs_lookup	= the_line.the_world.techs_lookup(lower=True)
	
	# Tech
	if groups['item_name'].lower() in techs_lookup:
		return send_tech(the_line, techs_lookup[groups['item_name'].lower()], groups)
	
	# Spell
	if groups['item_name'].lower() in spells_lookup:
		return send_spell(the_line, spells_lookup[groups['item_name'].lower()], groups)
		
	# Failure!
	results = order_block.default_line_results(the_line)
	return order_block.fail(results, "there is no spell or tech by the name of '%s'" % groups['item_name'])
		
def send_tech(the_line, tech_id, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	teams_lookup	= the_line.the_world.teams_lookup(lower=True)
	
	techs_lookup	= the_line.the_world.techs_lookup()
	tech_dict		= the_line.the_world.techs()
	
	team_dict		= the_line.the_world.teams()
	
	the_team		= team_dict[the_line.block.team]
	the_tech		= tech_dict[tech_id]
	
	# Can we find the team?
	if groups['team_name'].lower() not in teams_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team_name'])
	else:
		target_team = team_dict[teams_lookup[groups['team_name'].lower()]]
	
	# Limits of how many you can send a turn
	if the_team.research_sent >= 2:
		return order_block.fail(results, "%s could not be sent to %s because you have already sent the maximum number of spells/techs this turn" % (the_tech.name, target_team.name))
	
	# Is the item tradable?
	if not the_tech.tradable:
		return order_block.fail(results, "%s could not be sent to %s because it is not tradable" % (the_tech.name, target_team.name))
	
	# Do you have a high enough level?
	if the_team.tech_levels.get(tech_id, 0) <= target_team.tech_levels.get(tech_id, 0):
		return order_block.fail(results, "%s could not be sent to %s" % (the_tech.name, target_team.name))
	
	# Do they have a too high a level of it?
	if target_team.tech_levels.get(tech_id, 0) >= 5:
		return order_block.fail(results, "%s could not be sent to %s" % (the_tech.name, target_team.name))
	
	#	EXECUTION
	#------------------------
	# Check that there's an entry in the database for it
	if target_team.tech_levels.get(tech_id, 0) == 0:
		if target_team.tech_points.get(tech_id, 0) == 0:
			the_line.try_query(tech_f.check_row_exists(team_id=target_team.id, tech_id=the_tech.id))
	
	# Queries
	results['foreign_queries'][target_team.id] = tech_f.trade_query(target_team.id, tech_id)
	
	# Apply change to our copy of the world
	target_team.tech_levels[tech_id] = target_team.tech_levels.get(tech_id, 0) + 1
	target_team.tech_points[tech_id] = 0
	
	# Result
	results['results'].append("%s was sent to %s" % (the_tech.name, target_team.name))
	results['foreign_results'][target_team.id] = ["%s was sent from %s" % (the_tech.name, the_team.name)]
	
	# Update sending limits
	the_team.research_sent += 1
	
	return order_block.success(results)
	
def send_spell(the_line, spell_id, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	teams_lookup	= the_line.the_world.teams_lookup(lower=True)
	
	spells_lookup	= the_line.the_world.spells_lookup()
	spell_dict		= the_line.the_world.spells()
	
	team_dict		= the_line.the_world.teams()
	
	the_team		= team_dict[the_line.block.team]
	the_spell		= spell_dict[spell_id]
	
	# Can we find the team?
	if groups['team_name'].lower() not in teams_lookup:
		return order_block.fail(results, "There is no team by the name of '%s'" % groups['team_name'])
	else:
		target_team = team_dict[teams_lookup[groups['team_name'].lower()]]
	
	# Is the item tradable?
	if not the_spell.tradable:
		return order_block.fail(results, "%s could not be sent to %s because it is not tradable" % (the_spell.name, target_team.name))
	
	# Limits of how many you can send a turn
	if the_team.research_sent >= 2:
		return order_block.fail(results, "%s could not be sent to %s because you have already sent the maximum number of spells/techs this turn" % (the_spell.name, target_team.name))
	
	# Do you have a high enough level?
	if the_team.spell_levels.get(spell_id, 0) <= target_team.spell_levels.get(spell_id, 0):
		return order_block.fail(results, "%s could not be sent to %s" % (the_spell.name, target_team.name))
	
	#	EXECUTION
	#------------------------
	# Check that there's an entry in the database for it
	if target_team.spell_levels.get(spell_id, 0) == 0:
		if target_team.spell_points.get(spell_id, 0) == 0:
			the_line.try_query(spell_f.check_row_exists(team_id=target_team.id, spell_id=the_spell.id))
	
	# Queries
	results['foreign_queries'][target_team.id] = spell_f.trade_query(target_team.id, spell_id)
	
	# Apply change to our copy of the world
	target_team.spell_levels[spell_id] = target_team.spell_levels.get(spell_id, 0) + 1
	target_team.spell_points[spell_id] = 0
	
	# Result
	results['results'].append("%s was sent to %s" % (the_spell.name, target_team.name))
	results['foreign_results'][target_team.id] = ["%s was sent from %s" % (the_spell.name, the_team.name)]
	
	# Update sending limits
	the_team.research_sent += 1
	
	return order_block.success(results)

class Trade_block (order_block.Order_block):
	background_colour	= "#CCCC88"
	border_colour		= "#AAAA00"
	
	functions = (
		# Supply and demand
		(re.compile(r'(?i)Change (?P<city>.*?) supply production to (?P<res_item>.*)$'),
			supply_change_order),
		
		# Basic trade stuff
		(re.compile(r'(?i)(Send|Give) (?P<amount>[0-9.]*) (?P<item_name>(Materials|Food|Ship points|Balloon points)) to (?P<team_name>.*)$'),
			discrete_trade_order),
		(re.compile(r'(?i)(Send|Give) (?P<item_name>(Stone|Wood|Iron)) to (?P<team_name>.*)$'),
			boolean_trade_order),
		
		# Needs to be last so as not to confuse other line types
		(re.compile(r'(?i)Send (?P<item_name>.*?) to (?P<team_name>.*)$'),
			tech_trade_order),
	)
	
	def __init__(self, *args, **kwargs):
		super(Trade_block, self).__init__(*args, **kwargs)
		self.priority = "Trade"
			
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text
	
