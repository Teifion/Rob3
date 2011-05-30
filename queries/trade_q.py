import database
import collections

def get_distance_matrix(cursor):
	distances = {}
	
	query = """SELECT * FROM trade_distances"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['city_1'] not in distances:
			distances[row['city_1']] = {}
		
		distances[row['city_1']][row['city_2']] = row['distance']
	
	return distances