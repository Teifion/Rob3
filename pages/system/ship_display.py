from pages import common
from data_classes import equipment
from queries import equipment_q
from classes import res_dict
import math

page_data = {
	"Title":	"Ship list",
	"Admin":	True,
}

def main(cursor):
	equipment_dict = equipment_q.get_equipment_of_type(cursor, equipment.cat_list.index('Boat hull'))
	
	count = -1
	output = ["""
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Hull</th>
			<th>Material cost</th>
			<th>Point cost</th>
			<th>Crew</th>
			<th>Transport capacity</th>
		</tr>
	"""]
	
	for e, the_equipment in equipment_dict.items(): 
		if the_equipment.public == False:
			continue
	
		count+=1
	
		the_cost = res_dict.Res_dict(the_equipment.cost)
	
		# Equipment output
		output.append("""
		<tr class="row%(count)s">
			<td>%(hull)s</td>
			<td>%(materials)s</td>
			<td>%(points)s</td>
			<td>%(crew)s</td>
			<td>%(transport)s</td>
		</tr>""" % {
			"count":		count%2,
			"hull":			the_equipment.name,
			"materials":	the_cost.get("Materials"),
			"points":		the_cost.get("Ship points"),
			"crew":			the_equipment.crew,
			"transport":	the_equipment.transport,
		})
	
	output.append("</table>")
	return "".join(output)