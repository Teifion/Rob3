from pages import common
from classes import unit, world
# from data import unit, unit_q
# from data import team, team_f, team_q
# from data import equipment, equipment_f
# from rules import unit_rules
# 
# from data import squad_q, army

from queries import unit_q, army_q, squad_q, equipment_q
from functions import team_f, equipment_f
from rules import unit_rules

page_data = {
	"Title":	"Edit unit",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	unit_id = int(common.get_val('unit', 0))
	
	if unit_id < 1:
		return "No unit selected"
	
	the_unit	= unit_q.get_one_unit(cursor, unit_id)
	army_dict	= army_q.get_all_armies(cursor)#get_armies_from_team(cursor, the_unit.team, include_garrisons=True)
	squad_dict	= squad_q.get_squads_from_team_of_type(cursor, the_unit.team, unit_id)
	equipment_dict = equipment_q.get_all_equipment(cursor)
	
	page_data['Title'] = "Edit unit: %s" % the_unit.name
	
	output = ["<div style='padding: 5px;'>"]
	
	# Unit cost breakdown
	unit_cost_breakdown = unit_rules.print_unit_cost(the_unit, cursor=cursor, breakdown_mode=True)
	
	w = world.World(cursor)
	real_cost = "Post override: %s/%s" % (
		unit_rules.unit_cost_override(w, the_unit, the_unit.costs['material_cost'], w.teams()[the_unit.team]),
		unit_rules.unit_cost_override(w, the_unit, the_unit.costs['iron_cost'], w.teams()[the_unit.team]),
	)
	real_upkeep = "Post override: %s/%s" % (
		unit_rules.unit_upkeep_override(w, the_unit, the_unit.costs['material_cost'], w.teams()[the_unit.team]),
		unit_rules.unit_upkeep_override(w, the_unit, the_unit.costs['iron_cost'], w.teams()[the_unit.team]),
	)
	# real_cost = 0
	# real_upkeep = 0
	
	output.append("""
	<div style="float: right; width: 50%;">
		<strong>Unit cost breakdown</strong><br />
		{cost_breakdown}<br />
		{real_cost}
		<br /><br />
	
		<strong>Unit upkeep breakdown</strong><br />
		{upkeep_breakdown}<br />
		{real_upkeep}
		<br /><br />
		
		<strong>Unit categories</strong><br />
		Type category: {type_cat}<br />
		Weapon category: {weapon_cat}<br />
		
		
		<br />
		<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="unit" id="unit" value="{unit_id}" />
			<input type="hidden" name="mode" id="mode" value="remove_unit" />
			<input style="float:right; margin-right:100px;" type="button" value="Delete unit" onclick="var answer = confirm('Delete {name}?')
			if (answer) $('#delete_form').submit();" />
		</form>
	</div>
	""".format(
		cost_breakdown		= "<br />".join(unit_cost_breakdown['cost']),
		upkeep_breakdown	= "<br />".join(unit_cost_breakdown['upkeep']),
		real_cost			= real_cost,
		real_upkeep			= real_upkeep,
		
		unit_id				= unit_id,
		name				= the_unit.name,
		
		type_cat			= unit.categories[the_unit.type_cat],
		weapon_cat			= unit.weapon_categories[the_unit.weapon_cat],
	))
	
	# Main unit stuff
	output.append("""
	<form action="exec.py" id="the_unit_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="edit_unit_commit" />
		<input type="hidden" name="id" value="%(unit_id)s" />
	
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="name">Unit:</label></td>
				<td>%(name_text)s</td>
			
				<td>&nbsp;</td>
			
				<td><label for="team">Team:</label></td>
				<td>
					<select name="team" id="team">
						<option value="0">No team</option>
						%(team_option_box)s
					</select>
				</td>
			</tr>
			<tr>
				<td colspan="5" style="padding: 0px;"><a class="block_link" href="#" onclick="$('#the_unit_form').submit();">Apply changes</a></td>
			</tr>
		</table>
	</form>
	<br />

	""" % {
		"unit_id":			unit_id,
		"name_text":	common.text_box("name", the_unit.name),
		"team_option_box":	team_f.structured_list(cursor, default=the_unit.team),
	})
	
	# Unit equipment
	output.append("""
	<span class="stitle" id="equipment">Equipment</span>
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Item</th>
			<th>&nbsp;</th>
		</tr>""")

	the_unit.get_equipment(cursor)

	counter = -1
	for e in the_unit.equipment:
		counter += 1
		output.append("""
		<tr class="row%(row)s">
			<td>%(item_name)s</td>
			<td style="padding: 0px;">
				<form action="exec.py" id="form_%(item_id)s" method="post" accept-charset="utf-8">
					<input type="hidden" name="mode" value="remove_equipment" />
					<input type="hidden" name="unit" value="%(unit_id)s" />
					<input type="hidden" name="item" value="%(item_id)s" />
					<a href="#" class="block_link" onclick="$('#form_%(item_id)s').submit();">Remove</a>
				</form>
			</td>
		</tr>""" % {
			"row":			counter%2,
			"item_name":	equipment_dict[e].name,
			"unit_id":		unit_id,
			"item_id":		e,
		})

	counter += 1
	output.append("""
	<tr class="row%(row)s">
		<form action="exec.py" id="new_equipment_form" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="add_equipment" />
			<input type="hidden" name="unit" value="%(unit_id)s" />
			<td>
				<select name="item">
					%(equipment_list)s
				</select>
			</td>
			<td>
				<input type="submit" value="Apply" />
			</td>
		</form>
	</tr>
	""" % {
		"row":				counter%2,
		"unit_id":			unit_id,
		"equipment_list":	equipment_f.equipment_option_list(cursor, remove_list=the_unit.equipment),
	})

	output.append("</table>")
	
	# What squads does the unit appear in?
	output.append("""
	<br /><br />
	<span class="stitle" id="squads">Squads</span>
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Army</th>
			<th>Squad</th>
			<th>Size</th>
			<th>&nbsp;</th>
			<th>&nbsp;</th>
		</tr>""")

	the_unit.get_equipment(cursor)
	
	counter = -1
	for s, the_squad in squad_dict.items():
		counter += 1
		output.append("""
		<tr class="row%(row)s">
			<td>%(army_name)s</td>
			<td>%(name)s</td>
			<td>%(squad_size)s</td>
			<td style="padding: 0px;">
				<a href="web.py?mode=edit_army&amp;army=%(army_id)s" class="block_link">Edit army</a>
			</td>
			<td style="padding: 0px;">
				<a href="web.py?mode=edit_squad&amp;squad=%(squad_id)s" class="block_link">Edit squad</a>
			</td>
		</tr>""" % {
			"row":			counter%2,
			"army_name":	army_dict[the_squad.army].name,
			"army_id":		the_squad.army,
			"squad_id":		s,
			"name":			the_squad.name,
			"squad_size":	the_squad.amount,
		})
	
	output.append("</table>")
	output.append("</div>")
	
	return "".join(output)