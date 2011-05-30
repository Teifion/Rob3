from pages import common
# from data import team, team_q
# from data import artefact_q
# from data import city, city_q, team
from queries import team_q, city_q, artefact_q

page_data = {
	"Title":	"Artefact list",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	team_id = int(common.get_val('team', -1))
	
	# Get our list
	if team_id < 0:
		artefact_dict = artefact_q.get_all_artefacts(cursor)
	else:
		artefact_dict = artefact_q.get_artefacts_from_team(cursor, team_id)
	
	if len(artefact_dict) < 1:
		return "No artefacts found"
	
	team_dict = team_q.get_real_teams(cursor)
	city_dict = city_q.get_all_cities(cursor)
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Artefact name</th>
			<th>Location</th>
			<th>Description</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	for artefact_id, the_artefact in artefact_dict.items():
		if the_artefact.city not in city_dict:
			the_artefact.city = 0
		
		
		the_artefact = artefact_dict[artefact_id]
		count += 1
		
		if the_artefact.team > 0:	team_name = team_dict[the_artefact.team].name
		else:						team_name = "None"
		
		if the_artefact.city > 0:	city_name = city_dict[the_artefact.city].name
		else:						city_name = "None"
		
		output.append("""
		<tr class="row%(row)d" id="%(artefact_id)d">
			<td>%(name)s</td>
		
			<td>%(team)s, %(location)s</td>
		
			<td>%(description)s</td>
			
			<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_artefact&amp;artefact=%(artefact_id)d">Edit</a></td>
		</tr>
		""" % {	'row': (count % 2),
			
				'artefact_id':		the_artefact.id,
				'name':	the_artefact.name,
				'team':				team_name,
				'location':			city_name,
				'description':		the_artefact.description,
			})


	# # Add new artfiact
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_artefact_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_artefact" />
		<input type="hidden" name="team" id="team" value="0" />
		<input type="hidden" name="city" id="city" value="0" />
		<td style="padding: 1px;"><input type="text" name="name" id="new_name" value="" /></td>
		<td>&nbsp;</td>
		<td style="padding: 1px;"><input type="text" name="artefact_description" value="" style="width: 98%%;" /></td>
		
		<td style="padding: 1px;"><input type="submit" value="Add" /></td>
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),
			"onload":	common.onload("$('#new_name').focus();"),
			})

	output.append("</table>")
	return "".join(output)