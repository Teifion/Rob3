import database
from classes import mission
from pages import common

def get_missions(where = '',
				orderby = 'time_posted DESC',
				start = 0,
				limit = 0):
	"""Query to get the mission
	"""
	
	mission_order = []
	mission_found = {}
	
	query = "SELECT * FROM missions"
	
	# Where
	if where != '': query += " WHERE %s" % where
	
	# Order by
	if orderby != '': query += " ORDER BY %s" % orderby
	
	# Limit stuff
	if start > 0 and limit > 0: query += " LIMIT %s, %s" % (start, limit)
	if start > 0 and limit < 1: query += " LIMIT 0, %s" % (limit)
	if start < 1 and limit > 0: query += " LIMIT %s" % (limit)
	
	try:	 database.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in database.cursor:
		mission_order.append(row["id"])
		mission_found[row["id"]] = mission.Mission(row)
	
	return mission_order, mission_found

def get_one_mission(mission_id):
	query = "SELECT * FROM missions WHERE id = %d" % int(mission_id)
	
	try: database.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in database.cursor:
		return row

def get_missions_from_team(team_id):
	return get_missions(where="team=%d" % team_id)

def get_pending_missions():
	return get_missions(where="state = 0")

def get_one_pending_mission_id():
	query = """SELECT id FROM missions WHERE state = %d LIMIT 1""" % mission.mission_states.index("Pending result")
	try: database.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in database.cursor: return row['id']
	
	return -1

def delete_mission(mission_id):
	query = """DELETE FROM missions WHERE id = %d""" % mission_id
	try: database.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def get_missions_in_list(mission_list):
	mission_list2 = [str(x) for x in mission_list]# have to convert them from Ints to Strings
	where = 'id in (%s)' % (",".join(mission_list2))
	return get_missions(where = where)

def get_latest_missions(turns):
	since_turn = common.current_turn() - turns
	return get_missions(where="turn>%d" % since_turn)