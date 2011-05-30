from pages import common
from queries import wonder_q, city_q, team_q

page_data = {
	"Title":	"Wonder list",
	"Admin":	True,
}

def main(cursor):
	wonders_dict = wonder_q.get_all_wonders(cursor)
	cities_dict = city_q.get_all_cities(cursor)
	teams_dict = team_q.get_all_teams(cursor)
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Wonder name</th>
			<th>City</th>
			<th>Points</th>
			<th>Materials</th>
			<th>Description</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	if len(wonders_dict) > 0:
		for wonder_id, the_wonder in wonders_dict.items():
			count += 1
			
			# May need a key-exception try-catch block around this
			the_city = cities_dict[the_wonder.city]
			# city_string = "%s <em>(%s)</em>" % (the_city.name, teams_dict[the_city.team].name)
		
			output.append("""
			<tr class="row%(row)d" id="%(wonder_id)d">
				<td>%(name)s</td>
				<td>%(city)s <em>%(team)s</em></td>
			
				<td>%(completion)s/%(point_cost)s</td>
				<td>%(material_cost)s</td>
			
				<td>%(description)s</td>
			
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_wonder&amp;wonder=%(wonder_id)d">Edit wonder</a></td>
			</tr>
			""" % {	'row': (count % 2),
				
					'wonder_id':	the_wonder.id,
					'name':			common.doubleclick_text("wonders", "name", the_wonder.id, the_wonder.name, "font-weight:bold"),
				
					"completion":		common.doubleclick_text("wonders", "completion", the_wonder.id, the_wonder.completion, size=5),
					"point_cost":		common.doubleclick_text("wonders", "point_cost", the_wonder.id, the_wonder.point_cost, size=5),
					"material_cost":	common.doubleclick_text("wonders", "material_cost", the_wonder.id, the_wonder.material_cost, size=5),
				
					"description":		the_wonder.description,
				
					'city':		the_city.name,
					"team":		teams_dict[the_wonder.team].name,
				})



	cities_dict = city_q.get_live_cities(cursor)
	names = {}
	for c, the_city in cities_dict.items():
		names[c] = the_city.name

	# Add new wonder
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_wonder_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_wonder" />
	
		<td style="padding: 1px;"><input type="text" name="name" id="new_name" value="" /></td>
		<td style="padding: 0px;">%(city_menu)s</td>
		<td style="padding: 2px;"><input type="text" name="point_cost" value="" size="7"/></td>
		<td style="padding: 2px;"><input type="text" name="material_cost" value="" size="7"/></td>
	
		<td style="padding: 2px;"><input type="text" style="width:95%%;" name="description" value=""/></td>
	
		<td style="padding: 0px;"><a class="block_link" href="#" onclick="$('#add_wonder_form').submit();">Add</a></td>
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),
		
			"city_menu":					common.option_box(
				name='city',
				elements=names,
				element_order=cities_dict.keys(),
				custom_id="",
				# selected=the_artefact.city,
			),
			"onload":	common.onload("$('#new_name').focus();"),
			})


	output.append("</table>")

	return "".join(output)