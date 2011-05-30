import database
import collections
from data_classes import evolution

def _evolution_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM evolution_list"
	
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
		results[row['id']] = evolution.Evolution(row)
	
	return results

def get_all_evolutions(cursor):
	return _evolution_query(cursor=cursor)
	
def get_one_evolution(cursor, the_evolution):
	if type(the_evolution) == int:
		query = "SELECT * FROM evolution_list WHERE id = {0:d} LIMIT 1;".format(int(the_evolution))
	else:
		query = "SELECT * FROM evolution_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_evolution))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return evolution.Evolution(row)
	

def get_one_evolution_level(cursor, evo_id, team_id):
	query = """SELECT level FROM team_evolutions WHERE evolution = %d AND team = %d""" % (evo_id, team_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['level']
	
	return 0