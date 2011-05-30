import database
import collections
from classes import wonder

def _wonder_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM wonders"
	
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
		results[row['id']] = wonder.Wonder(row)
	
	return results

def get_all_wonders(cursor): return _wonder_query(cursor)

def get_one_wonder(cursor, the_wonder = ''):
	if int(the_wonder) > 0:
		query = "SELECT * FROM wonders WHERE id = {0:d} LIMIT 1;".format(int(the_wonder))
	else:
		query = "SELECT * FROM wonders WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_wonder))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return wonder.Wonder(row)
