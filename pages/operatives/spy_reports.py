from pages import common
from queries import city_q, team_q
from functions import team_f, spy_report_f

page_data = {
	"Title":	"Spy reports",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	# Team select
	team_select = team_f.structured_list(cursor, include_irs = False, default=-1, field_name="team", field_id="team_select", skip=[])
	team_select = team_select.replace(">", '><option value="-1" selected="selected">GM report</option>', 1)
	
	# City select
	city_names = {}
	cities_dict = city_q.get_live_cities(cursor)
	team_dict = team_q.get_all_teams(cursor)
	for c, the_c in cities_dict.items():
		if the_c.dead > 0: continue
		city_names[c] = "{0} (<em>{1}</em>)".format(the_c.name, team_dict[the_c.team].name)
	
	# Selection output
	output.append("""
	<form action="web.py?mode=generate_report" method="post" accept-charset="utf-8">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<td>Team:</td>
				<td style="padding:1px;">{team_select}</td>
			</tr>
			<tr>
				<td>Target team:</td>
				<td>{target_team_select}</td>
			</tr>
			<tr>
				<td colspan="2">
					<input type="submit" value="Continue &rarr;" />
				</td>
			</tr>
		</table>
	</form>
	<br /><br />
	
	<form action="web.py?mode=generate_report" id="report_form" method="post" accept-charset="utf-8">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<td>Team:</td>
				<td style="padding:1px;">{team_select}</td>
			</tr>
			<tr>
				<td>Target city:</td>
				<td>{city_select}</td>
			</tr>
			<tr>
				<td>Target area:</td>
				<td><input type="text" name="area" id="area_select" value="" size="10"/>
					<input type="text" name="radius" id="radius" value="1" size="5"/></td>
			</tr>
			<tr>
				<td colspan="2">
					<input type="submit" value="Continue &rarr;" />
				</td>
			</tr>
		</table>
	</form>
	{onload}
	""".format(
		team_select = team_select,
		target_team_select = team_f.structured_list(cursor, include_irs = False, default=-1, field_name="target_team", field_id="target_team", skip=[]),
		city_select = common.option_box(
			name			= 'city',
			elements		= city_names,
			element_order	= cities_dict.keys(),
			# custom_id="",
			# selected=the_artefact.city,
		),
		onload = common.onload("$('#team_select').focus();")
	))
	
	return "".join(output)
