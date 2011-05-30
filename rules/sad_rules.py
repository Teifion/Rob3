from pages import common
import math
import collections
from rules import map_data

wealth_retention_rate = lambda w: math.sqrt(w*10)
wealth_age_limit = 15

segregated_multiplier = 1.2
distance_power = 1.1
min_trade_distance = 10
max_trade_history_bonus = 2

max_trade_travel_time = 182
max_trade_travel_time = 90
# max_trade_travel_time = 50

# Used to allow us to skip pathing for trade_f.build_distance_matrix
max_crow_dist_land	= map_data.movement_speeds['Merchant'] * max_trade_travel_time
max_crow_dist_water	= map_data.movement_speeds['Sailing'] * max_trade_travel_time

# How much 1 unit of distance makes to a price
distance_percentage		= 0.01

trade_distance			= lambda d: d ** distance_power
reverse_trade_distance	= lambda d: d ** (1/distance_power)
distance_from_equator	= lambda y: abs(y-2000)

def tech_bonus(level, bonus_per_level):
	return 1 + (level * bonus_per_level/100)

def clean_output(orig_func):
	def temp_func(w, city, team):
		r = orig_func(w, city, team)
		
		if r == int(r):
			return int(r)
		
		return r
	return temp_func

# Only ever done in batch so may as well expect a world
def produce_wealth(the_world, the_city):
	if the_city.size < 5000:
		the_city.wealth = 0
		return
	
	the_city.wealth = wealth_retention_rate(the_city.wealth)
	
	
	age = common.current_turn() - the_city.founded
	# w = (the_city.size * the_city.size) * (1 + min(age, wealth_age_limit)/100)
	# w = (the_city.size/1000 * the_city.size/1000) * (1 + min(age, wealth_age_limit)/100)
	
	s = the_city.size/1000
	w = (s * s)
	w = math.floor(w/1000)
	
	the_city.wealth = w

res_list = (
	"Grain", "Linen", "Wool",
	"Pottery", "Olives", "Wine", "Dairy", "Meat", "Salt",
	"Silk", "Furs", "Gems", "Glass", "Precious metals", "Spices",
	# *Location specific production*
)

basic_list	= ("Grain", "Linen", "Wool")
nice_list	= ("Pottery", "Olives", "Wine", "Dairy", "Meat", "Salt")
luxury_list	= ("Silk", "Furs", "Gems", "Glass", "Precious metals", "Spices")
exotic_list	= ()

# 2 basic
# 7 nice
# 6 luxury

"""
Each city should statistically have:
	90% of each basic
	40% of each nice
	15% of each luxury
	0-1% of each exotic

Wrong Total amount = (0.9*2) + (0.4*7) + (0.15 * 6) = 5.5
Total amount = 2+7+6 = 15

Assuming an average city size of 1 each city should produce around:
Basic: 13.5 units
Nice: 6 units
Luxury: 2.25 units
Exotic: 1 unit

At 20k in size:
Basic: 270 units
Nice: 120 units
Luxury: 45 units
Exotic: 20 units

"""

# Basic: Grain, Linen*, Wool*
# Wants: Pottery, Olives, Wine, Dairy, Meat, Salt
# Luxury: Silk, Furs, Gems, Glass, Precious metals, Spices
# Exotic: *Location specific production*

# Basics give a 4% bonus to material production
# Wants give a 5% bonus to production
# Luxuries give a 6% bonus to production
# Exotics give a 7% bonus to production

# map_data.terrain = ["water", "lowlands", "shore", "hills", "mountains", "swamp", "N/A", "desert", "lake", "forest", "river", "large river", "N/A", "N/A", "forest swamp", "volcano"]

_terrain_factor_s = {
	#						Wat		Low		Sho		Hil		Mou		Swa		N/A		Des		Lak		For		Riv		LRi		N/A		N/A		FSw		Vol
	"Grain":			[	0.0,	1.3,	1.25,	1.1,	0.7,	1.2,	0,		0.5,	0.0,	1.0,	1.2,	1.2,	0,		0,		1.0,	0.7],
	"Linen":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Wool":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Pottery":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Olives":			[	0.0,	1.1,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Wine":				[	0.0,	1.1,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Dairy":			[	0.0,	1.1,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Meat":				[	0.0,	1.1,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Salt":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Silk":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Furs":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Gems":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Glass":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Precious metals":	[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Spices":			[	0.0,	1.1,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
}

base_rate = {
	"Grain":			1,
	"Linen":			1,
	"Wool":				1,
	"Pottery":			1,
	"Olives":			1,
	"Wine":				1,
	"Dairy":			1,
	"Meat":				1,
	"Salt":				1,
	"Silk":				1,
	"Furs":				1,
	"Gems":				1,
	"Glass":			1,
	"Precious metals":	1,
	"Spices":			1,
}


# Result of even distribution of production
supply_factor = {'Pottery': 6.601787881940771, 'Gems': 2.558853970602346, 'Olives': 22.9159988111362, 'Spices': 1.1407954788004537, 'Meat': 6.408739851698628, 'Glass': 2.371292632953878, 'Furs': 3.152310614597031, 'Linen': 9.79312952584373, 'Grain': 61.35823292235257, 'Precious metals': 2.381284871551449, 'Dairy': 6.166689003626762, 'Wool': 10.222057699427234, 'Salt': 6.356118663580839, 'Silk': 2.391169696686954, 'Wine': 6.181125413700849}

# Result of even random distribution of production
supply_factor = {'Pottery': 6.49309375230867, 'Gems': 2.4847104441139214, 'Olives': 21.4161080405776, 'Wool': 9.916548775201212, 'Meat': 6.267677167097126, 'Glass': 2.4031539704392837, 'Furs': 3.1352574196868255, 'Linen': 9.920428114104146, 'Grain': 62.38228853799035, 'Precious metals': 2.4071910457779957, 'Dairy': 6.239902709585061, 'Spices': 0.6659203703862477, 'Salt': 6.46571778093453, 'Silk': 2.412604099763663, 'Wine': 6.3827407952959145}


@clean_output
def _grain_supply(w, city, team):
	# supply = min(city.size/1000, 50)
	supply = math.sqrt(city.size/1000) * supply_factor['Grain']
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 4)
	supply *= _terrain_factor_s['Grain'][city.terrain]
	
	# 1 down to 0
	if distance_from_equator(city.y) >= 1000:
		supply /= (distance_from_equator(city.y)/1000)
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Grain', 1)
	return supply

@clean_output
def _linen_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Linen']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 3)
	supply *= _terrain_factor_s['Linen'][city.terrain]
	
	supply *= city.trade_history.get('Linen', 1)
	return supply

@clean_output
def _wool_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Wool']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 3)
	supply *= _terrain_factor_s['Wool'][city.terrain]
	
	supply *= city.trade_history.get('Wool', 1)
	return supply

@clean_output
def _pottery_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Pottery']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 4)
	supply *= _terrain_factor_s['Pottery'][city.terrain]
	
	supply *= city.trade_history.get('Pottery', 1)
	return supply

@clean_output
def _olives_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Olives']
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 4)
	supply *= _terrain_factor_s['Olives'][city.terrain]
	
	# If you are more than 750 units from the equator you cannot produce olives
	dist = (750-distance_from_equator(city.y))/750
	supply *= max(dist, 0)
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Olives', 1)
	return supply

@clean_output
def _wine_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Wine']
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 3)
	supply *= _terrain_factor_s['Wine'][city.terrain]
	
	if distance_from_equator(city.y) >= 1000:
		supply /= (distance_from_equator(city.y)/1000)
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Wine', 1)
	return supply

@clean_output
def _dairy_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Dairy']
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 2)
	supply *= _terrain_factor_s['Dairy'][city.terrain]
	
	if distance_from_equator(city.y) >= 1500:
		supply /= (distance_from_equator(city.y)/1500)
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Dairy', 1)
	return supply

@clean_output
def _meat_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Meat']
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 2)
	supply *= _terrain_factor_s['Meat'][city.terrain]
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Meat', 1)
	return supply

@clean_output
def _salt_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Salt']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 2)
	supply *= _terrain_factor_s['Salt'][city.terrain]
	
	supply *= city.trade_history.get('Salt', 1)
	return supply

@clean_output
def _silk_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Silk']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 3)
	supply *= _terrain_factor_s['Silk'][city.terrain]
	
	supply *= city.trade_history.get('Silk', 1)
	return supply

@clean_output
def _furs_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Furs']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 2)
	supply *= _terrain_factor_s['Furs'][city.terrain]
	
	# Further is better, further = colder and thus more furry things
	if distance_from_equator(city.y) <= 1000:
		supply *= (distance_from_equator(city.y)/1000)
	
	supply *= city.trade_history.get('Furs', 1)
	return supply

@clean_output
def _gems_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Gems']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 1)
	supply *= _terrain_factor_s['Gems'][city.terrain]
	
	if 'Stone' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Gems', 1)
	return supply

@clean_output
def _glass_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Glass']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 1)
	supply *= _terrain_factor_s['Glass'][city.terrain]
	
	supply *= city.trade_history.get('Glass', 1)
	return supply

@clean_output
def _precious_metals_supply(w, city, team):
	supply = min(city.size/1000, 50) * supply_factor['Precious metals']
	supply *= tech_bonus(team.tech_levels.get('Economy', 0), 1)
	supply *= _terrain_factor_s['Precious metals'][city.terrain]
	
	if 'Iron' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Precious metals', 1)
	return supply

@clean_output
def _spices_supply(w, city, team):
	supply = min(city.size/1000, 50) * 4
	supply *= tech_bonus(team.tech_levels.get('Farming', 0), 1)
	supply *= _terrain_factor_s['Spices'][city.terrain]
	
	if distance_from_equator(city.y) >= 1000:
		supply /= (distance_from_equator(city.y)/1000)
	
	if 'Fertile lands' in city.supplies:
		supply *= 2
	
	supply *= city.trade_history.get('Spices', 1)
	return supply

supply = {
	"Grain":			_grain_supply,
	"Linen":			_linen_supply,
	"Wool":				_wool_supply,
	"Pottery":			_pottery_supply,
	"Olives":			_olives_supply,
	"Wine":				_wine_supply,
	"Dairy":			_dairy_supply,
	"Meat":				_meat_supply,
	"Salt":				_salt_supply,
	"Silk":				_silk_supply,
	"Furs":				_furs_supply,
	"Gems":				_gems_supply,
	"Glass":			_glass_supply,
	"Precious metals":	_precious_metals_supply,
	"Spices":			_spices_supply,
}


# Demands for XYZ
_terrain_factor_d = {
	#						Wat		Low		Sho		Hil		Mou		Swa		N/A		Des		Lak		For		Riv		LRi		N/A		N/A		FSw		Vol
	"Grain":			[	0.0,	0.7,	0.75,	0.9,	0.7,	1.0,	0,		1.5,	0.0,	1.0,	0.8,	0.8,	0,		0,		1.0,	1.3],
	"Linen":			[	0.0,	0.9,	0.9,	1.0,	0.9,	0.8,	0,		0.7,	0.0,	1.0,	0.9,	0.9,	0,		0,		1.0,	1.0],
	"Wool":				[	0.0,	0.9,	0.9,	1.0,	0.9,	0.8,	0,		0.7,	0.0,	1.0,	0.9,	0.9,	0,		0,		1.0,	1.0],
	"Pottery":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Olives":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Wine":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Dairy":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Meat":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Salt":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Silk":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Furs":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Gems":				[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Glass":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Precious metals":	[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
	"Spices":			[	0.0,	1.0,	1.0,	1.0,	1.0,	1.0,	0,		1.0,	0.0,	1.0,	1.0,	1.0,	0,		0,		1.0,	1.0],
}


@clean_output
def _grain_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Grain'][city.terrain]
	return demand

@clean_output
def _linen_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= distance_from_equator(city.y)/2000 + ((city.size/1000)*0.01)
	demand *= _terrain_factor_d['Linen'][city.terrain]
	
	return demand

@clean_output
def _wool_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= distance_from_equator(city.y)/2000 + ((city.size/1000)*0.01)
	demand *= _terrain_factor_d['Wool'][city.terrain]
	
	return demand

@clean_output
def _pottery_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Pottery'][city.terrain]
	return demand

@clean_output
def _olives_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Olives'][city.terrain]
	return demand

@clean_output
def _wine_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Wine'][city.terrain]
	return demand

@clean_output
def _dairy_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Dairy'][city.terrain]
	return demand

@clean_output
def _meat_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Meat'][city.terrain]
	return demand

@clean_output
def _salt_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Salt'][city.terrain]
	return demand

@clean_output
def _silk_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Silk'][city.terrain]
	return demand

@clean_output
def _furs_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Furs'][city.terrain]
	demand *= distance_from_equator(city.y)/2000 + ((city.size/1000)*0.01)
	
	return demand

@clean_output
def _gems_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Gems'][city.terrain]
	return demand

@clean_output
def _glass_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Glass'][city.terrain]
	return demand

@clean_output
def _precious_metals_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Precious metals'][city.terrain]
	return demand

@clean_output
def _spices_demand(w, city, team):
	demand = int(city.size/1000)
	demand *= _terrain_factor_d['Spices'][city.terrain]
	return demand


demand = {
	"Grain":			_grain_demand,
	"Linen":			_linen_demand,
	"Wool":				_wool_demand,
	"Pottery":			_pottery_demand,
	"Olives":			_olives_demand,
	"Wine":				_wine_demand,
	"Dairy":			_dairy_demand,
	"Meat":				_meat_demand,
	"Salt":				_salt_demand,
	"Silk":				_silk_demand,
	"Furs":				_furs_demand,
	"Gems":				_gems_demand,
	"Glass":			_glass_demand,
	"Precious metals":	_precious_metals_demand,
	"Spices":			_spices_demand,
}