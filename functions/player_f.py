from pages import common
import database

def add_kill(killer, victim, turn=-1, battle=-1):
	if turn < 0: turn = common.current_turn()
	
	query = """INSERT INTO player_kills (killer, victim, turn, battle)
		values
		(%d, %d, %d, %d);""" % (killer, victim, turn, battle)
	
	return [query]

def remove_kill(killer, victim, turn=-1, battle=-1):
	if turn > 0 and battle > 0:
		where = "AND turn = %d AND battle = %d" % (turn, battle)
	elif turn > 0 and battle <= 0:
		where = "AND turn = %d" % (turn)
	elif turn <= 0 and battle > 0:
		where = "AND battle = %d" % (battle)
	else:
		raise Exception("Turn and Battle were both < 0")
	
	return ["""DELETE FROM player_kills WHERE killer = %d AND victim = %d %s""" % (killer, victim, where)]

def update_player_activity(player_dict):
	queries = []
	
	for p, t in player_dict.items():
		queries.append("UPDATE players SET last_posted = %d, team = %s WHERE id = %s;" % (common.current_turn(), t, p))
	
	return queries


def turn_history(the_world):
	current_turn = common.current_turn()
	
	# Delete the current history
	query = """DELETE FROM player_history WHERE turn = %d""" % current_turn
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Insert time
	players_dict = the_world.players()
	inserts = []
	
	for player_id, the_player in players_dict.items():
		inserts.append("(%d, %d, %d)" % (the_player.team, player_id, current_turn))
	
	if inserts == []: return
	
	# Insert!
	query = """INSERT INTO player_history (team, player, turn) values %s;""" % ",".join(inserts)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
