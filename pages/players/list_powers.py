from pages import common
# from data import team, team_q
# from data import power, power_q
# from data import player, player_q

from queries import power_q, player_q
from classes import power, player

page_data = {
	"Title":	"Power list",
	"Admin":	True,
}

def main(cursor):
	player_id	= int(common.get_val('player', 0))
	ajax		= bool(common.get_val('ajax', False))
	
	if player_id < 1:
		power_dict = power_q.get_all_powers(cursor)
	else:
		power_dict = power_q.get_powers_from_player(cursor, player_id)
	
	player_dict	= player_q.get_all_players(cursor)
	
	player_dict[0] = player.Player()
	player_dict[0].name = "None"
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Power name</th>
			<th>Player</th>
			<th>Type</th>
			<th>Description</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	if len(power_dict) > 0:
		for power_id, the_power in power_dict.items():
			count += 1
			
			output.append("""
			<tr class="row%(row)d" id="%(power_id)d">
				<td>%(name)s</td>
				<td>%(player_name)s</td>
				<td>%(type)s</td>
				<td>%(description)s</td>
				
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_power&amp;power=%(power_id)d">Edit</a></td>
			</tr>
			""" % {	'row': (count % 2),
				
					'power_id':		the_power.id,
					'name':			the_power.name,
					"type":			power.power_types[the_power.type],
					'player_name':	player_dict[the_power.player].name,
					'description':	the_power.description,
				})
	
	# Add new power
	names = {}
	for p, the_p in player_dict.items():
		names[p] = the_p.name
	
	# players_order.insert(0, 2)
	# names[2] = "Teifion"
	
	# ajax = bool(common.get_val('ajax', False))
	if not ajax:
		onload = common.onload("$('#new_name').focus();")
	else:
		onload = ""
	
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_power_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_power" />
		<td style="padding: 1px;"><input type="text" name="name" id="new_name" value="" size="12"/></td>
		<td style="padding: 1px;">%(player_menu)s</td>
		<td style="padding: 1px;">%(type)s</td>
		<td style="padding: 1px;"><input type="text" name="power_description" value="" style="width: 98%%;" /></td>
	
		<td style="padding: 1px;"><input type="submit" value="Continue &rarr;" /></td>
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),
			'player_menu':	common.option_box(
				name='player',
				elements=names,
				element_order=player_dict.keys(),
				custom_id="",
			),
			"type":	common.option_box(
				"type",
				power.power_types,
			),
			"onload":	onload,
			})
	
	output.append("</table>")
	return "".join(output)