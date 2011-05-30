import database
import collections
from classes import player
from pages import common

def _player_query(cursor,
				where = 'not_a_player = False',
				orderby = 'last_posted DESC, name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM players"
	
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
		results[row['id']] = player.Player(row)
	
	return results


def get_all_players(cursor):
	return _player_query(cursor=cursor)

def get_active_players(cursor, turn_count = 7):
	last_post_deadline = common.current_turn() - turn_count
	return _player_query(cursor, where="not_a_player = False AND last_posted > %s" % last_post_deadline, orderby="name")

def get_players_from_team(cursor, team_id):
	return _player_query(cursor, where="team = %d" % int(team_id))

def get_one_player(cursor, the_player):
	if int(the_player) > 0:
		query = "SELECT * FROM players WHERE id = {0:d} LIMIT 1;".format(int(the_player))
	else:
		query = "SELECT * FROM players WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_player))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return player.Player(row)

def get_kills(cursor, battle = -1, killer = -1, victim = -1):
	"""Returns all the player MSN requests"""
	results = []
	
	if type(battle) == int and battle > 0:
		query = """SELECT * FROM player_kills WHERE battle = %d ORDER BY turn DESC""" % battle
	elif type(battle) == list:
		query = """SELECT * FROM player_kills WHERE battle in (%s) ORDER BY turn DESC""" % ",".join([str(c) for c in battle])
	elif type(killer) == list:
		query = """SELECT * FROM player_kills WHERE killer in (%s) ORDER BY turn DESC""" % ",".join([str(k) for k in killer])
	elif killer > 0:
		query = """SELECT * FROM player_kills WHERE killer = %d ORDER BY turn DESC""" % killer
	elif type(victim) == list:
		query = """SELECT * FROM player_kills WHERE victim in (%s) ORDER BY turn DESC""" % ",".join([str(v) for v in victim])
	elif victim > 0:
		query = """SELECT * FROM player_kills WHERE victim = %d ORDER BY turn DESC""" % victim
	else:
		query = """SELECT * FROM player_kills"""
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results.append(row)
	
	return results

# def get_achievements(since_turn=0):
# 	"""Gets all the achievements since turn X"""
# 	query = """SELECT * FROM achievements WHERE turn >= %d ORDER BY turn DESC""" % since_turn
# 	
# 	results_list = []
# 	results_dict = {}
# 	
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		results_list.append({
# 			"killer":	row['killer'],
# 			"victim":	row['victim'],
# 			"turn":		row['turn'],
# 		})
# 		
# 		if not results_dict.has_key(row['turn']): results_dict[row['turn']] = []
# 		results_dict[row['turn']].append({
# 			"killer":	row['killer'],
# 			"victim":	row['victim'],
# 		})
# 	
# 	return results_list, results_dict


def mass_get_player_powers(cursor, player_dict):
	for k, the_player in player_dict.items():
		the_player.powers = []
	
	query = "SELECT id, player FROM powers"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		player_dict[row['player']].powers.append(row['id'])
	
	return player_dict