import database
import collections
from data_classes import servant

def _servant_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM servant_list"
	
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
		results[row['id']] = servant.Servant(row)
	
	return results

def get_all_servants(cursor):
	return _servant_query(cursor=cursor)
	
def get_servants_from_deity(cursor, deity_id):
	return _servant_query(where="deity = %d" % deity_id, cursor=cursor)

def get_one_servant(cursor, the_servant):
	if int(the_servant) > 0:
		query = "SELECT * FROM servants WHERE id = {0:d} LIMIT 1;".format(int(the_servant))
	else:
		query = "SELECT * FROM servants WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_servant))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return servant.Servant(row)

