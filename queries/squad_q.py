import database
import collections
from classes import squad
import random

def _squad_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM squads"
	
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
		results[row['id']] = squad.Squad(row)
	
	return results


def get_all_squads(cursor):
	return _squad_query(cursor)

def get_squads_from_team(cursor, team):
	return _squad_query(cursor, where = "team = %d" % int(team))

def get_squads_of_type(cursor, unit, team_id=-1):
	if team_id > 0:
		return _squad_query(cursor, where = "unit = %d AND team = %d" % (int(unit), int(team_id)))
	else:
		return _squad_query(cursor, where = "unit = %d" % int(unit))

def get_squads_from_army(cursor, army):
	return _squad_query(cursor, where = "army = %d" % int(army))

def get_squads_from_army_and_unit(cursor, army, unit):
	return _squad_query(cursor, where = "army = %d AND unit = %d" % (int(army), int(unit)))

def get_squads_from_list(cursor, squad_list):
	if len(squad_list) < 1:
		return collections.OrderedDict()
	return _squad_query(cursor, where = "id in (%s)" % ",".join([str(s) for s in squad_list]))

def get_squads_from_team_of_type(cursor, team, unit):
	return _squad_query(cursor, where = "team = %d and unit = %d" % (int(team), int(unit)))

def get_one_squad(cursor, the_squad):
	if int(the_squad) > 0:
		query = "SELECT * FROM squads WHERE id = {0:d} LIMIT 1;".format(int(the_squad))
	else:
		query = "SELECT * FROM squads WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_squad))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return squad.Squad(row)

def create_empty_squad(cursor, name, army_id, unit_id, team_id):
	# Insert
	query = """INSERT INTO squads (name, army, unit, team, amount)
		values
		(
			'{name}',
			{army},
			{unit},
			{team},
			0
		);""".format(
			name=database.escape(name),
			army=army_id,
			unit=unit_id,
			team=team_id,
		)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Now get the ID of the squad
	query = """SELECT id, name FROM squads
		WHERE army = {army}
		ORDER BY id DESC
		LIMIT 1""".format(
			army=army_id,
		)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if name == row['name']:
			return row['id']
	
	# Not entered in, this is a bad sign :(
	raise Exception("Squad was not found in the database args:(%s, %s, %s, %d, %d, %d)" % (cursor, name, army_id, unit_id, team_id))


def mass_get_squads(cursor, army_dict):
	id_list = [str(a) for a in army_dict.keys()]
	if len(id_list) < 1:
		return collections.OrderedDict()
	squad_dict = _squad_query(cursor, where = "army in (%s)" % ",".join(id_list))
	
	for squad_id, the_squad in squad_dict.items():
		army_dict[the_squad.army].squads[squad_id] = the_squad