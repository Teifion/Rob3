from pages import common

from classes import player
from queries import player_q
from functions import team_f

page_data = {
	"Title":	"Edit player",
	"Admin":	True,
}

def main(cursor):
	player_id	= int(common.get_val('player', 0))
	
	if player_id < 1:
		return "No player selected"
	
	the_player = player_q.get_one_player(cursor, player_id)
	
	output = ["<div style='padding: 5px;'>"]
	
	output.append("""
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_player_commit" />
		<input type="hidden" name="id" id="id" value="%(player_id)s" />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="name">Name:</label></td>
				<td>%(name_text)s</td>
				
				<td colspan="3">&nbsp;</td>
			</tr>
			<tr>
				<td><label for="team">Team:</label></td>
				<td>%(team)s</td>
				
				<td>&nbsp;</td>
				
				<td><label for="ir">IR:</label></td>
				<td>%(ir)s</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				
				<td colspan="3">&nbsp;</td>
			</tr>	
			<tr>
				<td><label for="last_posted">Last posted:</label></td>
				<td>%(last_posted_text)s</td>
				
				<td colspan="3">&nbsp;</td>
			</tr>
			<tr>
				<td><label for="daemon_type">Daemon type:</label></td>
				<td>%(daemon_type)s</td>
				
				<td colspan="3">&nbsp;</td>
			</tr>
			<tr>
				<td><label for="progression">Progression:</label></td>
				<td>%(progression)s</td>
				
				<td colspan="3">&nbsp;</td>
			</tr>
			<tr>
				<td><label for="not_a_player">Not a player:</label></td>
				<td>%(not_a_player)s</td>
				
				<td>&nbsp;</td>
				
				<td><label for="not_surplus">Not surplus:</label></td>
				<td>%(not_surplus)s</td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<br /><br />""" % {
		"player_id":		player_id,
		"name":				the_player.name,
		"team":				team_f.structured_list(cursor, default=the_player.team, field_name="team"),
		"name_text":	common.text_box("name", the_player.name, size=20),
		"last_posted_text":	common.text_box("last_posted", the_player.last_posted),
		"not_a_player":		common.check_box("not_a_player", the_player.not_a_player),
	
		"daemon_type":		common.option_box("daemon_type", elements=player.daemon_types, selected=player.daemon_types[the_player.daemon_type]),
		"progression":		common.option_box("progression", elements=player.progressions, selected=player.progressions[the_player.progression]),
		
		"not_surplus":		common.check_box("not_surplus", the_player.not_surplus),
		"ir":				common.check_box("ir", the_player.ir),
		
		# option_box(name, elements = {}, element_order = [], tab_index = -1, onchange="", custom_id = "<>", selected=""):
	})
	
	# This get's ajax'd
	output.append("""
	<div style="clear: left;">
		<br /><br />
		<span class="stitle">Player powers</span>
		<div id="player_powers">
			
		</div>
		<br /><br />
		<span class="stitle">Player kills/deaths</span><br />
		<div id="player_kills" style="float:left; width:49%; border: 0px solid #000;">
			&nbsp;
		</div>
		<div id="player_deaths" style="float:right; width:49%; border: 0px solid #000;">
			&nbsp;
		</div>
		<br /><br />
	</div>""")
	
	# End of padding
	output.append("</div>")
	
	# Load in the player powers
	output.append(common.onload("""
		$('#player_powers').load('web.py', {'mode':'list_powers','player':'%d', 'ajax':'True'});
		$('#player_kills').load('web.py', {'mode':'player_kills','killer':'%d', 'player':'%d', 'ajax':'True'});
		$('#player_deaths').load('web.py', {'mode':'player_kills','victim':'%d', 'player':'%d', 'ajax':'True'});
	""" % (player_id, player_id, player_id, player_id, player_id)))
	
	return "".join(output)