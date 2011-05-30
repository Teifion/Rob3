import re
from pages import common
# from data import unit_f
# from data import equipment, equipment_f
from queries import equipment_q
from functions import equipment_f, unit_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	team			= int(common.get_val("team", -1))
	uname			= common.get_val("name", "")
	total_string	= common.get_val("equipment_string", "")
	
	equipment_dict = equipment_q.get_all_equipment(cursor)
	
	if uname == "":
		uname = re.search(r"^([A-Za-z' ]*)", total_string.strip()).groups()[0].strip()
		total_string = total_string.replace(uname, "")
	
	# Get the size
	size_match = re.search(r'(size: ?([0-9]*))', total_string, re.IGNORECASE)
	if size_match != None:
		size = int(size_match.groups()[1])
		temp_string = total_string.replace(size_match.groups()[0], '')
	else:
		size = 100
		temp_string = total_string
	
	# Description
	desc_match = re.search(r'(description: ?(.*))$', temp_string, re.IGNORECASE)
	if desc_match != None:
		description = desc_match.groups()[1]
		temp_string = total_string.replace(desc_match.groups()[0], '')
	else:
		description = ""
	
	# And now equipment
	e_list = equipment_f.match_equipment_from_string(cursor, temp_string)
	
	# print("")
	# print("Team: %d<br />" % team)
	# print("Unit name: %s<br />" % uname)
	# print("Equ: %s<br />" % [equipment_dict[e].name for e in e_list])
	# print("Size: %s<br />" % size)
	# print("Desc: %s<br />" % description)
	# exit()
	
	unit_f.new_unit(cursor, team, uname, description, size, e_list)
	
	# Redirect
	page_data['Redirect'] = 'list_units&team={0:d}'.format(team)
	return ""

