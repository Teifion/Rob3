import database
import collections
from classes import power

def _power_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM powers"
	
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
		results[row['id']] = power.Power(row)
	
	return results


def get_all_powers(cursor): return _power_query(cursor)
def get_powers_in_list(cursor, power_list):
	power_list2 = [str(x) for x in power_list]# have to convert them from Ints to Strings
	where = 'id in (%s)' % (",".join(power_list2))
	return _power_query(cursor, where = where)

def get_one_power(cursor, the_power):
	if int(the_power) > 0:
		query = "SELECT * FROM powers WHERE id = {0:d} LIMIT 1;".format(int(the_power))
	else:
		query = "SELECT * FROM powers WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_power))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return power.Power(row)

# def get_powers_from_team(team_id):
# 	return get_powers(where="team = %s" % team_id)

def get_powers_from_player(cursor, player_id):
	return _power_query(cursor, where="player = %d" % int(player_id))
