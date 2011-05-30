import database
import collections
# import order_post
from classes import unit
from queries import team_q

def _unit_query(cursor,
				where = '',
				orderby = '',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM units"
	
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
		results[row['id']] = unit.Unit(row)
	
	return results


def get_all_units(cursor):
	return _unit_query(cursor)

def get_units_from_team(cursor, team, special_units=False):
	if special_units:
		where = 'team = %d OR team = 0' % int(team)
	else:
		where = 'team = %d' % int(team)
	
	return _unit_query(cursor, where=where)

def get_units_from_team_list(cursor, teams, special_units=False):
	if special_units:
		teams.append(0)
	
	where = 'team in (%s)' % ",".join([str(t) for t in teams])
	
	return _unit_query(cursor, where=where)

def get_all_live_units(cursor):
	team_list = list(team_q.get_real_active_teams(cursor, skip_irs = True).keys())
	team_list.append(1)
	
	return _unit_query(cursor, where="team in (%s)" % ",".join([str(t) for t in team_list]))

def get_one_unit(cursor, the_unit):
	if int(the_unit) > 0:
		query = "SELECT * FROM units WHERE id = {0:d} LIMIT 1;".format(int(the_unit))
	else:
		query = "SELECT * FROM units WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_unit))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return unit.Unit(row)

def mass_get_unit_equipment(cursor, unit_dict):
	for k, the_unit in unit_dict.items():
		the_unit.equipmet = []
	
	query = "SELECT equipment, unit FROM unit_equipment"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['unit'] not in unit_dict: continue
		unit_dict[row['unit']].equipment.append(row['equipment'])
	
	return unit_dict