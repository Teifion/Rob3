import database
import collections
from data_classes import deity

def _deity_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM deity_list"
	
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
		results[row['id']] = deity.Deity(row)
	
	return results

def get_all_deities(cursor):
	return _deity_query(cursor=cursor)

def get_one_deity(cursor, the_deity):
	if type(the_deity) != str and int(the_deity) > 0:
		query = "SELECT * FROM deity_list WHERE id = {0:d} LIMIT 1;".format(int(the_deity))
	else:
		query = "SELECT * FROM deity_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_deity))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return deity.Deity(row)