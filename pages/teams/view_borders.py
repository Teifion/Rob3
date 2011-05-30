import database
from pages import common
from queries import team_q
from classes import team

page_data = {
	"Admin":	True,
	"Redirect":	"View borders",
}

states = """<option value="-1">Default</option>
%s""" % "".join(['<option value="%d">%s</option>' % (i, b) for i, b in enumerate(team.border_states)])

def main(cursor):
	team_id = int(common.get_val('team', 0))
	if team_id < 1: return "No team selected"
	
	team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
	the_team = team_dict[team_id]
	
	borders = team_q.get_relations(cursor)
	team_borders = borders[team_id]
	
	# Find our default
	state_find = 'value="%s"' % the_team.default_borders
	
	# What to replace it with
	state_replace = '%s selected="selected"' % state_find
	
	output = ["""
	<form action="exec.py" method="post" accept-charset="utf-8" style="padding:5px;">
	<span class="stitle">Borders for {team.name}</span><br /><br />
		<input type="hidden" name="mode" id="mode" value="edit_borders" />
		<input type="hidden" name="team" id="team" value="{team.id}" />
		""".format(
			team=the_team,
		)]
	
	# Now the actual set of borders
	output.append('''
	Default border state:&nbsp;&nbsp;
	<select name="default_border_state" id="default_border_state">
		{states}
	</select>
	<br /><br />

	<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<th>Team</th>
			<th>{team.name} state</th>
			<th>Their state</th>
		</tr>'''.format(
		states	= states.replace('<option value="-1">Default</option>', '').replace(state_find, state_replace),
		team	= the_team,
	))
	
	for t, other_team in team_dict.items():
		if t == the_team.id: continue
		# if other_team.hidden: continue
		# if not other_team.active: continue
		
		ir = ""
		if other_team.ir:
			ir = " <em>(IR)</em>"
		
		other_team_borders = borders[t].get(the_team.id, {}).get('border', other_team.default_borders)
		other_default_borders = other_team.default_borders
		
		# print(other_team_borders)
		
		# The state to find
		# state_find = 'value="%s"' % team_borders.get(t, default_borders)
		
		if t in team_borders:	default_state = team_borders[t]
		else:					default_state = "-1"
		
		state_find = 'value="%s"' % default_state
		
		# What to replace it with
		state_replace = '%s selected="selected"' % state_find
		
		# Their state to you
		# if the_team.id in other_team_borders:
		# 	other_state = team.border_states[other_team_borders[the_team.id]]
		# else:
		# 	other_state = team.border_states[other_default_borders]
		other_state = other_team_borders
		
		output.append("""
		<tr>
			<td>%(name)s%(ir)s</td>
			<td>
				<select name="border_state_%(t)d" id="border_state_%(t)d">
					%(states)s
				</select>
			</td>
			<td>&nbsp;&nbsp;
				<span style="color:#%(other_state_c)s;">%(other_state)s</span>
			</td>
		</tr>
		""" % {
			"t":				t,
			"ir":				ir,
			"name":				other_team.name,
			"states":			states.replace(state_find, state_replace),
			"other_state":		team.border_states[other_state],
			"other_state_c":	team.border_colour(other_state),
		})
	
	
	# Close form
	output.append("""</table>
		<input type="submit" value="Save" />
	</form>""".format(
		team=team_id
	))
	
	
	return "".join(output)