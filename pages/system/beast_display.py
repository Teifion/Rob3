from pages import common
from data_classes import equipment
from queries import equipment_q
from classes import res_dict
from lists import continent_list
from rules import map_data

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	category = common.get_val("category", "Beast")
	
	equipment_dict = equipment_q.get_equipment_of_type(cursor, equipment.cat_list.index(category))
	
	output = []
	
	for e, the_eq in equipment_dict.items():
		if the_eq.description == "":
			continue
		
		location = ""
		if the_eq.continent > 0:
			if the_eq.terrain > 0:
				location = "<br /><em>Found on %s in %s terrain</em>" % (continent_list.data_list[the_eq.continent], map_data.terrain[the_eq.terrain])
			else:
				location = "<br /><em>Found on %s</em>" % continent_list.data_list[the_eq.continent].name
		else:
			if the_eq.terrain > 0:
				location = "<br /><em>Found in %s terrain</em>" % map_data.terrain[the_eq.terrain]
	
		output.append("""
		<span class="stitle">%(name)s</span> - Cost: %(cost)s<br />
		%(description)s
		%(location)s
		<br /><br />
	
		""" % {
			"name":			the_eq.name,
			"cost":			res_dict.Res_dict(the_eq.cost).get("Materials"),
			"description":	the_eq.description.replace("\n", "<br />"),
			"location":		location,
		})


	return "".join(output)