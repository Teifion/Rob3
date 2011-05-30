from pages import common
from data_classes import monster

from queries import monster_q, army_q
from rules import unit_rules

page_data = {
	"Title":	"Edit unit",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	monster_id = int(common.get_val('monster', 0))
	army_id = int(common.get_val('army', 0))
	
	if monster_id < 1:
		return "No monster selected"
	
	if army_id < 1:
		return "No army selected"
	
	the_monster	= monster_q.get_one_monster(cursor, monster_id)
	the_army = army_q.get_one_army(cursor, army_id)
	the_army.get_monsters(cursor)
	
	page_data['Title'] = "Edit army monster: %s: %s" % (the_army.name, the_monster.name)
	
	output = ["<div style='padding: 5px;'>"]
	
	# Main unit stuff
	output.append("""
	<form action="exec.py" id="the_unit_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="edit_army_monster_commit" />
		<input type="hidden" name="monster" value="{monster_id}" />
		<input type="hidden" name="army" value="{army_id}" />
	
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><strong>Monster:</strong></td>
				<td>{m_name}</td>
				
				<td>&nbsp;</td>
			
				<td><strong>Army:</strong></td>
				<td>{a_name}</td>
			</tr>
			<tr>
				<td><label for="amount">Amount:</label></td>
				<td><input type="text" name="amount" id="amount" value="{amount}" /></td>
				
				<td>&nbsp;</td>
			
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td colspan="5"><input type="submit" value="Apply" /></td>
			</tr>
		</table>
	</form>
	<br />

	""".format(
		monster_id	= monster_id,
		army_id		= army_id,
		m_name		= the_monster.name,
		a_name		= the_army.name,
		amount		= the_army.monsters.get(monster_id, 0),
	))
	
	output.append("</div>")
	
	return "".join(output)