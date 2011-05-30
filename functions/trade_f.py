import database
from functions import path_f, cli_f
from queries import city_q, team_q
from classes import team
from rules import sad_rules
import time
import random
import math

class DeadPath (object):
	def __init__(self, time_cost):
		super(DeadPath, self).__init__()
		self.time_cost = time_cost


def build_distance_matrix(the_world, verbose=False):
	borders		= the_world.relations()
	city_dict	= the_world.live_cities()
	
	# print(borders)
	# exit()
	
	distance_matrix = {}
	city_contintent = {}
	
	func_start = time.time()
	
	i = 0
	paths = 0
	
	it = city_dict.items()
	if verbose:
		it = cli_f.progressbar(city_dict.items(), "Pathing:", 60, True)
	
	worst_land_path = (-1, -1, -1)
	worst_water_path = (-1, -1, -1)
	for i1, c1 in it:
		# i1 = 1224
		# c1 = city_dict[i1]
		
		started = time.time()
		links = 0
		
		i += 1
		
		if i1 not in city_contintent:
			city_contintent[i1] = path_f.get_continent(the_world.cursor, (c1.x, c1.y))
		
		for i2, c2 in city_dict.items():
			# i2 = 1280
			# c2 = city_dict[i2]
			
			# print()
			# print(city_contintent[i1])
			# print(path_f.get_continent(the_world.cursor, (c2.x, c2.y)))
			
			# A city can't trade with itself...
			if i2 == i1:
				continue
			
			# Check we've not already done this
			if (i1, i2) in distance_matrix:
				continue
			
			# Check borders
			# [Host][Visitor]
			# if borders.get[c2.team][c1.team] <= team.border_states.index("Closed"):
			if the_world.get_border(c2.team, c1.team) <= team.border_states.index("Closed"):
				continue
			
			# if borders[c1.team][c2.team] <= team.border_states.index("At war"):
			if the_world.get_border(c1.team, c2.team) <= team.border_states.index("At war"):
				continue
			
			# Get continent stuff
			if i2 not in city_contintent:
				city_contintent[i2] = path_f.get_continent(the_world.cursor, (c2.x, c2.y))
			
			# Reset distance
			dist = None
			crow_dist = path_f.pythagoras_cities(c1, c2)
			
			# If on same continent
			if city_contintent[i1] == city_contintent[i2] and crow_dist < sad_rules.max_crow_dist_land:
				if crow_dist <= sad_rules.min_trade_distance:
					dist = DeadPath(sad_rules.min_trade_distance)
				else:
					path_time = time.time()
					try:
						dist = path_f.path(the_world.cursor, [(c1.x, c1.y), (c2.x, c2.y)], move_speed="Merchant", move_type="Merchant", exception_in_timeout=True, timeout_limit=1000)
						paths += 1
					except Exception as e:
						print("Trying to path %s (%d) to %s (%d)" % (c1.name, i1, c2.name, i2))
						print("Continent %s to %s" % (city_contintent[i1], city_contintent[i2]))
						raise
					path_time = time.time() - path_time
					if path_time > worst_land_path[2]:
						worst_land_path = ((c1.x, c1.y), (c2.x, c2.y), path_time, "points={0}%2C+{1}%2C+{2}%2C+{3}&move_speed=Merchant&move_type=Merchant".format(
							c1.x, c1.y, c2.x, c2.y
						))
			
			# If both are ports then we can try the water
			if c1.port and c2.port and crow_dist < sad_rules.max_crow_dist_water:
				path_time = time.time()
				try:
					dist_sea = path_f.path(the_world.cursor, [(c1.x, c1.y), (c2.x, c2.y)], move_speed="Sailing", move_type="Sail", exception_in_timeout=True)
					paths += 1
				except Exception as e:
					print("Trying to path %s (%d) to %s (%d)" % (c1.name, i1, c2.name, i2))
					raise
				
				path_time = time.time() - path_time
				if path_time > worst_water_path[2]:
					worst_water_path = ((c1.x, c1.y), (c2.x, c2.y), path_time, "points={0}%2C+{1}%2C+{2}%2C+{3}&move_speed=Sailing&move_type=Sail".format(
						c1.x, c1.y, c2.x, c2.y
					))
				
				# Now pick the fastest
				if dist == None or dist.time_cost > dist_sea.time_cost:
					dist = dist_sea
			
			# Is it none?
			if dist == None:
				time_cost = 99999
			else:
				time_cost = sad_rules.trade_distance(dist.time_cost)
				links += 1
			
			# if borders[c2.team][c1.team] == team.border_states.index("Segregated"):
			if the_world.get_border(c2.team, c1.team) <= team.border_states.index("Segregated"):
				time_cost *= sad_rules.segregated_multiplier
			
			if time_cost > sad_rules.max_trade_travel_time: continue
			distance_matrix[(i1, i2)] = time_cost
			
			# If we have the same borders round the other way then we can skip this path later
			# if borders[c2.team][c1.team] == borders[c1.team][c2.team]:
			if the_world.get_border(c2.team, c1.team) == the_world.get_border(c1.team, c2.team):
				distance_matrix[(i2, i1)] = distance_matrix[(i1, i2)]
		
		# print("%d of %d in %ss (%d links)" % (i, len(city_dict), round(time.time() - started, 2), links))
		"""
		Origional
		Tried 103,505 paths
		Completed in 446 seconds
		
		After applying: "if (i1, i2) in distance_matrix" with same border checking
		Tried 79,979 paths
		Completed in 338 seconds
		
		After dropping the timeout exception from 10k to 1k
		Tried 79,979 paths
		Completed in 335 seconds
		
		After adding in the min distance (10)
		Tried 79,958 paths
		Completed in 337 seconds
		
		Adding in dead tiles and a smaller (10 not 1000) move cost
		Tried 79,958 paths
		Completed in 336 seconds
		"""
	
	# Some stats stuff
	if verbose:
		print("Worst land path: %s -> %s in %s = http://localhost/rob3/web.py?mode=path_map&%s" % worst_land_path)
		print("Worst water path: %s -> %s in %s = http://localhost/rob3/web.py?mode=path_map&%s" % worst_water_path)
		
		total_time = time.time() - func_start
		print("Tried %s paths in %s seconds, avg %ss per path or %s paths per second" % (format(paths, ','), int(total_time), round(total_time/paths, 3), round(paths/total_time, 2)))
	
	# Now to save it
	q = "INSERT INTO trade_distances (city_1, city_2, distance) values %s;" % ",".join(
		["(%d, %d, %d)" % (c[0], c[1], d) for c, d in distance_matrix.items()]
	)
	
	the_world.cursor.execute("DELETE FROM trade_distances")
	if verbose:
		print("Completed in %d seconds" % int(time.time() - func_start))
	
	the_world.cursor.execute(q)


def make_supply_change_query(city_id, resource_id):
	return [
		"UPDATE cities SET supply_good = %d WHERE id = %d;" % (resource_id, city_id)
	]

