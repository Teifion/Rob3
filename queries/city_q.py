import database
import collections
from pages import common
from classes import city

def _city_query(cursor,
				where = '',
				orderby = 'dead ASC, team, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM cities"
	
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
		results[row['id']] = city.City(row)
	
	return results

def get_all_cities(cursor): return _city_query(cursor)

# def get_cities_in_list(city_list):
# 	city_list2 = [str(x) for x in city_list]# have to convert them from Ints to Strings
# 	where = 'id in (%s)' % (",".join(city_list2))
# 	return get_cities(where = where)
# 
def get_live_cities(cursor):
	return _city_query(cursor, where = "dead < 1", orderby="name")

def get_new_cities(cursor):
	return get_cities_from_turn(cursor, common.current_turn())

def get_cities_from_turn(cursor, turn):
	return _city_query(cursor, where = "founded = {0:d}".format(turn), orderby="team, name")

def get_cities_from_team(cursor, team, include_dead=False):
	if include_dead == False:
		dead_query = " AND dead < 1"
	else:
		dead_query = ''
	
	return _city_query(cursor, where = "team = %d%s" % (team, dead_query), orderby="dead asc, name")

def get_cities_for_dropdown(cursor, teams=[]):
	if teams != []:
		where = "AND team in (%s)" % ",".join([str(t) for t in teams])
	else:
		where = ""
	
	return _city_query(cursor, where="dead < 1 %s" % where, orderby="name")
	

def get_one_city(cursor=None, the_city = ''):
	if int(the_city) > 0:
		query = "SELECT * FROM cities WHERE id = {0:d} LIMIT 1;".format(int(the_city))
	else:
		query = "SELECT * FROM cities WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_city))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return city.City(row)
	

# Doesn't use the normal function because it needs to link a pair of tables
def get_cities_for_map(cursor, top, right, left, bottom):
	query = """SELECT c.* FROM cities c, teams t
		WHERE c.x > %(left)s
			AND c.x < %(right)s
			AND c.y > %(top)s
			AND c.y < %(bottom)s
			AND c.dead < 1
			AND c.team = t.id
			AND t.active = True
			ORDER BY c.population""" % {
				"left": left,
				"right": right,
				"top": top,
				"bottom": bottom,
			}
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = city.City(row)
	
	return results

# 1 big query rather than 300+ small ones
def mass_get_city_buildings(cursor, city_dict):
	for k, the_city in city_dict.items():
		the_city.buildings			= {}
		the_city.buildings_amount	= {}
	
	if city_dict == {}:
		return city_dict
	
	query = "SELECT city, building, amount, completion FROM city_buildings WHERE city in (%s)" % ",".join([str(c) for c in city_dict.keys()])
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['city'] not in city_dict: continue
		city_dict[row['city']].buildings[row['building']] = row['completion']
		city_dict[row['city']].buildings_amount[row['building']] = row['amount']
	
	return city_dict


def mass_get_city_artefacts(cursor, city_dict):
	for k, the_city in city_dict.items():
		the_city.artefacts = []
	
	query = "SELECT id, city FROM artefacts"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['city'] in city_dict:
			city_dict[row['city']].artefacts.append(row['id'])
	
	return city_dict


def mass_get_city_wonders(cursor, city_dict):
	for k, the_city in city_dict.items():
		the_city.wonders = []
	
	query = "SELECT id, city FROM wonders"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		city_dict[row['city']].wonders.append(row['id'])
	
	return city_dict

