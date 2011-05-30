import time
from classes import team
from pages import common
from rules import unit_rules, spell_rules, tech_rules, team_rules, sad_rules

jokes = {
	"Bake me a cake":		"The cake is a lie!",
	"Tell me a joke":		"Maybe next time",
}

def nomadic_city_block(oh, the_team, the_city):
	output, load_java, run_java = [], [], []
	
	# Supply and demand
	supply_menu = []
	for i, r in enumerate(sad_rules.res_list):
		if the_city.supply_good == i:
			supply_menu.append('<option value="" selected="selected">%s (current)</option>' % (r))
		else:
			supply_menu.append('<option value="%s">%s</option>' % (r, r))
	
	# Now to actually make the output
	output.append("""
	<div class="order_box_half">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<td colspan="2" style="font-weight:bold; font-size:1.1em;">%(name)s</td>
			</tr>
			<tr>
				<td>Current location:</td>
				<td>%(x)s, %(y)s</td>
			<tr>
			</tr>
				<td>New location:</td>
				<td><input type="text" id="migration_text_%(city_id)s" value="%(x)s, %(y)s" /></td>
			</tr>
			<tr>
				<td>Supply good:</td>
				<td>
					<select id="supply_menu_%(city_id)s">
						%(supply_menu)s
					</select>
				</td>
			</tr>
		</table>
	</div>
	""" % {
		"city_id":		the_city.id,
		"name":			the_city.name,
		"x":			the_city.x,
		"y":			the_city.y,
		"supply_menu":	"".join(supply_menu),
	})
	
	# Java
	run_java.append("""
	var temp_location = $('#migration_text_%(city_id)d').val();
	if (temp_location != '' && temp_location != '%(loc)s') {migration_orders += 'Move %(city_name)s towards ' + temp_location + '\\n';}
	
	var temp_good = $('#supply_menu_%(city_id)s option:selected').val();
	if (temp_good != '') {
		supply_demand_orders += 'Change %(city_name)s supply production to ' + temp_good + '\\n';
	}""" % {
		"city_id":		the_city.id,
		"city_name":	common.js_name(the_city.name),
		"loc":			"%s, %s" % (the_city.x, the_city.y),
	})
	
	return "".join(output), "".join(load_java), "".join(run_java)


def normal_city_block(oh, the_team, the_city):
	output, load_java, run_java = [], [], []
	
	building_menu = []
	building_menu_grey = []
	wall_menu = []
	wall_menu_grey = []
	
	buildings_progress, buildings_amount = the_city.buildings, the_city.buildings_amount
	selected_building = None
	selected_wall = None
	
	building_dict			= oh.the_world.buildings()
	buildings_requirements	= oh.the_world.building_requirements()
	
	# Can't cache it because it's unique for each city
	for b, the_building in building_dict.items():
		if not the_building.public: continue
		if the_building.name == "VOID": continue
		
		# Find out if we've already built one...
		true_amount = buildings_amount.get(b, 0)
		
		if b in buildings_requirements:
			for build_id in buildings_requirements[b]:
				if build_id in buildings_amount:
					true_amount += buildings_amount[build_id]
		
		if true_amount >= the_building.limit_per_city:
			if the_building.wall:
				wall_menu_grey.append("<option disabled='disabled'>%s</option>" % (the_building.name))
			else:
				building_menu_grey.append("<option disabled='disabled'>%s</option>" % (the_building.name))
			continue
		
		# Don't offer it if we can't upgrade to it
		if the_building.upgrades > 0:
			if the_building.upgrades not in buildings_amount:
				continue
		
		if the_building.wall:
			if buildings_progress.get(b,0) > 0 and selected_wall == None:
				selected_wall = "selected='selected'"
		else:
			if buildings_progress.get(b,0) > 0 and selected_building == None:
				selected_building = "selected='selected'"
		
		if the_building.wall:
			wall_menu.append("<option value='%s' %s>%s</option>" % (the_building.name, selected_wall, the_building.name))
			if selected_wall != None: selected_wall = ""
		else:
			building_menu.append("<option value='%s' %s>%s</option>" % (the_building.name, selected_building, the_building.name))
			if selected_building != None: selected_building = ""
	
	if wall_menu_grey != []:
		wall_menu_grey.insert(0, '<option disabled="disabled"></option>')
	
	if building_menu_grey != []:
		building_menu_grey.insert(0, '<option disabled="disabled"></option>')
	
	# Supply and demand
	supply_menu = []
	for i, r in enumerate(sad_rules.res_list):
		if the_city.supply_good == i:
			supply_menu.append('<option value="" selected="selected">%s (current)</option>' % (r))
		else:
			supply_menu.append('<option value="%s">%s</option>' % (r, r))
	
	# Wunders
	if oh.caches[the_team.id].get('wonder_menu', '') != "":
		wonder_menu = """
		<tr>
			<td>Wonder:</td>
			<td>
				<select id="wonder_menu_%d">
					<option value=""></option>
					%s
				</select>
			</td>
		</tr>
		""" % (the_city.id, oh.caches[the_team.id].get('wonder_menu', ''))
	else:
		wonder_menu = ""
	
	# Output
	output.append("""
	<div class="order_box_half">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<td colspan="2" style="font-weight:bold; font-size:1.1em;">%(name)s</td>
			</tr>
			<tr>
				<td>Building:</td>
				<td>
					<select id="building_menu_%(city_id)s">
						<option value=""></option>
						%(building_menu)s
					</select>
				</td>
			<tr>
			<tr>
				<td>Wall:</td>
				<td>
					<select id="wall_menu_%(city_id)s">
						<option value=""></option>
						%(wall_menu)s
					</select>
				</td>
			</tr>
			<tr>
				<td>Supply good:</td>
				<td>
					<select id="supply_menu_%(city_id)s">
						%(supply_menu)s
					</select>
				</td>
			</tr>
			%(wonder_menu)s
		</table>
	</div>
	""" % {
		"city_id":			the_city.id,
		"name":				the_city.name,
		"building_menu":	"".join(building_menu) + "".join(building_menu_grey),
		"wall_menu":		"".join(wall_menu) + "".join(wall_menu_grey),
		"supply_menu":		"".join(supply_menu),
		"wonder_menu":		wonder_menu,
	})
	
	# Java
	run_java.append("""
	var temp_building = $('#building_menu_%(city_id)s option:selected').val();
	if (temp_building != '') {
		construction_orders += 'Build ' + temp_building + ' at %(city_name)s\\n';
		construction_materials += 5;
	}
	
	var temp_walls = $('#wall_menu_%(city_id)s option:selected').val();
	if (temp_walls != '') {
		construction_orders += 'Build ' + temp_walls + ' at %(city_name)s\\n';
		construction_materials += 5;
	}
	
	var temp_good = $('#supply_menu_%(city_id)s option:selected').val();
	if (temp_good != '') {
		supply_demand_orders += 'Change %(city_name)s supply production to ' + temp_good + '\\n';
	}
	""" % {
		"city_id":		the_city.id,
		"city_name":	common.js_name(the_city.name),
	})
	
	if wonder_menu != "":
		run_java.append("""
		var temp_wonder = $('#wonder_menu_%(city_id)s option:selected').val();
		if (temp_wonder != '') {
			construction_orders += '%(city_name)s assist wonder at ' + temp_wonder + '\\n';
			construction_materials += 0;
		}""" % {
			"city_id":		the_city.id,
			"city_name":	common.js_name(the_city.name),
		})
	
	return "".join(output), "".join(load_java), "".join(run_java)


def founding_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Founding</a></h3>
	<div id="migration_help" style="display:none;">
		<ul style="list-style-type: circle;margin-left:25px;">
			<li>The city name is the name of the new city that you wish to create.</li>
			<li>In the location box you need to put the coordinates of the new city such as -90,1569.</li>
			<li>The type is if it's nomadic, a port or neither. If you declare it as a port and it's not near the sea then it will not be able to be a port yet will still be created.</li>
			<li>Size is simply the size of the new city.</li>
			<li>You can either take the civilians for the new city from only one city or from all availiable cities.</li>
		</ul>
	</div>
	<span id="migration_help_link" style="cursor:pointer;" onclick="$('#migration_help_link').hide();$('#migration_help').show(500);">Show help</span>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>City name</th>
				<th>Location</th>
				<th>Type</th>
				<th>Size</th>
				<th>Source(s)</th>
			</tr>""")
	
	for i in range(0,4):
		output.append("""
		<tr>
			<td><input type="text" id="new_city_name_%(i)s" value="" onchange=""/></td>
			<td><input type="text" id="new_city_location_%(i)s" value="" size="10" onchange=""/></td>
			<td>
				<select id="new_city_type_%(i)s">
					<option value="">&nbsp;</option>
					<option value="Port">Port</option>
					<option value="Nomadic">Nomadic</option>
				</select>
			</td>
			<td><input type="text" id="new_city_size_%(i)s" value="" size="7"/></td>
			<td>
				<select id="new_city_source_%(i)s">
					%(city_dropdown)s
				</select>
			</td>
		</tr>
		""" % {
			"i":		i,
			
			"city_dropdown":	oh.caches[the_team.id].get('founding_dropdown', ''),
		})
		
		run_java.append("""
		var temp_name = $('#new_city_name_%(i)d').val();
		var temp_location = $('#new_city_location_%(i)s').val();
		
		var temp_type = $('#new_city_type_%(i)d :selected').val();
		
		var temp_size = parseInt($('#new_city_size_%(i)d').val());
		var temp_source = $('#new_city_source_%(i)d :selected').val();
		
		if (temp_name != '' && temp_location != '' && temp_size > 0)
		{
			founding_orders += '' + temp_name + ' (' + temp_location + ') ';
			if (temp_type != '') {founding_orders += temp_type + ' ';}
			founding_orders += temp_size + ' ' + temp_source + '\\n';
		}
		""" % {
			"i":	i,
		})
	
	output.append("""
		</table>
	</div>
	""")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def relocation_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	run_java.append("var relocation_orders = '';")
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Relocation</a></h3>
	<div id="relocation_help" style="display:none;">
		<ul style="list-style-type: circle;margin-left:25px;">
			<li>The amount is the amount of people sent from one city to another.</li>
			<li>The first city is the source of the people while the second is the target.</li>
			<li>The fourth column decides the type of people to be sent.</li>
		</ul>
	</div>
	<span id="relocation_help_link" style="cursor:pointer;" onclick="$('#relocation_help_link').hide();$('#relocation_help').show(500);">Show help</span>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Amount</th>
				<th>From</th>
				<th>To</th>
				<th>&nbsp;</th>
			</tr>""")
	
	for i in range(0,3):
		output.append("""
		<tr>
			<td><input type="text" id="relocation_amount_%(i)s" value="" onchange="" size="10"/></td>
			<td>
				<select id="from_city_%(i)s">
					%(city_dropdown)s
				</select>
			</td>
			<td>
				<select id="to_city_%(i)s">
					%(city_dropdown)s
				</select>
			</td>
			<td>
				<select id="relocate_type_%(i)s">
					<option value="civilians">Civilians</option>
					<option value="slaves">Slaves</option>
				</select>
			</td>
		</tr>
		""" % {
			"count":	i%2,
			"i":		i,
		
			"city_dropdown":	oh.caches[the_team.id].get('relocation_dropdown', ''),
		})
		
		run_java.append("""
		var temp_amount = $('#relocation_amount_%(i)d').val();
		var temp_from = $('#from_city_%(i)d :selected').val();
		var temp_to = $('#to_city_%(i)d :selected').val();
		var temp_type = $('#relocate_type_%(i)s :selected').val();
		
		if (temp_amount != '' && temp_from != '' && temp_to != '')
		{
			if (temp_from != temp_to)
			{
				relocation_orders += 'Relocate ' + temp_amount + ' ' + temp_type + ' from ' + temp_from + ' to ' + temp_to + '\\n';
				relocation_materials += (parseInt(temp_amount)/1000);
			}
		}
		""" % {
			"i":	i,
		})
	
	output.append("</table></div>")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def army_block(oh, the_team, the_army):
	output, load_java, run_java = [], [], []
	
	# if the_army.id != 870:
	# 	return "".join(output), "".join(load_java), "".join(run_java)
	
	# unit_dict_c		= unit.get_unit_dict_c()
	# army_dict_c		= army.get_army_dict_c()
	squad_dict		= oh.the_world.squads()
	squads_lookup	= oh.the_world.squads_lookup_from_army(the_army.id)
	
	squad_java = []
	squad_output = []
	army_size = 0
	for sname, squad_id in squads_lookup.items():
		the_squad = squad_dict[squad_id]
		army_size += the_squad.amount
		
		additions = squad_block(oh, the_team, the_squad)
		squad_output.append(additions[0])
		load_java.append(additions[1])
		squad_java.append(additions[2])
	
	if the_army.garrison > 0:
		location = ""
		delete_army = ""
		form_spacing = ""
		rename_field = ""
		
	else:
		location = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Location: <input type="text" id="location_army_%d" value="%s, %s" />' % (the_army.id, the_army.x, the_army.y)
		delete_army = 'Delete army: <input type="checkbox" id="delete_army_%d" value="del"/>' % the_army.id
		form_spacing = "<br /><br />"
		rename_field = ' - <input type="text" id="rename_army_%d" value="New name?" />' % the_army.id
		
		run_java.append("""
		var temp_delete_army = $('#delete_army_%(army_id)d').attr("checked");
		if (temp_delete_army)
		{
			army_delete_orders += 'Delete army: %(army_name)s\\n';
		}
		
		var temp_army_location = $('#location_army_%(army_id)d').val();
		if (temp_army_location != '' && temp_army_location != '%(current_location)s')
		{
			army_relocate_orders += 'Relocate army: %(army_name)s, ' + temp_army_location + '\\n';
		}
		
		var temp_army_name = $('#rename_army_%(army_id)d').val();
		if (temp_army_name != '' && temp_army_name != 'New name?' && temp_army_name != '%(army_name)s')
		{
			army_rename_orders += 'Rename army: %(army_name)s, ' + temp_army_name + '\\n';
		}
		""" % {
			"army_name":		common.js_name(the_army.name),
			"army_id":			the_army.id,
			"current_location": "%s, %s" % (the_army.x, the_army.y),
		})
	
	output.append("""
	<div class="order_box">
		<a href="#" id="army_hide_%(id)s" onclick="$('#army_box_%(id)s').hide(500); $('#army_hide_%(id)s').hide(); $('#army_show_%(id)s').show(); return false;" class="block_link" style="float:right; margin: -5px;">Hide</a>
		<a href="#" id="army_show_%(id)s" onclick="$('#army_box_%(id)s').show(500); $('#army_show_%(id)s').hide(); $('#army_hide_%(id)s').show(); return false;" class="block_link" style="float:right; margin: -5px; display:none;">Show</a>
		
		<span class="stitle">%(name)s</span>
		
		<div class="army_order_box" id="army_box_%(id)s">
		<span style="">&nbsp;&nbsp;&nbsp;Size: %(army_size)s</span>
		%(rename_field)s
		
		%(form_spacing)s
		%(delete_army)s
		%(location)s
		
		<br /><br />
		<div id="%(id)d_squads" style="display:nnone;">
			<table border="0" cellspacing="0" cellpadding="5">
				<tr>
					<th>Squad name</th>
					<th>Type</th>
					<th>Squad size</th>
					<th>Amount to add</th>
					<!--<th>Move to army</th>-->
					<th>&nbsp;</th>
					<!--<th colspan="2">Merge</th>-->
				</tr>
			""" % {
		"id":			the_army.id,
		"name":			the_army.name,
		"army_size":	format(army_size, ','),
		"location":		location,
		"delete_army":	delete_army,
		"form_spacing": form_spacing,
		"rename_field": rename_field,
	})
	
	output.append("".join(squad_output))
	
	run_java.append("""
	var temp_army_recruit_orders = "";
	%s
	
	if (temp_army_recruit_orders != "")
	{
		army_recruit_orders += "\\n\\nSelect army: %s\\n" + temp_army_recruit_orders;
	}
	""" % ("".join(squad_java), common.js_name(the_army.name)))
	
	output.append("""
			</table>
			</div>
		</div>
	</div>
	""" % {
		"name": the_army.name,
	})
	
	return "".join(output), "".join(load_java), "".join(run_java)


def squad_block(oh, the_team, the_squad):
	output, load_java, run_java = [], [], []
	
	# unit_dict_c		= unit.get_unit_dict_c()
	# army_dict_c		= army.get_army_dict_c()
	# squad_dict_c	= squad.get_squad_dict_c()
	
	the_unit = oh.the_world.units()[the_squad.unit]
	the_army = oh.the_world.armies()[the_squad.army]
	
	if the_squad.amount <= 0:
		delete = '<label for="delete_squad_%d">Delete</label> <input type="checkbox" id="delete_squad_%d" value="del" />' % (the_squad.id, the_squad.id)
	else:
		delete = '<label for="disband_squad_%d">Disband</label> <input type="checkbox" id="disband_squad_%d" value="disb" />' % (the_squad.id, the_squad.id)
	
	output.append("""
	<tr>
		<td>%(name)s</td>
		<td>%(type)s</td>
		<td>%(amount)s</td>
		<td>%(amount_field)s</td>
		<td>%(delete)s</td>
	</tr>
	""" % {
		"id":		the_squad.id,
		"name":		'<input type="text" id="rename_squad_%d" value="%s" />' % (the_squad.id, the_squad.name),
		"type":		the_unit.name,
		"amount":	common.number_format(the_squad.amount),
		
		"amount_field": '<input type="text" id="squad_amount_%d" value="" size="7"/>' % the_squad.id,
		"delete":		delete,
		
		"merge_amount":		'<input type="text" id="merge_amount_%d" value="" size="7"/>' % the_squad.id,
	})
	
	run_java.append("""
	var temp_squad_amount = $('#squad_amount_%(id)d').val();
	var temp_delete_squad = $('#delete_squad_%(id)d').attr("checked");
	var temp_disband_squad = $('#disband_squad_%(id)d').attr("checked");
	
	if (temp_delete_squad)
	{
		squad_delete_orders += 'Delete squad: %(squad_name)s from %(army_name)s\\n';
	}
	else
	{
		if (temp_squad_amount != '')
		{
			if (temp_disband_squad)
			{
				temp_army_recruit_orders += 'Disband squad: %(squad_name)s, ' + temp_squad_amount + '\\n';
			}
			else
			{
				temp_army_recruit_orders += 'Reinforce squad: %(squad_name)s, ' + temp_squad_amount + '\\n';
			}
		}
	}
	
	var temp_squad_name = $('#rename_squad_%(id)d').val();
	var temp_squad_army = $('#move_field_%(id)d').val();
	
	if (temp_squad_name != '' && temp_squad_name != '%(squad_name)s')
	{
		squad_rename_orders += "\\nRename squad: %(squad_name)s in %(army_name)s, " + temp_squad_name;
	}
	""" % {
		"id":			the_squad.id,
		"squad_name":	common.js_name(the_squad.name),
		"army_name":	common.js_name(the_army.name),
	})
	
	return "".join(output), "".join(load_java), "".join(run_java)


def relocate_squad_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	unit_dict	= oh.the_world.units()
	army_dict	= oh.the_world.armies()
	squad_dict	= oh.the_world.squads()
	
	if oh.caches[the_team.id].get('squad_list', '') == "":
		return "".join(output), "".join(load_java), "".join(run_java)
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Squad relocation</a></h3>
	<span id="relocate_squad_help_link" style="cursor:pointer;" onclick="$('#relocate_squad_help_link').hide();$('#relocate_squad_help').show(500);">Show help</span>
	<div style="display:none;" id="relocate_squad_help">
		<ul>
			<li>The squad is the squad you wish to move from it's current army</li>
			<li>The new location is the army/garrison that you will be moving the squad to</li>
			<li>If you are creating a new army you will need to manually change the name of your target army</li>
		</ul>
	</div>
	<div class="order_box">
	<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<th>Squad</th>
			<th>New location</th>
		</tr>""")
	
	for i in range(0, 3):
		output.append("""
		<tr>
			<td>
				<select id="relocate_squad_squad_%(i)d">
					%(squad_dropdown)s
				</select>
			</td>
			<td>
				<select id="relocate_squad_army_%(i)d">
					<option value=""></option>
					%(army_dropdown)s
				</select>
			</td>
		</tr>""" % {
			"i":				i,
			"squad_dropdown":	oh.caches[the_team.id].get('squad_list', ''),#caches['squad_dropdown'],
			"army_dropdown":	oh.caches[the_team.id].get('army_list', ''),#caches['army_dropdown'],
		})
		
		run_java.append("""
		var temp_relocate_split = $('#relocate_squad_squad_%(i)d').val().split(',');
		var temp_army_c = temp_relocate_split[0];
		var temp_squad_c = temp_relocate_split[1];
		var temp_army_n = $('#relocate_squad_army_%(i)d').val();
		
		if (temp_army_c != '' && temp_army_n != '' && temp_army_c != temp_army_n && temp_squad_c != '')
		{
			squad_relocate_orders += "\\nMove squad: " + temp_army_c + " from " + temp_squad_c + " to " + temp_army_n;
		}
		""" % {
			"i":	i,
		})
	
	output.append("</table></div><br />")
	
	return "".join(output), "".join(load_java), "".join(run_java)
	


def merge_squad_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	if oh.caches[the_team.id].get('squad_list', '') == "":
		return "".join(output), "".join(load_java), "".join(run_java)
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Squad merging</a></h3>
	<span id="merge_squad_help_link" style="cursor:pointer;" onclick="$('#merge_squad_help_link').hide();$('#merge_squad_help').show(500);">Show help</span>
	<div style="display:none;" id="merge_squad_help">
		<ul>
			<li>Amount defines how many of the source squad move to the target squad</li>
			<li>Source squad is the squad that the units are taken from</li>
			<li>Target squad is the squad that units are sent to</li>
		</ul>
	</div>
	
	<div class="order_box">
	<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<th>Amount</th>
			<th>Source squad</th>
			<th>Target squad</th>
		</tr>""")
	
	for i in range(0, 3):
		output.append("""
		<tr>
			<td>
				<input type="text" id="merge_amount_%(i)d" value="" size="7"/>
			</td>
			<td>
				<select id="merge_source_%(i)d">
					%(squad_dropdown)s
				</select>
			</td>
			<td>
				<select id="merge_target_%(i)d">
					%(squad_dropdown)s
				</select>
			</td>
		</tr>""" % {
			"i":				i,
			"squad_dropdown":	oh.caches[the_team.id].get('squad_list', ''),#caches['squad_dropdown'],
		})
		
		run_java.append("""
		var temp_merge_amount = $('#merge_amount_%(i)d').val();
		
		var temp_merge_split = $('#merge_source_%(i)d').val().split(',');
		var temp_merge_squad_s = temp_merge_split[0];
		var temp_merge_army_s = temp_merge_split[1];
		
		var temp_merge_split = $('#merge_target_%(i)d').val().split(',');
		var temp_merge_squad_t = temp_merge_split[0];
		var temp_merge_army_t = temp_merge_split[1];
		
		if (temp_merge_squad_s != '' && temp_merge_squad_t != '' && temp_merge_amount != '')
		{
			squad_merge_orders += "\\Split squad: " + temp_merge_amount + " from " + temp_merge_squad_s + " in " + temp_merge_army_s + " to " + temp_merge_squad_t + " in " + temp_merge_army_t;
		}
		""" % {
			"i":	i,
		})
	
	output.append("</table></div><br />")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def new_armies(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">New army creation</a></h3>
	<div id="new_army_help" style="display:none;">
		<ul style="list-style-type: circle;margin-left:25px;">
			<li>The location of the army needs to be a map coordinate, not a city name or approximate place name.</li>
			<li>When an army is created it's also added to the create squads list of armies so you can put some squads in your new army.</li>
		</ul>
	</div>
	<span id="new_army_help_link" style="cursor:pointer;" onclick="$('#new_army_help_link').hide();$('#new_army_help').show(500);">Show help</span>
	<div class="order_box">
		<textarea id="new_army_text" rows="8" cols="40" style="display:none;"></textarea>
		<div id="new_army_html">
			&nbsp;
		</div>
		
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Army name</th>
				<th>Location</th>
				<th>&nbsp;</th>
			</tr>
				<form action="oops_teifion_made_a_mistake.html" method="post" accept-charset="utf-8">
					<tr>
						<td><input type="text" id="new_army_name_N" value="" /></td>
						<td><input type="text" id="new_army_location_N" value="" /></td>
						<td><input type="submit" id="new_army_add" value="Add to list" onclick="add_new_army(); return false;"/></td>
					</tr>
				</form>
			
			<div id="new_army_list">
				
			</div>
		</table>
	</div>
	""")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def new_squads(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">New squad creation</a></h3>
	<div id="new_squad_help" style="display:none;">
		<ul style="list-style-type: circle;margin-left:25px;">
			<li>Pushing enter while in the new-squad text fields will add the squad, wipe the name and size of the squad and place the cursor in the new squad box. It may only save you a few seconds but I figured it'd be a nice touch.</li>
			<li>To remove a created squad you need to edit the final output of the orders, I have currently not been able to make a more dynamic system of squad creation.</li>
		</ul>
	</div>
	<span id="new_squad_help_link" style="cursor:pointer;" onclick="$('#new_squad_help_link').hide();$('#new_squad_help').show(500);">Show help</span>
	<div class="order_box">
		<textarea id="new_squad_text" rows="8" cols="40" style="display:none;"></textarea>
		
		<div id="new_squad_html">
			&nbsp;
		</div>
		
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Squad name</th>
				<th>Size</th>
				<th>Unit type</th>
				<th>Army</th>
			</tr>
				<form action="oops_teifion_made_a_mistake.html" method="post" accept-charset="utf-8">
					<tr>
						<td><input type="text" id="new_squad_name_N" value="" /></td>
						<td><input type="text" id="new_squad_size_N" value="" /></td>
						<td>%(new_squad_type)s</td>
						<td>%(new_squad_army)s</td>
						<td><input type="submit" id="new_squad_add" value="Add to list" onclick="add_new_squad(); return false;"/></td>
					</tr>
				</form>
			
			<div id="new_squad_list">
				
			</div>
		</table>
	</div>
	""" % {
		"new_squad_type":	"""<select id="new_squad_type_N">
			%s
		</select>""" % oh.caches[the_team.id].get('all_unit_list', ''),#caches['unit_dropdown'],
		"new_squad_army":	"""<select id="new_squad_army_N">
			%s
		</select>
		""" % oh.caches[the_team.id].get('army_list', ''),#caches['army_dropdown'],
	})
	
	return "".join(output), "".join(load_java), "".join(run_java)


def mundane_research(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""<h3 style="clear:both;"><a href="#" onclick="return false;">Mundane research</a></h3>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">""")
	
	for i in range(0, 6):
		output.append("""
		<tr>
			<td>
				<select id="mundane_research_%(i)d" onchange="">
					%(tech_dropdown)s
				</select>
			</td>
		</tr>
		""" % {
			"i":				i,
			"tech_dropdown":	oh.caches[the_team.id].get('tech_list', ''),
		})
		
		run_java.append("""
		var temp_spell = $('#mundane_research_%(i)d').val();
		if (temp_spell != '')
		{
			research_orders += "\\n" + temp_spell;
		}
		""" % {
			"i": i,
		})
	
	output.append("</table></div>")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def magical_research(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""<h3 style="clear:both;"><a href="#" onclick="return false;">Magical research</a></h3>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">""")
	
	for i in range(0, 6):
		output.append("""
		<tr>
			<td>
				<select id="magical_research_%(i)d" onchange="">
					%(spell_dropdown)s
				</select>
			</td>
		</tr>
		""" % {
			"i":				i,
			"spell_dropdown":	oh.caches[the_team.id].get('spell_list', ''),
		})
		
		run_java.append("""
		var temp_spell = $('#magical_research_%(i)d').val();
		if (temp_spell != '')
		{
			research_orders += "\\n" + temp_spell;
		}
		""" % {
			"i": i,
		})
	
	output.append("</table></div>")
	
	return "".join(output), "".join(load_java), "".join(run_java)


# MAIN BLOCK - OPERATIVES
def reinforce_ops(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Reinforcement</a></h3>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Name</th>
				<th>Current size</th>
				<th style="font-size: 0.9em;">Stealth</th>
				<th style="font-size: 0.9em;">Observation</th>
				<th style="font-size: 0.9em;">Integration</th>
				<th style="font-size: 0.9em;">Sedition</th>
				<th style="font-size: 0.9em;">Sabotage</th>
				<th style="font-size: 0.9em;">Assassination</th>
				<th style="font-size: 0.9em;">City</th>
				<th>Add</th>
			</tr>""")
	
	operative_dict = oh.the_world.operatives_from_team(the_team.id)
	city_dict = oh.the_world.cities()
	for op_id, the_op in operative_dict.items():
		if the_op.died > 0: continue
		
		output.append("""
		<tr>
			<td>{name}</td>
			<td>{size}</td>
			<td>{stealth}</td>
			<td>{observation}</td>
			<td>{integration}</td>
			<td>{sedition}</td>
			<td>{sabotage}</td>
			<td>{assassination}</td>
			<td>{city}</td>
			<td>
				<input type="text" id="op_reinforce_{op_id}" value="" size="4"/>
			</td>
		</tr>
		""".format(
			name=the_op.name,
			size=the_op.size,
			stealth=the_op.stealth,
			observation=the_op.observation,
			integration=the_op.integration,
			sedition=the_op.sedition,
			sabotage=the_op.sabotage,
			assassination=the_op.assassination,
			city=city_dict[the_op.city].name,
			op_id=op_id,
		))
		
		run_java.append("""
		var temp_amount = $('#op_reinforce_%(op_id)d').val();
		
		if (temp_amount != "")
		{
			recruitment_orders += "\\nReinforce cell: %(name)s by " + temp_amount;
		}""" % {
			"op_id":	op_id,
			"name":		the_op.name,
		})
	
	output.append("</table></div><br /><br />")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def recruit_ops(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append("""
	<h3 style="clear:both;"><a href="#" onclick="return false;">Recruitment</a></h3>
	<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Name</th>
				<th>Size</th>
				<th style="font-size: 0.85em;">Stealth</th>
				<th style="font-size: 0.85em;">Observation</th>
				<th style="font-size: 0.85em;">Integration</th>
				<th style="font-size: 0.85em;">Sedition</th>
				<th style="font-size: 0.85em;">Sabotage</th>
				<th style="font-size: 0.85em;">Assassination</th>
				<th style="font-size: 0.85em;">City</th>
			</tr>""")
	
	for i in range(0, 6):
		output.append("""
		<tr>
			<td>
				<input type="text" id="new_op_name_%(i)d" value="" size="10" />
			</td>
			<td>
				<input type="text" id="new_op_size_%(i)d" value="1" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_stealth_%(i)d" value="1" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_observation_%(i)d" value="1" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_integration_%(i)d" value="1" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_sedition_%(i)d" value="0" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_sabotage_%(i)d" value="0" size="3" />
			</td>
			<td>
				<input type="text" id="new_op_assassination_%(i)d" value="0" size="3" />
			</td>
			<td>
				<select id="new_op_city_%(i)d">
					<option value=""></option>
					%(city_dropdown)s
				</select>
			</td>
		</tr>
		""" % {
			"i":				i,
			"city_dropdown":	oh.caches[0].get('operative_city_dropdown', ''),
		})
		
		run_java.append("""
		var temp_name = $('#new_op_name_%(i)d').val();
		var temp_size = $('#new_op_size_%(i)d').val();
		var temp_stealth = $('#new_op_stealth_%(i)d').val();
		var temp_observation = $('#new_op_observation_%(i)d').val();
		var temp_integration = $('#new_op_integration_%(i)d').val();
		var temp_sedition = $('#new_op_sedition_%(i)d').val();
		var temp_sabotage = $('#new_op_sabotage_%(i)d').val();
		var temp_assassination = $('#new_op_assassination_%(i)d').val();
		var temp_city = $('#new_op_city_%(i)d').val();
		
		if (temp_name != '' && temp_size != '' && temp_stealth != '' && temp_observation != '' && temp_integration != '' && temp_city != '')
		{
			recruitment_orders += "\\nRecruit cell: " + temp_name + " at " + temp_city + ", Size: " + temp_size + ", Stealth: " + temp_stealth + ", Observation: " + temp_observation + ", Integration: " + temp_integration;
			
			if (temp_sedition != 0 && temp_sedition > 0)
			{
				recruitment_orders += ", Sedition: " + temp_sedition;
			}
			if (temp_sabotage != 0 && temp_sabotage > 0)
			{
				recruitment_orders += ", Sabotage: " + temp_sabotage;
			}
			if (temp_assassination != 0 && temp_assassination > 0)
			{
				recruitment_orders += ", Assassination: " + temp_assassination;
			}
		}""" % {
			"i":	i,
		})
	
	output.append("</table></div><br /><br />")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def research_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append('''<h3 style="clear:both;"><a href="#" onclick="return false;">Research trade</a></h3>
	<div class="order_box">
	<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<th>Send a tech or a spell</th>
			<th>To</th>
		</tr>''')
	
	for i in range(0,2):
		output.append("""
			<tr>
				<td>
					<select id="research_trade_tech_%(i)d">
						%(tech_dropdown)s
					</select>
				
					<select id="research_trade_spell_%(i)d">
						%(spell_dropdown)s
					</select>
				</td>
				<td>
					<select id="research_trade_team_%(i)d">
						%(all_team_dropdown)s
					</select>
				</td>
			</tr>""" % {
			"i":					i,
			"all_team_dropdown":	oh.caches[the_team.id].get('team_list', ''),#caches['all_team_dropdown'],
			"spell_dropdown":		oh.caches[the_team.id].get('spell_trade', ''),#caches['spell_dropdown_trade'],
			"tech_dropdown":		oh.caches[the_team.id].get('tech_trade', ''),#caches['tech_dropdown_trade'],
		})
		
		run_java.append("""
		var temp_tech = $('#research_trade_tech_%(i)d').val();
		var temp_spell = $('#research_trade_spell_%(i)d').val();
		var temp_target = $('#research_trade_team_%(i)d').val();
		
		if (temp_target != '' && temp_spell != '')
		{
			trade_orders += '\\nSend ' + temp_spell + ' to ' + temp_target;
		}
		else if (temp_tech != '' && temp_target != '')
		{
			trade_orders += '\\nSend ' + temp_tech + ' to ' + temp_target;
		}
		""" % {
			"i":	i,
		})
	
	output.append("</table></div><br /><br />")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def resource_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append('<h3 style="clear:both;"><a href="#" onclick="return false;">Resource trade</a></h3>')
	
	if oh.caches[the_team.id].get('discrete_resources', '') != "":
		output.append("""
		<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Resource</th>
				<th>To</th>
			</tr>""")
		
		for i in range(0, 3):
			output.append("""
			<tr>
				<td>
					<input type="text" id="resource_amount_%(i)s" value="" size="5"/>
					&nbsp;
					<select id="resource_resource%(i)s">
						%(discrete_dropdown)s
					</select>
				</td>
				<td>
					<select id="resource_target_%(i)s">
						%(all_team_dropdown)s
					</select>
				</td>
			</tr>
			""" % {
				"all_team_dropdown":	oh.caches[the_team.id].get('team_list', ''),
				"discrete_dropdown":	oh.caches[the_team.id].get('discrete_resources', ''),
				"i":					i,
			})
			
			run_java.append("""
			var temp_target = $('#resource_target_%(i)d').val();
			var temp_amount = $('#resource_amount_%(i)s').val();
			var temp_resource = $('#resource_resource%(i)d').val();
			if (temp_target != '' && temp_resource != '' && temp_amount != '')
			{
				trade_orders += '\\nSend ' + temp_amount + ' ' + temp_resource + ' to ' + temp_target;
			}
			""" % {
				"i":	i,
			})
		
		output.append("""
		</table></div>""")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def supply_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	output.append('<h3 style="clear:both;"><a href="#" onclick="return false;">Supply trade</a></h3>')
	
	if oh.caches[the_team.id].get('boolean_resources', '') != "":
		output.append("""
		<div class="order_box">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Supply</th>
				<th>To</th>
			</tr>""")
		
		for i in range(0, 3):
			output.append("""
			<tr>
				<td>
					<select id="supply_supply_%(i)s">
						%(boolean_dropdown)s
					</select>
				</td>
				<td>
					<select id="supply_target_%(i)s">
						%(team_trade_dropdown)s
					</select>
				</td>
			</tr>
			""" % {
				"team_trade_dropdown":	oh.caches[the_team.id].get('trade_list', ''),
				"boolean_dropdown":		oh.caches[the_team.id].get('boolean_resources', ''),
				"i":					i,
			})
			
			run_java.append("""
			var temp_target = $('#supply_target_%(i)d').val();
			var temp_supply = $('#supply_supply_%(i)d').val();
			if (temp_target != '' && temp_supply != '')
			{
				trade_orders += '\\nSend ' + temp_supply + ' to ' + temp_target;
			}
			""" % {
				"i":	i,
			})
		
		output.append("""
			<tr>
				<td colspan="2">Only teams you have a trade route to are shown</td>
			</tr>
		</table></div><br />""")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def relations_block(oh, the_team):
	output, load_java, run_java = [], [], []
	
	states = """
	<option value="Default">Default</option>
	<option value="At war">At war</option>
	<option value="Closed">Closed</option>
	<option value="Segregated">Segregated</option>
	<option value="Open">Open</option>
	<option value="Allied">Allied</option>"""
	
	world_relations = oh.the_world.relations()
	team_relations = world_relations.get(the_team.id, {})
	
	# Find our default
	state_find = 'value="%s"' % team.border_states[the_team.default_borders]
	
	# What to replace it with
	state_replace = '%s selected="selected"' % state_find
	
	output.append('''
	<h3 style="clear:both;"><a href="#" onclick="return false;">Relations</a></h3>
	<div id="borders_help" style="display:none;">
		<ul style="list-style-type: circle;margin-left:25px;">
			<li></li>
		</ul>
	</div>
	<span id="borders_help_link" style="cursor:pointer;" onclick="$('#borders_help_link').hide();$('#borders_help').show(500);">Show help</span>
	<br /><br />
	
	Default border state:&nbsp;&nbsp;
	<select id="default_border_state">
		%(states)s
	</select>
	<br /><br />
	
	
	Default tax rate:&nbsp;&nbsp;
	<input type="text" id="default_taxes" value="%(default_taxes)s" size="4"/>%%
	<br /><br />
	
	<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<th>Team</th>
			<th>Your state</th>
			<th>Their state</th>
			<th>&nbsp;</th>
			<th>Your taxes</th>
			<th>Their taxes</th>
		</tr>''' % {
		"states":	states.replace('<option value="Default">Default</option>', '').replace(state_find, state_replace),
		"default_taxes":	the_team.default_taxes,
	})
	
	run_java.append("""
	var temp_state = $('#default_border_state').val();
	if (temp_state != '' && temp_state != "%(default)s")
	{
		border_orders += "\\nSet default borders to " + temp_state;
	}
	
	var default_taxes = $('#default_taxes').val();
	if (default_taxes != '' && default_taxes != "%(default_taxes)s")
	{
		tax_orders += "\\nSet default taxes to " + default_taxes;
	}
	""" % {
		"default":		team.border_states[the_team.default_borders],
		"default_taxes":	the_team.default_taxes,
	})
	
	team_dict = oh.the_world.teams()
	for t, other_team in team_dict.items():
		if t == the_team.id: continue
		if other_team.hidden: continue
		if not other_team.active: continue
		
		ir = ""
		if other_team.ir:
			ir = " <em>(IR)</em>"
		
		other_relations = world_relations.get(t, {})
		
		other_team_borders = other_relations.get("borders", {}).get(the_team.id, other_team.default_borders)
		other_default_borders = other_team.default_borders
		other_taxes = other_relations.get("taxes", {}).get(the_team.id, other_team.default_taxes)
		
		# The state to find
		# state_find = 'value="%s"' % team_borders.get(t, default_borders)
		
		if t in team_relations:	default_state = team.border_states[team_relations[t].get('border', the_team.default_borders)]
		else:					default_state = "Default"
		
		state_find = 'value="%s"' % default_state
		
		# What to replace it with
		state_replace = '%s selected="selected"' % state_find
		other_state = other_team_borders
		
		# TAXES
		if "taxes" not in team_relations.get(t, {}):
			# Currently default
			tax_check_box = '<input type="checkbox" id="default_rate_%d" value="1" checked="checked"/>' % t
			
			tax_if = 'if (use_default == false)'
		else:
			
			tax_check_box = '<input type="checkbox" id="default_rate_%d" value="1"/>' % t
			
			tax_if = 'if ((temp_taxes != "" && temp_taxes != "%s") || use_default == true)' % team_relations.get(t, {}).get('taxes', -1)
		
		# Output
		output.append("""
		<tr>
			<td>%(name)s%(ir)s</td>
			<td>
				<select id="border_state_%(t)d">
					%(states)s
				</select>
			</td>
			<td>&nbsp;&nbsp;
				<span style="color:#%(other_state_c)s;">%(other_state)s</span>
			</td>
			
			<td style="width:25px;">&nbsp;</td>
			
			<td>
				<input type="text" id="tax_rate_%(t)d" value="%(our_tax_rate)s" size="4" onchange="$('#default_rate_%(t)d').attr('checked', '')"/>%%
				&nbsp;&nbsp;
				Default: %(tax_check_box)s
			</td>
			<td>&nbsp;&nbsp;
				%(other_rate)s%%
			</td>
		</tr>
		""" % {
			"t":				t,
			"ir":				ir,
			"name":				other_team.name,
			"states":			states.replace(state_find, state_replace),
			"other_state":		team.border_states[other_state],
			"other_state_c":	team.border_colour(other_state),
			
			"our_tax_rate":		team_relations.get(t, {}).get('taxes', the_team.default_taxes),
			"other_rate":		other_taxes,
			"tax_check_box":	tax_check_box,
		})
		
		# Java
		run_java.append("""
		var temp_state = $('#border_state_%(t)d').val();
		if (temp_state != '' && temp_state != "%(default)s")
		{
			border_orders += "\\nBorders to %(other_team)s are " + temp_state;
		}
		
		var temp_taxes = $('#tax_rate_%(t)d').val();
		var use_default = $('#default_rate_%(t)d').attr("checked");
		
		%(tax_if)s
		{
			if (use_default == true)
			{
				tax_orders += "\\Taxes for %(other_team)s are default";
			}
			else
			{
				tax_orders += "\\nTaxes for %(other_team)s are " + temp_taxes;
			}
		}
		""" % {
			"t":			t,
			"default":		default_state,
			"other_team":	other_team.name,
			
			"tax_if":		tax_if,
		})
	
	output.append("</table>")
	
	return "".join(output), "".join(load_java), "".join(run_java)


def spelling_compression(text):
	return text.replace("\t", "")#.replace("\n", "")
	
	# Function calls
	text = text.replace("add_option", "a_o")
	
	# Construction
	text = text.replace("building_array", "b_arr")
	text = text.replace("building_menu", "b_mnu")
	text = text.replace("wall_menu", "w_mnu")
	# migration_text_
	
	return text


def javascript(load_java, run_java):
	return """
	function add_new_army()
	{
		var new_army_line = "";
		var new_name = $('#new_army_name_N').val();
		new_army_line = "Create army: " + new_name + ", " + $('#new_army_location_N').val();
	
		if (new_army_line != '')
		{
			$('#new_army_name_N').val('');
			$('#new_army_location_N').val('');
		
			$('#new_army_html').html("" + $('#new_army_html').html() + "<br>" + new_army_line);
			$('#new_army_text').text("" + $('#new_army_text').text() + "\\n" + new_army_line);
		
			$('#new_squad_army_N').append('<option value="' + new_name + '">' + new_name + '</option>');
			/*
			$('#new_squad_army_N').attr('selectedIndex', 0);
			*/
		}
	}
	
	function add_new_squad()
	{
		var new_unit_line = "";
	
		new_unit_line = "Create squad: " + $('#new_squad_name_N').val() + ", " + $('#new_squad_size_N').val() + ", " + $('#new_squad_type_N').val() + ", " + $('#new_squad_army_N').val();
	
		if (new_unit_line != '')
		{
			$('#new_name_N').val('');
			$('#new_squad_size_N').val('');
			$('#new_name_N').focus();
		
			/* We don't want to change their selection for now
			$('#new_squad_type_N').attr('selectedIndex', 0);
			$('#new_squad_army_N').attr('selectedIndex', 0);
			*/
		
			$('#new_squad_html').html("" + $('#new_squad_html').html() + "<br>" + new_unit_line);
			$('#new_squad_text').text("" + $('#new_squad_text').text() + "\\n" + new_unit_line);
		}
	}
	
	function on_load_setup ()
	{
		%(load_java)s
		
		/* build_orders(); */
		$('#loading_div').hide();
		 switch_to('construction');
		// switch_to('military');
		// switch_to('monsters');
		// switch_to('research');
		// switch_to('operative');
		// switch_to('trade');
		// switch_to('diplomacy');
	}
	
	function on_keyup_run ()
	{
		//build_orders();
	}
	
	function on_change_run ()
	{
		//build_orders();
	}
	
	%(run_java)s
	
	function clean_text (input_text)
	{
		return input_text.replace("\\t", "").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\n\\n\\n", "\\n\\n").replace("\\\\", "");
	}
	
	function build_orders ()
	{
		var final_output	= '';
	
		on_change_cities();
		on_change_military();
		/* on_change_monsters(); */
		on_change_research();
		on_change_operatives();
		on_change_trade();
		on_change_diplomacy();
	
		final_output += $('#city_orders').text();
		final_output += $('#military_orders').text();
		final_output += $('#monster_orders').text();
		final_output += $('#research_orders').text();
		final_output += $('#operative_orders').text();
		final_output += $('#trade_orders').text();
		final_output += $('#diplomacy_orders').text();
	
		final_output = clean_text(final_output)		
		$('#final_output').text(final_output);
	}
	
	function hide_all_sections ()
	{
		$('#construction_div').hide();
		$('#military_div').hide();
		$('#monsters_div').hide();
		$('#research_div').hide();
		$('#operative_div').hide();
		$('#trade_div').hide();
		$('#diplomacy_div').hide();
		$('#advanced_div').hide();
		$('#command_div').hide();
		
		$('#construction_tab').removeClass('ti_tab_selected');
		$('#military_tab').removeClass('ti_tab_selected');
		$('#monsters_tab').removeClass('ti_tab_selected');
		$('#research_tab').removeClass('ti_tab_selected');
		$('#operative_tab').removeClass('ti_tab_selected');
		$('#trade_tab').removeClass('ti_tab_selected');
		$('#diplomacy_tab').removeClass('ti_tab_selected');
		$('#advanced_tab').removeClass('ti_tab_selected');
		$('#command_tab').removeClass('ti_tab_selected');
		
		$('#bottom_construction_tab').removeClass('ti_tab_selected');
		$('#bottom_military_tab').removeClass('ti_tab_selected');
		$('#bottom_monsterstab').removeClass('ti_tab_selected');
		$('#bottom_research_tab').removeClass('ti_tab_selected');
		$('#bottom_operative_tab').removeClass('ti_tab_selected');
		$('#bottom_trade_tab').removeClass('ti_tab_selected');
		$('#bottom_diplomacy_tab').removeClass('ti_tab_selected');
		$('#bottom_advanced_tab').removeClass('ti_tab_selected');
		$('#bottom_command_tab').removeClass('ti_tab_selected');
	}
	
	function switch_to (div_name)
	{
		hide_all_sections();
		$('#' + div_name + '_div').show();
		$('#' + div_name + '_tab').addClass('ti_tab_selected');
		$('#bottom_' + div_name + '_tab').addClass('ti_tab_selected');
	}
	
	""" % {
		"load_java":	load_java,
		"run_java":		run_java,
	}