import database
import collections
from data_classes import equipment

def _equipment_query(cursor,
				where = '',
				orderby = 'name',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM equipment_list"
	
	# Where
	if where != '': query += " WHERE %s" % where
	
	# Order by
	if orderby != '': query += " ORDER BY %s" % orderby
	
	# Limit stuff
	if start > 0 and limit > 0: query += " LIMIT %s, %s" % (start, limit)
	if start > 0 and limit < 1: query += " LIMIT 0, %s" % (limit)
	if start < 1 and limit > 0: query += " LIMIT %s" % (limit)
	
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = equipment.Equipment(row)
	
	return results

def get_all_equipment(cursor):
	return _equipment_query(cursor=cursor)

def get_equipment_of_type(cursor, category):
	return _equipment_query(cursor=cursor, where="category = %d" % category)

def get_one_equipment(cursor, the_equipment):
	if int(the_equipment) > 0:
		query = "SELECT * FROM equipments WHERE id = {0:d} LIMIT 1;".format(int(the_equipment))
	else:
		query = "SELECT * FROM equipments WHERE name = '{0:s}' LIMIT 1;".format(database.escape(the_equipment))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return equipment.Team(row)

def replace_unit_equipment(cursor, unit, equipment=[]):
	"""Wipes all equipment a unit currently has an rebuilds it from the list"""
	query = "DELETE FROM unit_equipment WHERE unit = %d" % unit
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if len(equipment) < 1: return
	
	insert_string = []
	for e in equipment:
		insert_string.append("(%d, %d)" % (unit, e))
	
	query = "INSERT INTO unit_equipment (unit, equipment) values %s;" % ", ".join(insert_string)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))



# def get_public_equipment():
# 	return get_equipment(where="public = True")
# 
# def get_ships():
# 	return get_equipment(where="category = %s" % equipment.cat_list.index('Boat hull'), orderby="")