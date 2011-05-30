from pages import common
from data_classes import equipment
from queries import equipment_q
from classes import res_dict
import math

def equipment_line(the_equipment):
	return """%(material)s:%(iron)s:%(name)s""" % {
		"material": res_dict.Res_dict(the_equipment.cost).flatten(host_resources="Iron:1").get("Materials"),
		"iron":		res_dict.Res_dict(the_equipment.cost).get("Materials"),
		"name":		the_equipment.name,
	}

page_data = {
	"Title":	"Unit designer",
	"Admin":	True,
}

def main(cursor):
	equipment_dict	= equipment_q.get_all_equipment(cursor)
	
	output = []
	
	count = -1
	
	weapons, weapons_dict	= ["0:0:"], {"0:0:":""}
	armour, armour_dict		= ["0:0:"], {"0:0:":""}
	shields, shields_dict	= ["0:0:"], {"0:0:":""}
	mounts, mounts_dict		= ["0:0:"], {"0:0:":""}
	beasts, beasts_dict		= ["0:0:"], {"0:0:":""}
	boats, boats_dict		= [], {}
	training, training_dict	= [], {}

	for e, the_equipment in equipment_dict.items():
		if the_equipment.public == False: continue
	
		cat = equipment.cat_list[the_equipment.category]
		line = equipment_line(the_equipment)
	
		if cat in ('Sword','Axe','Hammer','Flail','Polearm','Dagger','Bow','Crossbow','Thrown','Gunpowder',):
			weapons_dict[line] = the_equipment.name
			weapons.append(line)
	
		elif cat == 'Armour':
			armour_dict[line] = the_equipment.name
			armour.append(line)
	
		elif cat == 'Shield':
			shields_dict[line] = the_equipment.name
			shields.append(line)
	
		elif cat == 'Mount':
			mounts_dict[line] = the_equipment.name
			mounts.append(line)
	
		elif cat == 'Beast':
			beasts_dict[line] = the_equipment.name
			beasts.append(line)
	
		elif cat == 'Boat hull':
			boats_dict[line] = the_equipment.name
			boats.append(line)
	
		elif cat == 'Training':
			line = """%(material)s:%(name)s""" % {
				"material": res_dict.Res_dict(the_equipment.cost_multiplier).get("Materials"),
				"name":		the_equipment.name,
			}
		
			training_dict[line] = the_equipment.name
			training.append(line)
	
		elif cat in ('Custom','Balloon','Siege engine','Seabourne mount'):
			pass
	
		else:
			raise Exception("No handler for type %s" % cat)

	# Army stuff
	output.append("""
	<table border="0" cellspacing="5" cellpadding="5">
		<tr>
			<td>Unit name:</td>
			<td><input type="text" id="name" value="" onkeyup="calc_army();"/></td>
		
			<td>&nbsp;</td>
		
			<td>Training:</td>
			<td>%(training)s</td>
		</tr>
		<tr>
			<td>Weapon 1:</td>
			<td>%(first_weapon)s</td>
		
			<td>&nbsp;</td>
		
			<td>Weapon 2:</td>
			<td>%(second_weapon)s</td>
		</tr>
	
		<tr>
			<td>Armour 1:</td>
			<td>%(first_armour)s</td>
		
			<td>&nbsp;</td>
		
			<td>Armour 2:</td>
			<td>%(second_armour)s</td>
		</tr>
	
		<tr>
			<td>Shield:</td>
			<td>%(shield)s</td>
		
			<td>&nbsp;</td>
		
			<td>Beast:</td>
			<td>%(beast)s</td>
		</tr>
	
		<tr>
			<td>Mount:</td>
			<td colspan="4">%(mount)s</td>
		</tr>
	</table>
	<div class="armyblock" id="army_bbcode">
		Awaiting your input
	</div>
	""" % {
		"training": common.option_box("",
			elements=training_dict,
			element_order=training,
			onchange="calc_army();",
			custom_id="army_training",
			selected="1:1:Standard training"),
	
		"first_weapon": common.option_box("",
			elements=weapons_dict,
			element_order=weapons,
			onchange="calc_army();",
			custom_id="first_weapon"),
		"second_weapon": common.option_box("",
			elements=weapons_dict,
			element_order=weapons,
			onchange="calc_army();",
			custom_id="second_weapon"),
	
		"first_armour": common.option_box("",
			elements=armour_dict,
			element_order=armour,
			onchange="calc_army();",
			custom_id="first_armour"),
		"second_armour": common.option_box("",
			elements=armour_dict,
			element_order=armour,
			onchange="calc_army();",
			custom_id="second_armour"),
	
		"shield": common.option_box("",
			elements=shields_dict,
			element_order=shields,
			onchange="calc_army();",
			custom_id="shield"),
		
		"mount": common.option_box("",
			elements=mounts_dict,
			element_order=mounts,
			onchange="calc_army();",
			custom_id="mount"),
		
		"beast": common.option_box("",
			elements=beasts_dict,
			element_order=beasts,
			onchange="calc_army();",
			custom_id="beast"),
	})

	# Navy stuff
	output.append("""
	<table border="0" cellspacing="5" cellpadding="5">
		<tr>
			<td>Ship name:</td>
			<td><input type="text" id="navy_name" value="" onkeyup="calc_navy();"/></td>
		
			<td>&nbsp;</td>
		
			<td>Training:</td>
			<td>
				<select id="navy_training" onchange="calc_navy();">
					<option value="1:Standard training">Standard training</option>
					<option value="1.5:Good training">Good training</option>
				</select>
			</td>
		</tr>
		<tr>
			<td>Hull 1:</td>
			<td>%(hull)s</td>
		</tr>
	</table>
	<div class="navyblock" id="navy_bbcode">
		Awaiting your input
	</div>
	""" % {	
		"hull": common.option_box("",
			elements=boats_dict,
			element_order=boats,
			onchange="calc_navy();",
			custom_id="hull"),
	})

	return "".join(output)