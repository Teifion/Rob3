import database
# import data

terrain_cache_dict = {}
def get_all_terrain(cursor):
	if terrain_cache_dict == {}:
		query = """SELECT x, y, terrain FROM map_terrain"""
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			terrain_cache_dict[(row['x'], row['y'])] = row['terrain']
	
	return terrain_cache_dict

def get_terrain(cursor, real_x, real_y):
	if terrain_cache_dict == {}:
		query = """SELECT x, y, terrain FROM map_terrain"""
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			terrain_cache_dict[(row['x'], row['y'])] = row['terrain']
	
	x = real_x - (real_x % 10)
	y = real_y - (real_y % 10)
	
	return terrain_cache_dict.get((x, y), 0)

# def get_resources(top, right, bottom, left):
# 	"""Returns a dictionary of the terrain within those bounds"""
# 	
# 	results = {}
# 	
# 	# Yes that's >= and < for a reason, it's to stop get getting of an extra col and row
# 	query = "SELECT x, y, resource FROM map_terrain WHERE x >= %(left)s AND x < %(right)s AND y >= %(top)s AND y < %(bottom)s" % {
# 		"left": left,
# 		"right": right,
# 		"bottom": bottom,
# 		"top": top,
# 	}
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 
# 		try:
# 			dummy_val = results[row['x']]
# 		except KeyError, e:
# 			results[row['x']] = {}
# 		except Exception as e:
# 			raise e
# 
# 		results[row['x']][row['y']] = row['resource']
# 
# 	return results
# 
# def get_resource_at_x_y(x, y, icon_size=15):
# 	resources_in_area = get_resources(
# 		left=x-(icon_size/2),
# 		right=x+(icon_size/2),
# 		top=y-(icon_size/2),
# 		bottom=y+(icon_size/2))
# 	
# 	if len(resources_in_area) < 1: return 0
# 	
# 	for k, r in resources_in_area.items():
# 		for kk, c in r.items():
# 			if c != 0: return c
# 	
# 	return 0

def set_terrain(cursor, coordinates, terrain):
	"""docstring for set_terrain"""
	coord_pairs = []
	
	for c in coordinates:
		query = "INSERT INTO map_terrain (terrain, x, y) values (%d, %d, %d);" % (terrain, c[0], c[1])
		try: cursor.execute(query)
		except Exception as e:
			# Need an insert instead
			query = "UPDATE map_terrain SET terrain = %d WHERE x = %d AND y = %d;" % (terrain, c[0], c[1])
			try: cursor.execute(query)
			except Exception as e:
				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# # Clean up
	# query = "DELETE FROM map_terrain WHERE terrain = 0"
	# try:
	# 	cursor.execute(query)
	# except Exception as e:
	# 	raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

# def set_resource(cursor, coordinates, resource):
# 	"""docstring for set_terrain"""
# 	coord_pairs = []
# 	
# 	for c in coordinates:
# 		query = "INSERT INTO map_terrain (resource, x, y) values (%d, %d, %d);" % (resource, c[0], c[1])
# 		try: cursor.execute(query)
# 		except Exception as e:
# 			# Need an insert instead
# 			query = "UPDATE map_terrain SET resource = %d WHERE x = %d AND y = %d;" % (resource, c[0], c[1])
# 			try:
# 				cursor.execute(query)
# 			except Exception as e:
# 				raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	
# 	# Clean up
# 	query = "DELETE FROM map_terrain WHERE terrain = 0 AND resource = 0"
# 	try:
# 		cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

# def get_continents():
# 	query = """SELECT * FROM map_continents ORDER BY name"""
# 	
# 	continent_list = []
# 	continent_dict = {}
# 	
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	for row in database.cursor:
# 		continent_list.append(row['id'])
# 		continent_dict[row['id']] = data.mapper.Map_continent(row)
# 	
# 	return continent_list, continent_dict