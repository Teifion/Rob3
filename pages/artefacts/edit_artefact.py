from pages import common
from queries import artefact_q, city_q

page_data = {
	"Title":	"Edit artefact",
	"Admin":	True,
}

def main(cursor):
	artefact_id = int(common.get_val('artefact', 0))
	all_teams	= int(common.get_val('all_teams', 0))
	
	if artefact_id < 1:
		return "No artefact selected"
	
	the_artefact = artefact_q.get_one_artefact(cursor, artefact_id)
	
	names = {}
	if all_teams == 0 and the_artefact.team > 0:
		cities_dict = city_q.get_cities_from_team(cursor, team=the_artefact.team, include_dead=1)
		for c, the_c in cities_dict.items():
			names[c] = the_c.name
	else:
		cities_dict = city_q.get_live_cities(cursor)
		for c, the_c in cities_dict.items():
			names[c] = the_c.name
	
	output = ["<div style='padding: 5px;'>"]
	
	if all_teams != 1:
		output.append("""<a class="block_link" href="web.py?mode=edit_artefact&amp;artefact=%s&amp;all_teams=1">Show all team cities</a>""" % artefact_id)
	else:
		output.append("""<a class="block_link" href="web.py?mode=edit_artefact&amp;artefact=%s&amp;all_teams=0">Show only this team's cities</a>""" % artefact_id)
	
	output.append("""
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_artefact_commit" />
		<input type="hidden" name="id" id="id" value="%(artefact_id)s" />
	
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="name">Name:</label></td>
				<td>%(name_text)s</td>
		
				<td width="5">&nbsp;</td>
			
				<td><label for="city">City:</label></td>
				<td>%(city_menu)s</td>
			</tr>
			<tr>
				<td><label for="description">Description:</label></td>
				<td colspan="5">%(artefact_description_text)s</td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<!--
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="artefact" id="artefact" value="%(artefact_id)s" />
		<input type="hidden" name="mode" id="mode" value="remove_artefact" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete artefact" onclick="var answer = confirm('Delete %(name)s?')
		if (answer) $('#delete_form').submit();" />
	</form>
	-->
	<br /><br />""" % {
		"artefact_id":					artefact_id,
		"name":				the_artefact.name,
		"city_menu":					common.option_box(
			name='city',
			elements=names,
			element_order=cities_dict.keys(),
			custom_id="",
			selected=the_artefact.city,
		),
		"name_text":			common.text_box("name", the_artefact.name, size=20),
		"artefact_description_text":	'<textarea name="description" id="description" rows="4" cols="40">%s</textarea>' % the_artefact.description,
	})
	
	output.append("</div>")
	
	return "".join(output)