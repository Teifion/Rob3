import database

def new_wonder(name, city, point_cost, material_cost, description):
	return """INSERT INTO wonders (name, city, point_cost, material_cost, description)
		values
		('%(name)s', %(city)d, %(point_cost)d, %(material_cost)d, '%(description)s');""" % {
			"name":		database.escape(name),
			"city":				city,
			"point_cost":		point_cost,
			"material_cost":	material_cost,
			"description":		database.escape(description),
		}

def completion_query(wonder_id, new_completion):
	queries = []
	queries.append("UPDATE wonders SET completion = %d WHERE id = %d" % (new_completion, wonder_id))
	
	return queries

def delete_wonder(wonder_id):
	return """DELETE FROM wonders WHERE id = %s;""" % int(wonder_id)