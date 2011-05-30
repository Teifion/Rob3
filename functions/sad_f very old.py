import database
from functions import path_f, cli_f
from queries import city_q, team_q
from classes import team
from rules import sad_rules
import time
import random
import math
import traceback, sys

# 2 = 17.66
# 3 = 
max_hops = 20
class Buy (object):
	def __init__(self, amount, resource, price, buyer, seller, source = None):
		super(Buy, self).__init__()
		self.amount = amount
		self.resource = resource
		self.price = price
		self.seller = seller
		self.buyer = buyer
		
		# Actual price when the buy is compressed
		self.source = source
	
	def get_actual(self):
		if self.source != None:
			return self.source.get_actual()
		else:
			return self.seller
	
	def set_amount(self, new_amount):
		self.amount = new_amount
		if self.source != None:
			self.source.set_amount(new_amount)
	
	def get_2nd_seller(self):
		# B = buyer
		# S = seller
		# 2-5 = nth seller, 2 is the 2nd city to sell
		# B - 5 - 4 - 3 - 2 - S
		
		# If we have an actual source it could be another buy or it could be a city
		if self.source != None:
			return self.source.get_2nd_seller()
		
		# We have no source, that means that we are the 2nd seller Buy instance
		else:
			return self.buyer
	
	def execute(self, root=True):
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
	
	def __str__(self):
		if self.source != None:
			return "<sad_f.Buy seller: %s, Source: %s, price: %s>" % (self.seller.name, self.source, self.price)
		else:
			return "(seller: %s, price: %s)" % (self.seller.name, self.price)
	
	def __repr__(self):
		return str(self)

# http://woarl.com/board/viewtopic.php?f=114&t=3326
max_batches = 9# Shouldn't need more than this
def sad_batch(w):
	city_dict = w.live_cities()
	
	# Reset buys
	for city_id, the_city in city_dict.items():
		the_city.buys = []
		the_city.sells = []
	
	# Find new buys
	find_buys(w, city_dict)
	
	# Hash buys to check data
	buys = []
	for city_id, the_city in city_dict.items():
		buys.extend(the_city.buys)
	
	h = hash("".join([str(b) for b in buys]))
	
	print()
	if h == -2068721650 or h == -1733152074:
		print("Data is correct")
	else:
		print("Data is incorrect: %s" % h)
	print()	
	exit()
	
	# -2068721650 @ 31.76
	# 28.61
	
	# Appove them
	approve_buys(w, city_dict)
	
	# Execute
	execute_buys(w, city_dict)
	
	print("Batch complete\n")

def find_buys(w, city_dict):
	# city_dict = w.live_cities()
	
	# End point stopper
	w.suppliers = {r:set() for r in sad_rules.res_list}
	for city_id, the_city in city_dict.items():
		for r in sad_rules.res_list:
			if the_city.goods[r] > 0:
				w.suppliers[r].add(city_id)
	
	i = 0
	# for city_id, the_city in city_dict.items():
	for city_id, the_city in cli_f.progressbar(city_dict.items(), "Finding buys: ", 60, True):
		needs = the_city.current_demands()
		
		i += 1
		# 20 = 115
		# 100 = 622.5
		# Full data at max hops 2 = 
		# if i >= 10: return
		
		# For each supply we want
		for r in needs:
			prices = []
			for c, d in the_city.connections.items():
				if city_id in city_dict[c].connections:
					prices.append(request_price(w, city_dict, the_city, city_dict[c], r, current_path=[city_id]))
			
			# We want to filter out the best
			best = best_price(prices)
			if best != None:
				# We need to work out how much of this we can afford
				availiable = the_city.wealth/len(needs)
				
				best.set_amount(min(availiable/best.price, -the_city.goods[r]))
				
				the_city.buys.append(best)
				best.get_actual().sells.append(best)

def approve_buys(w, city_dict):
	# city_dict = w.live_cities()
	team_dict = w.teams()
	
	for city_id, the_city in cli_f.progressbar(city_dict.items(), "Approving buys: ", 60, True):
	# for city_id, the_city in city_dict.items():
		
		accepted_sells = []
		
		# We need to work out which sells we're gonna do
		# preferential treatment is given to those that we have a low tax rate to
		# it's possible we can honour more than one sell
		# the sells should all be for just a single supply
		
		# Temporary counters
		goods = sum([(a if a > 0 else 0) for r, a in the_city.goods.items()])
		goods_dict = dict(the_city.goods)
		
		# Keep going while we can
		while goods > 0 and len(accepted_sells) < len(the_city.sells):
			favoured = (999999, None)
			
			for s in the_city.sells:
				if s in accepted_sells: continue
				if w.get_taxes(the_city.team, s.get_2nd_seller()) < favoured[0]:
					favoured = (w.get_taxes(the_city.team, s.buyer.team), s)
			
			# Actual amount needs to be limited
			accepted = favoured[1]
			accepted.set_amount(min(goods_dict[accepted.resource], accepted.amount))
			
			accepted_sells.append(accepted)
			goods -= accepted.amount
			goods_dict[accepted.resource] -= accepted.amount
		
		the_city.sells = accepted_sells

def execute_buys(w, city_dict):
	# city_dict = w.live_cities()
	
	for city_id, the_city in cli_f.progressbar(city_dict.items(), "Executing buys: ", 60, True):
	# for city_id, the_city in city_dict.items():
		for s in the_city.sells:
			s.execute()

# A city doesn't have something, it now asks it's neighbour for it instead
def request_price(w, city_dict, buyer, seller, supply, current_path = [], hops=1):
	# We have it, we can sell it
	if seller.goods.get(supply, 0) > 0:
		price = get_price(w, buyer, seller, supply)
		return Buy(buyer.goods[supply], supply, price, buyer, seller)
	
	# No we don't but we can ask around
	else:
		if seller.id in current_path or hops >= max_hops:
			return None
		
		# Add ourselves to the current path
		current_path.append(seller.id)
		
		prices = []
		
		# 3 = 14, 10 = 50.61
		if hops >= max_hops - 1:
			for c, d in seller.connections.items():
				if c in w.suppliers[supply]:
					prices.append(request_price(w, city_dict, seller, city_dict[c], supply, current_path, hops + 1))
		else:
			for c, d in seller.connections.items():
				prices.append(request_price(w, city_dict, seller, city_dict[c], supply, current_path, hops + 1))
		
		# 3 = 28, 10 = 108
		# for c, d in seller.connections.items():
		# 	prices.append(request_price(w, city_dict, seller, city_dict[c], supply, current_path, hops + 1))
		
		best = best_price(prices)
		
		if best != None:
			actual = get_price(w, buyer, seller, supply, input_price=best.price)
			return Buy(amount=best.amount, resource=supply, price=actual, buyer=buyer, seller=seller, source=best)
		else:
			return None

def _distance(buyer, seller):
	return (1 + (sad_rules.distance_percentage * seller.connections[buyer.id]/100))

def _p(p, i):
	p.append(i)

def get_price(w, buyer, seller, supply, input_price=-1):
	"""
	Price is always made by the code returning a price
	thus any price returned already has the multipliers worked out
	"""
	
	if input_price < 0:
		# Start with base rate, then apply tax
		input_price = sad_rules.base_rate[supply]
	
	# Distance seller -> buyer
	input_price *= _distance(buyer, seller)#(1 + (sad_rules.distance_percentage * seller.connections[buyer.id]/100))
	
	# Taxes
	input_price *= (1 + w.get_taxes(w._teams[seller.team].id, w.teams()[buyer.team].id)/100)
	
	return input_price

def best_price(prices):
	best = (1000, None)
	for p in prices:
		if p == None: continue
		
		if p.price < best[0]:
			best = (p.price, p)
	
	return best[1]

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
		if batches > max_batches:
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

