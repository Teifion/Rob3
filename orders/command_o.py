import re
import math
from classes import order_block, res_dict
from functions import path_f
from lists import resource_list

def path_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	if not the_line.block.msn_order:
		return order_block.fail(results, "Command not valid in live mode")
	
	groups['waypoints'] = groups['waypoints'].strip()
	
	the_path = groups['waypoints'].replace(": ", "").replace(".", ",")
	path_split = [x.strip() for x in the_path.split(',')]
	waypoints = []
	
	for p in path_split:
		if waypoints == []:				waypoints.append([])
		elif len(waypoints[-1]) == 2:	waypoints.append([])
		
		try:
			waypoints[-1].append(int(p))
		except Exception:
			return order_block.fail(results, "the coordinates you sent could not be converted")
	
	# Get times
	infantry_time = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=waypoints,
		move_speed="Marching",
		move_type="Medium foot"
	).time_cost
	
	cavalry_time = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=waypoints,
		move_speed="Riding",
		move_type="Medium cav"
	).time_cost
	
	airship_time = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=waypoints,
		move_speed="Sailing",
		move_type="Air"
	).time_cost
	
	ship_time = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=waypoints,
		move_speed="Sailing",
		move_type="Sail"
	).time_cost
	
	colonist_time = path_f.path(
		cursor=the_line.the_world.cursor,
		waypoints=waypoints,
		move_speed="Colonists",
		move_type="Colonists"
	).time_cost
	
	# Print results
	results['results'] = ["""Time taken to travel from %s to %s is:
%s days as infantry
%s days as cavalry
%s days as airships
%s days as ships
%s days as colonists""" % (waypoints[0], waypoints[-1],
		round(infantry_time),
		round(cavalry_time),
		round(airship_time),
		round(ship_time),
		round(colonist_time),
	)]
	
	return order_block.success(results)


def assume_supply_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	if not the_line.block.msn_order:
		return order_block.fail(results, "Command not valid in live mode")
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	res_name = groups['supply']
	if res_name.lower() not in resource_list.data_dict_n_l:
		return order_block.fail(results, "Supply not found in the list of supplies")
	
	# Force correct case
	res_name = resource_list.data_dict[resource_list.data_dict_n_l[res_name.lower()]]
	
	the_team.resources.set(res_name.name, 1)
	
	results['results'] = ["All subsequent orders will assume you have traded for a supply of %s" % groups['supply']]
	
	return order_block.success(results)

def assume_points_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	if not the_line.block.msn_order:
		return order_block.fail(results, "Command not valid in live mode")
	
	if groups['resource'].lower() not in resource_list.data_dict_n_l:
		return order_block.fail(results, "The resource '%s' could not be found" % groups['resource'])
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	the_team.resources.set(groups['resource'], float(groups['amount']))
	results['results'] = ["Your amount of %s has now been set to %s for this batch of orders" % (groups['resource'], groups['amount'])]
	
	return order_block.success(results)


def disable_overbudget_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	the_team.overbudget = []
	results['results'] = ["Overbudget checks enabled"]
	
	return order_block.success(results)

def enable_overbudget_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	the_team.overbudget = ["Materials"]
	results['results'] = ["Overbudget checks disabled"]
	
	return order_block.success(results)

class Command_block (order_block.Order_block):
	background_colour	= "#EEFFEE"
	border_colour		= "#00AA00"
	
	functions = (
		(re.compile(r'(?i)Path: (?P<waypoints>.*)$'),
			path_order),
		
		(re.compile(r'(?i)Assume supply: (?P<supply>.*)$'),
			assume_supply_order),
		
		(re.compile(r'(?i)Assume resource: (?P<amount>[0-9,]*) (?P<resource>.*)$'),
			assume_points_order),
		
		(re.compile(r'(?i)Enable: overbudget$'),
			enable_overbudget_order),
		
		(re.compile(r'(?i)Disable: overbudget$'),
			disable_overbudget_order),
	)
	
	def __init__(self):
		super(Command_block, self).__init__()
	
	# def common_mistakes(self, text):
	# 	"""Removes common spelling mistakes"""
	# 	for regex, replacement in replacements:
	# 		text = regex.sub(replacement, text)		
	# 	
	# 	return text