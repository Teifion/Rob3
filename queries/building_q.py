import database
import collections
from data_classes import building

def _building_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM building_list"
	
	# Where
	if where != '': query += " WHERE %s" % where
	
	# Order by
	if orderby != '': query += " ORDER BY %s" % orderby
	
	# Limit stuff
	if start > 0 and limit > 0: query += " LIMIT %s, %s" % (start, limit)
	if start > 0 and limit < 1: query += " LIMIT 0, %s" % (limit)
	if start < 1 and limit > 0: query += " LIMIT %s" % (limit)
	
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = building.Building(row)
	
	return results

def get_all_buildings(cursor, orderby="name"):
	return _building_query(cursor, orderby=orderby)

def get_all_walls(cursor):
	return _building_query(cursor, where="Wall = True")

def get_one_building(cursor, the_building):
	if type(the_building) != str:
		query = "SELECT * FROM building_list WHERE id = {0:d} LIMIT 1;".format(int(the_building))
	else:
		query = "SELECT * FROM building_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_building))

	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return building.Building(row)

# def team_building_count(team, building_id_list, city_in_progress=-1):
# 	"""Pass it a list and it'll return the number of working buildings in that list"""
# 	if len(building_id_list) < 1: return 0
# 	
# 	query = "SELECT b.amount, b.completion, c.id FROM city_buildings b, cities c WHERE c.team = %d AND b.city = c.id AND b.building in (%s)" % (team, ",".join([str(the_id) for the_id in building_id_list]))
# 	
# 	count = 0
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		count += row['amount']
# 		if row['id'] != city_in_progress:
# 			if row['completion'] > 0:
# 				count += 1
# 	
# 	return count
# 
# def city_building_count(city, building_id_list, count_in_progress=False):
# 	"""Pass it a list and it'll return the number of working buildings in that list"""
# 	if len(building_id_list) < 1: return 0
# 	
# 	query = "SELECT b.building, b.amount, b.completion FROM city_buildings b WHERE b.city = %d AND b.building in (%s);" % (city, ", ".join([str(the_id) for the_id in building_id_list]))
# 	
# 	count = 0
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		count += row['amount']
# 		if count_in_progress:
# 			if row['completion'] > 0:
# 				count += 1
# 	
# 	return count
# 
# def current_progress(city_id, building_id):
# 	"""Gets the current progress and amount for a building type in a city"""
# 	query = "SELECT amount, completion FROM city_buildings WHERE city = %d AND building = %d LIMIT 1;" % (city_id, building_id)
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	
# 	row = database.cursor.fetchone()
# 	if row == None:
# 		return 0, 0
# 	
# 	return row['amount'], row['completion']