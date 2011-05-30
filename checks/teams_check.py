from pages import common
import database
from classes import world

def clear_out_old_team_caches(cursor, verbose):
	"""Get rid of all caches older than 10 turns"""
	
	cutoff = common.current_turn()-10
	
	queries = []
	
	# TI cache
	queries.append("DELETE FROM ti_cache WHERE turn < %d" % cutoff)
	
	# Post cache
	queries.append("DELETE FROM post_cache WHERE turn < %d" % cutoff)
	
	# Orders cache
	# queries.append("DELETE FROM intorders WHERE id IN SELECT post_id FROM orders WHERE turn < %d" % cutoff)
	queries.append("DELETE FROM orders WHERE turn < %d" % cutoff)
	
	for q in queries:
		try:
			cursor.execute(q)
		except Exception as e:
			print("Query: %s\n" % q)
			raise e
	
	if verbose:
		print("teams_check.clear_out_old_team_caches() cleared out all cache info over 10 turns old")

def innactive_teams_cities(cursor, verbose):
	team_list = []
	query = """SELECT id FROM teams WHERE active = False"""
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		team_list.append(str(row['id']))
	
	query = """UPDATE cities SET dead = %d WHERE team in (%s) AND dead < 1;""" % (common.current_turn(), ",".join([t for t in team_list]))
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if verbose:
		print("teams_check.innactive_teams_cities() has killed all cities for innactive teams")

def run(cursor, check_all, verbose):
	clear_out_old_team_caches(cursor, verbose)
	innactive_teams_cities(cursor, verbose)
	
	if check_all:
		pass
	
	if verbose:
		print(database.shell_text("[g]Team checks complete[/g]"))