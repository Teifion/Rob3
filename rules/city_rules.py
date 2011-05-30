import math
from pages import common
from functions import path_f
from classes import world
from rules import team_rules

control_range = 100
max_control_age = 36

def city_control(distance, the_city, team_dict):
	"""How much of a control value does the city have over this square?"""
	if distance == 0:
		return 5000# You control any squares with a city on them
	
	# Nomads can't control much land
	if the_city.nomadic:
		# distance *= 2
		city_age = 1
	else:
		# Age
		city_age = common.current_turn() - the_city.founded
		
		# IRs always count as max age
		if team_dict[the_city.team].ir:
			pass
			# city_age = max_control_age
		
		city_age = min(max_control_age, city_age)
		city_age = max(city_age, 1)
	
	control = (the_city.population/1000.0 * math.sqrt(city_age)) - (distance*distance/15.0)
	control = max(0, math.floor(control))
	return control

def overlap(amount):
	amount = min(100, max(0, amount))
	return (100 - amount) * 0.01

def _hunger_rate(city_size, shortage):	
	if city_size < 0:
		raise ArithmeticError("city_size (%d) cannot be less than 0" % city_size)
	
	if shortage < 0:
		raise ArithmeticError("shortage (%d) cannot be less than 0" % shortage)
	elif shortage == 0:
		return 1, 0
	
	# 0-20% = Slow
	# 20%+ = Deaths
	rate = shortage/city_size
	if rate <= 0.2:
		return 1 - (rate * 5), 0
	else:
		return 0, -(city_size * rate * rate)

def city_growth_rate(cursor, the_team, the_city, the_world=None):
	"""Defines how fast a given city will grow"""
	constant = 0
	
	if the_world == None:
		the_world = world.World()
	
	evolutions_lookup	= the_world.evolutions_lookup()
	deities_lookup		= the_world.deities_lookup()
	buildings_lookup	= the_world.buildings_lookup()
	artefacts_lookup	= the_world.artefacts_lookup()
	
	# Swarm statue
	if artefacts_lookup['Swarm statue'] in the_team.get_artefacts(cursor):
		return 1, 1000
	
	small_size = the_city.population + the_city.slaves
	small_size /= 1000.0
	
	# Overcrowding stuff here
	buildings_completion, buildings_amount = the_city.get_buildings(cursor)
	
	if buildings_lookup['Hospital'] in buildings_amount:
		small_size -= (10 * buildings_amount[buildings_lookup['Hospital']])
	
	if buildings_lookup['Sewer system'] in buildings_amount:
		small_size -= (10 * buildings_amount[buildings_lookup['Sewer system']])
	
	if buildings_lookup['Sewer system'] in buildings_completion:
		small_size -= 10
	
	# Overcrowding bonuses from certain deities
	team_deities = the_team.get_deities(cursor)
	
	# Agashn reduces overcrowding by 10k per favour
	if deities_lookup['Agashn'] in team_deities:
		agashn_points = team_deities[deities_lookup['Agashn']]
		small_size -= (agashn_points*3)
	
	rate = 8 - (small_size - 20) * 0.2
	
	# Evolution?
	team_evos = the_team.get_evolutions(cursor)
	if evolutions_lookup["Population growth"] in team_evos:
		evolution_level = team_evos[evolutions_lookup["Population growth"]]
		if evolution_level > 0:
			rate *= (1+(evolution_level*0.05))
		elif evolution_level < 0:
			rate *= (1+(evolution_level*0.05))
	
	if artefacts_lookup['Fountain of limited youth'] in the_city.get_artefacts(cursor):
		rate *= 2
	
	"""
	# Lack of food?
	team_food = the_team.get_resources(cursor).get("Food") * 1000
	team_size = the_team.get_population(cursor) + the_team.get_slaves(cursor)
	
	# Sliding scale from 100% to 50% then to 0%
	if team_food < team_size:
		if team_food*2 < team_size:
			# Not good, starvation time
			food_ratio = (team_food/float(team_size))
			rate = 1-food_ratio
			rate = -(rate*50)
		else:
			food_ratio = (team_food/float(team_size))
			food_ratio -= 50
			food_ratio *= 2
			food_ratio /= 100.0
			
			rate *= food_ratio
	"""
	
	# New lack of food
	if the_city.surplus_food < 0 and (the_city.founded < common.current_turn() - 1):
		r = _hunger_rate(the_city.size, abs(the_city.surplus_food))
		rate *= r[0]
		constant += r[1]
	
	# Turn into %
	rate = max(rate, 0)
	rate = 1 + (rate/100.0);
	
	# print the_city.name, rate, constant, "<br />"
	return rate, constant


# City 1 is the supplier
def wonder_build_rate(assist_city, wonder_city):
	distance = path_f.pythagoras((assist_city.x, assist_city.y), (wonder_city.x, wonder_city.y))
	
	# Port allows for far greater distances
	if assist_city.port and assist_city.port: distance *= 0.2
	
	supply_size = (assist_city.population + assist_city.slaves)/1000.0
	
	return int(math.floor(max(supply_size - distance, 0)))

# NOT FOR USE IN TRUE SAD RULES
def wealth_rate(the_world, the_city):
	wealth = 0
	
	# Connections/Taxes
	for c, distance in the_city.connections_to.items():
		other_city = the_world._cities[c]
		
		t = 1 + (the_world.get_taxes(the_world._cities[c].team, the_city.team)/100)
		wealth += (1/max(distance, 1) / t)
	
	return wealth

happiness_bonuses = {
	"Basic":			4,
	
	"Allowed wars":		3,
	"Per war":			1,
	
	# Government
	"Monarchy plus":	2,
	"Monarchy minus":	3,
	
	"Democracy plus":	3,
	"Democracy minus":	1,
	
	# Religion
	"National religion plus":	1,
	"National religion minus":	2,
	
	"Chosen deity plus":		3,
	"Chosen deity minus":		3,
	
	# Focus
	"Warlike minus":		2,
	
	"Peaceful plus":		3,
	"Peaceful minus":		2,
	
	"Sailors plus":			1,
	"Sailors minus":		1,
	
	"Mercantile plus":		3,
	"Mercantile minus":		2,
	
	"Educated plus":		1,
	"Educated minus":		2,
	
	"Expansionist plus":	2,
	"Expansionist minus":	1,
	
	"Paranoid plus":		2,
	"Paranoid minus":		3,
	
	"Pious plus":			2,
	"Pious minus":			2,
	
	"Hygienic plus":		2,
	"Hygienic minus":		2,
	
	"Well fed plus":		2,
	"Well fed minus":		1,
	
	"Zealous plus":			1,
	"Zealous minus":		2,
}

def get_happiness(w, the_city, with_breakdown = False):
	trait_lookup = w.traits_lookup()
	building_lookup = w.buildings_lookup()
	
	w.mass_get_team_traits()
	w.mass_get_team_deities()
	w.mass_get_city_buildings()
	w.mass_get_campaign_teams()
	w.mass_get_army_squads()
	w.mass_get_team_resources()
	
	kills = w.kills_from_turn(common.current_turn())
	the_team = w._teams[the_city.team]
	campaign_dict = w.campaigns()
	army_dict = w.armies()
	
	recent_campaigns = w.recent_campaigns(5)
	relevant_recent_campaigns = []
	
	for c in recent_campaigns:
		if the_city.team in campaign_dict[c].teams:
			relevant_recent_campaigns.append(c)
	
	# Base happiness
	breakdown = []
	
	breakdown.append("+%d basic happiness" % happiness_bonuses['Basic'])
	result = happiness_bonuses['Basic']
	
	# Overcrowding
	if int(the_city.population/10000) > 0:
		breakdown.append("-%d for population size" % int(the_city.population/10000))
		result -= int(the_city.population/10000)
	
	# Minus 1 happiness for every war year of war past 2 in the last 5
	if trait_lookup['Warlike'] not in the_team.traits:
		if len(relevant_recent_campaigns) > happiness_bonuses['Allowed wars']:
			war_count = (len(relevant_recent_campaigns) - happiness_bonuses['Allowed wars']) * happiness_bonuses['Per war']
			
			breakdown.append("-%d for wars" % war_count)
			result -= war_count
		
	
	#	GOVERNMENT
	#------------------------
	# Monarchy
	if trait_lookup['Monarchy'] in the_team.traits:
		killed = False
		
		for k in kills:
			if k['victim'] == the_team.leader_id:
				killed = True
		
		if killed:
			breakdown.append("-%d from monarchy" % happiness_bonuses['Monarchy minus'])
			result -= happiness_bonuses['Monarchy minus']
		else:
			breakdown.append("+%d from monarchy" % happiness_bonuses['Monarchy plus'])
			result += happiness_bonuses['Monarchy plus']
	
	# Democracy
	if trait_lookup['Democracy'] in the_team.traits:
		avg_city_size = 0
		for k, v in w.live_cities_from_team(the_team.id).items():
			avg_city_size += v.population
		
		avg_city_size /= len(w.live_cities_from_team(the_team.id))
		avg_city_size /= 1.2
		
		if the_city.population < avg_city_size:
			breakdown.append("-%d from democracy" % happiness_bonuses['Democracy minus'])
			result -= happiness_bonuses['Democracy minus']
		else:
			breakdown.append("+%d from democracy" % happiness_bonuses['Democracy plus'])
			result += happiness_bonuses['Democracy plus']
	
	#	RELIGION
	#------------------------
	# National religion
	if trait_lookup['National religion'] in the_team.traits:
		all_happy = True
		
		for deity_id, favour in the_team.deities.items():
			if favour < 0: all_happy = False
		
		if not all_happy:
			breakdown.append("-%d from national religion" % happiness_bonuses['National religion minus'])
			result -= happiness_bonuses['National religion minus']
		else:
			breakdown.append("+%d from national religion" % happiness_bonuses['National religion plus'])
			result += happiness_bonuses['National religion plus']
	
	# Chosen deity
	if trait_lookup['Chosen deity'] in the_team.traits:
		killed = False
		
		for k in kills:
			if k['victim'] == the_team.leader_id:
				killed = True
		
		if killed:
			breakdown.append("-%d from chosen deity" % happiness_bonuses['Chosen deity minus'])
			result -= happiness_bonuses['Chosen deity minus']
		else:
			breakdown.append("+%d from chosen deity" % happiness_bonuses['Chosen deity plus'])
			result += happiness_bonuses['Chosen deity plus']
	
	#	SOCIETY
	#------------------------
	
	
	#	NATURAL FOCUS
	#------------------------
	# Warlike
	if trait_lookup['Warlike'] in the_team.traits:
		if len(relevant_recent_campaigns) < 4:
			breakdown.append("-%d from lack of wars" % happiness_bonuses['Warlike minus'])
			result -= happiness_bonuses['Warlike minus']
	
	# Mercantile
	if trait_lookup['Mercantile'] in the_team.traits:
		avg_city_wealth = 0
		for k, v in w.live_cities_from_team(the_team.id).items():
			avg_city_wealth += v.wealth
		
		avg_city_wealth /= len(w.live_cities_from_team(the_team.id))
		avg_city_wealth / 1.2
		
		if the_city.wealth < avg_city_wealth:
			breakdown.append("-%d from mercantile" % happiness_bonuses['Mercantile minus'])
			result -= happiness_bonuses['Mercantile minus']
		else:
			breakdown.append("+%d from mercantile" % happiness_bonuses['Mercantile plus'])
			result += happiness_bonuses['Mercantile plus']
	
	# Sailors
	if trait_lookup['Sailors'] in the_team.traits:
		if not the_city.port:
			breakdown.append("-%d from sailors" % happiness_bonuses['Sailors minus'])
			result -= happiness_bonuses['Chosen deity minus']
		else:
			breakdown.append("+%d from sailors" % happiness_bonuses['Sailors plus'])
			result += happiness_bonuses['Sailors plus']
	
	# Educated
	educated_buildings = (
		"University", "Expanded university",
		"Academy", "Expanded academy",
		"Academy of Light",
		"Academy of Dark",
		"Academy of Abjuration",
		"Academy of Destruction",
		"Academy of Daemonic",
		"Academy of Necromancy",
		"Academy of Enchantment",
		"Academy of Alchemy",
		"Academy of Animation",
		"Academy of Sourcery",
	)
	
	if trait_lookup['Educated'] in the_team.traits:
		happy = False
		
		for b in educated_buildings:
			if the_city.buildings_amount.get(building_lookup[b], 0) > 0:
				breakdown.append("+%d from educated (%s)" % (happiness_bonuses['Educated plus'], b))
				result -= happiness_bonuses['Educated plus']
				happy = True
		
		if not happy:
			breakdown.append("-%d from educated" % happiness_bonuses['Educated minus'])
			result -= happiness_bonuses['Educated minus']
	
	# Peaceful
	if trait_lookup['Peaceful'] in the_team.traits:
		if len(relevant_recent_campaigns) > 2:
			breakdown.append("-%d from too many wars" % happiness_bonuses['Peaceful minus'])
			result -= happiness_bonuses['Peaceful minus']
		else:
			breakdown.append("-%d from peace" % happiness_bonuses['Peaceful plus'])
			result -= happiness_bonuses['Peaceful plus']
	
	# Expansionist
	if trait_lookup['Expansionist'] in the_team.traits:
		# Age
		if common.current_turn() - the_city.founded < 5:
			breakdown.append("+%d from expansionist (young city)" % happiness_bonuses['Expansionist plus'])
			result -= happiness_bonuses['Expansionist plus']
		
		# Size
		if not the_city.size > 30000:
			breakdown.append("-%d from expansionist" % happiness_bonuses['Expansionist minus'])
			result -= happiness_bonuses['Expansionist minus']
		else:
			breakdown.append("+%d from expansionist" % happiness_bonuses['Expansionist plus'])
			result += happiness_bonuses['Expansionist plus']
	
	# Paranoid
	if trait_lookup['Paranoid'] in the_team.traits:
		garrison = w.garrison(the_city.id)
	
		if garrison < 1:
			garrison_size = 0
		else:
			garrison_size = army_dict[garrison].get_size(w.cursor)

		if garrison_size < the_city.size/10:
			breakdown.append("-%d from paranoid" % happiness_bonuses['Paranoid minus'])
			result -= happiness_bonuses['Paranoid minus']
		else:
			breakdown.append("+%d from paranoid" % happiness_bonuses['Paranoid plus'])
			result += happiness_bonuses['Paranoid plus']
	
	# Pious
	if trait_lookup['Pious'] in the_team.traits:
		if the_city.buildings_amount.get(building_lookup["Temple"], 0) > 0 or the_city.buildings_amount.get(building_lookup["Expanded temple"], 0) > 0:
			breakdown.append("+%d from pious" % happiness_bonuses['Pious plus'])
			result += happiness_bonuses['Pious plus']
		else:
			breakdown.append("-%d from pious" % happiness_bonuses['Pious minus'])
			result -= happiness_bonuses['Pious minus']
	
	# Hygienic
	if trait_lookup['Hygienic'] in the_team.traits:
		if the_city.buildings_amount.get(building_lookup["Hospital"], 0) > 0 or the_city.buildings_amount.get(building_lookup["Sewer system"], 0) > 0:
			breakdown.append("+%d from hygienic" % happiness_bonuses['Hygienic plus'])
			result += happiness_bonuses['Hygienic plus']
		else:
			breakdown.append("-%d from hygienic" % happiness_bonuses['Hygienic minus'])
			result -= happiness_bonuses['Hygienic minus']
	
	# Well fed
	if trait_lookup['Well fed'] in the_team.traits:
		food_amount = int(the_team.resources.get("Food"))
		needed = team_rules.resource_needed(w.cursor, "Food", the_team, the_world=w)
		food_ratio = food_amount/float(needed)
	
		if food_ratio < 1.1:
			breakdown.append("-%d from well fed" % happiness_bonuses['Well fed minus'])
			result -= happiness_bonuses['Well fed minus']
		else:
			breakdown.append("+%d from well fed" % happiness_bonuses['Well fed plus'])
			result += happiness_bonuses['Well fed plus']
	
	# Zealous, identical to National religion
	if trait_lookup['Zealous'] in the_team.traits:
		all_happy = True
	
		for deity_id, favour in the_team.deities.items():
			if favour < 0: all_happy = False
	
		if not all_happy:
			breakdown.append("-%d from zealous" % happiness_bonuses['Zealous minus'])
			result -= happiness_bonuses['Zealous minus']
		else:
			breakdown.append("+%d from zealous" % happiness_bonuses['Zealous plus'])
			result += happiness_bonuses['Zealous plus']
	
	if with_breakdown:
		return result, breakdown
	return result
	



