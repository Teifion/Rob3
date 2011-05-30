from classes import power
from pages import common
from queries import player_q

def _innactive_players_list(cursor):
	output = set()
	
	query = """SELECT p.id
		FROM players p, teams t
			WHERE p.team = t.id
				AND t.active = False
				OR p.last_posted < {turn}""".format(
			turn=common.current_turn()-6
		)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.add(str(row['id']))
	
	output.add("2")
	return output


def innactive_players_with_powers(cursor):
	player_list = _innactive_players_list(cursor)
	player_dict = player_q.get_all_players(cursor)
	
	output = []
	
	query = """SELECT p.id, w.name
		FROM players p, powers w
			WHERE p.id = w.player
				AND p.id in ({players})
				AND w.type = {standard}""".format(
		players = ",".join(player_list),
		standard=power.power_types.index("Standard"),
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.append("%s (%s): %s" % (player_dict[row['id']].name, row['id'], row['name']))
	
	if output != []:
		output.insert(0, "[r]Innactive players with powers[/r]")
		output.append("")
	
	return "\n".join(output)


def _players_that_moved_team(cursor):
	player_history = {}
	player_dict = player_q.get_all_players(cursor)
	
	# Get last two turns of data
	query = """SELECT * FROM player_history WHERE turn >= %d""" % (common.current_turn()-2)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['player'] not in player_dict: continue
		if player_dict[row['player']].last_posted <= common.current_turn()-6: continue
		
		if row['player'] not in player_history:
			player_history[row['player']] = {}
		player_history[row['player']][row['turn']] = row['team']
	
	# import pprint
	# pprint.pprint(player_history)
	
	# Now find players that don't match up
	t1 = common.current_turn()-2
	t2 = common.current_turn()-1
	moved_players = []
	for p, d in player_history.items():
		if d.get(t1, 0) != d.get(t2, -1):
			# print("%s moved from %s to %s" % (player_dict[p].name, d.get(t1, 0), d.get(t2, -1)))
			moved_players.append(str(p))
	
	return moved_players

def moved_players_with_powers(cursor):
	player_list = _players_that_moved_team(cursor)
	player_dict = player_q.get_all_players(cursor)
	
	output = []
	
	query = """SELECT p.id, w.name
		FROM players p, powers w
			WHERE p.id = w.player
				AND p.id in ({players})
				AND w.type = {standard}""".format(
		players = ",".join(player_list),
		standard=power.power_types.index("Standard"),
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.append("%s (%s): %s" % (player_dict[row['id']].name, row['id'], row['name']))
	
	if output != []:
		output.insert(0, "[r]Players with powers that moved team[/r]")
		output.append("")
	
	return "\n".join(output)

def run(cursor, verbose):
	output = []
	
	output.append(innactive_players_with_powers(cursor))
	output.append(moved_players_with_powers(cursor))
	
	return "".join(output)