import re
from classes import order_block, res_dict, team
from functions import building_f, wonder_f, team_f
from rules import city_rules

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

def default_tax_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the Rate?
	try:
		rate = int(groups['rate'])
	except Exception as e:
		return order_block.fail(results, "unable to interpret the number of  '%s'" % groups['rate'])
	
	results['queries'].extend(team_f.make_default_taxes(the_team.id, rate))
	results['results'].append("Taxes now default to %s%%" % (rate))
	
	return order_block.success(results)

def specific_tax_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	team_lookup	= the_line.the_world.teams_lookup(lower=True)
	team_dict = the_line.the_world.teams()
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the Rate?
	try:
		rate = int(groups['rate'])
	except Exception as e:
		return order_block.fail(results, "unable to interpret the number of  '%s'" % groups['rate'])
	
	# Can we find the team?
	if groups['team'].lower() not in team_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team'])
	else:
		target_team = team_lookup[groups['team'].lower()]
	
	# Make sure that it's in the database
	the_line.try_query("INSERT INTO team_relations (host, visitor) values (%d, %d);" % (the_team.id, target_team))
	
	results['queries'].extend(team_f.make_specific_taxes(the_team.id, target_team, rate))
	results['results'].append("taxes to %s set to %s%%" % (team_dict[target_team].name, rate))
	
	return order_block.success(results)

def tax_reset_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)

	team_lookup	= the_line.the_world.teams_lookup(lower=True)
	team_dict = the_line.the_world.teams()
	the_team = the_line.the_world.teams()[the_line.block.team]

	# Can we find the team?
	if groups['team'].lower() not in team_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team'])
	else:
		target_team = team_lookup[groups['team'].lower()]

	results['queries'].extend(team_f.specific_taxes_reset(the_team.id, target_team))
	results['results'].append("taxes to %s now set to default" % (team_dict[target_team].name))

	return order_block.success(results)

def default_border_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the State?
	try:
		state = team.border_states.index(groups['state'])
	except Exception as e:
		state = -1
		for i, s in enumerate(team.border_states):
			if s.lower() == groups['state'].lower():
				state = i
		
		if state == -1:
			return order_block.fail(results, "there is no border state of '%s'" % groups['state'])
	
	results['queries'].extend(team_f.make_default_borders(the_team.id, state))
	results['results'].append("Borders now default to %s" % (team.border_states[state]))
	
	return order_block.success(results)


def specific_border_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	team_lookup	= the_line.the_world.teams_lookup(lower=True)
	team_dict = the_line.the_world.teams()
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the State?
	try:
		state = team.border_states.index(groups['state'])
	except Exception as e:
		if groups['state'].lower() == "default":
			return border_reset_order(the_line, groups)
		else:
			state = -1
			for i, s in enumerate(team.border_states):
				if s.lower() == groups['state'].lower():
					state = i
			
			if state == -1:
				return order_block.fail(results, "there is no border state of '%s'" % groups['state'])
	
	# Can we find the team?
	if groups['team'].lower() not in team_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team'])
	else:
		target_team = team_lookup[groups['team'].lower()]
	
	# Make sure that it's in the database
	the_line.try_query("INSERT INTO team_relations (host, visitor) values (%d, %d);" % (the_team.id, target_team))
	
	results['queries'].extend(team_f.make_specific_borders(the_team.id, target_team, state))
	results['results'].append("Borders to %s set to %s" % (team_dict[target_team].name, team.border_states[state]))
	
	return order_block.success(results)

def border_reset_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	team_lookup	= the_line.the_world.teams_lookup(lower=True)
	team_dict = the_line.the_world.teams()
	the_team = the_line.the_world.teams()[the_line.block.team]
	
	# Can we find the team?
	if groups['team'].lower() not in team_lookup:
		return order_block.fail(results, "there is no team by the name of '%s'" % groups['team'])
	else:
		target_team = team_lookup[groups['team'].lower()]
	
	results['queries'].extend(team_f.specific_borders_reset(the_team.id, target_team))
	results['results'].append("Borders to %s now set to default" % (team_dict[target_team].name))

	return order_block.success(results)

class Diplomacy_block (order_block.Order_block):
	background_colour	= "#CCCCFF"
	border_colour		= "#0000AA"
	
	functions = (
		# Taxes
		(re.compile(r'(?i)(Set default taxes to) (?P<rate>[0-9]*?)$'),	
			default_tax_order),
		
		(re.compile(r'(?i)(Taxes for) (?P<team>.*?) are Default$'),
			tax_reset_order),
		
		(re.compile(r'(?i)(Taxes for) (?P<team>.*?) are (?P<rate>[0-9]*?)$'),
			specific_tax_order),
		
		# Borders
		(re.compile(r'(?i)(Set default borders to) (?P<state>.*?)$'),	
			default_border_order),
		
		(re.compile(r'(?i)(Borders to) (?P<team>.*?) are (?P<state>.*?)$'),	
			specific_border_order),
	)
	
	def __init__(self):
		super(Diplomacy_block, self).__init__()
	
	# def common_mistakes(self, text):
	# 	"""Removes common spelling mistakes"""
	# 	for regex, replacement in replacements:
	# 		text = regex.sub(replacement, text)		
	# 	
	# 	return text

"""
[o]Diplomacy[/o]
Set default borders to Segregated
Borders to Albed are At war
Borders to Aracnar are Closed
Borders to Crown of Machtburg are Segregated
Borders to Daninia are Open
Borders to Exions are Allied
Borders to Greymin are Default
"""