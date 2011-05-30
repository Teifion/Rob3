# import math
import database
# from rules import military_rules
# from data import squad_f
# from data import army_q
# 
def create_garrison(cursor, city_id):
	"""Creates a new garrison for a city"""
	# Get city name
	query = "SELECT name, team FROM cities WHERE id = %d LIMIT 1;" % city_id
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	row = cursor.fetchone()
	if row == None: return
	
	return new_army("%s garrison" % row['name'], row['team'], x=0, y=0, garrison=city_id)

def name_garrison(city_id, city_name):
	return "UPDATE armies SET name = '%s garrison' WHERE garrison = %d;" % (database.escape(city_name), city_id)

def new_army(name, team, x, y, garrison=0):
	query = """INSERT INTO armies (name, team, x, y, garrison)
		values
		('%(name)s', %(team)d, %(x)s, %(y)s, %(city_id)d)""" % {
			"name":			database.escape(name),
			"team":			int(team),
			"city_id":		int(garrison),
			"x":			int(x),
			"y":			int(y),
		}
	
	return query

def move_armies(armies, location):
	x, y = location
	return "UPDATE armies SET x = %d, y = %d WHERE id in (%s);" % (x, y, ",".join([str(a) for a in armies]))

def location_history(the_world):
	query = """UPDATE armies SET old_x = x, old_y = y"""
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def make_relocation_query(army_id, new_position):
	return ["UPDATE armies SET x = %d, y = %d WHERE id = %d;" % (int(new_position[0]), int(new_position[1]), int(army_id))]

def make_delete_query(army_id):
	query = [
		"DELETE FROM campaign_armies WHERE army = %d" % (int(army_id)),
		"DELETE FROM squads WHERE army = %d;" % (int(army_id)),
		"DELETE FROM armies WHERE id = %d;" % (int(army_id)),
	]
	return query

def make_rename_query(army_id, new_name):
	return ["UPDATE armies SET name = '%s' WHERE id = %d;" % (database.escape(new_name), army_id)]