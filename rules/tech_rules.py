import math
from queries import tech_q
from classes import res_dict

def cost_for_this_level(cursor, the_tech, level, completed=0):
	return cost_for_next_level(cursor, the_tech, level-1, completed)

def cost_for_next_level(cursor, the_tech, level, completed=0):
	if type(the_tech) == int:
		the_tech = tech_q.get_one_tech(cursor, the_tech)
	
	base_cost	= res_dict.Res_dict(the_tech.base_cost)
	extra_cost	= res_dict.Res_dict(the_tech.extra_cost)
	
	extra_cost *= (level+1)
	
	base_cost += (extra_cost)
	
	if completed > 0:
		base_cost -= "Tech points:%d" % completed
	
	return base_cost

def cost_to_get_to_level(cursor, the_tech, level):
	"""Calls cost_for_next_level several times to get the points spent on something"""
	total = res_dict.Res_dict()
	if type(the_tech) == int:
		the_tech = tech_q.get_one_tech(cursor, the_tech)
	
	for l in range(0, level):
		total += cost_for_next_level(cursor, the_tech, l)
	
	return total