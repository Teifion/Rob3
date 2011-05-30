import database
import collections
from data_classes import lore_entry

def _lore_query(cursor,
				where = '',
				orderby = 'id',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM lore_entries"
	
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
		results[row['id']] = lore_query.Lore_query(row)
	
	return results

def get_all_entries(cursor, orderby="id"):
	return _lore_query(cursor, orderby=orderby)

def get_one_entry(cursor, cat, page):
	query = "SELECT * FROM lore_entries WHERE cat = '{0:s}' AND page = '{1:s}' LIMIT 1;".format(database.escape(cat.lower().replace(" ", "_")), database.escape(page.lower().replace(" ", "_")))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return lore_entry.Lore_entry(row)