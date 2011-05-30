import database
import collections
from data_classes import spell

def _spell_query(cursor,
				where = '',
				orderby = 'tier ASC, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM spell_list"
	
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
		results[row['id']] = spell.Spell(row)
	
	return results

def get_all_spells(cursor):
	return _spell_query(cursor)

def get_spells_from_lore(cursor, lore):
	return _spell_query(cursor, where="category = %d" % int(lore))

def get_one_spell(cursor, the_spell):
	if type(the_spell) == int:
		query = "SELECT * FROM spell_list WHERE id = {0:d} LIMIT 1;".format(int(the_spell))
	else:
		query = "SELECT * FROM spell_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_spell))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return spell.Spell(row)
