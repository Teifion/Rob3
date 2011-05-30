from classes import res_dict
from data_classes import equipment
from queries import unit_q, equipment_q

mage_list = ["Low tier mage", "Mid tier mage", "High tier mage", "Master tier mage"]
mage_training = ["Low tier magic", "Mid tier magic", "High tier magic"]

# Allows you to override a unit cost, here we're only using it for mages
def unit_cost_override(the_world, the_unit, unit_cost, the_team):
	multiplier = 1
	
	evolutions_lookup	= the_world.evolutions_lookup()
	team_evolutions		= the_team.get_evolutions(the_world.cursor)
	equipment_dict		= the_world.equipment()
	
	if evolutions_lookup['Innately magical'] in team_evolutions:
		# Find out if there's magical training there
		the_unit.get_equipment(the_world.cursor)
		
		found_training = False
		for e in the_unit.equipment:
			the_e = equipment_dict[e]
			if the_e.name in mage_training:
				found_training = True
		
		if found_training:
			level = team_evolutions[evolutions_lookup['Innately magical']]
			if level > 0:
				multiplier = (1-(level*0.04))
			else:
				multiplier = (1+(level*0.04))
	
	deities_lookup		= the_world.deities_lookup()
	
	team_deities = the_team.get_deities(the_world.cursor)
	if deities_lookup['Orakt'] in team_deities:
		orakt_points = team_deities[deities_lookup['Orakt']]
		multiplier = (1+(orakt_points*0.1))
	
	unit_cost *= multiplier
	return unit_cost

def unit_upkeep_override(the_world, the_unit, unit_cost, the_team):
	multiplier = 1
	
	evolutions_lookup	= the_world.evolutions_lookup()
	team_evolutions		= the_team.get_evolutions(the_world.cursor)
	equipment_dict		= the_world.equipment()
	
	if evolutions_lookup['Innately magical'] in team_evolutions:
		# Find out if there's magical training there
		the_unit.get_equipment(the_world.cursor)
		
		found_training = False
		for e in the_unit.equipment:
			the_e = equipment_dict[e]
			if the_e.name in mage_training:
				found_training = True
		
		if found_training:
			level = team_evolutions[evolutions_lookup['Innately magical']]
			if level > 0:
				multiplier = (1-(level*0.04))
			else:
				multiplier = (1+(level*0.04))
	
	unit_cost *= multiplier
	return unit_cost

def print_unit_cost(the_unit, cursor=None, the_world=None, equipment_dict=None, breakdown_mode = False):
	res = the_unit.get_cost(
		cursor=cursor,
		the_world=the_world,
		equipment_dict=equipment_dict,
		breakdown_mode=breakdown_mode,
	)
	
	if breakdown_mode:
		return res
	
	# Not in breakdown mode? Lets format it
	return "(%s/%s, %s/%s)" % (
		res["material_cost"].get("Materials", 0),
		res["iron_cost"].get("Materials", 0),
		res["material_upkeep"].get("Materials", 0),
		res["iron_upkeep"].get("Materials", 0),
	)

def disband_cost(unit_cost):
	"""Returns the money to be made from disbanding a unit"""
	unit_cost.discrete()
	unit_cost *= 0.5
	unit_cost.invert()
	
	return unit_cost