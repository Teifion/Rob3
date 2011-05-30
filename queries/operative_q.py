import database
import collections
from classes import operative
from pages import common

def _operative_query(cursor,
					where = '',
					orderby = 'team, died',
					start = 0,
					limit = 0,):
	
	query = "SELECT * FROM operatives"
	
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
		results[row['id']] = operative.Operative(row)
	
	return results

def get_all_operatives(cursor):
	return _operative_query(cursor)

def get_operatives_in_list(cursor, operative_list):
	operative_list2 = [str(x) for x in operative_list]# have to convert them from Ints to Strings
	where = 'id in (%s)' % (",".join(operative_list2))
	return _operative_query(cursor, where = where)

def get_operatives_from_team(cursor, team):
	return _operative_query(cursor, where = "team = %d" % (team))

def get_operatives_from_city(cursor, city):
	return _operative_query(cursor, where = "city = %d" % (city))

def get_one_operative(cursor=None, the_op = ''):
	if type(the_op) == str:
		query = "SELECT * FROM operatives WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_op))
	else:
		query = "SELECT * FROM operatives WHERE id = {0:d} LIMIT 1;".format(int(the_op))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return operative.Operative(row)

def operatives_caught_in_cities(cursor, city_list, since=0):
	return _operative_query(cursor, where = "died >= %d AND city IN (%s)" % (int(since), ",".join([str(c) for c in city_list])))