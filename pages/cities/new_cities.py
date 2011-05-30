from pages import common
from queries import city_q, team_q

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	cities_dict = city_q.get_new_cities(cursor)
	teams_dict = team_q.get_all_teams(cursor)
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>City name</th>
			<th>&nbsp;</th>
			<th>X</th>
			<th>Y</th>
			<th>Port</th>
			<th>Secret</th>
			<th>Dead</th>
			<th>Nomadic</th>
			<th>Population</th>
			<th>Slaves</th>
			<th>&nbsp;</th>
		</tr>""")

	count = -1
	if len(cities_dict) > 0:
		for city_id, the_city in cities_dict.items():
			count += 1
			
			output.append("""
			<tr class="row%(row)d" id="%(city_id)d">
				<td>%(city_name)s (%(team_name)s)</td>
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=view_map&amp;%(map_link)s">Map link</a></td>
		
				<td>%(x)s</td>
				<td>%(y)s</td>
		
				<td style="text-align: center;">%(port)s</td>
				<td style="text-align: center;">%(secret)s</td>
				<td style="text-align: center;">%(dead)s</td>
				<td style="text-align: center;">%(nomadic)s</td>
		
				<td>%(population)s</td>
				<td>%(slaves)s</td>
			
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_city&amp;city=%(city_id)d">Edit city</a></td>
			</tr>
			""" % {	'row': (count % 2),
			
					'city_id': the_city.id,
					'city_name': common.doubleclick_text("cities", "name", the_city.id, the_city.name, "font-weight:bold"),
					"map_name":	the_city.name.replace(" ", "").lower(),
					'team_name': teams_dict[the_city.team].name,
					'x': common.doubleclick_text("cities", "x", the_city.id, the_city.x, ""),
					'y': common.doubleclick_text("cities", "y", the_city.id, the_city.y, ""),
					
					"map_link":	the_city.map_link_args(),
					
					'port': common.bstr(the_city.port),
					'secret': common.bstr(the_city.secret),
					'dead': common.bstr(the_city.dead),
					'nomadic': common.bstr(the_city.nomadic),
			
					'population': common.doubleclick_text("cities", "population", the_city.id, the_city.population, ""),
					'slaves': common.doubleclick_text("cities", "slaves", the_city.id, the_city.slaves, ""),
				})



	output.append("</table>")

	return "".join(output)