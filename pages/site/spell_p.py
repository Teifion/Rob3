from pages import common
from queries import building_q
from data_classes import trait

def spell_list(cursor, cat=None, page=None, **kwargs):
	building_dict = building_q.get_all_buildings(cursor)
	
	output = []
	
	for building_id, the_building in building_dict.items():
		if not the_building.public: continue
		# if the_trait.category not in output_dict:
		# 	output_dict[the_trait.category] = []
		
		output.append("""
		<strong><a class="clear_link" id="%(js_name)s" href="#%(js_name)s">%(building_name)s</a></strong>
		<br />
		%(description)s
		<br /><br />""" % {
			"js_name":		common.js_name(the_building.name),
			"building_name":	the_building.name,
			"description":	the_building.description,
		})
	
	return "".join(output)