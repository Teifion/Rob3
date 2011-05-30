import database
# import data
# import rules
from classes import city
from queries import mapper_q
from functions import path_f
from rules import map_data, city_rules


def mod_ten_tuple(location):
	"""Pass it a tuple and it returns the tuple for tile numbers"""
	return ((location[0] - location[0]%10, location[1] - location[1]%10))

def team_influence(the_world, team_id):
	"""Returns a list of tiles that the team has influence on and by how much"""
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	terrain_tuples = mapper_q.get_all_terrain(the_world.cursor)
	
	tile_control = {}
	
	# First pass, we're only using our cities
	for k, c in city_dict.items():
		if c.dead > 0 or c.secret == 1: continue
		if c.team != team_id: continue
		
		city_loc = mod_ten_tuple((c.x, c.y))
		min_x = city_loc[0]-50
		max_x = city_loc[0]+50
		
		min_y = city_loc[1]-50
		max_y = city_loc[1]+50
		
		for x in range(min_x, max_x, 10):
			for y in range(min_y, max_y, 10):
				tile_loc = (x,y)
				
				# Ignore water
				if tile_loc not in terrain_tuples: continue
				
				tile_range = path_f.pythagoras(city_loc, tile_loc)
				
				if (x,y) not in tile_control:
					tile_control[(x,y)] = 0
				
				tile_control[(x, y)] += city_rules.city_control(tile_range, c, team_dict)
	
	# Second pass, reduce it
	for k, c in city_dict.items():
		if c.dead or c.secret == 1: continue
		if team_dict[c.team].active == 0: continue
		if c.team == team_id: continue
		
		city_loc = mod_ten_tuple((c.x, c.y))
		min_x = city_loc[0]-50
		max_x = city_loc[0]+50
		
		min_y = city_loc[1]-50
		max_y = city_loc[1]+50
		
		for x in range(min_x, max_x, 10):
			for y in range(min_y, max_y, 10):
				tile_loc = (x,y)
				
				# Ignore water
				if tile_loc not in tile_control: continue
				if terrain_tuples[tile_loc] == 0: continue
				
				tile_range = path_f.pythagoras(city_loc, tile_loc)
				tile_control[(x, y)] -= city_rules.city_control(tile_range, c, team_dict)
	
	
	# # Output for a map link
	# output_list = []
	# remove_list = []
	# for k, v in tile_control.items():
	# 	if v > 0.5:
	# 		output_list.append("(%s,%s,%s)" % (k[0], k[1], int(v)))
	# 	else:
	# 		remove_list.append(k)
	# 
	# for r in remove_list:
	# 	del(tile_control[r])
	# 
	# print '<a href="value_map?list=%s">Map</a>' % (":".join(output_list))
	
	return tile_control#, output_list
# 
# def total_influence():
# 	"""Returns a list of tiles that the team has influence on and by how much
# 	it will probably take a while to run"""
# 	city_dict = city.get_city_dict()
# 	team_dict = data.team.get_teams_dict_c()
# 	
# 	terrain_tuples = data.mapper.terrain_tuples()
# 	
# 	tile_control = {}
# 	
# 	# For each city, look at what land they control
# 	for k, c in city_dict.items():
# 		if c.dead or c.secret == 1: continue
# 		if team_dict[c.team].active == 0: continue# Note that IRs affect land control
# 		
# 		# Debug skip stuff
# 		if c.team in [104]:# Skip Seraphim
# 			continue
# 		
# 		city_loc = mod_ten_tuple((c.x, c.y))
# 		min_x = city_loc[0]-rules.city_rules.control_range
# 		max_x = city_loc[0]+rules.city_rules.control_range
# 		
# 		min_y = city_loc[1]-rules.city_rules.control_range
# 		max_y = city_loc[1]+rules.city_rules.control_range
# 		
# 		city_continent = get_tile_continent(city_loc)
# 		# if city_continent < 1: continue
# 		
# 		for x in range(min_x, max_x, 10):
# 			for y in range(min_y, max_y, 10):
# 				tile_loc = (x,y)
# 				
# 				# Ignore water
# 				if tile_loc not in terrain_tuples: continue
# 				if terrain_tuples[tile_loc] == 0: continue
# 				
# 				# Can't control stuff on other continents
# 				tile_continent = get_tile_continent(tile_loc)
# 				if tile_continent != city_continent: continue
# 				
# 				# Default value if it doesn't exist yet
# 				if (x,y) not in tile_control: tile_control[(x,y)] = {}
# 				
# 				tile_range = data.path.pythagoras(city_loc, tile_loc)
# 				control = rules.city_rules.city_control(tile_range, c)
# 				
# 				if control <= 0: continue
# 				
# 				if c.team not in tile_control[(x,y)]:
# 					tile_control[(x,y)][c.team] = 0
# 				tile_control[(x,y)][c.team] += control
# 	
# 	return tile_control
# 
# 
# def new_continent(name, x, y):
# 	query = """INSERT INTO map_continents (name, x, y)
# 		values
# 		('%s', %s, %s);""" % (database.escape(name), x, y)
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))