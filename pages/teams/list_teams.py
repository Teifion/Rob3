from pages import common
from queries import team_q

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	all_teams = common.get_val('all_teams', False)
	
	# Get the turn we'll want to get stuff for
	current_turn = common.current_turn()
	
	# Get our list
	if not all_teams:
		team_dict = team_q.get_real_teams(cursor)
	else:
		team_dict = team_q.get_all_teams(cursor)
	
	if len(team_dict) < 1:
		raise Exception("No teams found")
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="0" style="width: 100%;">
		<tr class="row2">
			<th style="padding: 5px;">Team name</th>
			<th colspan="6">Forum</th>
			<th>&nbsp;</th>
			<th colspan="10">Rob</th>
			<th>&nbsp;</th>
			<th colspan="5">Internal</th>
			<th>&nbsp;</th>
			<th colspan="1">&nbsp;</th>
		</tr>""")

	count = -1

	last_active	= 1
	last_ir		= 0
	last_queue	= 0

	# for team_id, team in team_dict.items():
	# print(team_dict)
	for team_id, the_team in team_dict.items():
		count += 1
		
		if last_active != the_team.active or last_ir != the_team.ir or last_queue != the_team.not_in_queue:
			output.append("""
		<tr>
			<td colspan="24">&nbsp;</td>
		</tr>""")

		last_active	= the_team.active
		last_ir		= the_team.ir
		last_queue	= the_team.not_in_queue
		
		name_image = '<img src="http://localhost/woa/images/teams/%s.png" alt="%s"/>' % (the_team.name.replace(' ', '_').replace("'", '').lower(), the_team.name)
		
		output.append("""
		<tr class="row%(row)d" id="%(team_id)d">
		<td><strong class="block_cell">%(name)s</strong></td>
		<td><a class="block_link" href="%(board_url)sviewforum.php?f=%(team_forum)d">F</a></td>
		<td><a class="block_link" href="%(board_url)sviewtopic.php?t=%(team_orders)d">O</a></td>
		<td><a class="block_link" href="%(board_url)sviewtopic.php?t=%(team_intorders)d">IO</a></td>
		<td><a class="block_link" href="%(board_url)sviewtopic.php?t=%(team_results)d">R</a></td>
		<td><a class="block_link" href="%(board_url)sviewtopic.php?t=%(team_teaminfo)d">TI</a></td>
		<td><a class="block_link" href="%(board_url)sviewtopic.php?t=%(team_culture)d">C</a></td>
		<td width="10">&nbsp;</td>
		
		<td><a class="block_link" href="web.py?mode=list_cities&amp;team=%(team_id)d">Cit</a></td>
		<td><a class="block_link" href="web.py?mode=list_spells&amp;team=%(team_id)d">Mag</a></td>
		<td><a class="block_link" href="web.py?mode=list_techs&amp;team=%(team_id)d">Tech</a></td>
		<td><a class="block_link" href="web.py?mode=list_units&amp;team=%(team_id)d">Mil</a></td>
		<td><a class="block_link" href="web.py?mode=list_armies&amp;team=%(team_id)d">Arm</a></td>
		<td><a class="block_link" href="web.py?mode=list_operatives&amp;team=%(team_id)d">Op</a></td>
		<td><a class="block_link" href="web.py?mode=results&amp;team=%(team_id)d">Res</a></td>
		<td><a class="block_link" href="web.py?mode=list_artefacts&amp;team=%(team_id)d">Art</a></td>
		<td><a class="block_link" href="web.py?mode=team_stats&amp;team=%(team_id)d">Stat</a></td>
		<td><a class="block_link" href="web.py?mode=list_players&amp;team=%(team_id)d">Plyr</a></td>
			
			<td width="10">&nbsp;</td>
			
			<td><a class="block_link" href="web.py?mode=view_borders&amp;team=%(team_id)d">Bord</a></td>
			<td><a class="block_link" href="web.py?mode=view_orders&amp;turn=%(current_turn)d&amp;team=%(team_id)d&amp;topic_id=%(team_orders)d">Ord</a></td>
			<td><a class="block_link" href="web.py?mode=view_intorders&amp;team=%(team_id)d&amp;turn=%(current_turn)d&amp;topic_id=%(team_intorders)d">Int</a></td>
			<td><a class="block_link" href="web.py?mode=ti&amp;team=%(team_id)d">TI</a></td>
			<td><a class="block_link" href="web.py?mode=spyrep&amp;team=%(team_id)d">Spy Rep</a></td>

			<td width="10">&nbsp;</td>

			<td><a class="block_link" href="web.py?mode=edit_team&amp;team=%(team_id)d">Edit team</a></td>
		</tr>
		""" % {	'current_turn': current_turn,
				'row': (count % 2),
				'board_url': common.data['board_url'],

				'team_id': the_team.id,
				'name': the_team.name,
				"name_image": name_image,
				'team_forum': the_team.forum_url_id,
				'team_orders': the_team.orders_topic,
				'team_intorders': the_team.intorders_topic,
				'team_results': the_team.results_topic,
				'team_teaminfo': the_team.teaminfo_topic,
				'team_culture': the_team.culture_topic,
		})

	output.append("</table><br /><br />")

	output.append("""&nbsp;&nbsp;&nbsp;
	<a href="get_teams">Check for more teams</a>
	<br />
	""")
	
	return "".join(output)

