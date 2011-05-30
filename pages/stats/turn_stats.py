from pages import common
from data import stat, stat_f
from data import team
from data import resource_f

selected_turn = int(common.get_val("turn", common.current_turn()))
selected_turn = min(common.current_turn(), selected_turn)

output = []

# Get stats dict
stat_by_turn = stat.get_stat_by_turn()
if selected_turn not in stat_by_turn:
	print "The stats for turn %d do not exist" % selected_turn
	exit()

stat_dict = stat_by_turn[selected_turn]

# Build team dict
team_list		= team.get_teams_list()
teams_dict_c	= team.get_teams_dict_c()

output.append("""
<table border="0" cellspacing="0" cellpadding="5">
	<tr>
		<td>
			<span class="stitle">Turn %(selected_turn)s stats</span>
		</td>
		<td>
			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		</td>
		<td style="padding:0;">
			<a class="block_link" href="turn_stats&amp;turn=%(previous_turn)s">Previous turn</a>
		</td>
		<td style="padding:0;"
			<a class="block_link" href="turn_stats&amp;turn=%(next_turn)s">Next turn</a>
		</td>
		<td>
			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		</td>
	</tr>
</table><br />""" % {
	"previous_turn":	selected_turn-1,
	"selected_turn":	selected_turn,
	"next_turn":		selected_turn+1,
})

output.append("""
<table border="0" cellspacing="0" cellpadding="5" style="width:100%;">
	<tr class="row2">
		<th>Team</th>
		<th>Population</th>
		<th>Slaves</th>
		<th>Resources</th>
		<th>Production</th>
		<th>Army</th>
		<th>Navy</th>
		<th>Airforce</th>
		<th>Operatives</th>
		<th>Mages</th>
		<th>Land</th>
		<th>Cities</th>
		<th>Losses</th>
	</tr>""")

i = -1
for t in team_list:
	the_team = teams_dict_c[t]
	if the_team.dead or the_team.not_a_team or the_team.ir or not the_team.active: continue
	
	i += 1
	
	the_stat = stat_dict[t]
	
	# Currently
	res_dict = res_dict.Res_dict(the_stat.resources)
	materials = res_dict.get("Materials")
	if materials < 0:
		resources_string = '<strong class="neg">%s</strong>' % int(materials)
	else:
		resources_string = int(materials)
	
	# Production
	res_dict = res_dict.Res_dict(the_stat.production)
	materials = res_dict.get("Materials")
	if materials < 0:
		production_string = '<strong class="neg">%s</strong>' % int(materials)
	else:
		production_string = int(materials)
	
	output.append("""
	<tr class="row%(count)s">
		<td style="padding:0;"><a style="text-align:right;" href="team_stats&amp;team=%(t)s" class="block_link">%(name)s</a></td>
		<td>%(population)s</td>
		<td>%(slaves)s</td>
		<td>%(resources)s</td>
		<td>%(production)s</td>
		<td>%(army_size)s</td>
		<td>%(navy_size)s</td>
		<td>%(airforce_size)s</td>
		<td>%(operatives)s</td>
		<td>%(mages)s</td>
		<td>%(land_controlled)s</td>
		<td>%(city_count)s</td>
		<td>%(war_losses)s</td>
	</tr>
	""" % {
		"count":			i%2,
		"t":				t,
		"name":				the_team.name,
		"population":		common.number_format(the_stat.population),
		"slaves":			common.number_format(the_stat.slaves),
		"resources":		resources_string,
		"production":		production_string,
		"army_size":		common.number_format(the_stat.army_size),
		"navy_size":		common.number_format(the_stat.navy_size),
		"airforce_size":	common.number_format(the_stat.airforce_size),
		"operatives":		common.number_format(the_stat.operatives),
		"mages":			common.number_format(the_stat.mages),
		"land_controlled":	common.number_format(the_stat.land_controlled),
		"city_count":		common.number_format(the_stat.city_count),
		"war_losses":		common.number_format(the_stat.war_losses),
	})

output.append("</table>")

print "".join(output)