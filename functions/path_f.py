import database
import math
# from data import city_q
# from data import team_q
# from data import mapper

from queries import mapper_q
from rules import map_data
from classes import world, city

# terrain_tuples = mapper.terrain_tuples()

def _sort_dict(d):
    """ Returns the keys of dictionary d sorted by their values """
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0,len(backitems))]

def pythagoras_tuples(point_a, point_b):
	"""Takes two tuples and returns the distnace between them as the crow flies"""
	x = abs(point_a[0] - point_b[0])
	y = abs(point_a[1] - point_b[1])
	return pythagoras(x, y)

def pythagoras_cities(city_1, city_2):
	x = abs(city_1.x - city_2.x)
	y = abs(city_1.y - city_2.y)
	return pythagoras(x, y)

def pythagoras(x, y):
	if type(x) == tuple or type(y) == list:
		return pythagoras_tuples(x, y)
	elif type(x) == city.City and type(y) == city.City:
		return pythagoras_cities(x, y)
	else:
		return math.sqrt(x*x + y*y)

map_continent_tiles_cache = {}
def get_map_continent_tiles(cursor):
	if map_continent_tiles_cache == {}:
		query = """SELECT * FROM map_continent_tiles;"""
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			map_continent_tiles_cache[(row['x'], row['y'])] = row['continent']
	
	return map_continent_tiles_cache

def get_continent(cursor, point):
	x = point[0] - (point[0] % 10)
	y = point[1] - (point[1] % 10)
	
	return get_map_continent_tiles(cursor).get((x, y), None)

trade_route_cache = {}
def find_trade_route(cursor, team_1, team_2, resource=-1, the_world=None):
	"""If there's a path between two cities then there's a trade route
	
	Resource means that there needs to be a route from a city with that supply"""
	
	if (team_1, team_2, resource) in trade_route_cache:
		return trade_route_cache[(team_1, team_2, resource)]
	if (team_2, team_1, resource) in trade_route_cache:
		return trade_route_cache[(team_2, team_1, resource)]
	
	if the_world == None:
		the_world = world.World(cursor)
	
	team_1_cities = the_world.cities_from_team(team_1)
	team_2_cities = the_world.cities_from_team(team_2)
	
	# If a resource is involved we want to make sure that they have a supply they can send it from
	cities_with_supply = []
	if resource != -1:
		for k, the_city in team_1_cities.items():
			if the_city.supply() != resource: continue
			else: cities_with_supply.append(k)
		
		if len(cities_with_supply) < 1:
			trade_route_cache[(team_1, team_2, resource)] = (-1,-1)
			return -1, -1
	else:
		for k, the_city in team_1_cities.items():
			cities_with_supply.append(k)
	
	# Second we want to create an array of all the city pairs, then we sort them by distance
	city_pairs = {}
	pairs_dist = {}
	
	for c1_id, c1 in team_1_cities.items():
		for c2_id, c2 in team_2_cities.items():
			city_pairs["%s,%s" % (c1_id, c2_id)] = (c1_id, c2_id)
			pairs_dist["%s,%s" % (c1_id, c2_id)] = pythagoras((c1.x,c1.y), (c2.x,c2.y))
	
	# Get a list of them based on how close they are
	pairs_order = _sort_dict(pairs_dist)
	
	# Are they on the same continent?
	for p in pairs_order:
		c1 = team_1_cities[city_pairs[p][0]]
		c2 = team_2_cities[city_pairs[p][1]]
		
		if resource != -1:
			if c1.supply() != resource: continue
		
		if get_continent(cursor, (c1.x,c1.y)) == get_continent(cursor, (c2.x,c2.y)):
			trade_route_cache[(team_1, team_2, resource)] = (c1.id, c2.id)
			return c1.id, c2.id
	
	# Is there a port (if there's a resource the resource needs to get to a port)
	team_1_port = -1
	team_1_supply_city = -1
	for res_city in cities_with_supply:
		c1 = team_1_cities[res_city]
		if c1.port:
			team_1_port = res_city
			team_1_supply_city = res_city
		if team_1_port > 0: continue
		
		for k, c2 in team_1_cities.items():
			if k == res_city: continue
			if not c2.port: continue
			
			if get_continent(cursor, (c1.x,c1.y)) == get_continent(cursor, (c2.x,c2.y)):
				team_1_port = k
				team_1_supply_city = k
	
	# If we can't get to a port, it's not happening
	if team_1_port < 1:
		trade_route_cache[(team_1, team_2, resource)] = (-1,-1)
		return -1, -1
	
	# Does team 2 have a port at all?
	team_2_port = -1
	for k, the_city in team_2_cities.items():
		if the_city.port: team_2_port = k
	
	if team_2_port > 0:
		trade_route_cache[(team_1, team_2, resource)] = (team_1_port, team_2_port)
		return team_1_port, team_2_port
	
	# A = supply, B = port on isle of A, C = Port on isle of D, D = a city of theirs
	for p in pairs_order:
		c1 = team_1_cities[city_pairs[p][0]]
		c2 = team_2_cities[city_pairs[p][1]]
		
		# Have we found C?
		if c1.port and get_continent(cursor, (c1.x,c1.y)) == get_continent(cursor, (c2.x,c2.y)):
			trade_route_cache[(team_1, team_2, resource)] = (team_1_supply_city, c2.id)
			return team_1_supply_city, c2.id
	
	trade_route_cache[(team_1, team_2, resource)] = (-1,-1)
	return -1, -1


class Pathway (object):
	"""The class for holding a pathway between two points"""
	def __init__(self, start_point, end_point, move_speed="Marching", move_type="Medium foot", exception_in_timeout=False, timeout_limit=10000):
		super(Pathway, self).__init__()
		self.start_point	= (start_point[0]-(start_point[0]%10), start_point[1]-(start_point[1]%10))
		self.end_point		= (end_point[0]-(end_point[0]%10), end_point[1]-(end_point[1]%10))
		
		self.move_speed = move_speed
		self.move_type = move_type
		
		self.exception_in_timeout = exception_in_timeout
		self.timeout_limit = timeout_limit
		
		# A list of all the steps taken, each is a dictionary with a few metrics
		self.steps			= []
		
		# Output stuff
		self.time_cost		= 0
		self.walk_distance	= 0
		self.distance		= pythagoras(start_point, end_point)
	
	def __add__(self, other):
		if type(other) != Pathway:
			raise Exception("Pathways can only be added with other Pathways")
		
		p = Pathway(self.start_point, other.end_point)
		
		p.steps = self.steps
		p.steps.extend(other.steps)
		
		p.time_cost = self.time_cost + other.time_cost
		p.distance = self.distance + other.distance
		p.walk_distance = self.walk_distance + other.walk_distance
		
		return p
		
	def compile_results(self):
		for s in self.steps:
			self.walk_distance += s['walk_distance']
		
		self.time_cost = self.walk_distance / map_data.movement_speeds[self.move_speed]
		
		# Formatting
		if self.time_cost == int(self.time_cost):
			self.time_cost = int(self.time_cost)
	
	def new_step(self, tile=(0,0)):
		return {
			"tile":			tile,# The tile we're stepping into
			"time_cost":	0,# The cost in time for stepping into it
			"new_distance":	0,# The new distance (as crow flies) from our target
			"walk_distance":0,
		}
	
	def search(self):
		self.steps = []
		walked_tiles = set()
		dead_tiles = set()
		
		timeout = 0
		success = False
		
		# Get the terrain dictionary
		terrain_dict = mapper_q.terrain_cache_dict
		if terrain_dict == {}: raise Exception("terrain_dict == {}")
		
		self.steps.append(self.new_step(self.start_point))
		
		while not success:
			timeout += 1
			if timeout >= self.timeout_limit:# If it takes over 500 then there's probably a problem
				if self.exception_in_timeout:
					print("Started at step: %s<br />" % self.steps[0])
					print("Targeting: %s<br />" % str(self.end_point))
					print("Distance as crow: %s<br />" % str(pythagoras(self.start_point, self.end_point)))
					print("Currently at: %s<br />\n" % self.steps[-1])
					print("Path map: http://localhost/rob3/web.py?mode=path_map&points={0}%2C+{1}%2C+{2}%2C+{3}&move_speed={4}&move_type={5}".format(
						self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], self.move_speed, self.move_type
					))
					raise Exception("Timeout")
				else:
					return False
				# print("Steps: %s<br />" % self.steps)
				
				"""
				Started at step: {'tile': (750, 1350), 'time_cost': 0, 'new_distance': 0, 'walk_distance': 0}<br />
				Targeting: (760, 1300)<br />
				Distance as crow: 50.9901951359<br />
				Currently at: {'tile': (590, 1190), 'time_cost': 0.141, 'new_distance': 202.48456731316588, 'walk_distance': 141}<br />

				Started at step: {'tile': (750, 1280), 'time_cost': 0, 'new_distance': 0, 'walk_distance': 0}<br />
				Targeting: (760, 1300)<br />
				Distance as crow: 22.360679775<br />
				Currently at: {'tile': (950, 1270), 'time_cost': 0.1, 'new_distance': 192.35384061671346, 'walk_distance': 100}<br />

				Started at step: {'tile': (770, 1270), 'time_cost': 0, 'new_distance': 0, 'walk_distance': 0}<br />
				Targeting: (760, 1300)<br />
				Distance as crow: 31.6227766017<br />
				Currently at: {'tile': (600, 1180), 'time_cost': 0.1, 'new_distance': 200.0, 'walk_distance': 100}<br />

				Started at step: {'tile': (780, 1360), 'time_cost': 0, 'new_distance': 0, 'walk_distance': 0}<br />
				Targeting: (760, 1300)<br />
				Distance as crow: 63.2455532034<br />
				Currently at: {'tile': (750, 1090), 'time_cost': 0.141, 'new_distance': 210.23796041628637, 'walk_distance': 141}<br />
				"""
				
				return False
				raise Exception("Timeout")
			
			# Get our current position
			try:
				x, y = self.steps[-1]['tile']
			except Exception as e:
				# No steps?
				if self.steps == []:
					return False
				
				raise
			
			view_dict = {
				"n":	(x, y-10),
				"ne":	(x+10, y-10),
				"e":	(x+10, y),
				"se":	(x+10, y+10),
				"s":	(x, y+10),
				"sw":	(x-10, y+10),
				"w":	(x-10, y),
				"nw":	(x-10, y-10),
			}
			
			# Set the best_cost to something that any tile beats
			best_cost = [(-1,-1), 999999999, 999999999, 0, 0, 10]
			
			for k, v in view_dict.items():
				# We don't want to move back and forth all the time
				if v in walked_tiles: continue
				if v in dead_tiles: continue
				
				# Handles
				tile_terrain = map_data.terrain[terrain_dict.get(v, 0)]
				
				# Build cost metrics
				new_distance	= pythagoras(v, self.end_point)
				# move_cost		= map_data.movement_speeds[self.move_speed]
				move_cost		= map_data.move_costs[tile_terrain][self.move_type]
				if len(k) == 2:# Diagonal
					move_cost *= 1.41
					walk_dist = 141
				else:
					walk_dist = 100
				
				# Combine metrics
				if move_cost > 10:
					metric_cost = 1000
					dead_tiles.add(v)
				else:
					metric_cost = (new_distance) + (move_cost * 10)
				
				# If it's the destination then we'll force a movement there
				if v == self.end_point:
					metric_cost = -1
					success = True
				
				# If it's next to the destination we'll rank it pretty good
				if new_distance < 15:
					metric_cost = -1
					move_cost = 0
				
				# Rank it
				if metric_cost < best_cost[1]:
					best_cost = [v, metric_cost, new_distance, move_cost, walk_dist]
			
			# Dead end?
			if best_cost[0] == (-1,-1) or best_cost[3] > 100:
				# best_cost[0] = self.steps[-1]['tile']
				# success = True
				# Lets jump back 1 step
				del(self.steps[-1])
			else:
				# We should now have a tile to move to
				s = self.new_step()
				s['tile']			= best_cost[0]
				s['new_distance']	= best_cost[2]
				s['time_cost']		= best_cost[3]
				s['walk_distance']	= best_cost[4]
				# print(best_cost[3], "<br />")
				self.steps.append(s)
			
			# Ensure we don't go back over this one
			walked_tiles.add(best_cost[0])
		
	def _neighbour_steps(self, look_ahead=15):
		step_count = len(self.steps)
		i = -1
		
		# view_dict = {
		# 	"n":	(x, y-10),
		# 	"ne":	(x+10, y-10),
		# 	"e":	(x+10, y),
		# 	"se":	(x+10, y+10),
		# 	"s":	(x, y+10),
		# 	"sw":	(x-10, y+10),
		# 	"w":	(x-10, y),
		# 	"nw":	(x-10, y-10),
		# }
		
		while i < step_count-1:# Use while because we're re-ordering our steps list
			i += 1
			x1, y1 = self.steps[i]['tile']
			jumped = False
			
			for j in range(min(step_count-1, i+look_ahead), i+3, -1):
				if jumped: continue
				
				x2, y2 = self.steps[j]['tile']
				
				if abs(x1 - x2) > 10: continue
				if abs(y1 - y2) > 10: continue
				
				# It's next to another tile much further on, we can jump it!
				for c in range(i+1, j):
					del(self.steps[i+1])
				
				jumped = True
				step_count = len(self.steps)
				
	def _crow_path(self, look_ahead=999999):
		"""Runs a search to see if there's a tile X steps ahead that's a lot closer than it should be"""
		pass
	
	def optimise(self, look_ahead=99999):
		self._neighbour_steps(look_ahead)
		self._crow_path(look_ahead)


# The main function, actually more of a filter for the real function
def path(cursor, waypoints, move_speed="Marching", move_type="Medium foot", exception_in_timeout=False, timeout_limit=10000):
	# Build the terrain cache
	mapper_q.get_terrain(cursor, 0, 0)
	
	# Too few waypoints?
	if len(waypoints) < 2:
		raise Exception("path_f.path() was called with less than 2 waypoints (%s)" % waypoints)
	
	# Needs to be a list for what we want to do
	if type(waypoints) == tuple:
		waypoints = list(waypoints)
	
	# Clean waypoints to make sure they're compatable of mod 10
	for i, w in enumerate(waypoints):
		x = w[0] - w[0]%10
		y = w[1] - w[1]%10
		waypoints[i] = (x, y)
	
	pathway_list = []
	for i in range(1, len(waypoints)):
		p = Pathway(waypoints[i-1], waypoints[i], move_speed, move_type, exception_in_timeout)
		pathway_list.append(p)
	
	for p in pathway_list:
		p.search()
		p.optimise()
		p.compile_results()
	
	# If we've several then add them together
	if len(pathway_list) > 1:
		big_pathway = Pathway(waypoints[0], waypoints[-1], move_speed, move_type)
		
		for p in pathway_list:
			big_pathway += p
		
		return big_pathway
	else:
		return pathway_list[0]
	
	

