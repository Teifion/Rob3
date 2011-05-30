from pages import common
from queries import wonder_q, city_q, team_q

page_data = {
	"Title":	"Edit wonder",
	"Admin":	True,
}

def main(cursor):
	wonder_id = int(common.get_val('wonder', 0))
	
	if wonder_id < 1: return "No wonder selected"
	
	the_wonder = wonder_q.get_one_wonder(cursor, wonder_id)
	cities_dict = city_q.get_live_cities(cursor)
	teams_dict = team_q.get_real_teams(cursor)
	
	names = {}
	for c, the_city in cities_dict.items():
		names[c] = the_city.name
	
	# TODO Make this do it properly
	tnames = {}
	for t, the_team in teams_dict.items():
		tnames[t] = the_team.name
	
	output = ["<div style='padding: 5px;'>"]
	
	output.append("""
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_wonder_commit" />
		<input type="hidden" name="id" id="id" value="%(wonder_id)s" />
	
		Editing: %(name_text)s
		<br /><br />
	
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="city">City:</label></td>
				<td>%(city_menu)s</td>
		
				<td width="5">&nbsp;</td>
			
				<td><label for="team">Team:</label></td>
				<td>%(team_menu)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="completed">Completed:</label></td>
				<td style="padding: 1px;">%(completed)s</td>
			</tr>
			<tr>
				<td><label for="completion">Completion:</label></td>
				<td style="padding: 1px;">%(completion)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="point_cost">Point cost:</label></td>
				<td style="padding: 1px;">%(point_cost)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="material_cost">Material cost:</label></td>
				<td style="padding: 1px;">%(material_cost)s</td>
			</tr>
			<tr>
				<td colspan="10">&nbsp;&nbsp;&nbsp;Description:<br />
					%(description)s
				</td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="wonder" id="wonder" value="%(wonder_id)s" />
		<input type="hidden" name="mode" id="mode" value="remove_wonder" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete wonder" onclick="var answer = confirm('Delete %(name_safe)s?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""" % {
		"wonder_id":					wonder_id,
		"name_text":				common.text_box("name", the_wonder.name),
		
		"city_menu":					common.option_box(
			name='city',
			elements=names,
			element_order=cities_dict.keys(),
			custom_id="",
			selected=the_wonder.city,
		),
		
		"team_menu":					common.option_box(
			name='team',
			elements=tnames,
			element_order=teams_dict.keys(),
			custom_id="",
			selected=the_wonder.team,
		),
		
		"completed":				common.check_box("completed", the_wonder.completed),
		"completion":				common.text_box("completion", the_wonder.completion, size=7),
		"point_cost":				common.text_box("point_cost", the_wonder.point_cost, size=7),
		"material_cost":			common.text_box("material_cost", the_wonder.material_cost, size=7),
		
		"description":	'<textarea name="description" id="description" rows="4" style="width:99%%;">%s</textarea>' % the_wonder.description,
		
		"name_safe":			common.js_name(the_wonder.name),
	})
	
	output.append("</div>")
	
	return "".join(output)