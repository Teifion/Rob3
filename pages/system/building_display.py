from pages import common
from data_classes import building
from classes import res_dict
from queries import building_q
import math

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	building_dict	= building_q.get_all_buildings(cursor)
	
	count = -1
	output = ["""
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Name</th>
			<th>Turns</th>
			<th>Effect</th>
		</tr>
	"""]
	
	for b, the_building in building_dict.items(): 
		if the_building.public == False:
			continue
		
		count+=1
		
		the_cost = res_dict.Res_dict(the_building.cost_per_turn)
		
		# Equipment output
		output.append("""
		<tr class="row%(count)s">
			<td>%(name)s</td>
			<td>%(turns)s</td>
			<td>%(effect)s</td>
		</tr>""" % {
			"count":		count%2,
			"name":			the_building.name,
			"turns":		int(the_building.build_time/100.0),
			"effect":		the_building.description,
		})
	
	output.append("</table>")
	return "".join(output)