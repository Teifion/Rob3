import database
import collections
import time

def _timestamp_query(cursor,
					where = '',
					orderby = 'turn DESC',
					start = 0,
					limit = 0):
	
	query = "SELECT * FROM turns"
	
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
		results[row['turn']] = row['turn_time']
	
	return results

def get_all_turns(cursor):
	return _timestamp_query(cursor=cursor)

def most_recent_turns(cursor, limit=30):
	return _timestamp_query(cursor=cursor, limit=limit)