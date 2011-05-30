import re
from lists import resource_list
from pages import common
from rules import map_data

# To save us converting the same one all the time
def print_form_element(resource_id, current_value):
	"""Prints the relevant form element for a given type of resource"""
	this_type = resource_list.data_dict[resource_id].type
	
	# We don't want a 10.0, we want 10
	if current_value == int(current_value):
		current_value = int(current_value)
	
	output = ''
	
	if this_type == 'discrete':
		return common.text_box("res_%s" % resource_list.data_dict[resource_id].name, current_value, size=6)
	
	elif this_type == 'boolean':
		return common.check_box("res_%s" % resource_list.data_dict[resource_id].name, current_value)
	
	return output

# def all_supplies():
# 	"""docstring for all_supplies"""
# 	res_dict = resource.get_resources_dict_c()
# 	d = Res_dict()
# 	
# 	for k, v in res_dict.items():
# 		if v.type == "boolean":
# 			d.value[k] = 1
# 	
# 	return d

# def resource_grep_list(tradable_only=False):
# 	"""Returns order-grep lists"""
# 	if tradable_only:
# 		query = """SELECT id, resource_name FROM resource_list WHERE tradable = True ORDER BY id DESC"""
# 	else:
# 		query = """SELECT id, resource_name FROM resource_list ORDER BY id DESC"""
# 	
# 	resource_id_list = []
# 	resource_name_list = []
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		resource_id_list.append(row['id'])
# 		resource_name_list.append(row['resource_name'])
# 	
# 	return resource_id_list, resource_name_list