import database
import collections
from data_classes import tech

def _tech_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM tech_list"
	
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
		results[row['id']] = tech.Tech(row)
	
	return results

def get_all_techs(cursor):
	return _tech_query(cursor)

def get_techs_from_lore(cursor, lore):
	return _tech_query(cursor, where="lore = %d" % int(lore))

def get_one_tech(cursor, the_tech):
	if type(the_tech) == int:
		query = "SELECT * FROM tech_list WHERE id = {0:d} LIMIT 1;".format(int(the_tech))
	else:
		query = "SELECT * FROM tech_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_tech))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return tech.Tech(row)
