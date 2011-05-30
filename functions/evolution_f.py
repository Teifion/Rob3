from queries import evolution_q

def evolution_option_list(cursor, remove_list=[], default=0):
	"""docstring for evolution_option_list"""
	output = []
	
	evolution_dict = evolution_q.get_all_evolutions(cursor)
	
	for evo_id, the_evo in evolution_dict.items():
		if evo_id in remove_list:
			continue
		
		if evo_id == default:
			output.append("<option value='%s' selected='selected'>%s</option>" % (evo_id, the_evo.name))
		else:
			output.append("<option value='%s'>%s</option>" % (evo_id, the_evo.name))
	
	return "".join(output)


# def get_team_evo_level(name, team_id):
# 	"""Returns the level that the team has of a given evolution"""
# 	evo_id = evolution.get_evolution_dict_n()[name]
# 	
# 	query = """SELECT level FROM team_evolutions WHERE evolution = %d AND team = %d""" % (evo_id, team_id)
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	
# 	row = database.cursor.fetchone()
# 	if row == None: return 0
# 	return row['level']
# 	
