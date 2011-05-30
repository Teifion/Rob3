import database
from pages import common

ir_players = (
	2, # Teifion
	325, # Jaegis
	326, # Lascha
	242, # Rob
)

def ir_player_activity(cursor, verbose):
	query = """UPDATE players SET last_posted = %d WHERE id in (%s);""" % (
		common.current_turn()-5,
		",".join((str(i) for i in ir_players)))
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		print("players_check.ir_player_activity() updated all IR accounts")


def innactive_players_on_teams(cursor, verbose):
	query = """UPDATE players SET team = 0 WHERE last_posted < %d;""" % (common.current_turn()-6)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	query = """UPDATE players SET team = 0 WHERE id in (2, 242);"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		print("players_check.innactive_players_on_teams() checked player activity")


def run(cursor, check_all, verbose):
	ir_player_activity(cursor, verbose)
	innactive_players_on_teams(cursor, verbose)
	
	if check_all:
		pass
	
	if verbose:
		print(database.shell_text("[g]Player checks complete[/g]"))