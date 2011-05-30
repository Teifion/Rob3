import re
from classes import order_block, res_dict
from rules import spell_rules, tech_rules
from data_classes import spell
from functions import spell_f, tech_f

replacements = (
	(re.compile(r'(?i)enchantment low$'), 	'enchantment (low)'),
	(re.compile(r'(?i)enchantment mid$'), 	'enchantment (mid)'),
	(re.compile(r'(?i)enchantment high$'), 	'enchantment (high)'),
	(re.compile(r'(?i)enchantment master$'), 'enchantment (master)'),
)

def research_order(the_line, groups, debug=False):
	spells_lookup	= the_line.the_world.spells_lookup(lower=True)
	techs_lookup	= the_line.the_world.techs_lookup(lower=True)
	
	# Tech
	if groups['item_name'].lower().strip() in techs_lookup:
		return research_tech(the_line, techs_lookup[groups['item_name'].lower().strip()])
	
	# Spell
	if groups['item_name'].lower().strip() in spells_lookup:
		return research_spell(the_line, spells_lookup[groups['item_name'].lower().strip()])
		
	# Failure!
	results = order_block.default_line_results(the_line)
	return order_block.fail(results, "there is no spell or tech by the name of '%s'" % groups['item_name'])
		

def research_tech(the_line, tech_id, debug=False):
	tech_dict		= the_line.the_world.techs()
	the_team		= the_line.the_world.teams()[the_line.block.team]
	the_tech		= tech_dict[tech_id]
	
	current_level	= the_team.tech_levels.get(tech_id, 0)
	current_points	= the_team.tech_points.get(tech_id, 0)
	
	results = order_block.default_line_results(the_line, "%s could not be researched to level %s because" % (the_tech.name, current_level+1))
	
	new_level		= current_level + 1
	new_points		= 0
	
	# Level limit
	if the_tech.max_level > 0:
		if current_level >= the_tech.max_level:
			return order_block.fail(results, "%s is it's maximum level" % (the_tech.max_level))
	
	# Cost
	tech_cost = tech_rules.cost_for_next_level(the_line.the_world.cursor, the_tech, current_level, completed=current_points)
	
	# If we've started it then we don't need to worry about materials
	if current_points > 0:
		tech_cost.set("Materials", 0)
	
	# Lets get some stuff here for working out partiality of research
	points_cost = tech_cost.get("Tech points")
	real_points_cost = points_cost# Used for output later
	points_availiable = the_team.resources.get("Tech points")
	
	afford_result = the_team.resources.affordable(tech_cost, overbudget_list=the_team.overbudget)
	
	# It's possible we cannot afford it
	if not afford_result[0]:
		
		# Check materials - Fail outright
		materials_cost = tech_cost.get("Materials")
		if materials_cost > the_team.resources.get("Materials"):
			if "Materials" not in the_team.overbudget:
				return order_block.fail(results, "you do not have enough materials for it")
		
		# Lets try points - Fail outright if 0 points
		if points_availiable == 0:
			if current_points > 0:
				return order_block.fail(results, "you do not have any more tech points availiable this turn")
			else:
				return order_block.fail(results, "you do not have any more tech points availiable this turn")
		
		# At this point they cannot afford the whole tech, set cost to what's available - Fail partial
		if 0 < points_availiable < points_cost:
			tech_cost.set("Tech points", the_team.resources.get("Tech points"))
			
			new_level		= current_level
			new_points		= current_points + points_availiable
	
	
	#	EXECUTION
	#------------------------
	# Check we've got a DB row ready to update
	if current_level == 0 and current_points == 0:
		the_line.try_query(tech_f.check_row_exists(team_id=the_team.id, tech_id=the_tech.id))
	
	# Tell them it's only being partially completed
	if new_level == current_level:
		result_line = "%s was researched to %s out of %s points towards level %d" % (the_tech.name, new_points, real_points_cost, new_level+1)
	
	# It's complete
	else:
		result_line	= "%s is now level %s" % (the_tech.name, new_level)
	
	# Save cost into results dictionary
	results['cost'] = tech_cost
	
	# Queries
	results['queries'].append("-- Tech research %s to %d.%d for team:%d" % (the_tech.name, new_level, new_points, the_team.id))
	results['queries'].extend(tech_f.research_query(the_team.id, tech_id, new_level, new_points))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	# Update team tech level/points
	the_team.tech_levels[the_tech.id] = new_level
	the_team.tech_points[the_tech.id] = new_points
	
	# Result
	results['results'].append(result_line)
	
	return order_block.success(results)
	
def research_spell(the_line, spell_id, debug=False):
	results = order_block.default_line_results(the_line)
	
	spell_dict		= the_line.the_world.spells()
	the_team		= the_line.the_world.teams()[the_line.block.team]
	the_spell		= spell_dict[spell_id]
	
	lore_name		= spell.categories[the_spell.category]
	current_level	= the_team.spell_levels.get(spell_id, 0)
	current_points	= the_team.spell_points.get(spell_id, 0)
	
	new_level		= current_level + 1
	new_points		= 0
	
	results = order_block.default_line_results(the_line, "%s could not be researched to level %s because" % (the_spell.name, current_level+1))
	
	# Level limit
	if the_spell.max_level > 0:
		if current_level >= the_spell.max_level:
			return order_block.fail(results, "%s is it's maximum level" % the_spell.max_level)
	
	# Cost, it's a bit more complicated here...
	spell_cost = spell_rules.cost_for_next_level(the_line.the_world.cursor, the_spell, current_level, completed=current_points)
	
	# If we've started it then we don't need to worry about materials
	if current_points > 0:
		spell_cost.set("Materials", 0)
	
	# Lets get some stuff here for working out partiality of research
	points_cost = spell_cost.get("%s points" % lore_name) + spell_cost.get("Spell points")
	real_points_cost = points_cost# Used for output later
	points_availiable = the_team.resources.get("%s points" % lore_name) + the_team.resources.get("Spell points")
	
	afford_result = the_team.resources.affordable(spell_cost, overbudget_list=the_team.overbudget)
	
	# We cannot afford it
	if afford_result[0]:
		# We need to apply swappables
		spell_cost = res_dict.Res_dict(afford_result[1])
		
	elif not afford_result[0]:
		# Check materials - Fail outright
		materials_cost = spell_cost.get("Materials")
		if materials_cost > the_team.resources.get("Materials"):
			if "Materials" not in the_team.overbudget:
				return order_block.fail(results, "you do not have enough materials for it")
		
		# Lets try points - Fail outright if 0 points (either spell or lore)
		if points_availiable == 0:
			return order_block.fail(results, "you do not have any more spell points availiable this turn")
		
		# At this point they cannot afford the whole spell, set cost to what's available - Fail partial
		if 0 < points_availiable < points_cost:
			
			spell_cost.set("Spell points", the_team.resources.get("Spell points"))
			spell_cost.set("%s points" % lore_name, the_team.resources.get("%s points" % lore_name))
			
			new_level		= current_level
			new_points		= current_points + points_availiable
	
	#	EXECUTION
	#------------------------
	# Check we've got a DB row ready to update
	if current_level == 0 and current_points == 0:
		the_line.try_query(spell_f.check_row_exists(team_id=the_team.id, spell_id=the_spell.id))
	
	# Tell them it's only being partially completed
	if new_level == current_level:
		result_line = "%s was researched to %s out of %s points towards level %d" % (the_spell.name, new_points, real_points_cost, new_level+1)
	
	# It's complete
	else:
		result_line	= "%s is now level %s" % (the_spell.name, new_level)
	
	# Save cost into results dictionary
	results['cost'] = spell_cost
	
	# Queries
	results['queries'].append("-- Spell research %s to %d.%d for team:%d" % (the_spell.name, new_level, new_points, the_team.id))
	results['queries'].extend(spell_f.research_query(the_team.id, spell_id, new_level, new_points))
	
	# Apply cost
	the_team.resources -= results['cost'].discrete()
	
	# Update team spell level/points
	the_team.spell_levels[the_spell.id] = new_level
	the_team.spell_points[the_spell.id] = new_points
	
	# Result
	results['results'].append(result_line)
	
	return order_block.success(results)

class Research_block (order_block.Order_block):
	background_colour	= "#CC88CC"
	border_colour		= "#AA00AA"
	
	functions = (
		(re.compile(r'(?P<item_name>.*)$'),	
			research_order),
	)
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text