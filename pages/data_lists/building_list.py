import math
from pages import common
from queries import building_q

page_data = {
	"Title":	"Building data list",
	"Admin":	True,
}

def main(cursor):
	building_dict = building_q.get_all_buildings(cursor, orderby="id")
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" sstyle="width: 100%;">
		<tr class="row2">
			<th>ID</th>
			<th>Building</th>
			<th>Upgrades</th>
			<th>Build time</th>
			
			<th>Wall</th>
			<th>Needs port</th>
			<th>Public</th>
		</tr>""")
		
		# database.Varchar_field("cost_per_turn",	max_length=50),
		# database.Varchar_field("cost_up_front",	max_length=50),
		# database.Varchar_field("upkeep",		max_length=50),
		# 
		# database.Integer_field("limit_per_city"),
		# 
		# database.Varchar_field("description",		max_length=255),
	
	count = -1
	for building_id, the_building in building_dict.items():
		count += 1
		
		upgrade_string = ""
		if the_building.upgrades > -1:
			upgrade_string = "%s (%d)" % (building_dict[the_building.upgrades].name, the_building.upgrades)
		
		output.append("""
		<tr class="row{row}" id="{id}">
			<td>{id}</td>
			<td>{name}</td>
			<td>{upgrades}</td>
			<td>{build_time}</td>
			
			<td>{wall}</td>
			<td>{needs_port}</td>
			<td>{public}</td>
		</tr>
		""".format(
			id=building_id,
			row=count%2,
			
			name = the_building.name,
			build_time = the_building.build_time,
			
			upgrades = upgrade_string,
			
			wall = the_building.wall,
			needs_port = the_building.needs_port,
			public = the_building.public,
	))
	
	output.append("</table>")

	return "".join(output)