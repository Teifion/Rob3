import re
from classes import order_block, res_dict
from functions import building_f, wonder_f, monster_f
from rules import city_rules, map_data
from lore import pages
from queries import mapper_q
from lists import resource_list

replacements = (
	# (re.compile(r'(?i)Fortifications for ([0-9\.]{1,4})k?'),	r'\1k Fortifications'),
	# (re.compile(r'(?i)Walls for ([0-9\.]{1,4})k?'),				r'\1 walls'),
)

# Monsters: Map area, Monster type, Number of men, Budget
"""
[o]Monsters[/o]
Map area: -710, 831
Target: Karithor
Men: 100
Budget: 100
Army: Abek garrison

Orders orders orders"""
class Monster_block (order_block.Interactive_order_block):
	background_colour	= "#FFAA55"
	border_colour		= "#CC7700"
	
	greps = {
		"map_area":	re.compile(r'(?i)(?:Map )?area: (-?[0-9]*), ?(-?[0-9]*)'),
		"target":	re.compile(r'(?i)(?:Target|Type): (.*)'),
		"men":		re.compile(r'(?i)Men: ([0-9]*)'),
		"budget":	re.compile(r'(?i)Budget: ([0-9\.]*)'),
		"army":		re.compile(r'(?i)Army: (.*)'),
	}
	
	def common_mistakes(self, text):
		"""Removes common spelling mistakes"""
		for regex, replacement in replacements:
			text = regex.sub(replacement, text)		
		
		return text
	
	def ml_check(self):
		debug = self.debug
		results = order_block.default_multi_line_results()
		
		monster_lookup	= self.the_world.monsters_lookup(lower=True)
		army_lookup		= self.the_world.armies_lookup_from_team(self.team)
		
		map_area, target, men, budget, army = None, None, None, None, None
		temp_lines = list(self.lines)
		
		# Block matching
		i = 0
		while i < len(temp_lines):
			found = False
			for g, regex in self.greps.items():
				r = regex.search(temp_lines[i])
				
				if r != None:
					found = True
					
					if g == "map_area":	map_area = (int(r.groups()[0]), int(r.groups()[1]))
					elif g == "target":	target = r.groups()[0]
					elif g == "men":	men = int(r.groups()[0])
					elif g == "budget":	budget = float(r.groups()[0])
					elif g == "army":	army = r.groups()[0]
			
			# Strip this line and look at the next
			if found:
				del(temp_lines[i])
				continue
			
			# No match, must be part of the main content
			# content.append(temp_lines[i])
			i += 1
		
		# Check blocks
		fail_on_data = []
		if map_area == None:
			fail_on_data.append("map area")
			if debug:
				results['debug'].append("Failed to find map_area")
		
		if target == None:
			fail_on_data.append("target monster")
			if debug:
				results['debug'].append("Failed to find target")
		elif target.lower() not in monster_lookup:
			fail_on_data.append("Target monster (no monster of name %s)" % target)
			if debug:
				results['debug'].append("Failed to find the monster '%s' in the list" % target)
		
		if men == None:
			fail_on_data.append("men sent")
			if debug:
				results['debug'].append("Failed to find men")
		
		if budget == None:
			fail_on_data.append("budget")
			if debug:
				results['debug'].append("Failed to find budget")
		
		if army == None:
			fail_on_data.append("army")
			if debug:
				results['debug'].append("Failed to find army")
		elif army.lower() not in army_lookup:
			fail_on_data.append("Target army (no army of name %s)" % army)
			if debug:
				results['debug'].append("Failed to find the army '%s' in the list" % army)
		
		if fail_on_data:
			return order_block.fail(results, "failed to find data for %s" % ", ".join(fail_on_data))
		
		# Right, we've got an actual order here
		results['queries'].extend(self.approve(self.team, self.title_name, self.content))
		
		results['input_response'] = "Order parsed correctly, will require GM input to create the results."
		return order_block.success(results)
	
	def interactive_setup(self, cursor):
		map_area, target, men, budget, army = None, None, None, None, None
		temp_lines = self.content.split("\n")
		content = []
		
		monster_lookup	= self.the_world.monsters_lookup(lower=True)
		army_lookup		= self.the_world.armies_lookup_from_team(self.team)
		
		# Block matching
		i = 0
		while i < len(temp_lines):
			found = False
			for g, regex in self.greps.items():
				r = regex.search(temp_lines[i])
				
				if r != None:
					found = True
					
					if g == "map_area":	map_area = (int(r.groups()[0]), int(r.groups()[1]))
					elif g == "target":	target = r.groups()[0]
					elif g == "men":	men = int(r.groups()[0])
					elif g == "budget":	budget = float(r.groups()[0])
					elif g == "army":	army = r.groups()[0]
			
			# Strip this line and look at the next
			if found:
				del(temp_lines[i])
				continue
			
			# No match, must be part of the main content
			content.append(temp_lines[i])
			i += 1
		
		# Show this as an integer if possible
		if budget == int(budget): budget = int(budget)
		
		monster_id = monster_lookup[target.lower()]
		the_monster = self.the_world.monsters()[monster_id]
		
		army_id = army_lookup[army.lower()]
		the_army = self.the_world.armies()[army_id]
		
		# Apply multiplier for man count
		multiplier = 1
		# multiplier = (men - the_monster.min_men)/(the_monster.max_men - the_monster.min_men)
		# multiplier = min(1, max(multiplier, 0))
		
		multiplier *= (budget - the_monster.min_budget)/(the_monster.max_budget - the_monster.min_budget)
		multiplier = min(1, max(multiplier, 0))
		
		self.interactivity['multiplier'] = multiplier
		
		# Make sure they have monsters in this army
		self.try_query(monster_f.check_row_exists(army_id=the_army.id, monster_id=the_monster.id))
		
		# Query producing function
		self.interactivity['query_func'] = """
		amount = parseInt(score/100 * {amount});
		return "UPDATE army_monsters SET amount = amount + " + amount + " WHERE army = {army_id} AND monster = {monster_id};" +
		"\\nUPDATE team_resources SET amount = amount - {budget} WHERE team = {team} AND resource = {materials};";
		""".format(
			army_id = the_army.id,
			monster_id = the_monster.id,
			amount = the_monster.max_amount,
			budget = budget,
			team = self.team,
			materials = resource_list.data_dict_n['Materials'],
		)
		
		self.interactivity['result_func'] = """
		amount = parseInt(score/100 * {amount});
		if (amount < 1)
		{{
			return "[o]{title}[/o]\\nYou captured no {monster}s";
		}}
		else
		{{
			if (amount > 1)
			{{
				return "[o]{title}[/o]\\nYou captured " + amount + " {monster}s";
			}}
			else
			{{
				return "[o]{title}[/o]\\nYou captured 1 {monster}";
			}}
		}}
		""".format(
			army_id = the_army.id,
			monster_id = the_monster.id,
			monster = the_monster.name,
			amount = the_monster.max_amount,
			title = self.title_name,
		)
		
		# General info about the order context
		self.interactivity['pre_calculations'] = """
		Monster: <a href="web.py?mode=lore&amp;cat=monsters&page={monster_l}">{monster}</a>,
		Terrain: {terrain},
		Men: {men},
		Budget: {budget},
		Army: <a href="web.py?mode=edit_army&amp;army={army_id}">{army}</a>
		""".format(
			monster = target,
			monster_l = target.lower(),
			terrain = map_data.terrain[mapper_q.get_terrain(cursor, map_area[0], map_area[1])],
			men = ('<span class="neg" style="font-weight:bold;">%s</span>' % men if men < the_monster.min_men else men),
			budget = ('<span class="neg" style="font-weight:bold;">%s</span>' % budget if budget < the_monster.min_budget else budget),
			army = the_army.name,
			army_id = the_army.id,
		)
		
		self.interactivity['content'] = "<br />".join(content)
		self.interactivity['points'] = pages.get_plaintext(cursor, "monsters", "karithor", "gm", ['capture_points']).split("\n")
		
	



