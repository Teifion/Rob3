from pages import common
from queries import player_q, team_q
from functions import player_f
from classes import player

page_data = {
	"Title":	"Player list",
	"Admin":	True,
}

def main(cursor):
	team_id = int(common.get_val('team', 0))
	
	if team_id < 1:
		player_dict = player_q.get_all_players(cursor)
	else:
		player_dict = player_q.get_players_from_team(cursor, team_id)
	
	team_dict = team_q.get_all_teams(cursor)
	
	last_turn_count = 0
	last_three_turns_count = 0
	
	output = [""]# That's later swapped out for something else
	output.append('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="web.py?mode=get_players">Get new players</a>')
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Player name</th>
			<th>Team</th>
			<th>Last posted</th>
			<th>Daemonic</th>
			<th colspan="2">&nbsp;</th>
		</tr>""")
	
	current_turn = common.current_turn()
	count = -1
	if len(player_dict) > 0:
		for player_id, the_player in player_dict.items():
			if the_player.last_posted >= current_turn:
				last_turn_count += 1
			if the_player.last_posted >= current_turn-3:
				last_three_turns_count += 1
			
			count += 1
			
			if the_player.team in team_dict:
				team_name = team_dict[the_player.team].name
			else:
				team_name = "None"
			
			output.append("""
			<tr class="row%(row)d" id="%(player_id)d">
				<td>%(name)s</td>
				<td>%(team)s</td>
				<td>%(daemon)s</td>
				<td>%(last_posted)s</td>
				<td style="padding:0px;"><a href="http://woarl.com/board/ucp.php?i=pm&mode=compose&u=%(player_id)s" class="block_link">PM</a></td>
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_player&amp;player=%(player_id)d">Edit</a></td>
			</tr>
			""" % { 'row': (count % 2),
				
					'player_id':		the_player.id,
					'name':		the_player.name,
					'team':				team_name,
					'last_posted':		the_player.last_posted,
					"daemon":			"%s, %s" % (player.progressions[the_player.progression], player.daemon_types[the_player.daemon_type]),
				})

	output.append("</table>")
	
	output[0] = "Last turn: %s, Last 3 turns: %s" % (last_turn_count, last_three_turns_count)

	return "".join(output)