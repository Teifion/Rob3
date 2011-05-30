import time
from pages import common
from data import mission, mission_q
from data import team, team_f
from data import city, city_q

mission_order, mission_dict = mission_q.get_missions(limit=50)
cities_order, cities_dict = city_q.get_live_cities()

# Used for the option box later
names = {}
for c in cities_order:
	names[c] = cities_dict[c].name

city_missions_list, city_missions_dict = [], {}
team_missions_list, team_missions_dict = [], {}
for m in range(0, len(mission.mission_types)):
	if mission.mission_types[m] in mission.city_targets:
		city_missions_list.append(m)
		city_missions_dict[m] = mission.mission_types[m]
	
	elif mission.mission_types[m] in mission.team_targets:
		team_missions_list.append(m)
		team_missions_dict[m] = mission.mission_types[m]


teams_dict = team.get_teams_dict()

output = []
output.append("""
<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
	<tr class="row2">
		<th>Team</th>
		<th>Turn</th>
		<th>State</th>
		<!--
		<th>Posted</th>
		<th>Closed</th>
		-->
		<th>Type</th>
		<th>Target</th>
		<!--
		<th>Information</th>
		-->
		<th>&nbsp;</th>
		<th>&nbsp;</th>
	</tr>""")

count = -1
for mission_id in mission_order:
	the_mission = mission_dict[mission_id]
	count += 1
	
	if the_mission.target not in cities_dict:
		continue
	
	# Target text
	if mission.mission_types[the_mission.type] in mission.city_targets:
		the_target = cities_dict[the_mission.target].name
		target_team = "(%s)" % teams_dict[cities_dict[the_mission.target].team]
	elif mission.mission_types[the_mission.type] in mission.team_targets:
		the_target = teams_dict[the_mission.target]
		target_team = ""
	
	# Handle link and current state
	handle = '<td>&nbsp;</td>'
	state_text = mission.mission_states[the_mission.state]
	if the_mission.state == 0:
		state_text = "<strong>%s</strong>" % mission.mission_states[the_mission.state]
		handle = '<td style="padding: 0px;"><a class="block_link" href="handle_mission&amp;mission=%d">Handle</a></td>' % mission_id
	
	output.append("""
	<tr class="row%(row)d" id="%(mission_id)d">
		<td>%(name)s</td>
		<td>%(turn)s</td>
		
		<td>%(state)s</td>
		
		<td>%(type)s</td>
		<td>%(target)s <em>%(target_team)s</em></td>
		
		%(handle)s		
		<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_mission&amp;mission=%(mission_id)d">Edit mission</a></td>
	</tr>
	""" % {	'row': (count % 2),
			
			'mission_id':	mission_id,
			'name':	teams_dict[the_mission.team],
			'turn':			the_mission.turn,
			'state':		state_text,
			'posted':		the_mission.time_posted,
			'closed':		the_mission.time_closed,
			'type':			mission.mission_types[the_mission.type],
			'target':		the_target,
			"target_team":	target_team,
			'information':	the_mission.information,
			
			"handle":		handle,
		})


# Add new mission, city targets
count += 1
output.append("""
<tr class="row%(row)d">
	<form action="exec.py" id="add_mission_form" method="post" accept-charset="utf-8">
	<input type="hidden" name="mode" value="add_mission" />
	<td style="padding: 1px;">
		%(team)s
	</td>
	<td style="padding: 1px;">
		%(turn)s
	</td>
	<td style="padding: 1px;">
		%(state)s
	</td>
	
	<!--
	<td>&nbsp;</td>
	<td>&nbsp;</td>
	-->
	
	<td style="padding: 1px;">%(type)s</td>
	<td style="padding: 1px;">%(target)s</td>
	
	<!--
	<td>&nbsp;</td>
	-->
	
	<td style="padding: 0px;" colspan="2"><a class="block_link" href="#" onclick="$('#add_mission_form').submit();">Add</a></td>
	</form>
	%(onload)s
</tr>
""" % {	'row':			(count % 2),
		
		"team":			team_f.structured_list(field_name="team", field_id="new_mission_team"),
		"turn":			common.text_box('turn', text=common.current_turn(), size=5),
		"state":		common.option_box("state", mission.mission_states),
		
		"type":			common.option_box("type",
			elements=city_missions_dict,
			element_order=city_missions_list,
		),
		"target":		common.option_box(
			name='target',
			elements=names,
			element_order=cities_order,
		),
		
		"time_posted":	int(time.time()),
		"onload":		common.onload("$('#new_mission_team').focus();"),
		})


# New mission, team targets
count += 1
output.append("""
<tr class="row%(row)d">
	<form action="exec.py" id="add_mission_form_team" method="post" accept-charset="utf-8">
	<input type="hidden" name="mode" value="add_mission" />
	<td style="padding: 1px;">
		%(team)s
	</td>
	<td style="padding: 1px;">
		%(turn)s
	</td>
	<td style="padding: 1px;">
		%(state)s
	</td>

	<!--
	<td>&nbsp;</td>
	<td>&nbsp;</td>
	-->

	<td style="padding: 1px;">%(type)s</td>
	<td style="padding: 1px;">%(target)s</td>

	<!--
	<td>&nbsp;</td>
	-->

	<td style="padding: 0px;" colspan="2"><a class="block_link" href="#" onclick="$('#add_mission_form_team').submit();">Add</a></td>
	</form>
</tr>
<tr class="row%(row_two)d">
	<td style="padding:0px;" colspan="7">
		<a href="latest_missions" class="block_link">Show unhandled missions</a>
	</td>
</tr>
""" % {	'row':			(count % 2),
		'row_two':		((count+1) % 2),
		
		"team":			team_f.structured_list(field_name="team"),
		"turn":			common.text_box('turn', text=common.current_turn(), size=5),
		"state":		common.option_box("state", mission.mission_states),
		
		"type":			common.option_box("type",
			elements=team_missions_dict,
			element_order=team_missions_list,
		),
		"target":		team_f.structured_list(field_name="target"),
		
		"time_posted":	int(time.time()),
		})

output.append("</table>")

print("".join(output))