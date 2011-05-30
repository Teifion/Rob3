import database
from classes import world
from queries import unit_q

def rebuild_equipment_string(cursor, unit_id, the_world=None):
	if the_world == None:
		the_world = world.World(cursor)
	
	# Does what it says on the tin
	equipment_dict = the_world.equipment()
	
	equipment_list = []
	equipment_list_name = []
	
	query = """SELECT equipment FROM unit_equipment WHERE unit = %d""" % unit_id
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		equipment_list.append(row['equipment'])
		equipment_list_name.append(equipment_dict[row['equipment']].name)
	
	equipment_string = ""
	
	if len(equipment_list_name) == 1:
		equipment_string = equipment_list_name[0]
		
	if len(equipment_list_name) > 1:
		equipment_string = "%s and %s" % (", ".join(equipment_list_name[0:-1]), equipment_list_name[-1])
	
	query = """UPDATE units SET equipment_string = '%s' WHERE id = %d;""" % (database.escape(equipment_string), unit_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	

def add_equipment(unit, item):
	return "INSERT INTO unit_equipment (unit, equipment) values (%d, %d)" % (unit, item)

def remove_equipment(unit, item):
	return "DELETE FROM unit_equipment WHERE unit = %d AND equipment = %d;" % (unit, item)

def replace_equipment(unit, equipment_list):
	inserts = ["(%d, %d)" % (unit, e) for e in equipment_list]
	
	return [
		"DELETE FROM unit_equipment WHERE unit = %d" % (unit),
		"INSERT INTO unit_equipment (unit, equipment) values %s;" % ",".join(inserts),
	]

def delete_unit(unit_id):
	queries = []
	
	# Delete the equipment
	queries.append("DELETE FROM unit_equipment WHERE unit = %d;" % unit_id)
	
	# Now to delete the city
	queries.append("DELETE FROM units WHERE id = %d;" % unit_id)
	
	return queries

def new_unit(cursor, team_id, name, description, size, equipment_list):
	"""Inserts a new unit into the database"""
	
	if size < 1: size = 100
	
	# Insert unit
	query = """INSERT INTO units (team, name, description, size) values (%d, '%s', '%s', %d);""" % (team_id, database.escape(name), database.escape(description), size)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if len(equipment_list) < 1:
		return
	
	# Get unit id
	query = """SELECT id FROM units WHERE name = '%s' AND team = %d LIMIT 1;""" % (database.escape(name), team_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	row = cursor.fetchone()
	if row == None: return
	unit_id = row['id']
	
	# Insert equipment
	query = """INSERT INTO unit_equipment (unit, equipment) values %s;"""% (
		",".join(["(%d, %d)" % (unit_id, e) for e in equipment_list]))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	return unit_id
