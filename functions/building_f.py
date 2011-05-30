import database
from queries import building_q

def building_option_list(cursor, remove_list = []):
	output = []
	
	building_dict = building_q.get_all_buildings(cursor)
	
	for c, b in building_dict.items():
		if c in remove_list: continue
		
		output.append("<option value='%s'>%s</option>" % (c, b.name))
	
	return "".join(output)	

def check_row_exists(building_id, city_id):
	return "INSERT INTO city_buildings (city, building) values (%d, %d);" % (city_id, building_id)

def completion_query(the_city, the_building, new_completion):
	"""Returns a query to improve the completion of a building, if this will complete the building it'll say so"""
	queries = []
	
	if new_completion >= the_building.build_time:
		queries.append("UPDATE city_buildings SET completion = 0, amount = amount + 1 WHERE city = %d AND building = %d;" % (the_city.id, the_building.id))
		
		# Delete the uprgadable building
		if the_building.upgrades >= 0:
			queries.append("DELETE FROM city_buildings WHERE city = %d AND building = %d;" % (the_city.id, the_building.upgrades))
	else:
		queries.append("UPDATE city_buildings SET completion = %s WHERE city = %d AND building = %d;" % (new_completion, the_city.id, the_building.id))
	
	return queries
