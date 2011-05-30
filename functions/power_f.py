import database
from pages import common
# from data import power

def new_power(name, player, power_type, description):
	query = """INSERT INTO powers (name, player, type, description)
		values
		('%s', %d, %d, '%s');""" % (database.escape(name), player, power_type, database.escape(description))
	return query

def turn_history(the_world):
	"""Saves the turn history for all powers"""
	current_turn = common.current_turn()
	
	# Delete the current history
	query = """DELETE FROM power_history WHERE turn = %d""" % current_turn
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Insert time
	powers_dict = the_world.powers()
	inserts = []
	
	for power_id, the_power in powers_dict.items():
		inserts.append("(%d, %d, %d)" % (the_power.player, power_id, current_turn))
	
	if inserts == []: return
	
	# Insert!
	query = """INSERT INTO power_history (player, power, turn) values %s;""" % ",".join(inserts)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
