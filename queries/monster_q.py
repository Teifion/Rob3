import database
import collections
from data_classes import monster

def _monster_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM monster_list"
	
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
		results[row['id']] = monster.Monster(row)
	
	return results

def get_all_monsters(cursor, orderby="name"):
	return _monster_query(cursor, orderby=orderby)

def get_all_walls(cursor):
	return _monster_query(cursor, where="Wall = True")

def get_one_monster(cursor, the_monster):
	if type(the_monster) != str:
		query = "SELECT * FROM monster_list WHERE id = {0:d} LIMIT 1;".format(int(the_monster))
	else:
		query = "SELECT * FROM monster_list WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_monster))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return monster.Monster(row)

def get_monsters_from_army(cursor, army_id):
	query = """SELECT monster, amount FROM army_monsters WHERE army = %d""" % army_id
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	results = {}
	for row in cursor:
		results[row['monster']] = row['amount']
	
	return results

