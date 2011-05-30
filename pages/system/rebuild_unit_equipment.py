from queries import unit_q, equipment_q
from functions import equipment_f

page_data = {
	"Title":	"Rebuild unit equipment",
	"Admin":	True,
}

def main(cursor):
	return rebuild_units(cursor)

def rebuild_units(cursor):
	output = []
	unit_dict = unit_q.get_all_units(cursor)
	equipment_dict = equipment_q.get_all_equipment(cursor)
	
	for unit_id, the_unit in unit_dict.items():
		equipment_string = the_unit.equipment_string
		
		if equipment_string == "":
			continue
		
		equipment_list = equipment_f.match_equipment_from_string(cursor, equipment_string, equipment_dict)
		
		# print the_unit.unit_name, ", ", unit_id, '&nbsp;&nbsp;&nbsp;&nbsp;'
		equipment_q.replace_unit_equipment(cursor, unit_id, equipment_list)
		# print "<br />"
		
		output.append(the_unit.name)
	
	return "<br />".join(output)