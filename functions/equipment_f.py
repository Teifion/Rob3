import re
# import database
# 
# from data import equipment
from queries import equipment_q

def equipment_option_list(cursor, remove_list=[], default=0):
	output = []
	
	equipment_dict = equipment_q.get_all_equipment(cursor)
	for current_equipment, the_equip in equipment_dict.items():
		if current_equipment in remove_list:
			continue
		
		if current_equipment == default:
			output.append("<option value='%s' selected='selected'>%s</option>" % (current_equipment, the_equip.name))
		else:
			output.append("<option value='%s'>%s</option>" % (current_equipment, the_equip.name))
	
	return "".join(output)

def equipment_grep_string(cursor, force_requery=False):
	grep_list = []
	query = "SELECT name FROM equipment_list ORDER BY grep_priority DESC"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		grep_list.append(row['name'])
	
	return "(%s)" % "|".join(grep_list)

def match_equipment_from_string(cursor, equipment_string, equipment_dict={}):
	equipment_string = ". %s" % equipment_string.lower()
	
	origional_equipment_string = equipment_string
	
	if equipment_dict == {}:
		equipment_dict = equipment_q.get_all_equipment(cursor)
	grep_string = equipment_grep_string(cursor)
	
	e_list = []
	
	mapping = {
		"untrained":		"no training",
		"low training":		"basic training",
		"normal training":	"standard training",
		"high training":	"good training",
	}
	for k, v in mapping.items():
		equipment_string = equipment_string.replace(k, v)
	
	# Case sensetivity
	equipment_dict_new = {}
	for k, e in equipment_dict.items():
		equipment_dict_new[e.name.lower()] = k
	
	equipment_string = equipment_string.replace('. transport.', '. transport ship.')
	
	equipment_string = equipment_string.replace('. 160kg.', '. 160kg balloon.')
	equipment_string = equipment_string.replace('. 350kg.', '. 350kg balloon.')
	equipment_string = equipment_string.replace('. 650kg.', '. 650kg balloon.')
	equipment_string = equipment_string.replace('. 1000kg.', '. 1000kg balloon.')
	equipment_string = equipment_string.replace('. 1800kg.', '. 1800kg balloon.')
	
	equipment_string = equipment_string.replace('. 100 tonnes.', '. 100 tonne hull.')
	equipment_string = equipment_string.replace('. 250 tonnes.', '. 250 tonne hull.')
	equipment_string = equipment_string.replace('. 400 tonnes.', '. 400 tonne hull.')
	equipment_string = equipment_string.replace('. 600 tonnes.', '. 600 tonne hull.')
	equipment_string = equipment_string.replace('. 800 tonnes.', '. 800 tonne hull.')
	equipment_string = equipment_string.replace('. flat bottom boat.', '. landing craft.')
	
	training_exists = False
	results = re.findall(grep_string.lower(), equipment_string)#, re.IGNORECASE)
	set_list = []
	for r in results:
		if equipment_dict_new[r] in (1,2,3,4,5, 6):
			training_exists = True
		
		if r in set_list: continue
		e_list.append(equipment_dict_new[r])
		set_list.append(r)
		equipment_string = equipment_string.replace(r, '')
	
	if training_exists == False:
		e_list.append(3)# Standard training
	
	return e_list
