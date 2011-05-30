import database
import collections
from classes import artefact

def _artefact_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM artefacts"
	
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
		results[row['id']] = artefact.Artefact(row)
	
	return results

def get_all_artefacts(cursor): return _artefact_query(cursor)

# def get_artefacts_in_list(artefact_list):
# 	artefact_list2 = [str(x) for x in artefact_list]# have to convert them from Ints to Strings
# 	where = 'id in (%s)' % (",".join(artefact_list2))
# 	return get_artefacts(where = where)

def get_artefacts_from_team(cursor, team):
	return _artefact_query(cursor, where = "team = %d" % (team), orderby="name")

def get_one_artefact(cursor, the_artefact):
	if int(the_artefact) > 0:
		query = "SELECT * FROM artefacts WHERE id = %d LIMIT 1;" % int(the_artefact)
	else:
		query = "SELECT * FROM artefacts WHERE name = '%s' LIMIT 1;" % database.escape(the_artefact)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return artefact.Artefact(row)
