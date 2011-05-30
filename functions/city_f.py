import database
import math
from classes import team
from pages import common
from queries import building_q
from rules import map_data, sad_rules
from functions import path_f, cli_f
import time

def set_building(cursor, city_id, building_id, completion=0, amount=0):
	completion = max(completion, 0)
	amount = max(amount, 0)
	
	# Delete it
	query = """DELETE FROM city_buildings WHERE city = %d AND building = %d;""" % (city_id, building_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if completion < 1 and amount < 1: return
	
	query = """INSERT INTO city_buildings (city, building, completion, amount) values (%d, %d, %d, %d)""" % (city_id, building_id, completion, amount)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))


def new_city(name, team, x, y, port, secret, dead, nomadic, population, slaves):
	return """INSERT INTO cities (name, team, x, y, port, secret, dead, nomadic, population, slaves, founded)
		values
		('%(name)s', %(team)s, %(x)s, %(y)s, %(port)s, %(secret)s, %(dead)s, %(nomadic)s, %(population)s, %(slaves)s, %(founded)s);""" % {
			"name":			database.escape(name),
			"team":			team,
			"port":			port,
			"secret":		secret,
			"dead":			int(dead),
			"nomadic":		nomadic,
			"population":	population,
			"slaves":		slaves,
			"x":			x,
			"y":			y,
			"founded":		int(common.current_turn()),
		}

def make_disbanding_queries(amount, city_list):
	"""Returns a set of queries to lower the population from the team cities"""
	per_city_amount = int(amount/len(city_list))
	
	# We need to have these people refunded!
	if per_city_amount < 1:
		return ["UPDATE cities SET population = population + %d WHERE id = %d;" % (amount, city_list[0])]
	
	queries = []
	for c in city_list:
		queries.append("UPDATE cities SET population = population+%s WHERE id = %d;" % (per_city_amount, c))
	
	return queries

def make_recruitment_queries(amount, city_list):
	"""Returns a set of queries to lower the population from the team cities"""
	queries = []
	per_city_amount = math.ceil(amount/len(city_list))
	for c in city_list:
		queries.append("UPDATE cities SET population = population-%s WHERE id = %d;" % (per_city_amount, c))
	
	return queries

def make_migration_query(city_id, new_location, time_taken):
	return ["UPDATE cities SET x = %d, y = %d, days_travelled = %d WHERE id = %d;" % (new_location[0], new_location[1], time_taken, city_id)]

def make_founding_query(team_id, name, city_location, is_port, is_nomadic, city_size, city_list):
	"""Makes a set of queries for founding a new city"""
	if city_list == []:
		return []
	
	queries = []
	
	queries.append("""INSERT INTO cities (name, team, x, y, port, nomadic, population, founded, dead, secret)
		values
		('%(name)s', %(team)s, %(x)s, %(y)s, %(port)s, %(nomadic)s, %(population)s, %(founded)s, 0, False);""".replace("\n", "") % {
			"name":			database.escape(name),
			"team":			team_id,
			"port":			is_port,
			"nomadic":		is_nomadic,
			"population":	city_size,
			"x":			city_location[0],
			"y":			city_location[1],
			"founded":		int(common.current_turn()),
		})
	
	amount_per_city	= math.ceil(city_size/len(city_list))
	
	for c in city_list:
		queries.append("""UPDATE cities SET population = population-%d WHERE id = %d;""" % (amount_per_city, c))
	
	return queries

def make_remove_dead_city_query(city_id):
	return [
		"DELETE FROM city_buildings WHERE city = %d;" % city_id,
		"DELETE FROM armies WHERE garrison = %d;" % city_id,
		"DELETE FROM cities WHERE id = %d;" % city_id,
	]

def make_relocation_query(from_city, to_city, amount, move_type):
	if move_type.lower() == "civilians":
		return [
		"""UPDATE cities SET population = population-%s WHERE id = %s;""" % (amount, from_city),
		"""UPDATE cities SET population = population+%s WHERE id = %s;""" % (amount, to_city),
		]
	elif move_type.lower() == "slaves":
		return [
		"""UPDATE cities SET slaves = slaves-%s WHERE id = %s;""" % (amount, from_city),
		"""UPDATE cities SET slaves = slaves+%s WHERE id = %s;""" % (amount, to_city),
		]


# def make_connections(the_world, verbose=False):
# 	from rules import sad_rules
# 	
# 	start_time = time.time()
# 	
# 	# Handle
# 	bstate		= team.border_states.index
# 	team_dict	= the_world.active_teams()
# 	city_dict	= the_world.live_cities()
# 	
# 	# Border/Attitude matrix
# 	border_matrix = the_world.borders()
# 	# for t1 in team_dict.keys():
# 	# 	border_matrix[t1] = {}
# 	# 	the_team = team_dict[t1]
# 	# 	
# 	# 	for t2 in team_dict.keys():
# 	# 		if t1 == t2:
# 	# 			border_matrix[t1][t2] = bstate("Open")
# 	# 			continue
# 	# 		
# 	# 		border_matrix[t1][t2] = the_team.borders.get(t2, the_team.default_borders)
# 	
# 	# Get a list of the active cities
# 	active_cities = []
# 	for city_id, the_city in city_dict.items():
# 		the_city.connections = {}
# 		active_cities.append(city_id)
# 	
# 	map_continent_tiles = path_f.get_map_continent_tiles(the_world.cursor)
# 	
# 	if verbose:
# 		it = []
# 		for i, c in enumerate(active_cities):
# 			it.append((i, c))
# 		
# 		the_iter = cli_f.progressbar(it, "Creating links: ", 60, True)
# 		# for team_id in progressbar(team_dict.keys(), "Creating TIs: ", 60, True):
# 	else:
# 		the_iter = enumerate(active_cities)
# 	
# 	# Now for our main loop
# 	inserts = []
# 	# print border_matrix
# 	# for i1, c1 in enumerate(active_cities):
# 	for i1, c1 in the_iter:
# 		city1 = city_dict[c1]
# 		team1 = team_dict[city1.team]
# 		
# 		city1_cont = map_continent_tiles.get((city1.x - city1.x % 10, city1.y - city1.y % 10), -1)
# 		
# 		for i2, c2 in enumerate(active_cities):
# 			if i2 <= i1: continue
# 			
# 			city2 = city_dict[c2]
# 			team2 = team_dict[city2.team]
# 			
# 			# Their state to you
# 			bstate_12 = border_matrix[team1.id][team2.id]
# 			bstate_21 = border_matrix[team2.id][team1.id]
# 			
# 			if bstate_12 == bstate("Closed") and bstate_21 == bstate("Closed"):
# 				continue
# 			
# 			# Check IR to IR
# 			# if team1.ir and team2.ir: continue
# 			
# 			# Check team borders
# 			
# 			city2_cont = map_continent_tiles.get((city2.x - city2.x % 10, city2.y - city2.y % 10), -1)
# 			
# 			waypoints = ((city1.x, city1.y), (city2.x, city2.y))
# 			
# 			sea_results, land_results = 999999, 999999
# 			
# 			if city1.port and city2.port:
# 				sea_results = path_f.path(the_world.cursor, waypoints, "Sailing", "Sail").time_cost
# 			
# 			if city1_cont == city2_cont:
# 				# We can save some time by guessing if things are too far apart
# 				if path_f.pythagoras(city1, city2) < 250:
# 					land_results = path_f.path(the_world.cursor, waypoints, "Marching", "Heavy foot").time_cost
# 			
# 			if sea_results < 1000 or land_results < 1000:
# 				dist = int(min(land_results, sea_results))
# 				
# 				# If 1->2 is open, city2 can send people to city1
# 				if bstate_12 == bstate("Open"):
# 					inserts.append("(%d, %d, %d)" % (c2, c1, dist))
# 				
# 				if bstate_12 == bstate("Segregated"):
# 					inserts.append("(%d, %d, %d)" % (c2, c1, dist * sad_rules.segregated_multiplier))
# 				
# 				# If 2->1 is open, city1 can send people to city2
# 				if bstate_21 == bstate("Open"):
# 					inserts.append("(%d, %d, %d)" % (c1, c2, dist))
# 				
# 				if bstate_21 == bstate("Segregated"):
# 					inserts.append("(%d, %d, %d)" % (c1, c2, dist * sad_rules.segregated_multiplier))
# 				
# 				# city1.connections[c2] = dist
# 				# city2.connections[c1] = dist
# 				# inserts.append("(%d, %d, %d)" % (c1, c2, dist))
# 				# inserts.append("(%d, %d, %d)" % (c2, c1, dist))
# 		
# 		# print i1, len(city1.connections)
# 	
# 	# Now to make our database query
# 	
# 	query = """INSERT INTO city_connection_matrix (city_from, city_to, distance) values %s;""" % ",".join(inserts)
# 	
# 	try: the_world.cursor.execute("DROP TABLE city_connection_matrix")
# 	except Exception as e: pass
# 	
# 	try: the_world.cursor.execute("""CREATE TABLE city_connection_matrix (
# 	  city_from integer NOT NULL default 0,
# 	  city_to integer NOT NULL default 0,
# 	  distance integer NOT NULL default 0,
# 	  PRIMARY KEY  (city_from, city_to)
# 	);""")
# 	except Exception as e:
# 		raise Exception("Database error: %s\n" % (e.message.replace("\n","")))
# 	
# 	try: the_world.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	
# 	if verbose:
# 		print("Completed city connection matrix in %d seconds" % int(time.time() - start_time))

def get_terrain_ratios(the_world):
	terrain = {}
	
	for k, v in the_world.live_cities().items():
		if v.terrain not in terrain:
			terrain[v.terrain] = 0
		terrain[v.terrain] += 1
		
		if v.terrain == 0:
			print(k)
	
	for k, v in terrain.items():
		print(map_data.terrain[k], v)
	
	from queries import mapper_q
	terrain = {}
	mterrain = mapper_q.get_all_terrain(the_world.cursor)
	
	for k, v in mterrain.items():
		if v not in terrain:
			terrain[v] = 0
		terrain[v] += 1
	
	print("")
	for k, v in terrain.items():
		print(map_data.terrain[k], v)

def apply_city_matrix(the_world, compress=True):
	# Handles
	the_world.cities()
	
	# Get a list of the active cities
	query = """SELECT * FROM trade_distances"""
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		the_world._cities[row['city_1']].connections[row['city_2']] = row['distance']
		
		the_world._cities[row['city_2']].connections_to[row['city_1']] = row['distance']
	
	if compress:
		to_remove = []
		
		for city_id, the_city in the_world._cities.items():
			for c in the_city.connections.keys():
				if city_id not in the_world._cities[c].connections:
					to_remove.append((city_id,c))
		
		for c1, c2 in to_remove:
			del(the_world._cities[c1].connections[c2])
	
	"""
	total = 0
	conns = 0
	for city_id, the_city in the_world._cities.items():
		for c, d in the_city.connections.items():
			total += d
			conns += 1
	
	print(conns)
	print(total/conns)
	exit()
	"""

def delete_city(city_id):
	queries = []
	
	# Delete from distances
	queries.append("DELETE FROM trade_distances WHERE city_1 = %d OR city_2 = %d" % (city_id, city_id))
	
	# Move all ops
	queries.append("UPDATE operatives SET city = 0 WHERE city = %d;" % city_id)
	
	# Delete all buildings from that city
	queries.append("DELETE FROM city_buildings WHERE city = %s" % city_id)
	
	# Now to delete the army
	queries.append("DELETE FROM armies WHERE garrison = %s;" % city_id)
	
	# Now to delete the city
	queries.append("DELETE FROM cities WHERE id = %s;" % city_id)
	
	return queries

def mass_city_wall_check(cursor, city_dict):
	"""It assumes that each city's buildings are already in place"""
	
	building_dict = building_q.get_all_walls(cursor)
	
	for city_id, the_city in city_dict.items():
		the_city.walls = []
		for building_id, the_building in building_dict.items():
			# Complete and is a wall
			if the_city.buildings_amount.get(building_id, 0) >= 1:
				the_city.walls.append(building_id)
				continue
			
			# "Completed" but not registered as such
			if the_city.buildings.get(building_id, 0) >= the_building.build_time:
				the_city.walls.append(building_id)
				continue
			
			# What if it's an upgrade?
			if the_building.upgrades > 0 and the_city.buildings.get(the_building.upgrades, 0) > 0:
				the_city.walls.append(building_id)
				continue
	
	return city_dict

# http://mathworld.wolfram.com/Circle-CircleIntersection.html - halfay down page
def overlap(c1, c2, debug=False):
	if not _check_area(c1, c2, debug=debug):
		return 0
	
	acos = math.acos
	sqrt = math.sqrt
	
	r = map_data.map_image_size(c1.size)/5
	R = map_data.map_image_size(c2.size)/5
	d = path_f.pythagoras((c1.x, c1.y), (c2.x, c2.y))
	
	if d > r + R: return 0
	if d == 0: return math.pi * max((r*r), (R*R))
	
	# r is the radius of circle 1
	# R is the radius of circle 2
	# d is the distance of the centre of circle 2 from the centre of circle 1.
	# cos-1 is the inverse cosine operator.
	
	try:
		a = r**2 * acos((d**2 + r**2 - R**2) / (2 * d * r))
		b = R**2 * acos((d**2 + R**2 - r**2) / (2 * d * R))
		c = (-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R)
		c = sqrt(c) / 2
	except Exception as e:
		# It may be that the smaller is completely covered by the bigger
		# C = centre, R = Radius
		# C1 -- C2 -- R2 ----- R1
		
		R = map_data.map_image_size(c1.size)/2
		S = map_data.map_image_size(c2.size)
		D = path_f.pythagoras(c1, c2)
		
		# Area = pi * r^2
		if R > S + D:
			return math.pi * (S/2) * (S/2)
		
		
		print("")
		print("Error overlapping %s (%d) with %s (%d)" % (c1.name, c1.id, c2.name, c2.id))
		print(r)
		print(R)
		print(d)
		
		raise
	a = r**2 * acos((d**2 + r**2 - R**2) / (2 * d * r))
	b = R**2 * acos((d**2 + R**2 - r**2) / (2 * d * R))
	c = (-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R)
	c = sqrt(c) / 2
	
	# print(a + b - c)
	
	return (a + b - c)

def _check_area(c1, c2, debug=False):
	i1 = map_data.map_image_size(c1.size)/2.5
	i2 = map_data.map_image_size(c2.size)/2.5
	
	c1.left = c1.x - i1/2
	c1.right = c1.x + i1/2
	
	c1.top = c1.y - i1/2
	c1.bottom = c1.y + i1/2
	
	c2.left = c2.x - i2/2
	c2.right = c2.x + i2/2
	
	c2.top = c2.y - i2/2
	c2.bottom = c2.y + i2/2
	
	xlap, ylap = 0, 0
	
	if debug:
		print("")
	
	# Does this sit to the left, between or right of the other?
	# C1 is Left
	if c1.left <= c2.left and c1.right <= c2.right and c1.right >= c2.left:
		xlap = c1.right - c2.left
		if debug: print("xlap 1 = %d (R1 - L2) (%d - %d)" % (xlap, c1.right, c2.left))
	
	# C1 is Right
	elif c1.left >= c2.left and c1.right >= c2.right and c1.left <= c2.right:
		xlap = c2.right - c1.left
		if debug: print("xlap 2 = %d (R2 - L1) (%d - %d)" % (xlap, c2.right, c1.left))
	
	# Between, C1 is bigger
	elif c1.left <= c2.left and c1.right >= c2.right:
		xlap = min(i1, i2)
		if debug: print("xlap 3 = %d min(x1, x2) min(%d, %d)" % (xlap, i1, i2))
	
	# Between, C2 is bigger
	elif c1.left >= c2.left and c1.right <= c2.right:
		xlap = min(i1, i2)
		if debug: print("xlap 4 = %d min(x1, x2) min(%d, %d)" % (xlap, i1, i2))
	
	if xlap <= 0:
		if debug: print("xlap <= 0")
	
	# Does this sit to the left, between or right of the other?
	# C1 is Above
	if c1.top <= c2.top and c1.bottom <= c2.bottom and c1.bottom >= c2.top:
		ylap = c1.bottom - c2.top
		if debug: print("ylap 1 = %d (B1 - T2) (%d - %d)" % (ylap, c1.bottom, c2.top))
	
	# C1 is Below
	elif c1.top >= c2.top and c1.bottom >= c2.bottom and c1.top <= c2.bottom:
		ylap = c2.bottom - c1.top
		if debug: print("ylap 2 = %d (B2 - T1) (%d - %d)" % (ylap, c2.bottom, c1.top))
	
	# Between, C1 is bigger
	elif c1.top <= c2.top and c1.bottom >= c2.bottom:
		ylap = min(i1, i2)
		if debug: print("ylap 3 = %d min(y1, y2) min(%d, %d)" % (ylap, i1, i2))
		
	# Between, C2 is bigger
	elif c1.top >= c2.top and c1.bottom <= c2.bottom:
		ylap = min(i1, i2)
		if debug: print("ylap 4 = %d min(y1, y2) min(%d, %d)" % (ylap, i1, i2))
	
	if ylap <= 0:
		if debug: print("ylap <= 0")
	
	if debug:
		print("")
		print("C1: %s x(%s, %s) y(%s, %s) (%s)" % (c1.name, c1.left, c1.right, c1.top, c1.bottom, i1))
		print("C2: %s x(%s, %s) y(%s, %s) (%s)" % (c2.name, c2.left, c2.right, c2.top, c2.bottom, i2))
		print("(%s * %s = %s) -> (%d, %d)" % (xlap, ylap, (xlap*ylap), c1.team, c2.team))
		print("")
	
	overlap = (xlap * ylap)
	return overlap

# For circular icons
def overlap_percentage(the_city, amount):
	r = map_data.map_image_size(the_city.size)/5
	area = math.pi * (r ** 2)
	percentage = (amount / area) * 100
	
	return max(min(percentage, 100), 0)

def overlap_percentage_square(the_city, amount):
	the_city.size = map_data.map_image_size(the_city.population + the_city.slaves)/2.5
	area = the_city.size ** 2
	percentage = (amount / area) * 100
	
	return max(min(percentage, 100), 0)
	