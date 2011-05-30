# Preprocesses map info and caches it in the database

import database
import os, time
from queries import mapper_q

def reset_tables(cursor):
	"""Wipes all information from the tables it's about to repopulate"""
	query = """DELETE FROM map_continent_tiles"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def explore_continent(continent_id, x, y):
	pending_set	= set()
	valid_set	= set()
	viewed_set	= set()
	
	# Initialise
	pending_set.add((x,y))
	
	# Get the terrain dictionary
	terrain_dict = mapper_q.terrain_cache_dict
	
	# As long as we've got tiles to look at
	while len(pending_set) > 0:
		x, y = pending_set.pop()
		
		# If it's in the dictionary it's land and we'll use it
		if (x,y) in terrain_dict and terrain_dict[(x,y)] != 0:
			valid_set.add((x,y))
			
			# Add new tiles to pending list
			if (x-10,y-10) not in viewed_set: pending_set.add((x-10,y-10))
			if (x-10,y) not in viewed_set: pending_set.add((x-10,y))
			if (x-10,y+10) not in viewed_set: pending_set.add((x-10,y+10))
			
			if (x,y-10) not in viewed_set: pending_set.add((x,y-10))
			if (x,y+10) not in viewed_set: pending_set.add((x,y+10))
			
			if (x+10,y-10) not in viewed_set: pending_set.add((x+10,y-10))
			if (x+10,y) not in viewed_set: pending_set.add((x+10,y))
			if (x+10,y+10) not in viewed_set: pending_set.add((x+10,y+10))
		
		# Mark the tile as having been viewed
		viewed_set.add((x,y))
	
	return valid_set

def run(cursor):
	reset_tables(cursor)
	
	# Make mapper_q build the terrain dictionary
	mapper_q.get_terrain(cursor, 0, 0)
	
	# Get a list of the continents so we can loop through them
	continent_list = []
	continent_x = []
	continent_y = []
	continent_names = []
	query = """SELECT id, x, y, name FROM map_continents"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		continent_list.append(row['id'])
		continent_x.append(row['x'])
		continent_y.append(row['y'])
		continent_names.append(row['name'])
	
	for c in range(0, len(continent_list)):
		# Tile list is a list of all the tiles on that continent
		time_at_start = time.time()
		tile_list = explore_continent(continent_list[c], continent_x[c], continent_y[c])
		
		# print("Mapped %s to a length of %s in %s seconds" % (continent_names[c], len(tile_list), round(time.time() - time_at_start, 2)))
		insert_list = ["(%s, %s, %s)" % (t[0], t[1], continent_list[c]) for t in tile_list]
		
		if insert_list == []:
			print(database.shell_text("[r]Zero length insert_list for %s[/r]" % continent_names[c]))
			continue
		
		query = """INSERT INTO map_continent_tiles (x, y, continent) values %s;""" % ",".join(insert_list)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	print("Map preprocesses complete")

