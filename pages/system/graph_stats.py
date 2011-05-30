import urllib2
from pages import common
from data import stat
from data import team, team_q
from data import graph_stats_f

# Get team Id
team_id		= int(common.get_val('team', 0))

if team_id <= 0:
	print """<div style="padding: 5px;">
	<form style="padding: 5px;" action="web.py" method="get" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="team_stats" />
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="team">Team:</label></td>
				<td>%(team_option_box)s</td>
				<td width="10">&nbsp;</td>
				<td><input type="submit" value="Get Stats" /></td>
			</tr>
		</table>
	</form>""" % {
		"team_option_box":		team_f.structured_list(default=team_id),
		"last_id":				team_q.get_latest_active_team_id(skip_irs = True),
		}

if team_id > 0:
	the_team = team.Team(team_q.get_one_team(team_id))
	md5_name = the_team.get_hash()
	
	output = graph_stats_f.make_graphs(the_team)
	headers = common.headers("%s stats" % the_team.name, css="", javascript="", local_path=True)
	footers = common.footers(with_analytics=False)
	
	# print headers
	print output
	# print footers

# print "</div>"