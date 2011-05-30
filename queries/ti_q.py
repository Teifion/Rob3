import json
import database
import collections
from classes import army

def get_json_ti(cursor, team, turn):
	query = """SELECT content FROM team_json_ti WHERE team = %d AND turn = %d""" % (team, turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return json.loads(row['content'].replace(r'\\', '\\'))
	
	return {}

def get_json_tis_from_turn(cursor, turn):
	results = {}
	
	query = """SELECT team, content FROM team_json_ti WHERE turn = %d""" % (turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		j = json.loads(row['content'].replace(r'\\', '\\'))
		results[row['team']] = j
	
	return results