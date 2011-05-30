from pages import common
# from data import power, power_q
# from data import player, player_q

from queries import power_q, player_q
from classes import power

page_data = {
	"Title":	"Edit power",
	"Admin":	True,
}

def main(cursor):
	power_id	= int(common.get_val('power', 0))
	
	if power_id < 1:
		return "No power selected"
	
	the_power = power_q.get_one_power(cursor, power_id)
	
	output = ["<div style='padding: 5px;'>"]
	
	# Used for the player select menu
	player_dict = player_q.get_all_players(cursor)
	recent_dict = player_q.get_active_players(cursor)
	
	names = {}
	for p in recent_dict.keys():
		names[p] = player_dict[p].name
	
	if the_power.player not in names:
		# recent_dict[the_power.id] = the_power.player
		names[the_power.player] = player_dict[the_power.player].name
	
	
	output.append("""
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_power_commit" />
		<input type="hidden" name="id" id="id" value="%(power_id)s" />
	
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="name">Name:</label></td>
				<td>%(name_text)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="player">Player:</label></td>
				<td>%(player_select)s</td>
			</tr>
			<tr>
				<td><label for="type">Type:</label></td>
				<td>%(type)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td colspan="5"><label for="description">Description:</label><br />
				<textarea name="description" rows="4" cols="60">%(description)s</textarea></td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<br /><br />""" % {
		"power_id":			power_id,
		"name":		the_power.name,
		"description":		the_power.description,
		"name_text":	common.text_box("name", the_power.name, size=20),
		"player_select":	common.option_box(
			name='player',
			elements=names,
			element_order=recent_dict.keys(),
			selected=the_power.player,
			custom_id="",
		),
		"type":	common.option_box(
			name='type',
			elements=power.power_types,
			selected=power.power_types[the_power.type],
		),
	})


	# End of padding
	output.append("</div>")

	return "".join(output)