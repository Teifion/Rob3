from pages import common
from queries import squad_q, army_q, unit_q

page_data = {
	"Title":	"Edit squad",
	"Admin":	True,
}

def main(cursor):
	squad_id = int(common.get_val('squad'))
	
	the_squad = squad_q.get_one_squad(cursor, squad_id)
	armies_dict = army_q.get_armies_from_team(cursor, the_squad.team, include_garrisons=True)
	the_unit = unit_q.get_one_unit(cursor, the_squad.unit)
	
	names = {}
	for a, the_army in armies_dict.items():
		names[a] = the_army.name
	
	output = []
	
	output.append("<div style='padding: 5px;'>")
	
	output.append("""
	<form action="exec.py" id="the_squad_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_squad_commit" />
		<input type="hidden" name="id" id="id" value="%(squad_id)s" />
		
		<label for="name">Editing:</label> %(name_text)s
		<br /><br />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="army">Army:</label></td>
				<td style="padding: 1px;">%(army_select)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td>Type: </td>
				<td>%(unit_type)s</td>
			</tr>
			<tr>
				<td><label for="amount">Amount:</label></td>
				<td>%(amount)s</td>
			
				<td>&nbsp;</td>
			
				<td><label for="experience">Experince:</label></td>
				<td>%(experience)s</td>
			</tr>
			<tr>
				<td colspan="5">
					<strong>%(unit_name)s</strong>: %(unit_description)s
				</td>
			</tr>
			<tr>
				<td colspan="5">
					<input type="submit" value="Apply" />
				</td>
			</tr>
		</table>
	</form>
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="squad" id="squad" value="%(squad_id)s" />
		<input type="hidden" name="mode" id="mode" value="remove_squad" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete squad" onclick="var answer = confirm('Delete %(name)s?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""" % {
		"squad_id":			squad_id,
		"name":				the_squad.name,
		"name_text":		common.text_box("name", the_squad.name),
		"unit_type":		the_unit.name,
		"army_select":		common.option_box(
			name='army',
			elements=names,
			element_order=armies_dict.keys(),
			custom_id="army",
			selected=the_squad.army,
		),
		
		"unit_name":		the_unit.name,
		"unit_description":	the_unit.equipment_string,
		
		"amount":			common.text_box("amount", the_squad.amount),
		"experience":		common.text_box("experience", the_squad.experience),
	})
	
	output.append("</div>")
	
	page_data['Title'] = "Editing squad (%s)" % the_squad.name
	return "".join(output)