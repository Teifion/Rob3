import re
from classes import order_block, res_dict
from functions import operative_f
from rules import operative_rules

replacements = (
	# (re.compile(r'(?i)mundane academy'), 	'university'),
	# (re.compile(r'(?i)magical academy'),	'academy'),
	# (re.compile(r'(?i)airshipyard'),		'shipyard'),
	# (re.compile(r'(?i)academy of runic'),	'academy of runes'),
	# (re.compile(r'(?i)fortified walls'),	'fortifications'),
	# (re.compile(r'(?i) port'),				'shipyard'),
	# 
	# # (re.compile(r'(?i)([0-9\.]{1,4}) ?k '),						r'\1k'),
	# (re.compile(r'(?i)([0-9\.]{1,4}) fortifications'),			r'\1k Fortifications'),
	# (re.compile(r'(?i)([0-9\.]{1,4}) walls'),					r'\1k Walls'),
	
	# (re.compile(r'(?i)Fortifications for ([0-9\.]{1,4})k?'),	r'\1k Fortifications'),
	# (re.compile(r'(?i)Walls for ([0-9\.]{1,4})k?'),				r'\1 walls'),
)

def reinforce_cell(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	operative_dict			= the_line.the_world.operatives()
	operative_lookup		= the_line.the_world.operatives_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	
	# DB checks
	#------------------------
	# Can we find the building?
	if groups['name'].lower() not in operative_lookup:
		return order_block.fail(results, "there is no cell by the name of '%s'" % groups['name'])
	
	the_op = operative_dict[operative_lookup[groups['name'].lower()]]
	
	# If it's ours then we can reinforce it
	if the_op.team != the_team.id:
		return order_block.fail(results, "the cell named '%s' is not yours" % groups['name'])
	
	amount = int(groups['size'])
	
	# Get cost
	try:
		results['cost'] = operative_rules.get_reinforce_cost(the_op, amount)
	except Exception as e:
		return order_block.fail(results, e.args[0])
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability:
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Queries
	results['queries'].append("-- Operatives %s reinforce by %s for team:%d" % (groups['name'], amount, the_team.id))
	results['queries'].extend(operative_f.reinforce_query(the_op.id, amount))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	# Results
	results['results'].append("%s reinforced by %d" % (groups['name'], amount))
	
	return order_block.success(results)
	
def move_cell(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	city_dict				= the_line.the_world.cities()
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	operative_dict			= the_line.the_world.operatives()
	operative_lookup		= the_line.the_world.operatives_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	
	# DB checks
	#------------------------
	# Can we find the building?
	if groups['name'].lower() not in operative_lookup:
		return order_block.fail(results, "there is no cell by the name of '%s'" % groups['name'])
	
	the_op = operative_dict[operative_lookup[groups['name'].lower()]]
	
	# If it's ours then we can reinforce it
	if the_op.team != the_team.id:
		return order_block.fail(results, "the cell named '%s' is not yours" % groups['name'])
	
	# Now we want the city
	if groups['city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['city'])
	else:
		the_city = city_dict[cities_lookup[groups['city'].lower()]]
	
	# Is this a dead city?
	if the_city.dead > 0:
		return order_block.fail(results, "there is no living city by the name of '%s'" % groups['city'])
	
	#	EXECUTION
	#------------------------
	# Queries
	results['queries'].append("-- Operatives %s move to %s for team:%d" % (groups['name'], the_city.name, the_team.id))
	results['queries'].extend(operative_f.move_operative_query(the_op.id, the_city.id))
	
	# Results
	results['results'].append("%s moved to %s" % (groups['name'], the_city.name))
	
	return order_block.success(results)
	

stat_grep = {
	"Size":				re.compile(r'size: ?([0-9]*)'),
	"Stealth":			re.compile(r'stealth: ?([0-9]*)'),
	"Observation":		re.compile(r'observation: ?([0-9]*)'),
	"Integration":		re.compile(r'integration: ?([0-9]*)'),
	"Sedition":			re.compile(r'sedition: ?([0-9]*)'),
	"Sabotage":			re.compile(r'sabotage: ?([0-9]*)'),
	"Assassination":	re.compile(r'assassination: ?([0-9]*)'),
}

def operative_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	city_dict				= the_line.the_world.cities()
	cities_lookup			= the_line.the_world.cities_lookup(lower=True)
	
	operative_dict			= the_line.the_world.operatives()
	operative_lookup		= the_line.the_world.operatives_lookup(lower=True)
	
	the_team				= the_line.the_world.teams()[the_line.block.team]
	
	# Stats
	# Stealth: 3, Observation: 4, Integration: 5, Sedition: 9, Sabotage: 8, Assassination: 3
	stats = {}
	lower_content = the_line.content.lower()
	for key, reg in stat_grep.items():
		m = reg.search(lower_content)
		if m:
			try:
				stats[key] = int(m.groups()[0])
			except Exception as e:
				print(m.groups)
				raise
		else:
			stats[key] = 0
	
	# DB checks
	#------------------------
	# Can we find the building?
	if groups['name'].lower() in operative_lookup:
		# If it's ours then we can reinforce it
		if operative_dict[operative_lookup[groups['name'].lower()]].team == the_team.id:
			return reinforce_cell(the_line, {"name":groups['name'], "size":stats['Size']})
		else:
			return order_block.fail(results, "there is already a cell by the name of '%s'" % groups['name'])
	
	# Can we find the city?
	if groups['city'].lower() not in cities_lookup:
		return order_block.fail(results, "there is no city by the name of '%s'" % groups['city'])
	else:
		the_city = city_dict[cities_lookup[groups['city'].lower()]]
	
	# Is this a dead city?
	if the_city.dead > 0:
		return order_block.fail(results, "there is no living city by the name of '%s'" % groups['city'])
	
	# Rule checks
	#------------------------
	results = order_block.default_line_results(the_line, "%s could not be recruited at %s because" % (groups['name'], the_city.name))
	
	# Get cost
	try:
		results['cost'] = operative_rules.get_cost(stats)
	except Exception as e:
		return order_block.fail(results, e.args[0])
	
	# Check affordability
	affordability = the_team.resources.affordable(results['cost'])[0]
	
	if not affordability:
		return order_block.fail_cost(results)
	
	#	EXECUTION
	#------------------------
	# Queries
	results['queries'].append("-- Operatives %s at %s for team:%d" % (groups['name'], the_city.name, the_team.id))
	results['queries'].extend(operative_f.recruitment_query(groups['name'], the_city.id, the_team.id, stats))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	# Result
	pstats = []
	for k, v in stats.items():
		if v > 0:
			pstats.append("%s: %s" % (k, v))
	results['results'].append("%s recruited to %s with the stats of: %s" % (groups['name'], the_city.name, ", ".join(pstats)))
	
	return order_block.success(results)

class Operative_block (order_block.Order_block):
	background_colour	= "#DDDDAA"
	border_colour		= "#AAAA00"
	
	functions = (
		(re.compile(r'(?i)(Recruit cell:) (?P<name>.*?) at (?P<city>.*?), (?P<args>.*)$'),
			operative_order),
		
		(re.compile(r'(?i)(Reinforce cell:) (?P<name>.*?) by (?P<amount>[0-9]*?)$'),
			reinforce_cell),
		
		(re.compile(r'(?i)(Move cell:) (?P<name>.*?) to (?P<city>.*?)$'),
			move_cell),
	)
	
	def __init__(self):
		super(Operative_block, self).__init__()
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text