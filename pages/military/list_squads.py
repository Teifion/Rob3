from pages import common
# from data import squad_q
# from data import army, army_q
# from data import unit, unit_q
from queries import army_q, squad_q, unit_q, monster_q

page_data = {
	"Title":	"Squad list",
	"Admin":	True,
}

def main(cursor):
	# Get squad Id
	army_id = int(common.get_val('army', 0))
	
	if army_id < 1:
		exit()
	
	the_army = army_q.get_one_army(cursor, army_id)
	squads_dict = squad_q.get_squads_from_army(cursor, army=army_id)
	
	monster_dict = monster_q.get_all_monsters(cursor)
	army_monsters_dict = monster_q.get_monsters_from_army(cursor, army_id)
	
	unit_dict = unit_q.get_units_from_team(cursor, the_army.team, special_units=True)
	
	output = []
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Name</th>
			<th>Unit type</th>
			<th>Size</th>
			<th>Exp</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	if len(squads_dict) > 0:
		for squad_id, the_squad in squads_dict.items():
			if the_squad.unit not in unit_dict: continue
			
			count += 1
			
			output.append("""
			<tr class="row%(row)d" id="%(squad_id)d">
				<td>%(name)s</td>
				<td>%(unit_type)s</td>
				<td>%(size)s</td>
				<td>%(exp)s</td>
				<td style="padding: 0px;"><a href="web.py?mode=edit_squad&amp;squad=%(squad_id)d" class="block_link">Edit</a></td>
			</tr>
			""" % {	'row': (count % 2),
				
					"squad_id":		squad_id,
					"name":	common.doubleclick_text("squads", "name", squad_id, the_squad.name, "font-weight:bold", size=18),
					"unit_type":	unit_dict[the_squad.unit].name,
					"size":			common.doubleclick_text("squads", "amount", squad_id, the_squad.amount, size=7),
					"exp":			common.doubleclick_text("squads", "experience", squad_id, the_squad.experience, size=7),
					})
	else:
		output.append("""
		<tr class="row0">
			<td colspan="5">No squads in this army</td>
		</tr>""")
		count += 1
	
	
	if len(army_monsters_dict) > 0:
		for monster_id, amount in army_monsters_dict.items():
			if amount < 1: continue
			the_monster = monster_dict[monster_id]
			
			count += 1
			
			output.append("""
			<tr class="row{row}">
				<td>{name}</td>
				<td><em>Monster</em></td>
				<td>{amount}</td>
				<td>&nbsp;</td>
				<td style="padding: 0px;"><a href="web.py?mode=edit_army_monster&amp;army={army_id}&amp;monster={monster_id}" class="block_link">Edit</a></td>
			</tr>
			""".format(
					row			= (count % 2),
					army_id		= army_id,
					monster_id	= monster_id,
					name		= the_monster.name,
					amount		= common.doubleclick_text_full("army_monsters", "amount", "army = %d AND monster = %d" % (army_id, monster_id), amount, size=5),
			))
	
	# Add new squad to army thingie
	names = {}
	for u, the_unit in unit_dict.items():
		names[u] = the_unit.name
	
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_squad_form_%(army_id)d" method="post" accept-charset="utf-8">	
		<td style="padding: 1px;">
			<input type="text" name="name" value=""/>
		
			<input type="hidden" name="team" value="%(team_id)s" />
			<input type="hidden" name="mode" value="add_squad" />
			<input type="hidden" name="army" value="%(army_id)s" />
		</td>
		<td style="padding: 1px;">%(unit_type)s</td>
		<td style="padding: 1px;"><input type="text" name="size" value="" size="5"/></td>
		<td style="padding: 1px;"><input type="text" name="experience" value="" size="5"/></td>
		<td style="padding: 0px;">
			<a class="block_link" href="#" onclick="$('#add_squad_form_%(army_id)d').submit();">Add</a>
		</td>
		</form>
	</tr>
	""" % {	'row': (count % 2),
		
			"army_id":			army_id,
			"team_id":			the_army.team,
			'unit_type':		common.option_box(
				name='unit_type',
				elements=names,
				element_order=unit_dict.keys(),
				custom_id="",
			),
			})
	
	output.append('</table>')
	return "".join(output)
