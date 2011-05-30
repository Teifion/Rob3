import database
import time, math
from pages import common
from classes import team, player, power, city
from functions import stat_f, path_f, team_f
from lists import resource_list
from queries import mapper_q, operative_q
import traceback
from rules import deity_rules
from rules import tech_rules, spell_rules, team_rules, unit_rules, map_data, city_rules, sad_rules

def headers(the_team):
	# Makes printing those flashy links that much easier
	def linkfade(link_name):
		return '''class="clear_link" onmouseover="$('#%sLinkInfo').fadeIn(250);" onmouseout="$('#%sLinkInfo').fadeOut(250);"''' % (link_name, link_name)
	
	return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<title>%(name)s Team Information</title>
		<script type="text/javascript" src="../includes/jquery.js" charset="utf-8"></script>
		<link rel="stylesheet" href="../styles.css" type="text/css" media="screen" title="no title" charset="utf-8" />
		%(javascript)s
		<style type="text/css" media="screen">
			body
			{
				font-size:0.9em;
			}
		</style>
	</head>
	<body id="order_form" onload="">
		<div class="page">
			<div class="header">
			<div id="logo">
				<a id="woaLogo" href="../"></a>
			</div>
			<ul>
				<li id="registerLink"><a href="http://woarl.com/board/ucp.php?mode=register" %(linkfade_register)s>Register</a></li>
				<li id="loginLink"><a href="http://woarl.com/board/ucp.php?mode=login" %(linkfade_login)s>Login</a></li>
				<li id="contactLink"><a href="../pages/general/contact.html" %(linkfade_contact)s>Contact</a></li>
				<li id="aboutLink"><a href="../pages/general/about.html" %(linkfade_about)s>About</a></li>
				<li id="blogLink"><a href="http://woarl.com/blog/" %(linkfade_blog)s>Blog</a></li>
				<li id="guideLink"><a href="../pages/general/starting.html" %(linkfade_guide)s>Guide</a></li>
				<li id="homeLink"><a href="../" %(linkfade_home)s>Home</a></li>
			</ul>
			<div id="infoLinkWrapper">
				<div id="homeLinkInfo">&nbsp;</div>
				<div id="guideLinkInfo">&nbsp;</div>
				<div id="blogLinkInfo">&nbsp;</div>
				<div id="aboutLinkInfo">&nbsp;</div>
				<div id="contactLinkInfo">&nbsp;</div>
				<div id="loginLinkInfo">&nbsp;</div>
				<div id="registerLinkInfo">&nbsp;</div>
			</div>
		</div>
		<!-- 852px width normally, 20px padding -->
		<div class="contentWide" style="padding: 0px; width: 892px;">
		""" % {
			"name":			the_team.name,
			"javascript":			javascript(the_team),
			"linkfade_register":	linkfade('register'),
			"linkfade_login":		linkfade('login'),
			"linkfade_contact":		linkfade('contact'),
			"linkfade_about":		linkfade('about'),
			"linkfade_blog":		linkfade('blog'),
			"linkfade_guide":		linkfade('guide'),
			"linkfade_home":		linkfade('home'),
		}


def footers(the_team):
	"""docstring for footers"""
	return """<br />Last updated: %s</div><!-- content -->
			<div class="clear">
				&nbsp;
			</div>
			</div><!-- page -->
			
			<div class="footer">
			<br />
			Game copyright <a href="http://woarl.com/blog">Teifion Jordan</a>, all rights reserved.<br />
			If you want to use these game rules for your own game, please contact Teifion, all player written stories and cultures are property of their authors
			</div><!-- footer -->
			%s
		</body>
	</html>""" % (time.strftime("%H:%M %A %d %B", time.localtime()),
		common.data['analytics'])


def javascript(the_team):
	return """
	<script type="text/javascript" charset="utf-8">
		function hide_all_sections ()
		{
			$('#evolutions_div').hide();
			$('#resources_div').hide();
			$('#deities_div').hide();
			$('#units_div').hide();
			$('#armies_div').hide();
			$('#operatives_div').hide();
			$('#techs_div').hide();
			$('#spells_div').hide();
			$('#chosen_div').hide();
			$('#cities_div').hide();
			$('#diplomacy_div').hide();
			
			$('#evolutions_tab').removeClass('ti_tab_selected');
			$('#resources_tab').removeClass('ti_tab_selected');
			$('#deities_tab').removeClass('ti_tab_selected');
			$('#units_tab').removeClass('ti_tab_selected');
			$('#armies_tab').removeClass('ti_tab_selected');
			$('#operatives_tab').removeClass('ti_tab_selected');
			$('#techs_tab').removeClass('ti_tab_selected');
			$('#spells_tab').removeClass('ti_tab_selected');
			$('#chosen_tab').removeClass('ti_tab_selected');
			$('#cities_tab').removeClass('ti_tab_selected');
			$('#diplomacy_tab').removeClass('ti_tab_selected');
		}
		
		function switch_to_evolutions ()
		{
			hide_all_sections();
			$('#evolutions_div').show();
			$('#evolutions_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_resources ()
		{
			hide_all_sections();
			$('#resources_div').show();
			$('#resources_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_deities ()
		{
			hide_all_sections();
			$('#deities_div').show();
			$('#deities_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_units ()
		{
			hide_all_sections();
			$('#units_div').show();
			$('#units_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_armies ()
		{
			hide_all_sections();
			$('#armies_div').show();
			$('#armies_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_operatives ()
		{
			hide_all_sections();
			$('#operatives_div').show();
			$('#operatives_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_techs ()
		{
			hide_all_sections();
			$('#techs_div').show();
			$('#techs_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_spells ()
		{
			hide_all_sections();
			$('#spells_div').show();
			$('#spells_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_chosen ()
		{
			hide_all_sections();
			$('#chosen_div').show();
			$('#chosen_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_cities ()
		{
			hide_all_sections();
			$('#cities_div').show();
			$('#cities_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_diplomacy ()
		{
			hide_all_sections();
			$('#diplomacy_div').show();
			$('#diplomacy_tab').addClass('ti_tab_selected');
		}
	</script>
	"""


def tabs(cursor, the_team):
	# reports_dict = spy_report_q.get_reports_from_team(cursor, the_team.id, common.current_turn()-3)
	reports_dict = {}
	
	report_count = 0
	for r, the_report in reports_dict.items():
		if the_report.turn == common.current_turn():
			report_count += 1
	
	if report_count > 0:
		report_count_string = " (%d)" % report_count
	else:
		report_count_string = ""
	
	# 892px to play with
	return """
	<div id="tabs" style="border-bottom: 3px solid #EEE; height: 30px;">
		<div class="ti_tab" id="evolutions_tab" onclick="switch_to_evolutions();">
			Evolutions
		</div>
		<div class="ti_tab" id="resources_tab" onclick="switch_to_resources();">
			Resources
		</div>
		<div class="ti_tab" id="deities_tab" onclick="switch_to_deities();">
			Deities
		</div>
		<div class="ti_tab" id="units_tab" onclick="switch_to_units();">
			Units
		</div>
		<div class="ti_tab" id="armies_tab" onclick="switch_to_armies();">
			Armies
		</div>
		<div class="ti_tab" id="operatives_tab" onclick="switch_to_operatives();">
			Covert%(covert_count)s
		</div>
		<div class="ti_tab" id="techs_tab" onclick="switch_to_techs();">
			Techs
		</div>
		<div class="ti_tab" id="spells_tab" onclick="switch_to_spells();">
			Spells
		</div>
		<div class="ti_tab" id="chosen_tab" onclick="switch_to_chosen();">
			Chosen
		</div>
		<div class="ti_tab" id="cities_tab" onclick="switch_to_cities();">
			Cities
		</div>
		<div class="ti_tab" id="diplomacy_tab" onclick="switch_to_diplomacy();" style="width:82px;">
			Diplomacy
		</div>
	</div>
	""" % {
		"covert_count": report_count_string
	}


def evolutions(cursor, the_world, the_team):
	output = []
	
	evolution_dict = the_world.evolutions()
	the_team.get_evolutions(cursor)
	
	output.append('<div class="ti_section" id="evolutions_div">')
	
	for evolution_id, evo_level in the_team.evolutions.items():
		the_evo = evolution_dict[evolution_id]
		
		if evo_level == 0:
			continue
		
		if the_evo.max_level == 1 and evo_level == 1:
			output.append("""<strong>%(evo_name)s [%(cost)s]</strong><br />
			%(description)s<br /><br />""" % {
				"evo_name":	the_evo.name,
				"cost":		the_evo.cost_per_level * the_team.evolutions[evolution_id],
				"description":	the_evo.description,
			})
		else:
			output.append("""<strong>%(level)sx %(evo_name)s [%(cost)s]</strong><br />
			%(description)s<br /><br />""" % {
				"level":	the_team.evolutions[evolution_id],
				"evo_name":	the_evo.name,
				"cost":		the_evo.cost_per_level * the_team.evolutions[evolution_id],
				"description":	the_evo.description,
			})
	
	output.append('</div>')
	return "".join(output)

def resources(cursor, the_world, the_team):
	output = []
	
	# We need to do this to predict them correctly
	# TODO Confirm that this does/does not need to be force_requery
	team_resources = the_team.get_resources(cursor, force_requery=False)
	
	produced_resources, new_resources = team_rules.produce_resources(cursor, the_team, the_world, force_requery=False)
	
	# Now we repeat this to display the current amounts correctly
	the_team.resources = team_resources
	
	output.append('''<div class="ti_section" id="resources_div">
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Resource</th>
			<th>Currently availiable</th>
			<th>Production</th>
			<th>Upkeep</th>
			<th>Predicted to be availiable</th>
		</tr>''')
	
	count = -1
	for res_id, the_res in enumerate(resource_list.data_list):
		if res_id not in the_team.resources.value:
			the_team.resources.value[res_id] = 0
		
		# If all of them are 0 then there's no need to show it
		if the_team.resources.value[res_id] == 0:
			if produced_resources.get(res_id) == 0:
				if new_resources.get(res_id) == 0:
					continue
		
		if the_res.name == "Materials":
			upkeep_amount = int(team_f.get_upkeep(the_team, the_world))
			future_amount = int(new_resources.value[res_id]-int(upkeep_amount))
			
		elif the_res.name == "Food":
			upkeep_amount = team_rules.resource_needed(cursor, "Food", the_team)
			upkeep_amount = round(upkeep_amount, 2)
			future_amount = int(new_resources.value[res_id]-int(upkeep_amount))
			
			upkeep_amount = int(upkeep_amount)
		else:
			upkeep_amount = ""
			future_amount = int(new_resources.value[res_id])
		
		count += 1
		output.append('''
		<tr class="row%(count)s">
			<td>%(resource_name)s</td>
			<td>%(current_amount)s</td>
			<td>%(produce_amount)s</td>
			<td>%(upkeep_amount)s</td>
			<td>%(future_amount)s</td>
		</tr>
		''' % {
			"count":			count%2,
			"resource_name":	the_res.name,
			"current_amount":	int(the_team.resources.value.get(res_id, 0)),
			"produce_amount":	int(produced_resources.value.get(res_id, 0)),
			"upkeep_amount":	upkeep_amount,
			"future_amount":	future_amount,
		})
	
	output.append('</table></div>')
	return "".join(output)

def deities(cursor, the_world, the_team):
	output = []
	
	# Possible time saver
	the_team.get_deities(cursor)
	if len(the_team.deities.items()) == 0:
		return "".join('<div class="ti_section" id="deities_div"></div>')
	
	deity_dict		= the_world.deities()
	city_dict		= the_world.cities()
	servant_dict_c	= the_world.servants()
	deity_favour_info = {}
	
	# Get favour
	for deity_id, deity_favour in the_team.deities.items():
		favour_result = deity_rules.calculate_favour(the_world, the_team, deity_id)
		the_team.deities[deity_id] = favour_result[0]
		deity_favour_info[deity_id] = favour_result[1]
	
	# Get temple points
	if the_team.temple_points < 0:
		the_team.temple_points = 0
		for city_id, the_city in city_dict.items():
			if the_city.team != the_team.id: continue
			if the_city.population < 15000: continue
			
			multiplier = int(math.floor(the_city.population / 15000.0))
			
			# print "%s: %s * %s<br />" % (the_city.name, the_city.get_temple_points(), multiplier)
			the_team.temple_points += (the_city.get_temple_points(cursor) * multiplier)
	
	output.append('<div class="ti_section" id="deities_div">')
	output.append("<span class='stitle'>Favour breakdown</span><br /><br />")
	
	for deity_id, deity_favour in the_team.deities.items():
		output.append("""<strong>%(name)s</strong> &nbsp; %(deity_favour)s favour
		<br />%(deity_favour_info)s
		<br /><br />""" % {
			'name':			deity_dict[deity_id].name,
			'deity_favour':			deity_favour,
			'deity_favour_info':	deity_favour_info[deity_id]
		})
	
	# Servants
	output.append("""<br /><br /><span class="stitle">Servants</span>
	&nbsp;&nbsp;&nbsp;
	Temple points: %s
	<br /><br />""" % the_team.temple_points)
	for deity_id, deity_favour in the_team.deities.items():
		for servant_id, the_servant in servant_dict_c.items():
			if the_servant.deity != deity_id: continue
			
			# Favour
			if deity_favour < the_servant.favour_needed: continue
			
			# Temple points
			if the_team.temple_points < the_servant.temple_points: continue
			
			# Monotheism
			if len(the_team.deities.keys()) > 1 and the_servant.monotheistic: continue
			
			# Print servant
			output.append("""<div class="servant_block">
				<strong>%(name)s</strong>
				&nbsp;&nbsp;&nbsp;
				Summon cost: %(cost)s
				&nbsp;&nbsp;&nbsp;
				Summon amount: %(amount)s<br />
				%(description)s
			</div>
			""" % {
				"name":			the_servant.name,
				"description":	the_servant.description,
				
				"cost":			the_servant.summon_cost,
				"amount":		the_servant.summon_amount,
			})
	
	output.append('</div>')
	return "".join(output)

def units(cursor, the_world, the_team):
	unit_dict = the_world.units_from_team(the_team.id)
	special_unit_dict = the_world.units_from_team(0)
	monster_dict = the_world.monsters()
	
	the_team.get_units(cursor)
	
	output = []
	output.append('''<div class="ti_section" id="units_div">
	<table border="0" cellspacing="0" cellpadding="5" style="width:100%%;">
		<tr class="row2">
			<th>Amount</th>
			<th>Unit name</th>
			<th>Cost</th>
			<th>Equipment</th>
		</tr>''')
	
	unit_row = 	'''
		<tr class="row{count}">
			<td>{amount}</td>
			<td>{name}</td>
			<td>{cost}</td>
			<td>{equipment}</td>
		</tr>
		'''
	
	count = -1
	
	# Team units
	for u, the_unit in unit_dict.items():
		count += 1
		output.append(unit_row.format(
			count =		count%2,
			amount =	common.number_format(the_team.units.get(u, 0)),
			name =		the_unit.name,
			cost =		unit_rules.print_unit_cost(the_unit, cursor=cursor, the_world=the_world),
			equipment =	the_unit.equipment_string,
		))
	
	# Special units
	for u, the_unit in special_unit_dict.items():
		count += 1
		output.append(unit_row.format(
			count =		count%2,
			amount =	common.number_format(the_team.units.get(u, 0)),
			name =		the_unit.name,
			cost =		unit_rules.print_unit_cost(the_unit, cursor=cursor, the_world=the_world),
			equipment =	the_unit.equipment_string,
		))
	
	output.append('</table></div>')
	return "".join(output)

def armies(cursor, the_world, the_team):
	output = []
	unit_dict = the_world.units()#(the_team.id)
	army_dict = the_world.armies_from_team(the_team.id)
	city_dict = the_world.cities()
	monster_dict = the_world.monsters()
	
	output.append('''<div class="ti_section" id="armies_div">
	<table border="0" cellspacing="0" cellpadding="5" style="width:100%%;">
		<tr class="row2">
			<th>Army</th>
			<th>Location</th>
			<th>Size</th>
			<th>&nbsp;</th>
		</tr>''')
	
	count = -1
	for a, the_army in army_dict.items():
		count+=1
		
		if the_army.garrison < 1:
			# First lets see if the city is dead...
			
			# Default
			army_location = str((int(the_army.x), int(the_army.y)))
			
			# Now to see if it's near something
			min_dist = 9999
			for c, the_city in city_dict.items():
				if the_city.dead == True: continue
				distance = path_f.pythagoras((the_army.x, the_army.y), (the_city.x, the_city.y))
				
				if distance < 150 and distance < min_dist:
					army_location = "%s, near %s" % (str((int(the_army.x), int(the_army.y))), the_city.name)
					min_dist = distance
				
		else:
			if the_army.garrison not in city_dict: continue# Skip dead cities
			if city_dict[the_army.garrison].dead == True: continue
			army_location = "Garrison"
		
		output.append("""
		<tr class="row%(row)s">
			<td>%(name)s</td>
			<td>%(army_location)s</td>
			<td>%(army_size)s</td>
			<td style="padding: 0px;">
				<a href="#" id="army_%(army_id)s_squad_show" onclick="$('#army_%(army_id)s_squad_show').hide(); $('#army_%(army_id)s_squads').show(); $('#army_%(army_id)s_squad_hide').show(); return false;" class="block_link">Show squads</a>
				<a href="#" id="army_%(army_id)s_squad_hide" onclick="$('#army_%(army_id)s_squad_show').show(); $('#army_%(army_id)s_squads').hide(); $('#army_%(army_id)s_squad_hide').hide(); return false;" class="block_link" style="display: none;">Hide squads</a>
			</td>
		</tr>""" % {
				"row":				count%2,
				"name":		the_army.name,
				"army_id":			the_army.id,
				
				"army_location":	army_location,
				"army_size":		the_army.get_size(cursor),
			})
		
		# Army squads
		output.append("<tr id='army_%s_squads' style='display: none;'><td style='padding: 5px 20px 10px;' colspan='4'>" % the_army.id)
		
		output.append("""
			<table border="0" cellspacing="0" cellpadding="5" style="width:100%%;">
				<tr class="row2">
					<th>Squad</th>
					<th>Type</th>
					<th>Size</th>
					<!--<th>Experience</th>-->
				</tr>""")
		
		count2 = -1
		# Squads
		for s, the_squad in the_army.squads.items():
			if the_squad.unit not in unit_dict:
				continue
			
			count2 += 1
			output.append("""
			<tr class="row%(count)s">
				<td>%(name)s</td>
				<td>%(squad_type)s</td>
				<td>%(squad_size)s</td>
			</tr>""" % {
				"count":		count2%2,
				"name":	the_squad.name,
				"squad_type":	unit_dict[the_squad.unit].name,
				"squad_size":	the_squad.amount,
				"squad_id":		the_squad.id
			})
		
		# Monsters
		for monster_id, amount in the_army.monsters.items():
			if amount < 1: continue
			the_monster = monster_dict[monster_id]
			
			count2 += 1
			output.append("""
			<tr class="row{count}">
				<td>{name}</td>
				<td><em>Monster</em></td>
				<td>{amount}</td>
			</tr>""".format(
				count	= count2 % 2,
				name	= the_monster.name,
				amount	= amount,
			))
		
		output.append("</table>")
	
	output.append('</table></div>')
	return "".join(output)

def operatives(cursor, the_world, the_team):
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	operatives_dict	= the_world.operatives_from_team(the_team.id)
	
	# reports_dict	= spy_report_q.get_reports_from_team(cursor, the_team.id, common.current_turn()-3)
	reports_dict = {}
	
	if len(operatives_dict) <= 0 and len(reports_dict) <= 0:
		return '<div class="ti_section" id="operatives_div">You have no operatives and no spy reports</div>'
	
	# Location stuff
	team_location = {}
	for o, the_op in operatives_dict.items():
		if the_op.died > 0: continue
		
		o_team = city_dict[the_op.city].team
		
		if o_team not in team_location:
			team_location[o_team] = []
		
		team_location[o_team].append(o)
	
	# Overview numbers
	city_set = set()
	city_count = {}
	operative_count = 0
	recent_deaths = 0
	for operative_id, the_operative in operatives_dict.items():
		if the_operative.died > 0:
			if common.current_turn() - the_operative.died < 3:
				recent_deaths += 1
			continue
		
		city_set.add(the_operative.city)
		
		if the_operative.city not in city_count:
			city_count[the_operative.city] = 0
		
		city_count[the_operative.city] += 1
		operative_count += 1
	
	# Starting the output
	output = []
	output.append('<div class="ti_section" id="operatives_div">')
	
	output.append("""
	You have %s spies spread across %s cities. You have lost %s spies in the last 3 turns.<br /><br />""" % (operative_count, len(city_set), recent_deaths))
	
	spies_out		= []
	couterspies_out	= []
	for city_id, op_count in city_count.items():
		if city_id < 1: continue
		the_city = city_dict[city_id]
		
		if the_city.team == the_team.id:
			couterspies_out.append("""<li>%s at %s</li>""" % (op_count, city_dict[city_id].name))
		else:
			spies_out.append("""<li>%s at %s</li>""" % (op_count, city_dict[city_id].name))
	
	
	# Caught ops
	caught_ops = operative_q.operatives_caught_in_cities(
		cursor,
		the_world.cities_from_team(the_team.id),
		since=common.current_turn()-3,
	)
	
	if len(caught_ops) == 0:
		output.append("<strong>You have caught no spies in the last 3 years</strong>")
	else:
		output.append("<strong>You caught the following spies in the last 3 years:</strong>")
		
		for k, the_op in caught_ops.items():
			output.append("<br />{name} (found in {city}) from {team}, caught in turn {turn}".format(
				name=the_op.name,
				city=city_dict[the_op.city].name,
				team=team_dict[the_op.team].name,
				turn=the_op.died,
			))
		
	output.append("<br /><br />")
		
		# <table border="0" cellspacing="0" cellpadding="5">
		# 	<tr>
		# 		<th>Counterspies</th>
		# 		<th width="100">&nbsp;</th>
		# 		<th>Spies</th>
		# 	</tr>
		# 	<tr>
		# 		<td><ul>%(counterspies)s</ul></td>
		# 		<td width="100">&nbsp;</td>
		# 		<td><ul>%(spies)s</ul></td>
		# 	</tr>
		# </table><br />
		# """ % {
		# 	"counterspies":	"".join(couterspies_out),
		# 	"spies":		"".join(spies_out),
		# })
		
	
	# Operatives overview
	if len(operatives_dict) <= 0:
		output.append("You have no operatives")
	else:
		output.append("""<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Counterspies</th>
				<th width="100">&nbsp;</th>
				<th>Spies</th>
			</tr>
			<tr>
				<td><ul>%(counterspies)s</ul></td>
				<td width="100">&nbsp;</td>
				<td><ul>%(spies)s</ul></td>
			</tr>
		</table><br />
		""" % {
			"counterspies":	"".join(couterspies_out),
			"spies":		"".join(spies_out),
		})
	
	# Op list
	if len(operatives_dict) > 0:
		output.append("""
		<div style="" id="op_table_link">
			<a href="#" onclick="$('#op_table_link').hide();$('#op_table').show();return false;" class="block_link">Show all operatives</a>
		</div>
		<table border="0" cellspacing="0" cellpadding="5" style="width: 100%; display:none;" id="op_table">
			<tr class="row2">
				<th>ID</th>
				<th>Size</th>
				
				<th>Stealth</th>
				<th>Observation</th>
				<th>Integration</th>
				<th>Sedition</th>
				<th>Sabotage</th>
				<th>Assassination</th>
				
				<th>Location</th>
				<th>Arrival</th>
			</tr>""")
	
		count = -1
	
		for city_team, op_list in team_location.items():
			for operative_id in op_list:
				the_operative = operatives_dict[operative_id]
			
				count += 1
			
				output.append("""
				<tr class="row{row}" id="op_{operative_id}">
					<td>{name}</td>
					<td>{size}</td>
					
					<td>{stealth}</td>
					<td>{observation}</td>
					<td>{integration}</td>
					<td>{sedition}</td>
					<td>{sabotage}</td>
					<td>{assassination}</td>
					
					<td>{city} ({city_team})</td>
					<td>{arrival}</td>
				</tr>
				""".format(
						row = (count % 2),
						
						operative_id	= operative_id,
						name		= the_operative.name,
						size			= the_operative.size,
						
						arrival			= the_operative.arrival,
						stealth			= the_operative.stealth,
						observation		= the_operative.observation,
						integration		= the_operative.integration,
						sedition		= the_operative.sedition,
						sabotage		= the_operative.sabotage,
						assassination	= the_operative.assassination,
						
						city		= city_dict[the_operative.city].name,
						city_team	= team_dict[city_team].name,
			))
	
		output.append('</table>')
	output.append('</div>')
	return "".join(output)

def techs(cursor, the_world, the_team):
	output = []
	
	tech_dict = the_world.techs()
	the_team.get_techs(cursor)
	
	output.append('<div class="ti_section" id="techs_div">')
	
	output.append("""
	<table style="width: 100%;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>#</th>
		<th>&nbsp;</th>
	</tr>""")
	
	max_tech_level = 1
	skip_tech_list = {}
	table_dict = {}
	tech_points_spent = 0
	
	for tech_id, tech_level in the_team.tech_levels.items():
		if tech_level == 0 and the_team.tech_points[tech_id] < 1:
			continue
		
		if tech_level not in table_dict:
			table_dict[tech_level] = []
		
		max_tech_level = max(max_tech_level, tech_level)
		
		# Total that they've spent
		tech_points_spent += tech_rules.cost_to_get_to_level(cursor, tech_dict[tech_id], tech_level).get("Tech points")
		tech_points_spent += the_team.tech_points[tech_id]
		
		current_tech = tech_dict.get(tech_id, 0)
		
		if the_team.tech_points[tech_id] > 0:
			table_dict[tech_level].append("""%(name)s %(points)s/%(points_to_next)s""" % {
				"name":				current_tech.name,
				"points":			the_team.tech_points[tech_id],
				"points_to_next":	tech_rules.cost_for_next_level(cursor, tech_dict[tech_id], tech_level).get("Tech points"),
			})
		else:
			table_dict[tech_level].append(current_tech.name)
	
	for i in range(0, max_tech_level+1):
		if i not in table_dict:
			table_dict[i] = []
		
		if table_dict[i] == [] and i > 10:
			continue
		
		output.append("""
		<tr class="row%(row_count)s">
			<td width="15">%(i)s</td>
			<td style="padding: 5px 2px 0 2px;">%(techs)s</td>
		</tr>
		""" % {
			"i":			i,
			"row_count":	(i%2),
			"techs":		", ".join(table_dict[i]),
		})
	
	output.append('</table></div>')
	return "".join(output)

def spells(cursor, the_world, the_team):
	output = []
	
	spell_dict = the_world.spells()
	the_team.get_spells(cursor)
	
	output.append('<div class="ti_section" id="spells_div">')
	
	output.append("""
	<table style="width: 100%;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>#</th>
		<th>&nbsp;</th>
	</tr>""")
	
	max_spell_level = 1
	skip_spell_list = {}
	table_dict = {}
	spell_points_spent = 0
	
	for spell_id, spell_level in the_team.spell_levels.items():
		if spell_level == 0 and the_team.spell_points[spell_id] < 1:
			continue
		
		if spell_level not in table_dict:
			table_dict[spell_level] = []
		
		max_spell_level = max(max_spell_level, spell_level)
		
		# Total that they've spent
		spell_points_spent += spell_rules.cost_to_get_to_level(cursor, spell_dict[spell_id], spell_level).get("spell points")
		spell_points_spent += the_team.spell_points[spell_id]
		
		current_spell = spell_dict[spell_id]
		
		if the_team.spell_points[spell_id] > 0:
			table_dict[spell_level].append("""%(name)s (%(points)s/%(points_to_next)s)""" % {
				"name":				current_spell.name,
				"points":			the_team.spell_points[spell_id],
				"points_to_next":	spell_rules.cost_for_next_level(cursor, spell_dict[spell_level], spell_level, True).get("Spell points"),
			})
		else:
			table_dict[spell_level].append(current_spell.name,)
	
	for i in range(0, max_spell_level+1):
		if i not in table_dict:
			table_dict[i] = []
		
		if table_dict[i] == [] and i > 10:
			continue
		
		output.append("""
		<tr class="row%(row_count)s">
			<td width="15">%(i)s</td>
			<td style="padding: 5px 2px 0 2px;">%(spells)s</td>
		</tr>
		""" % {
			"i":			i,
			"row_count":	(i%2),
			"spells":		", ".join(table_dict[i]),
		})
	
	output.append('</table></div>')
	return "".join(output)

def chosen(cursor, the_world, the_team):
	player_dict = the_world.players_from_team(the_team.id)
	powers_dict = the_world.powers()
	
	team_powers_list = []
	team_powers_list_names = []
	
	output = []
	output.append("""<div class="ti_section" id="chosen_div">
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Player name</th>
			<th>Daemonic status</th>
			<th>Powers</th>
		</tr>""")
	
	count = -1
	if len(player_dict) > 0:
		for player_id, the_player in player_dict.items():
			
			player_powers = []
			for p in the_player.powers:
				player_powers.append(powers_dict[p].name)
				
				# Most powers have dupes, we track names to only list each "power" once
				# even if we have multiple copies
				if powers_dict[p].name not in team_powers_list_names:
					team_powers_list_names.append(powers_dict[p].name)
					team_powers_list.append(p)
			
			count += 1
			
			player_powers_list = ""
			
			if the_player.progression < 1:
				daemonic_status = "None"
			else:
				if the_player.daemon_type < 1:
					daemonic_status = player.progressions[the_player.progression]
				else:
					daemonic_status = "%s, %s" % (player.progressions[the_player.progression], player.daemon_types[the_player.daemon_type])
			
			output.append("""
			<tr class="row%(row)d">
				<td>%(name)s</td>
				<td>%(daemon)s</td>
				<td>%(powers)s</td>
			</tr>
			""" % {	'row': (count % 2),
					'name':	the_player.name,
					"powers":		", ".join(player_powers),
					
					"daemon":		daemonic_status,
				})
	
	output.append('</table>')
	
	# Powers
	if len(team_powers_list) > 0:
		output.append('<br /><br /><span class="stitle">First one powers</span><br />')
		
		for p in team_powers_list:
			output.append("""&nbsp;&nbsp;&nbsp;&nbsp;<strong>%(name)s</strong> (%(type)s)<br />%(description)s<br /><br />""" % {
				"name":			powers_dict[p].name,
				"type":			power.power_types[powers_dict[p].type],
				"description":	powers_dict[p].description,
			})
	
	# Artefacts
	city_dict = the_world.cities()
	artefact_dict = the_world.artefacts()
	
	artefacts_list = []
	for artefact_id, the_artefact in artefact_dict.items():
		if the_artefact.city in city_dict:
			if city_dict[the_artefact.city].team == the_team.id:
				artefacts_list.append(artefact_id)
	
	if len(artefacts_list) > 0:
		output.append('<br /><br /><span class="stitle">First one artefacts</span><br />')
		
		for a in artefacts_list:
			output.append("""&nbsp;&nbsp;&nbsp;&nbsp;<strong>%(name)s</strong> - Located in %(city_name)s<br />%(description)s<br /><br />""" % {
				"name":				artefact_dict[a].name,
				"city_name":		city_dict[artefact_dict[a].city].name,
				"description":		artefact_dict[a].description,
			})
	
	# Wonders
	wonder_dict = the_world.wonders()
	city_dict = the_world.cities()
	
	wonder_list = []
	for wonder_id, the_wonder in wonder_dict.items():
		if city_dict[the_wonder.city].team == the_team.id and city_dict[the_wonder.city].dead < 1:
			if the_wonder.team == the_team.id:
				wonder_list.append(wonder_id)
	
	# print(wonder_list)
	# print("<br />")
	# print(the_wonder.name, the_wonder.city)
	# exit()
	
	if len(wonder_list) > 0:
		output.append('<br /><br /><span class="stitle">Wonders</span><br />')
		
		for w in wonder_list:
			the_wonder = wonder_dict[w]
			
			output.append("""&nbsp;&nbsp;&nbsp;&nbsp;<strong>%(name)s</strong> - Located in %(city_name)s, progress: %(points)d/%(needed_points)d<br />%(description)s<br /><br />""" % {
				"name":				the_wonder.name,
				"city_name":		city_dict[the_wonder.city].name,
				"description":		the_wonder.description,
				"points":			the_wonder.completion,
				"needed_points":	the_wonder.point_cost,
			})
	
	output.append('</div>')
	return "".join(output)

def cities(cursor, the_world, the_team):
	city_dict		= the_world.cities_from_team(the_team.id)
	building_dict	= the_world.buildings()
	
	output = []
	output.append("""<div class="ti_section" id="cities_div">
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>City name</th>
			<th>Location</th>
			<th>Port</th>
			<!--<th>Secret</th>-->
			<th>Nomadic</th>
			<th>Artefacts</th>
			<th>Population</th>
			<th>Slaves</th>
			<th>Production</th>
			<!--<th>Wealth</th>-->
			<th>Happiness</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	if len(city_dict) > 0:
		for city_id, the_city in city_dict.items():
			if the_city.dead > 0: continue
			count += 1
			
			# sad_rules.produce_wealth(the_world, the_city)
			
			artefacts = the_city.artefacts
			if len(artefacts) > 0:
				artefacts = len(artefacts)
			else:
				artefacts = ""
			
			# Growth
			growth_rate, growth_constant = city_rules.city_growth_rate(cursor, the_team, the_city, the_world)
			new_population = int((the_city.population * growth_rate) + growth_constant)
			growth_rate = round((growth_rate-1)*100,1)
			
			# Formatting
			if growth_rate == int(growth_rate): growth_rate = int(growth_rate)
			
			# Happiness
			happiness = city.happiness_str(the_city.happiness)
			
			if happiness == "Rebellious":
				happiness = '<span style="font-weight:bold;color:#A00;">Rebellious</span>'
			
			if happiness == "Utopian":
				happiness = '<span style="font-weight:bold;color:#0A0;">Utopian</span>'
			
			output.append("""
			<tr class="row%(row)d" id="%(city_id)d">
				<td>%(name)s</td>
				
				<td>%(terrain)s &nbsp; %(x)s, %(y)s</td>
				
				<td style="text-align: center;">%(port)s</td>
				<!--<td style="text-align: center;">%(secret)s</td>-->
				<td style="text-align: center;">%(nomadic)s</td>
				<td style="text-align: center;">%(artefact)s</td>
				
				<td>%(population)sk, &nbsp;&nbsp;
				%(growth_rate)s%%</td>
				<td>%(slaves)s</td>
				<td>%(production)s + %(wealth)s = %(economy)s</td>
				<!--<td>%(wealth)s</td>-->
				<td>%(happiness)s</td>
				
				<td style="padding: 0px;">
					<a href="#" id="city_%(city_id)s_building_show" onclick="$('#city_%(city_id)s_building_show').hide(); $('#city_%(city_id)s_buildings').show(); $('#city_%(city_id)s_building_hide').show(); return false;" class="block_link">Show buildings</a>
					<a href="#" id="city_%(city_id)s_building_hide" onclick="$('#city_%(city_id)s_building_show').show(); $('#city_%(city_id)s_buildings').hide(); $('#city_%(city_id)s_building_hide').hide(); return false;" class="block_link" style="display: none;">Hide buildings</a>
				</td>
			</tr>
			""" % {	'row': (count % 2),
					
					'city_id': the_city.id,
					'name': the_city.name,
					'x': the_city.x,
					'y': the_city.y,
					
					"terrain":	map_data.terrain[mapper_q.get_terrain(cursor, the_city.x, the_city.y)].title(),
					'port':		common.bstr(the_city.port),
					'secret':	common.bstr(the_city.secret),
					'artefact':	artefacts,
					'nomadic':	common.bstr(the_city.nomadic),
					
					'population':		round(the_city.population/1000.0,1),
					'new_population':	round(new_population/1000.0,1),
					"growth_rate":		growth_rate,
					"wealth":			int(the_city.wealth),
					'slaves':			the_city.slaves,
					
					"production":		int(team_rules.Materials(cursor, the_team, the_world=the_world, one_city_id=city_id)),
					"happiness":		happiness,
					
					"economy":			int(the_city.wealth + team_rules.Materials(cursor, the_team, the_world=the_world, one_city_id=city_id)),
				})
			
			# City buildings
			output.append("<tr id='city_%s_buildings' style='display: none;'><td style='padding: 5px 20px 10px;' colspan='9'>" % the_city.id)
			
			output.append("""
				<table border="0" cellspacing="0" cellpadding="5" style="width:100%%;">
					<tr class="row2">
						<th>Building</th>
						<th>Progress</th>
					</tr>""")
			
			count2 = -1
			buildings_progress, buildings_amount = the_city.get_buildings(cursor)
			
			for b, the_building in building_dict.items():
				if b not in buildings_progress and b not in buildings_amount:
					continue
				
				if buildings_progress.get(b, 0) > 0:
					percentage = float(buildings_progress.get(b, 0))/float(the_building.build_time)
					percentage = int(round(percentage*100))
				
					
				if buildings_amount.get(b, 0) > 0 and buildings_progress.get(b, 0) > 0:
					progress = "%s completed and 1 in progress at %s%%" % (buildings_amount[b], percentage)
				
				elif buildings_amount.get(b, 0) > 0 and buildings_progress.get(b, 0) == 0:
					progress = "%s completed" % (buildings_amount[b])
				
				elif buildings_amount.get(b, 0) == 0 and buildings_progress.get(b, 0) > 0:
					progress = "In progress at %s%%" % (percentage)
				
				else:
					# It's in both but at 0 and 0 so will get removed with the check
					continue
				
				count2 += 1
				output.append("""
				<tr class="row%(count)s">
					<td>%(building_name)s</td>
					<td>%(progress)s</td>
				</tr>""" % {
					"count":			count2%2,
					"building_name":	the_building.name,
					"progress":			progress,
				})
			
			if artefacts != "":
				output.append("<tr><td colspan='2'>The artefact information is located in the <a href='#' onclick='switch_to_chosen();'>Chosen tab</a></td></tr>")
			
			output.append("</table>")
	
	output.append('</table></div>')
	return "".join(output)

def diplomacy(cursor, the_world, the_team):
	team_dict		= the_world.teams()
	relations		= the_world.relations()
	border_history	= the_world.border_history()
	
	output = []
	output.append('<div class="ti_section" id="diplomacy_div">')
	
	allied_list, open_list, segregated_list, closed_list, war_list = [], [], [], [], []
	for ot, other_team in team_dict.items():
		if not other_team.active: continue
		if other_team.hidden: continue
		
		# Our position to them?
		# our_status = relations.get(the_team.id, {}).get(ot, {}).get('border', the_team.default_borders)
		our_status = the_world.get_border(the_team.id, ot)
		
		# Them to us?
		# their_status = relations.get(ot, {}).get(the_team.id, {}).get('border', team_dict[ot].default_borders)
		their_status = the_world.get_border(ot, the_team.id)
		
		# Get previous status
		previous_status = border_history.get(ot, {})
		if the_team.id in previous_status:
			previous_status = previous_status[the_team.id]
		else:
			previous_status = previous_status.get(-1, team.default_border_state)
		
		# Has it changed?
		if previous_status != their_status:
			their_status_str = "<span style='background-color:#EEF;border:1px dotted #F00;'>%s, used to be %s</span>" % (team.border_states[their_status], team.border_states[previous_status])
		else:
			their_status_str = "<span style='background-color:#FFF;border:1px dotted #FFF;'>%s</span>" % team.border_states[their_status]
		
		if our_status == team.border_states.index("Allied"):
			allied_list.append("%s (%s)" % (team_dict[ot].name, their_status_str))
		elif our_status == team.border_states.index("Open"):
			open_list.append("%s (%s)" % (team_dict[ot].name, their_status_str))
		elif our_status == team.border_states.index("Segregated"):
			segregated_list.append("%s (%s)" % (team_dict[ot].name, their_status_str))
		elif our_status == team.border_states.index("Closed"):
			closed_list.append("%s (%s)" % (team_dict[ot].name, their_status_str))
		elif our_status == team.border_states.index("At war"):
			war_list.append("%s (%s)" % (team_dict[ot].name, their_status_str))
		else:
			raise Exception("No border state of '%d'. Team with state '%s' towards '%s'" % (our_status, the_team.name, other_team.name))
	
	output.append("""
	The status in brackets is their stance towards you<br />
	<table border="0" cellspacing="0" cellpadding="5" width="100%%;">
		<tr>
			<td>
				<strong>You are allied to</strong><br />
				%s
			</td>
			<td>&nbsp;</td>
			<td>
				<strong>You are open to</strong><br />
				%s
			</td>
			<td>&nbsp;</td>
			<td>
				<strong>You are segregated to</strong><br />
				%s
			</td>
			<td>&nbsp;</td>
			<td>
				<strong>You are closed to</strong><br />
				%s
			</td>
				<td>&nbsp;</td>
			<td>
				<strong>You are at war with</strong><br />
				%s
			</td>
		</tr>
	</table>""" % ("<br />".join(allied_list), "<br />".join(open_list), "<br />".join(segregated_list), "<br />".join(closed_list), "<br />".join(war_list)))
	
	output.append('</div>')
	
	return "".join(output)


def make_ti(cursor, the_world, the_team, return_stats=False):
	the_stats = {}
	
	start_time = time.time()
	
	# Build team stats
	temp = time.time()
	stat_f.build_team_stats(cursor, the_team, the_world)
	
	# Get some properties
	the_team.get_population(cursor)
	the_stats['stats'] = time.time() - temp
	
	output = []
	
	# Tabs
	output.append(tabs(cursor, the_team))
	
	# Evolutions
	temp = time.time()
	output.append(evolutions(cursor, the_world, the_team))
	the_stats['evolutions'] = time.time() - temp
	
	# Deities
	temp = time.time()
	output.append(deities(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_deities();"))
	the_stats['deities'] = time.time() - temp
	
	# Resources and points
	temp = time.time()
	output.append(resources(cursor, the_world, the_team))
	output.append(common.onload("switch_to_resources();"))
	the_stats['resources'] = time.time() - temp
	
	# Cities
	temp = time.time()
	output.append(cities(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_cities();"))
	the_stats['cities'] = time.time() - temp
	
	# Units
	temp = time.time()
	temp = time.time()
	output.append(units(cursor, the_world, the_team))
	the_stats['units'] = time.time() - temp
	
	# Armies
	temp = time.time()
	output.append(armies(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_armies();"))
	the_stats['armies'] = time.time() - temp
	
	# Operatives
	temp = time.time()
	output.append(operatives(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_operatives();"))
	the_stats['operatives'] = time.time() - temp
	
	# Techs
	temp = time.time()
	output.append(techs(cursor, the_world, the_team))
	the_stats['techs'] = time.time() - temp
	
	# Spells
	temp = time.time()
	output.append(spells(cursor, the_world, the_team))
	the_stats['spells'] = time.time() - temp
	
	# Chosen
	temp = time.time()
	output.append(chosen(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_chosen();"))
	the_stats['chosen'] = time.time() - temp
	
	# Diplomacy
	temp = time.time()
	output.append(diplomacy(cursor, the_world, the_team))
	# output.append(common.onload("switch_to_diplomacy();"))
	the_stats['diplomacy'] = time.time() - temp
	
	the_stats['total'] = time.time() - start_time
	
	# output.append(common.onload("switch_to_resources();"))
	
	return "".join(output)


# Quick summary
def bbcode_ti(the_team, md5_name):
	output = []
	
	# Links
	output.append("Last updated: %s<br />" % time.strftime("%H:%M %A %d %B", time.localtime()))
	output.append('''[url=http://woarl.com/ti/%(md)s]Full team info[/url] - 
	[url=http://woarl.com/orders/%(md)s]Orders helper[/url] - 
	[url=http://woarl.com/wh/%(md)s]War helper[/url] - 
	[url=http://woarl.com/tmap/%(md)s]Team map[/url] - 
	[url=http://woarl.com/stats/%(md)s]Team stats[/url] - 
	[url=http://woarl.com/spyrep/%(md)s]Spy reports[/url]
	'''.replace('\n', '') % {'md': "%s.html" % md5_name})
	
	output.append("\n[b]Old spy reports[/b]")
	
	for t in range(common.current_turn()-1, max(common.current_turn()-5, 78), -1):
		output.append('''[url=http://woarl.com/spyrep/%(md)s]Spy report (Turn %(t)d)[/url]''' % {'md': "%s.html" % team_f.team_hash(the_team.name, turn=t), "t": t})
	
	output.append("""\n[b]JSON data[/b]
	[url=http://woarl.com/ti/%(md)s]Team info[/url] - [url=http://woarl.com/map/latest.json]Map[/url] - [url=http://woarl.com/data]Data lists[/url]
	
	Secret key: %(md)s""" % {'md': "%s.json" % md5_name})
	
	return "\n".join(output)


def save_json(team, content):
	from pages import common
	turn = common.current_turn()
	
	return [
		"DELETE FROM team_json_ti WHERE team = %d AND turn = %d" % (team, turn),
		"INSERT INTO team_json_ti (turn, team, content) values (%d, %d, '%s');" % (turn, team, database.escape(content)),
	]