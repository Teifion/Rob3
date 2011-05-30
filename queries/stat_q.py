import database
import collections
from classes import stat
from rules import building_rules

def _stat_query(cursor,
				where = '',
				orderby = 'team, turn DESC',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM team_stats"
	
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
		results[(row['team'],row['turn'])] = stat.Stat(row)
	
	return results

def get_all_stats(cursor):
	return _stat_query(cursor)

def get_stats_from_team(cursor, team):
	return _stat_query(cursor, where = "team = %d" % (int(team)))

def get_temple_count(cursor, team):
	cursor = database.get_cursor()
	query = """SELECT count(*) FROM
		cities c, city_buildings b
			WHERE c.team = {team} AND c.dead < 1
				AND b.city = c.id AND b.building in (23, 50)
	""".format(
		team = team,
	)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		return row['count']
		
	


