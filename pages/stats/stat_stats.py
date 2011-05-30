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


# 
# /*	Work out teams
# *******************************/
# asort($teamsWithStats);
# 
# 
# 
# /*	Fit data together
# *******************************/
# $teamCount = 0;
# foreach ($teamsWithStats as $teamId => $teamName)
# {
#	++$teamCount;
#	$dataGrid[$teamId] = array();
#	
#	foreach ($statTypeArrayNice as $statKey => $statName)
#	{
#		// We might need to set the stat
#		if (!isset($totalStat[$statKey]))
#		{
#			$totalStat[$statKey]	= 0;
#			$minStat[$statKey]		= 999999999;
#			$maxStat[$statKey]		= -99999999;
#		}
#		
#		$value = $statsArray[$teamId]->getStat($statKey);
#		
#		// Overall stat stuff
#		$totalStat[$statKey]	+= $value;
#		$minStat[$statKey]		= min($value, $minStat[$statKey]);
#		$maxStat[$statKey]		= max($value, $maxStat[$statKey]);
#		
#		
#		// Actually assign the value
#		$dataGrid[$teamId][$statKey] = $value;
#	}
# }
# 
# 
# 
# 
# /*	Do stuff to data?
# *******************************/
# foreach ($statTypeArrayNice as $statKey => $statName)
# {
#	$averageStat[$statKey] = round($totalStat[$statKey]/$teamCount);
# }
# 
# 
# /*	Headings
# *******************************/
# $output = '
# <table border="0" cellspacing="1" cellpadding="5">
#	<tr>
#		<th>&nbsp;</th>';
# 
# foreach ($statTypeArrayNice as $statKey => $statName)
# {
#	$output .= '
#	<th style="padding: 0px;">
#		<a class="blockLink" href="index.php?mode=statStats&amp;stat=' . $statKey . '">' . $statTypeArrayShort[$statKey] . '</a>
#	</th>';
# }
# 
# $output .= '
# </tr>';
# 
# 
# /*	Rows
# *******************************/
# foreach ($dataGrid as $teamId => $teamStats)
# {
#	$output .= '
#	<tr>
#		<td style="padding: 0px;">
#			<a href="index.php?mode=teamStats&amp;team=' . $teamId . '" class="blockLink">' . $teamArray[$teamId] . '</a>
#		</td>';
#	
#	
#	foreach ($teamStats as $statKey => $statValue)
#	{
#		$colour = 'CCC';
#		if ($statValue == $minStat[$statKey] && $statValue != 0)		$colour = 'F33';
#		elseif ($statValue < $averageStat[$statKey])					$colour = 'F77';
#		
#		elseif ($statValue == $maxStat[$statKey] && $statValue != 1)	$colour = '0F0';
#		elseif ($statValue > $averageStat[$statKey])					$colour = '7F7';
#		
#		$output .= '
#		<td style="background-color: #' . $colour . '">
#			' . $statValue . '
#		</td>';
#	}
#	
#	$output .= '
#	</tr>';
# }
# 
# 
# 
# 
# /*	Max
# *******************************/
# $output .= '
# <tr>
#	<td>Maximum</td>';
# 
# foreach ($statTypeArrayNice as $statKey => $statName)
# {
#	$output .= '
#	<td style="background-color: #CCC;">
#		' . $maxStat[$statKey] . '
#	</td>';
# }
# 
# $output .= '
# </tr>';
# 
# /*	Average
# *******************************/
# $output .= '
# <tr>
#	<td>Averages</td>';
# 
# foreach ($statTypeArrayNice as $statKey => $statName)
# {
#	$output .= '
#	<td style="background-color: #CCC;">
#		' . $averageStat[$statKey] . '
#	</td>';
# }
# 
# $output .= '
# </tr>';
# 
# /*	Min
# *******************************/
# $output .= '
# <tr>
#	<td>Minimum</td>';
# 
# foreach ($statTypeArrayNice as $statKey => $statName)
# {
#	$output .= '
#	<td style="background-color: #CCC;">
#		' . $minStat[$statKey] . '
#	</td>';
# }
# 
# $output .= '
# </tr>';
# 
# 
# 
# $output .= '
# </table>';
# 
# 
print "".join(output)