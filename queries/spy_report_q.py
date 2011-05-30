import database
import collections
from classes import army

def _army_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM armies"
	
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
		results[row['id']] = army.Army(row)
	
	return results

def get_all_armies(cursor):
	return _army_query(cursor)

def get_all_non_garrisons(cursor):
	return _army_query(cursor, where="garrison < 1")

def get_armies_from_team(cursor, team, include_garrisons=False):
	if include_garrisons:
		garrison_query = ''
	else:
		garrison_query = " AND garrison < 1"
	
	return _army_query(cursor, where = "team = %d%s" % (int(team), garrison_query))

def get_armies_from_team_list(cursor, teams, include_garrisons=False):
	if include_garrisons:
		garrison_query = ''
	else:
		garrison_query = " AND garrison < 1"
	
	return _army_query(cursor, where = "team in (%s)%s" % (",".join([str(t) for t in teams]), garrison_query))

def get_armies_from_list(cursor, army_list):
	return _army_query(cursor, where = "id in (%s)" % (",".join([str(a) for a in army_list])))

def get_one_army(cursor, the_army):
	if int(the_army) > 0:
		query = "SELECT * FROM armies WHERE id = {0:d} LIMIT 1;".format(int(the_army))
	else:
		query = "SELECT * FROM armies WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_army))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return army.Army(row)

# def get_one_army(army_id = -1, name = '', team_id=-1):
# 	if army_id > 0:
# 		query = "SELECT * FROM armies WHERE id = %d" % army_id
# 	else:
# 		if team_id > 0:
# 			query = "SELECT * FROM armies WHERE name = '%s' AND team = %d" % (database.escape(name), int(team_id))
# 		else:
# 			query = "SELECT * FROM armies WHERE name = '%s'" % database.escape(name)
# 	
# 	try: database.cursor.execute(query)
# 	except Exception as e:
# 		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
# 	for row in database.cursor:
# 		return row
# 
# def get_all_armies_from_team(team_id):
# 	return get_armies(where="team = %s AND dead = False" % team_id)
# 
# 
# 
# def delete_army(army_id):
# 	"""Deletes a army of that ID, returns the Team ID of the army"""
# 	query = """SELECT team FROM armies WHERE id = %s LIMIT 1;""" % army_id
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	
# 	row = database.cursor.fetchone()
# 	if row == None: return -1
# 	the_team = row['team']
# 	
# 	# Now to delete the army
# 	query = """DELETE FROM armies WHERE id = %s;""" % army_id
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	
# 	# Delete all squads from that army
# 	query = """DELETE FROM squads WHERE army = %s""" % army_id
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 		
# 	return the_team


def create_empty_army(cursor, name, team_id, x, y):
	# Insert
	query = """INSERT INTO armies (name, team, x, y)
		values
		(
			'{name}',
			{team},
			{x},
			{y},
		);""".format(
			name=database.escape(name),
			team=team_id,
			x=x,
			y=y,
		)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Now get the ID of the army
	query = """SELECT id, name FROM armies
		WHERE team = {team}
		ORDER BY id DESC
		LIMIT 1""".format(
			team=team_id,
		)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if name == row['name']:
			return row['id']
	
	# Not entered in, this is a bad sign :(
	raise Exception("Army was not found in the database args:(%s, %s, %d, %d, %d)" % (cursor, name, team_id, x, y))
