from queries import spell_q
from classes import res_dict
from data_classes import spell

def cost_for_this_level(cursor, the_spell, level, completed=0, in_spell_points=False):
	return cost_for_next_level(cursor, the_spell, level-1, completed, in_spell_points)
 
def cost_for_next_level(cursor, the_spell, level, completed=0, in_spell_points=False):
	if type(the_spell) == int:
		the_spell = spell_q.get_one_spell(cursor, the_spell)
	
	# print spell.spell_category[the_spell.
	lore_points = "%s points" % spell.categories[the_spell.category]
	
	if the_spell.tier == spell.tiers.index('Low'):
		base 	= (1, 10)
		extra	= (1, 5)
		
	elif the_spell.tier == spell.tiers.index('Mid'):
		base 	= (2, 10)
		extra	= (1.5, 15)
		
	elif the_spell.tier == spell.tiers.index('High'):
		base 	= (5, 60)
		extra	= (2, 40)
	
	elif the_spell.tier == spell.tiers.index('Master'):
		base 	= (6, 100)
		extra	= (3, 200)
	
	else:
		raise Exception("No handler for tier %s" % spell.spell_tier)
	
	# Now to build the cost
	materials = base[0] + (extra[0] * (level + 1))
	points = base[1] + (extra[1] * (level + 1))
	points -= completed
	
	the_cost = res_dict.Res_dict("Materials:%(materials)s,%(lore)s:%(points)s(Spell points:%(lore)s)" % {
		"materials":	materials,
		"points":		points,
		"lore":			lore_points
	})
	
	# Do we want it in spell points rather than lore points?
	if in_spell_points:
		the_cost.set("Spell points", the_cost.get(lore_points))
		the_cost.set(lore_points, 0)
	
	return the_cost

def cost_to_get_to_level(cursor, the_spell, level, in_spell_points=False):
	"""Calls cost_for_next_level several times to get the points spent on something"""
	total = res_dict.Res_dict()
	if type(the_spell) == int:
		the_spell = spell_q.get_one_spell(cursor, the_spell)
	
	for l in range(0, level):
		total += cost_for_next_level(cursor, the_spell, l, in_spell_points=in_spell_points).flatten()
	
	return total
