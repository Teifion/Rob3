import time
from pages import common
from data import mission, mission_q
from data import team_f, city_q

mission_id = int(common.get_val('mission', 0))

if mission_id < 1:
	print "No mission selected"
	exit()

the_mission = mission.Mission(mission_q.get_one_mission(mission_id))

output = []

# If it's not closed then time = 0
if the_mission.time_closed == 0:
	closed_string = "<span class='neg'>Still open</span>"
else:
	closed_string = time.strftime("%A, %d %B %Y", time.localtime(the_mission.time_closed))

# Target stuff
if mission.mission_types[the_mission.type] in mission.city_targets:
	cities_order, cities_dict = city_q.get_live_cities()
	names = {}
	for c in cities_order:
		names[c] = cities_dict[c].name
	
	target_string = common.option_box(name='target', elements=names, element_order=cities_order, selected=the_mission.target)
elif mission.mission_types[the_mission.type] in mission.team_targets:
	target_string = team_f.structured_list(field_name="target", default=the_mission.target)



output.append("""
<form action="exec.py" method="post" accept-charset="utf-8" style="padding:10px;">
	<input type="hidden" name="mode" id="mode" value="edit_mission_commit" />
	<input type="hidden" name="id" id="id" value="%(mission_id)d" />
	
	<input type="hidden" name="requestTime" id="requestTime" value="' . $the_team->requestTime . '" />
	<table border="0" cellspacing="5" cellpadding="5">
		<tr>
			<td><label for="team">Team:</label></td>
			<td style="padding: 1px;">%(team)s</td>
		
			<td>&nbsp;</td>
			
			<td><label for="target">Target:</label></td>
			<td style="padding: 1px;">%(target)s</td>
		</tr>
		<tr>
			<td><label for="state">State:</label></td>
			<td style="padding: 5px;">%(state)s</td>
		
			<td>&nbsp;</td>
		
			<td><label for="turn">Turn:</label></td>
			<td style="padding: 1px;">%(turn)s</td>
		</tr>
		<tr>
			<td><label for="time_posted">Posted:</label></td>
			<td>%(time_posted)s</td>
			
			<td>&nbsp;</td>
			
			<td><label for="time_closed">Closed:</label></td>
			<td>%(time_closed)s</td>
		</tr>
	</table>
	<input type="submit" value="Perform edit" />
</form>
<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
	<input type="hidden" name="mission" id="mission" value="%(mission_id)s" />
	<input type="hidden" name="mode" id="mode" value="remove_mission" />
	<input style="float:right; margin-right:100px;" type="button" value="Delete mission" onclick="var answer = confirm('Delete this mission?')
	if (answer) $('#delete_form').submit();" />
</form>""" % {
	"mission_id":	mission_id,
	"team":			team_f.structured_list(default=the_mission.team, field_name="team"),
	"target":		target_string,
	
	"turn":			common.text_box("turn", the_mission.turn),
	"state":		mission.mission_states[the_mission.state],	
	# "state":		common.option_box("state", elements=mission.mission_states, selected=mission.mission_states[the_mission.state]),
	
	"time_posted":	time.strftime("%A, %d %B %Y", time.localtime(the_mission.time_posted)),
	"time_closed":	closed_string,
	
	
})

# # Fields
# self.add_field("type",				"int")
# self.add_field("target",			"int")
# 
# self.add_field("information",		"text")
# 
# # Calc'd fields
# self.cities		= []
# self.enemy_ops	= []
# self.allied_ops	= []

print("".join(output))