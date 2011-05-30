from pages import common
from data import team
from data import player, player_q, player_f

player_dict = player.get_player_dict()

achievement_list, achevement_dict = player_q.get_achievements()

last_turn_count = 0
last_three_turns_count = 0

output = []

output.append("""
<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
	<tr class="row2">
		<th>Killer</th>
		<th>Victim</th>
		<th>Turn</th>
		<th>&nbsp;</th>
	</tr>""")

count = -1
last_turn = -1
if len(achievement_list) > 0:
	for a in achievement_list:
		count += 1
		
		if last_turn == -1: last_turn = a['turn']
		
		if last_turn != a['turn']:
			output.append("""
			<tr class="row%d">
				<td colspan="4">&nbsp;</td>
			</tr>
			""" % (count%2))
			count += 1
			last_turn = a['turn']
			
		
		output.append("""
		<tr class="row%(row)d">
			<td>%(killer_name)s</td>
			<td>%(victim_name)s</td>
			<td>%(turn)s</td>
			
			<td style="padding: 0px;"><a class="block_link" href="exec.py?mode=remove_kill&amp;killer=%(killer_id)d&amp;victim=%(victim_id)d">Delete</a></td>
		</tr>
		""" % {	'row': (count % 2),
				
				'killer_id':	a['killer'],
				'victim_id':	a['victim'],
				'killer_name':	player_dict[a['killer']],
				'victim_name':	player_dict[a['victim']],
				'turn':			a['turn'],
			})

# And the form to add a new achievement
recent_list, recent_dict = player_q.get_active_players()

names = {}
for p in recent_list:
	names[p] = player_dict[p]

count += 1
output.append("""
<tr class="row%(row)d">
	<form action="exec.py" id="add_achievement_form" method="post" accept-charset="utf-8">
	<input type="hidden" name="mode" value="add_kill" />
	<td style="padding: 1px;">%(killer_select)s</td>
	<td style="padding: 1px;">%(victim_select)s</td>
	<td style="padding: 1px;"><input type="text" name="turn" value="%(turn)s" /></td>
	
	<td style="padding: 0px;"><a class="block_link" href="#" onclick="$('#add_achievement_form').submit();">Add</a></td>
	</form>
</tr>
""" % {	'row': (count % 2),
		"killer_select":	common.option_box(
			name='killer',
			elements=names,
			element_order=recent_list,
			custom_id="",
		),
		"victim_select":	common.option_box(
			name='victim',
			elements=names,
			element_order=recent_list,
			custom_id="",
		),
		'turn':				common.current_turn(),
	})


output.append("</table>")

print("".join(output))