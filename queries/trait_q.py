import database
import collections
from data_classes import trait

def _trait_query(cursor,
				where = '',
				orderby = 'category, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM trait_list"
	
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
		results[row['id']] = trait.Trait(row)
	
	return results

def get_all_traits(cursor, orderby="name"):
	return _trait_query(cursor, orderby=orderby)

def get_one_trait(cursor, the_trait):
	if type(the_trait) != str:
		query = "SELECT * FROM trait_list WHERE id = {0:d} LIMIT 1;".format(int(the_trait))
	else:
		query = "SELECT * FROM trait_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_trait))

	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return trait.Trait(row)