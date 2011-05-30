from pages import common
from queries import battle_q, team_q
# from data import battle, battle_f, battle_q
# from data import team

page_data = {
	"Title":	"Battle list (battles)",
	"Admin":	True,
}

def main(cursor):
	turn = int(common.get_val("turn", -1))
	
	if turn < 1:
		turn = common.current_turn()
	
	battle_dict	= battle_q.get_battles_from_turn(cursor, turn)
	teams_dict	= team_q.get_all_teams(cursor)
	
	output = []
	
	output.append("""
	<div style="padding: 5px;">
	
	<form action="web.py" method="get" accept-charset="utf-8">
		<a href="list_battles" style="text-align:left;" class="block_link">This turn's battles</a>
		<br />
		<input type="hidden" name="mode" id="mode" value="list_battles" />
		Turn: <input type="text" name="turn" value="%s" />
		&nbsp;&nbsp;&nbsp; <input type="submit" value="Show" />
	</form>
	<br /><br />""" % (turn))
	
	output.append("""<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Turn</th>
			<th>Battle name</th>
			<th>Participants</th>
			<th>&nbsp;</th>
			<th>&nbsp;</th>
		</tr>
	""")
	
	count = -1
	for b, the_battle in battle_dict.items():
		participants = the_battle.get_participants(cursor)
		
		participants_list = []
		for t, s in participants.items():
			if s:
				participants_list.append("<em style='color:#555;'>%s</em>" % teams_dict[t].name)
			else:
				participants_list.append(teams_dict[t].name)
		
		count += 1
		
		output.append("""
		<tr class="row%(count)s">
			<td>%(turn)s</td>
			<td>%(name)s</td>
			<td>%(participants)s</td>
			<td style="padding:0px;"><a href="web.py?mode=edit_battle&amp;battle=%(battle_id)s" class="block_link">Edit</a></td>
			<td style="padding:0px;"><a href="view_battle&amp;battle=%(battle_id)s" class="block_link">View</a></td>
		</tr>
		""" % {
			"count":		count%2,
			"turn":			turn,
			"name":	the_battle.name,
			"participants":	", ".join(participants_list),
			"battle_id":	the_battle.id,
		})
	
	count += 1
	output.append("""
	<tr class="row%(count)s">
		<form action="exec.py" id="add_battle_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="add_battle" />
		<td style="padding: 1px;"><input type="text" name="battle_turn" value="%(turn)s" size="5"/></td>
		<td style="padding: 1px;"><input type="text" name="name" id="name" value="" /></td>
		<td>&nbsp;</td>
		<td style="padding: 0px;" colspan="2"><a class="block_link" href="#" onclick="$('#add_battle_form').submit();">Add</a></td>
		</form>
		%(onload)s
	</tr>
	""" % {
		"turn":			turn,
		"count":		count%2,
		"onload":		common.onload("$('#name').focus();"),
	})
	
	output.append("</table></div>")
	
	return "".join(output)
