import database
from pages import common

def save_results(cursor, result_dict, turn=-1):
	if turn < 1: turn = common.current_turn()
	
	# Delete any existing
	query = """DELETE FROM results_log WHERE turn = {turn} AND failures = False AND team in ({teams})""".format(
		turn = turn,
		teams = ",".join([str(k) for k in result_dict.keys()]),
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Write in the new stuff
	query = """INSERT INTO results_log (team, turn, failures, content) VALUES {content};""".format(
		content = ",".join(["(%d, %d, False, '%s')" % (t, turn, database.escape("\n".join(c))) for t, c in result_dict.items()])
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))


def save_failures(cursor, result_dict, turn=-1):
	if turn < 1: turn = common.current_turn()
	
	# Delete any existing
	query = """DELETE FROM results_log WHERE turn = {turn} AND failures = True AND team in ({teams})""".format(
		turn = turn,
		teams = ",".join([str(k) for k in result_dict.keys()]),
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Write in the new stuff
	query = """INSERT INTO results_log (team, turn, failures, content) VALUES {content};""".format(
		content = ",".join(["(%d, %d, True, '%s')" % (t, turn, database.escape("\n".join(c))) for t, c in result_dict.items()])
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))