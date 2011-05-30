import database
from functions import path_f, cli_f
from queries import city_q, team_q
from classes import team
from rules import sad_rules
import time
import random
import math
import traceback, sys

# http://woarl.com/board/viewtopic.php?f=114&t=3326
# max_batches = 100# Shouldn't need more than this
config = {
	"batches":	100,
	"hops":		1,
	"max hops":	20,
}

def sad_batch(w, verbose=True):
	city_dict = w.live_cities()
	
	# raise Exception("Alter wealth production rate")
	# raise Exception("Make it so cities take into account what they can afford")
	
	# Reset buys
	total_demand = 0
	total_surplus = 0
	wealth = 0
	need_len = 0
	cities_needing_grain = 0
	for city_id, the_city in city_dict.items():
		the_city.buys = []
		the_city.sells = []
		
		
		total_demand += sum([(-a if a < 0 else 0) for r, a in the_city.goods.items()])
		# total_demand += (-the_city.goods['Grain'] if the_city.goods['Grain'] < 0 else 0)
		total_surplus += sum([(a if a > 0 else 0) for r, a in the_city.goods.items()])
		# total_surplus += (the_city.goods['Grain'] if the_city.goods['Grain'] > 0 else 0)
		wealth += the_city.wealth
		
		if the_city.goods['Grain'] < 0:
			cities_needing_grain += 1
		
		need_len += len(the_city.current_demands())
	
	# 451
	print("Kruzen: %s" % str(city_dict[451].goods))
	print("Kruzen: %s" % str(city_dict[451].wealth))
	print("Demand: %s, Avg demand: %s" % (total_demand, total_demand/len(city_dict.keys())))
	print("Surplus: %s" % total_surplus)
	print("Wealth: %s, avg wealth: %s" % (wealth, wealth/len(city_dict.keys())))
	print("cities_needing_grain: %s" % cities_needing_grain)
	print("Avg needs: %s" % (need_len/len(city_dict.keys())))
	
	# Find new buys
	find_buys(w, city_dict, verbose)
	
	# Appove them
	approve_buys(w, city_dict, verbose)
	
	sale_total = 0
	for city_id, the_city in city_dict.items():
		for s in the_city.sells:
			# print(s)
			sale_total += s[2]
	
	print("Quantity sold: %s" % sale_total)
	
	# Execute
	execute_buys(w, city_dict, verbose)
	
	print("Batch complete\n")

def find_buys(w, city_dict, verbose=True):
	# city_dict = w.live_cities()
	
	# End point stopper
	# w.suppliers = {r:set() for r in sad_rules.res_list}
	# for city_id, the_city in city_dict.items():
	# 	the_city.best_price = {}
	# 	
	# 	for r in sad_rules.res_list:
	# 		if the_city.goods[r] > 0:
	# 			w.suppliers[r].add(city_id)
	
	for city_id, the_city in city_dict.items():
		the_city.needs_cache = the_city.current_demands()
	
	
	if verbose:
		it = cli_f.progressbar(range(0, config['hops']+1), "Hopping: ", 60, True)
	else:
		it = range(0, config['hops']+1)
	
	for h in it:
	# for h in range(0, max_hops+1):
		# for city_id, the_city in cli_f.progressbar(city_dict.items(), "Hopping %d: " % h, 60, True):
		for city_id, the_city in city_dict.items():
			_discover(w, city_dict, the_city, h)
	
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "Finding buys: ", 60, True)
	else:
		it = city_dict.items()
	
	for city_id, the_city in it:
		if the_city.wealth <= 5: continue
		
		needs = the_city.current_demands()
		
		offers = {}
		for r in needs:
			offers[r] = []
		
		# For each supply we want
		for c, d in the_city.connections.items():
			if city_id in city_dict[c].connections:
				for r in needs:
					if city_dict[c].best_price[config['hops']][r][0] > 1000: continue
					
					# Price is made from price saved at other city times the get_price multiplier
					offer_price = get_price(w, the_city, city_dict[c]) * city_dict[c].best_price[config['hops']][r][0]
					availiable = the_city.wealth/len(needs)
					amount = min(availiable/offer_price, -the_city.goods[r])
					offers[r].append((offer_price, list(city_dict[c].best_price[config['hops']][r][1]) + [the_city.id], amount))
		
		# Now to turn them into Buys
		for r in needs:
			availiable = the_city.wealth/len(needs)
			amount_needed = -the_city.goods[r]
			
			while amount_needed > 0 and len(offers[r]) > 0:
				best_offer = None
				best_price = 99999
				
				for i, o in enumerate(offers[r]):
					if o[0] < best_price:
						best_offer = i
						best_price = o[0]
				
				accepted_offer = offers[r][best_offer]
				
				del(offers[r][best_offer])
				
				# print("")
				# print(accepted_offer)
				city_dict[accepted_offer[1][0]].sells.append((r, accepted_offer[1], accepted_offer[2]))

# Asks the city what the best price it can get for a given supply is in a certain range
# Best price is a tuple (price, city_pathway)
# Cost: 9999 = can't get it
# Pathway uses a stack system, build from supplier, read from buyer
def _discover(w, city_dict, the_city, hops_allowed=0):
	# If 0 hops then we're looking at suppliers
	if hops_allowed == 0:
		the_city.best_price[0] = {}
		for r in sad_rules.res_list:
			if the_city.goods[r] > 0:
				the_city.best_price[0][r] = (sad_rules.base_rate[r], [the_city.id])
			else:
				the_city.best_price[0][r] = (9999, [])
		
	# If we can hop then we check our neighbours for their best hop -1
	else:
		# Start by setting best price as what we can do with 1 fewer hop
		if hops_allowed in the_city.best_price:
			tot = sum([a[0] for r, a in the_city.best_price[hops_allowed].items()])
			if tot < 5:
				print(tot)
		the_city.best_price[hops_allowed] = {}
		
		for r in sad_rules.res_list:
			the_city.best_price[hops_allowed][r] = the_city.best_price[hops_allowed-1][r]
		
		# Now to try it with one more hop!
		for c, d in the_city.connections.items():
			if the_city.id in city_dict[c].connections:
				for r in sad_rules.res_list:
					if city_dict[c].best_price[hops_allowed-1][r][0] > 1000: continue
					
					best_price = the_city.best_price[hops_allowed-1][r][0]
					
					# Price is made from price saved at other city times the get_price multiplier
					new_price = get_price(w, the_city, city_dict[c]) * city_dict[c].best_price[hops_allowed-1][r][0]
					
					if new_price < best_price:
						the_city.best_price[hops_allowed][r] = (new_price, list(city_dict[c].best_price[hops_allowed-1][r][1]) + [the_city.id])

price_cache = {}
def get_price(w, buyer, seller):
	"""
	Price is always made by the code returning a price
	thus any price returned already has the multipliers worked out
	"""
	
	# Call count: 4360709 (that's with max_hops = 9)
	# No cache - 18.52, time in func: 4.7, approx time per city: 2.0s
	# With cache - 16.87, time in func: 3.4, approx time per city: 1.7s
	
	if (buyer.id, seller.id) not in price_cache:
		price_cache[(buyer.id, seller.id)] = (w.distance_cache[(seller.id, buyer.id)]) * (1 + w.tax_cache[(seller.team, buyer.team)]/100)
	return price_cache[(buyer.id, seller.id)]

def approve_buys(w, city_dict, verbose=True):
	team_dict = w.teams()
	
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "Approving buys: ", 60, True)
	else:
		it = city_dict.items()
	
	sales_count = 0
	sales_lowered = 0
	
	for city_id, the_city in it:
		if len(the_city.sells) == 0: continue
		
		# print("\n\n")
		# print(the_city.sells)
		# exit()
		
		accepted_sells = []
		marked_sells = []
		
		# We need to work out which sells we're gonna do
		# preferential treatment is given to those that we have a low tax rate to
		# it's possible we can honour more than one sell
		# the sells should all be for just a single supply
		
		# If the sells are not for a single supply it will be an inefficent system as only 1 favoured is tracked
		
		# Temporary counters
		goods = sum([(a if a > 0 else 0) for r, a in the_city.goods.items()])
		goods_dict = dict(the_city.goods)
		
		# Keep going while we can
		i = 0
		while goods > 0 and len(accepted_sells) < len(the_city.sells):
			i += 1
			if i > 100:
				break
			
			favoured = None
			favoured_tax = 9999
			
			for i, s in enumerate(the_city.sells):
				if i in marked_sells: continue
				
				# s[1] is the path
				# 0 is us
				# 1 is the first buyer
				buyer = s[1][1]
				
				if w.tax_cache[(the_city.team, city_dict[buyer].team)] < favoured_tax:
					favoured_i = i
					favoured = s
					favoured_tax = w.tax_cache[(the_city.team, city_dict[buyer].team)]
			
			# print("Fav: %s, %s" % (favoured_tax, str(favoured)))
			
			# Actual amount needs to be limited
			# marked_sells.append(favoured)
			marked_sells.append(favoured_i)
			final_buyer = favoured[1][-1]
			r = favoured[0]
			
			sales_count += 1
			if goods_dict[r] < favoured[2]:
				sales_lowered += 1
			
			amount = min(goods_dict[r], favoured[2])
			
			# print(amount, "                        ")
			
			# Move counters, add amount to the sell
			favoured = (favoured[0], favoured[1], amount)
			accepted_sells.append(favoured)
			goods -= amount
			goods_dict[r] -= amount
			
			# goods = -100
		
		the_city.sells = accepted_sells
		# for s in the_city.sells:
		# 	print(s)
		# exit()
	
	print("Sale count: %s" % sales_count)
	print("Sales lowered: %s" % sales_lowered)

def execute_buys(w, city_dict, verbose=True):
	# city_dict = w.live_cities()
	
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "Executing buys: ", 60, True)
	else:
		it = city_dict.items()
	
	for city_id, the_city in it:
		for s in the_city.sells:
			_execute(w, city_dict, s)


def _execute(w, city_dict, sell):
	"""
	if self.source != None:
		self.source.execute(root=False)
	else:
		self.seller.goods[self.resource] -= self.amount
	
	loss = self.price - (self.price / (_distance(self.buyer, self.seller)))
	
	# Loss is paid by buyer but never reaches the seller
	self.seller.wealth += self.price - loss
	self.buyer.wealth -= self.price
	
	if root:
		self.buyer.goods[self.resource] += self.amount
	"""
	
	# Aliases
	r = sell[0]
	route = sell[1]
	amount = sell[2]
	
	# Split up the route into city pairs
	path = []
	for i in range(1, len(route)):
		path.append((route[i-1], route[i]))
	
	# For each path part, redistribute wealth
	# price_counter = sad_rules.base_rate[r]
	previous_sale = sad_rules.base_rate[r] * amount
	for seller, buyer in path:
		# price_cache[(buyer.id, seller.id)] = (w.distance_cache[(seller.id, buyer.id)]) * (1 + w.tax_cache[(seller.team, buyer.team)]/100)
		
		# Sell with distance and tax taken into account
		sale_price = previous_sale * price_cache[(buyer, seller)]
		
		# Seller gets price without the distance, that's lost
		profit = sale_price/w.distance_cache[(seller, buyer)]
		
		# Apply wealth difference
		city_dict[seller].wealth += profit
		city_dict[buyer].wealth -= sale_price
		
		previous_sale = sale_price
	
	# Apply difference to first buyer and seller's goods
	buyer = route[-1]
	seller = route[0]
	
	city_dict[buyer].goods[r] += amount
	city_dict[seller].goods[r] -= amount

def supply_and_demand(the_world):
	city_dict = the_world.live_cities()
	team_dict = the_world.active_teams()
	
	the_world.mass_get_team_techs()
	the_world.mass_get_team_deities()
	the_world.mass_get_team_evolutions()
	
	# Randomise city production type
	random.seed()
	r = -1
	for k, v in city_dict.items():
		r += 1
		if r >= len(sad_rules.res_list): r = 0
		v.supply_good = r
		# v.supply_good = random.randrange(0, len(sad_rules.res_list))
	
	# Build a cache of taxes and borders
	the_world.tax_cache = {}
	# the_world.border_cache = {}
	for t1 in team_dict.keys():
		for t2 in team_dict.keys():
			if t1 == t2:
				the_world.tax_cache[(t1, t2)] = 0
			else:
				the_world.tax_cache[(t1, t2)] = the_world.get_taxes(t1, t2)
				# the_world.border_cache[(t1, t2)] = the_world.get_border(t1, t2)
	
	# Build a distance cache, K1 going to K2
	the_world.distance_cache = {}
	for k1, c1 in city_dict.items():
		for k2, c2 in city_dict.items():
			if k1 == k2:
				the_world.distance_cache[(k1, k2)] = 0
			else:
				if k2 in c1.connections:
					the_world.distance_cache[(k1, k2)] = (1 + (sad_rules.distance_percentage * c1.connections[k2]/100))
	
	# Total, Min, Max
	production = {r:[0, 9999, -9999] for r in sad_rules.res_list}
	demand = {r:[0, 9999, -9999] for r in sad_rules.res_list}
	wealth = [0, 9999, -9999]
	
	city_count = len(city_dict.keys())
	city_size = sum([c.size for i, c in city_dict.items()])/city_count
	
	# First work out demand
	for city_id, the_city in city_dict.items():
		sad_rules.produce_wealth(the_world, the_city)
		wealth[0] += the_city.wealth
		wealth[1] = min(wealth[1], the_city.wealth)
		wealth[2] = max(wealth[2], the_city.wealth)
		the_city.satisfied = False
		
		for r in sad_rules.res_list:
			d = sad_rules.demand[r](the_world, the_city, the_world._teams[the_city.team])
			demand[r][0] += d
			demand[r][1] = min(d, demand[r][1])
			demand[r][2] = max(d, demand[r][2])
			the_city.goods[r] = -d
		
		if the_city.goods["Linen"] > the_city.goods["Wool"]:
			the_city.wool_is_nice = True
		
		city_supply = sad_rules.res_list[the_city.supply_good]
		
		p = sad_rules.supply[city_supply](the_world, the_city, the_world._teams[the_city.team])
		production[city_supply][0] += p
		production[city_supply][1] = min(p, production[city_supply][1])
		production[city_supply][2] = max(p, production[city_supply][2])
		the_city.goods[city_supply] += p
		# print(sad_rules.supply["Grain"](the_city, the_world._teams[the_city.team].tech_levels), sad_rules.demand["Grain"](the_city, the_world._teams[the_city.team].tech_levels))
	
	pre_report = generate_sad_pre_report(the_world)
	
	# Now begin to satisfy it
	satisfied = False
	batches = 0
	while not satisfied:
		sad_batch(the_world)
		
		satisfied = True
		for city_id, the_city in city_dict.items():
			if not the_city.satisfied and the_city.wealth > 0:
				satisfied = False
		
		# Force a breakout
		batches += 1
		config['hops'] = min(config['hops'] + 1, config['max hops'])
		if batches > config['batches']:
			satisfied = True
	
	post_report = generate_sad_post_report(the_world)
	
	# print(pre_report['res_surplus']['Grain'])
	
	return {
		"pre": pre_report,
		"post": post_report,
		"production": production,
		"demand": demand,
		"wealth": wealth,
	}

def print_reports(the_world, report_dict, reports=['res_summary', 'production', 'demand', 'wealth']):
	city_dict = the_world.cities()
	
	city_count = len(city_dict.keys())
	city_size = sum([c.size for i, c in city_dict.items()])/city_count
	
	if 'res_summary' in reports:
		print(print_res_dict(report_dict['pre']['res_summary'],		the_world, "''Summary''"), "\n")
	
	if 'res_surplus' in reports:
		print(print_res_dict(report_dict['pre']['res_surplus'],		the_world, "''Surplus''"), "\n")
	
	if 'res_demand' in reports:
		print(print_res_dict(report_dict['pre']['res_demand'],		the_world, "''Demand''"), "\n")
	
	if 'res_producers' in reports:
		print(print_res_dict(report_dict['pre']['res_producers'],	the_world, "''Producers'' (out of %d)" % city_count), "\n")
	
	ksize = city_size/1000
	
	if 'production' in reports:
		production = report_dict['production']
		print(database.shell_text("''Production''           Min    Max    Avg   Ratio"))
		for r in sad_rules.res_list:
			avg = production[r][0]/city_count
		
			print("{res:17} {min:6} {max:6} {avg:6} {ratio:6}".format(
				res = r,
				total = production[r][0],
				min = round(production[r][1], 2),
				max = round(production[r][2], 2),
				avg = round(avg, 2),
				ratio = round(avg/ksize, 2),
			))
		print("")
	
	if 'demand' in reports:
		demand = report_dict['demand']
		
		print(database.shell_text("\n''Demand''               Min    Max    Avg   Ratio"))
		for r in sad_rules.res_list:
			avg = demand[r][0]/city_count
		
			print("{res:17} {min:6} {max:6} {avg:6} {ratio:6}".format(
				res = r,
				total = demand[r][0],
				min = round(demand[r][1], 2),
				max = round(demand[r][2], 2),
				avg = round(avg, 2),
				ratio = round(avg/ksize, 2),
			))
	
	if 'wealth' in reports:
		wealth = report_dict['wealth']
		avg = wealth[0]/city_count
		
		print(database.shell_text("\n''Wealth''\n   Min    Max    Avg   Ratio"))
		print("{min:6} {max:6} {avg:6} {ratio:6}".format(
			total = wealth[0],
			min = round(wealth[1], 2),
			max = round(wealth[2], 2),
			avg = round(avg, 2),
			ratio = round(avg/ksize, 2),
		))
	
	# Attempt at ratios
	if 'ratios' in reports:
		print(database.shell_text("\n''Ratios''"))
		# print(report_dict['pre'].keys())
		production = report_dict['production']
		demand = report_dict['demand']
		for r in sad_rules.res_list:
			print("{res:17} {ratio:6}".format(
				res = r,
				ratio = round(production[r][0]/demand[r][0], 2),
			))

def print_res_dict(res_dict, the_world, title="", one_line=False):
	city_dict = the_world.live_cities()
	output = []
	
	if title != "":
		output.append(database.shell_text(title))
	
	for r in sad_rules.res_list:
		output.append("{0}: {1} avg: {2}".format(r, res_dict[r], round(res_dict[r]/len(the_world.live_cities()), 2)))
	
	return "\n".join(output)

def generate_sad_pre_report(the_world):
	"""Runs through the cities of the world and finds out how many of them have XYZ"""
	city_dict = the_world.live_cities()
	
	res_summary		= {r:0 for r in sad_rules.res_list}
	res_surplus		= {r:0 for r in sad_rules.res_list}
	res_demand		= {r:0 for r in sad_rules.res_list}
	res_producers	= {r:0 for r in sad_rules.res_list}
	
	for city_id, the_city in city_dict.items():
		res_producers[sad_rules.res_list[the_city.supply_good]] += 1
		for r in sad_rules.res_list:
			amount = the_city.goods[r]
			
			if amount > 0:
				res_surplus[r] += amount
			else:
				res_demand[r] -= amount
			res_summary[r] += amount
	
	return {
		"res_producers":	res_producers,
		"res_summary":		res_summary,
		"res_surplus":		res_surplus,
		"res_demand":		res_demand,
	}

def generate_sad_post_report(the_world):
	"""Runs through the cities of the world and finds out how many of them have XYZ"""
	city_dict = the_world.live_cities()
	
	return {}

