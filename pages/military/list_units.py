from pages import common
from classes import unit
from rules import unit_rules
from queries import team_q, unit_q, army_q, equipment_q

page_data = {
	"Title":	"Unit list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	
	# Build team
	the_team = team_q.get_one_team(cursor, team_id)
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'list_units')
	
	unit_dict = unit_q.get_units_from_team(cursor, team=team_id)
	equipment_dict = equipment_q.get_all_equipment(cursor)
	the_team.get_units(cursor)
	
	output = []
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Icon</th>
			<th>Amount</th>
			<th>Name</th>
			<th>Cost</th>
			<th colspan='4'>Categories</th>
			<th>Equipment</th>
			<th style="width:70px;">Edit</th>
			<!--
			<th colspan="2">Add</th>
			-->
		</tr>""")

	names = {}
	count = -1
	if len(unit_dict) > 0:
		# for team_id, team in team_dict.items():
		for unit_id, the_unit in unit_dict.items():
			if unit_id not in the_team.units: the_team.units[unit_id] = 0
			
			names[unit_id] = the_unit.name
			count += 1
			
			output.append("""
			<tr class="row%(row)d" id="%(unit_id)d">
				<td>%(icon)s</td>
				<td>%(count)s</td>
				<td>%(name)s</td>
			
				<td>%(cost)s</td>
				<td>%(weapon_cat)s</td>
				<td>%(armour_cat)s</td>
				<td>%(move_cat)s</td>
				<td>%(training_cat)s</td>
				<td>%(equipment)s</td>
			
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_unit&amp;unit=%(unit_id)d">Edit unit</a></td>
				<!--
				<td style="padding: 1px;">
					<form action="exec.py" method="post" accept-charset="utf-8">
						<input type="text" name="amount" value="" size="8"/>
						<input type="hidden" name="mode" value="alter_unit_count" />
						<input type="hidden" name="team" value="%(team_id)s" />
						<input type="hidden" name="unit" value="%(unit_id)s" />
					</form>
				</td>
				<td style="padding: 0px;">
					<a class="block_link" href="#" onclick="$('#form_add_%(unit_id)s').submit();">Add unit</a>
				</td>
				-->
			</tr>
			""" % {	'row': (count % 2),
				
					"team_id":		team_id,
					'unit_id':		unit_id,
					'name':	common.doubleclick_text("units", "name", unit_id, the_unit.name, "font-weight:bold"),
					'icon':			"",
					'count':		common.number_format(the_team.units[unit_id]),
					
					'weapon_cat':	unit.weapon_categories[the_unit.weapon_cat],
					'armour_cat':	unit.armour_categories[the_unit.armour_cat],
					'move_cat':	unit.move_categories[the_unit.move_cat],
					'training_cat':	unit.training_categories[the_unit.training_cat],
				
					"cost":			unit_rules.print_unit_cost(the_unit, cursor=cursor, equipment_dict=equipment_dict),
					"equipment":	the_unit.equipment_string,
				
					})
	
	# Add unit type
	# armies_dict = army_q.get_armies_from_team(cursor, team=team_id, include_garrisons=1)
	count += 1
	
	# armies_names = {}
	# has_non_garrison = False
	# for k, v in armies_dict.items():
	# 	armies_names[k] = v.name
	# 	if v.garrison < 0: has_non_garrison = True
	# 
	# armies_order.reverse()
	# armies_order.append("disabled")
	# armies_order.append("XYZ_all_garrisons")
	# if has_non_garrison == True:
	# 	armies_order.append("XYZ_all_non_garrisons")
	# 	armies_order.append("XYZ_all_armies")
	# armies_order.reverse()
	# 
	# if has_non_garrison == True:
	# 	armies_names["XYZ_all_armies"]			= "All armies"
	# 	armies_names["XYZ_all_non_garrisons"]	= "All non garrisons"
	# armies_names["XYZ_all_garrisons"]		= "All garrisons"


	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" method="post" id="new_unit_form" accept-charset="utf-8">
		<input type="hidden" name="mode" value="create_new_unit" />
		<input type="hidden" name="team" value="%(team_id)s" />
		<td>&nbsp;</td>
		<td style="padding: 1px;">&nbsp;</td>
		<td style="padding: 1px;"><input type="text" name="name" id="name" value="" size="13"/></td>
		<td colspan='4'>&nbsp;</td>
		<td style="padding: 1px;">&nbsp;</td>
		<td style="padding: 2px;">
			<textarea name="equipment_string" id="equipment_string" rows="1" cols="30"></textarea>
		</td>
	
		<td style="padding: 0px;"><a class="block_link" onclick="$('#new_unit_form').submit();" href="#">Add</a></td>
		%(onload)s
		</form>
	</tr>
	""" % {	'row': (count % 2),

			"team_id":		team_id,
			'onload':		common.onload("$('#name').focus();"),
			})

	# Now for solo units
	unit_dict = unit_q.get_units_from_team(cursor, team=0)
	if len(unit_dict) > 0:
		# for team_id, team in team_dict.items():
		for unit_id, the_unit in unit_dict.items():
			if unit_id not in the_team.units: the_team.units[unit_id] = 0
			
			names[unit_id] = the_unit.name
			count += 1
		
			output.append("""
			<tr class="row%(row)d" id="%(unit_id)d">
				<td>%(icon)s</td>
				<td>%(count)s</td>
				<td>%(name)s</td>
			
				<td>%(cost)s</td>
				
				<td colspan='4'>&nbsp;</td>
				
				<td>%(equipment)s</td>
			
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_unit&amp;unit=%(unit_id)d">Edit unit</a></td>
				<!--
				<td style="padding: 1px;">
					<form action="exec.py" method="post" accept-charset="utf-8">
						<input type="text" name="amount" value="" size="8"/>
						<input type="hidden" name="mode" value="alter_unit_count" />
						<input type="hidden" name="team" value="%(team_id)s" />
						<input type="hidden" name="unit" value="%(unit_id)s" />
					</form>
				</td>
				<td style="padding: 0px;">
					<a class="block_link" href="#" onclick="$('#form_add_%(unit_id)s').submit();">Add unit</a>
				</td>
				-->
			</tr>
			""" % {	'row': (count % 2),
				
					"team_id":		team_id,
					'unit_id':		unit_id,
					'name':	common.doubleclick_text("units", "name", unit_id, the_unit.name, "font-weight:bold"),
					'icon':			"",
					'count':		common.number_format(the_team.units[unit_id]),
				
					"cost":			unit_rules.print_unit_cost(the_unit, cursor=cursor, equipment_dict=equipment_dict),
					"equipment":	the_unit.equipment_string,
				
					})
	
	output.append("</table>")
	page_data['Title'] = "%s unit list" % the_team.name
	return "".join(output)