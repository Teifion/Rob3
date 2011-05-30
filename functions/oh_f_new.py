import collections
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
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def normal_city_block(oh, the_team, the_city):
	walls, normals = [], []
	wall_selected, normal_selected = -1, -1
	
	# Handles
	buildings_progress, buildings_amount = the_city.buildings, the_city.buildings_amount
	building_dict			= oh.the_world.buildings()
	buildings_requirements	= oh.the_world.building_requirements()
	
	for b, the_building in building_dict.items():
		if not the_building.public: continue
		if the_building.name == "VOID": continue
		
		do_not_list = False
		
		# Value used in the list
		b_value = [b, False, 0]
		
		if the_building.needs_port and not the_city.port:
			continue
		
		# Find out if we've already built one...
		if buildings_amount.get(b, 0) > 0:
			b_value[1] = True
			
			# Have we upgraded it (and thus don't want it to appear at all)?
			if b in buildings_requirements:
				for target in buildings_requirements[b]:
					if buildings_amount.get(target, 0) > 0: do_not_list = True
					if buildings_progress.get(target, 0) > 0: do_not_list = True
			
		else:
			# In progress?
			if buildings_progress.get(b,0) > 0:
				b_value[2] = buildings_progress[b]
				
				if the_building.wall:
					wall_selected = b
				else:
					normal_selected = b
			
			# Does it require something else?
			if b in buildings_requirements:
				for build_id in buildings_requirements[b]:
					if buildings_amount.get(build_id, 0) > 0:
						do_not_list = True
		
			# We've not started it but that might be because we can't
			if the_building.upgrades > -1:
				if buildings_amount.get(the_building.upgrades, 0) <= 0:
					do_not_list = True
		
			# We've not started it but that might be because we've already upgraded it and it's been replaced
			if b in buildings_requirements:
				for target in buildings_requirements[b]:
					if buildings_amount.get(target, 0) > 0: do_not_list = True
					if buildings_progress.get(target, 0) > 0: do_not_list = True
			
		if not do_not_list:
			if the_building.wall:
				walls.append(b_value)
			else:
				normals.append(b_value)
	
	return {
		"name":				the_city.name,
		"walls":			walls,
		"normals":			normals,
		"wall_selected":	wall_selected,
		"normal_selected":	normal_selected,
	}

def founding_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)


def relocation_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def army_block(oh, the_team, the_army):
	city_dict = oh.the_world.live_cities_from_team(the_team.id)
	
	squads = collections.OrderedDict()
	amount = 0
	
	for s, the_squad in the_army.squads.items():
		squads[s] = squad_block(oh, the_team, the_squad)
		
		amount += max(the_squad.amount, 0)
	
	city_pos = ""
	for i, c in city_dict.items():
		if c.x == the_army.x and c.y == the_army.y:
			city_pos = c.name
		
	
	return {
		"name":				the_army.name,
		"position":			"%s, %s" % (the_army.x, the_army.y),
		"garrison":			the_army.garrison,
		"base":				the_army.base,
		"city_pos":			city_pos,
		"amount":			format(amount, ","),
		"squad_list":		list(squads.keys()),
	}

def squad_block(oh, the_team, the_squad):
	return {
		"name":			the_squad.name,
		"unit_type":	the_squad.unit,
		"amount":		format(the_squad.amount, ","),
	}

def relocate_squad_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def merge_squad_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def new_armies(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def new_squads(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def mundane_research(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def magical_research(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

# MAIN BLOCK - OPERATIVES
def reinforce_ops(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def recruit_ops(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def research_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def resource_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def supply_trade_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)

def relations_block(oh, the_team):
	output, load_java, run_java = [], [], []
	raise Exception("Not implimented")
	return "".join(output), "".join(load_java), "".join(run_java)


command_text = """
This section is designed to hold special commands for test orders, these are not for normal orders but can allow you to get more information through Rob Requests. All commands found here should be headed by a <strong>[o]Rob command[/o]</strong> heading.<br /><br />

<h3 style="clear:both;"><a href="#" onclick="return false;">Assumption</a></h3>
Rob can assume that you have traded for a given supply and run all further orders in the test orders with that in mind.
<textarea rows="4" style="width:99%;">Assume supply: Iron
Assume supply: Stone
Assume supply: Wood</textarea>
<br /><br />

Additionally you can assume a certain amount of a normal resource like so:
<textarea rows="4" style="width:99%;">Assume resource: 500 Materials
Assume resource: 500 Ship points
Assume resource: 100 Balloon points</textarea>
<br /><br />

<h3 style="clear:both;"><a href="#" onclick="return false;">Paths</a></h3>
Rob can give information on travel times using the pathing system used for colonisation and founding orders. It'll output several travel times for you. As long as there are an even number of number pairs then Rob will try to work out the path.
<textarea rows="3" style="width:99%;">Path: 170, 1269, 405, 1332// North west Humyti to Tishrashi desert
Path: 273, 1605, 536, 1537, 186, 1264</textarea>
<br /><br />

<h3 style="clear:both;"><a href="#" onclick="return false;">Overbudget</a></h3>
By default Rob will try to prevent you going overbudget on materials, using the overbudget command you can disable this. Be careful with this one because when overbudget you generally cannot conduct wars and civilian morale falls fast.
<textarea rows="3" style="width:99%;">Enable: overbudget
Disable: overbudget</textarea>
<br /><br />"""

advanced_text = """This section is designed to hold more advanced and less frequently used order types.
<br /><br />

<h3 style="clear:both;"><a href="#" onclick="return false;">Re-equipping</a></h3>
This needs to be placed under a military heading such as <strong>[o]Military[/o]</strong>.
<br /><br />

<span class="stitle">Adding</span><br />
<textarea rows="3" style="width:99%;">Add equipment: {unit name}, {item 1}, {item 2}
Add equipment: Swordsmen, Short sword</textarea>
<br /><br />

<span class="stitle">Removing</span><br />
<textarea rows="3" style="width:99%;">Remove equipment: {unit name}, {item 1}, {item 2}
Remove equipment: Swordsmen, Spear</textarea>
<br /><br />

<span class="stitle">Changing / Replacing</span><br />
Note that here you must list <strong>all</strong> of the equipment for the unit, not just what you are changing. This order is useful if you want to both add and remove equipment so that you only need to retrain the unit once.
<textarea rows="3" style="width:99%;">New equipment: {unit name}, {item 1}, {item 2}
New equipment: Swordsmen, Short sword, Good training</textarea>
<br /><br />

<h3 style="clear:both;"><a href="#" onclick="return false;">New unit</a></h3>
You can add units to your TI through rob requests and orders themselves. Be sure to test the order through rob requests and pay attention to the instructions to confirm the adding of the unit. The new unit command needs to be in a <strong>[o]Military[/o]</strong> block.
<textarea rows="3" style="width:99%;">New unit: {unit name}, {list of equipment}
New unit: Elite swordsmen, Short sword, Elite training, Leather suit</textarea>
<br /><br />"""
