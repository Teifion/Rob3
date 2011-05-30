from pages import common
from queries import power_q, player_q, battle_q
from classes import power, player, battle

page_data = {
	"Title":	"Power list",
	"Admin":	True,
}

def main(cursor):
	player_id	= int(common.get_val('player', 0))
	killer		= int(common.get_val('killer', 0))
	victim		= int(common.get_val('victim', 0))
	battle_id	= int(common.get_val('battle', 0))
	ajax		= bool(common.get_val('ajax', False))
	
	battle_dict = battle_q.get_all_battles(cursor)
	player_dict = player_q.get_all_players(cursor)
	active_dict = player_q.get_active_players(cursor)
	
	battle_dict[0] = battle.Battle({"name":"None"})
	
	if killer > 0:
		kill_list = player_q.get_kills(cursor, killer=killer)
	elif victim > 0:
		kill_list = player_q.get_kills(cursor, victim=victim)
	elif battle_id > 0:
		kill_list = player_q.get_kills(cursor, battle=battle_id)
	else:
		kill_list = player_q.get_kills(cursor)
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Killer</th>
			<th>Victim</th>
			<th>Battle</th>
			<th>Turn</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	for kill in kill_list:
		count += 1
		
		output.append("""
		<tr class="row%(row)d">
			<td><a href="web.py?mode=edit_player&amp;player=%(k_id)s">%(killer)s</a></td>
			<td><a href="web.py?mode=edit_player&amp;player=%(v_id)s">%(victim)s</a></td>
			<td>%(battle)s <em>(%(c_id)s)</em></td>
			<td>%(turn)s</td>
			
			<td style="padding: 0px;"><a class="block_link" href="exec.py?mode=remove_kill&amp;victim=%(v_id)s&amp;killer=%(k_id)s&amp;turn=%(turn)s&amp;battle=%(c_id)s%(p_id)s">Remove</a></td>
		</tr>
		""" % {	'row': (count % 2),
				
				'v_id':			kill['victim'],
				'k_id':			kill['killer'],
				'c_id':			kill['battle'],
				'p_id':			("&amp;player=%d" % player_id if player_id > 0 else ""),
				
				'killer':		player_dict[kill['killer']].name,
				'victim':		player_dict[kill['victim']].name,
				"battle":		battle_dict[kill['battle']].name,
				
				'turn':			kill['turn'],
			})
	
	# Add new power
	names = {}
	for p, the_p in active_dict.items():
		names[p] = the_p.name
	
	if not ajax:
		onload = common.onload("$('#killer').focus();")
	else:
		onload = ""
	
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_kill_form" method="post" accept-charset="utf-8">
		<td style="padding: 1px;">%(killer)s</td>
		<td style="padding: 1px;">%(victim)s</td>
		<td style="padding: 0px;">%(battle)s</td>
		<td style="padding: 0px;">%(turn)s</td>
		
		<td style="padding: 1px;">
			<input type="hidden" name="mode" value="add_kill" />
			%(player_id)s
			<input type="submit" value="Add" />
		</td>
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),
			'killer':	common.option_box(
				name='killer',
				elements=names,
				element_order=active_dict.keys(),
				selected = killer if killer > 0 else "",
			),
			'victim':	common.option_box(
				name='victim',
				elements=names,
				element_order=active_dict.keys(),
				selected = victim if victim > 0 else "",
			),
			"turn":		'<input type="text" name="turn" id="turn" value="%d" />' % common.current_turn(),
			"battle":	'<input type="text" name="battle" id="battle" value="%d" />' % battle_id,
			"onload":	onload,
			"player_id": ('<input type="hidden" name="player" value="%d" />' % player_id if player_id > 0 else ""),
			})
	
	output.append("</table>")
	return "".join(output)