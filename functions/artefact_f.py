import database
from pages import common
# from data import artefact

def new_artefact(name, team, city, description):
	query = """INSERT INTO artefacts (name, team, city, description)
		values
		('%(name)s', %(team)d, %(city)d, '%(description)s');""" % {
			"name":	database.escape(name),
			"team":				int(team),
			"city":				int(city),
			"description":		database.escape(description),
		}
	return query

def turn_history(the_world):
	"""Saves the turn history for all powers"""
	current_turn = common.current_turn()
	
	# Delete the current history
	query = """DELETE FROM artefact_history WHERE turn = %d""" % current_turn
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Insert time
	artefacts_dict = the_world.artefacts()
	inserts = []
	
	for artefact_id, the_artefact in artefacts_dict.items():
		inserts.append("(%d, %d, %d)" % (the_artefact.team, artefact_id, current_turn))
	
	if inserts == []: return
	
	query = """INSERT INTO artefact_history (team, artefact, turn) values %s;""" % ",".join(inserts)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
