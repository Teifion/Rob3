import database
from pages import common
from classes import stat, res_dict, unit
from functions import team_f, mapper_f
from queries import team_q, city_q, battle_q, stat_q, campaign_q
# from data import stat
# from data import mapper_f
# import data
from rules import team_rules, military_rules

def delete_stat(cursor, team_id, turn):
	query = """DELETE FROM team_stats WHERE team = %d AND turn = %d""" % (team_id, turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))

def insert_stat(cursor, the_stat):
	values = ["'%s'" % database.escape(str(the_stat.__dict__[s])) for s in stat.stat_tuple]
	
	query = """INSERT INTO team_stats (team, turn, {fields})
		values
		({team}, {turn}, {field_values})""".format(
			team =			the_stat.team,
			turn =			the_stat.turn,
			
			fields =		",".join(stat.stat_tuple),
			field_values =	",".join(values),
		)
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))


def check_team_stats(cursor, the_team, the_world=None):
	"""Checks that the team has stats for that turn, if not it makes them"""
	turn = common.current_turn()
	
	query = """SELECT team FROM team_stats WHERE team = %d and turn = %d LIMIT 1;""" % (the_team.id, turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	row = cursor.fetchone()
	if row == None:
		build_team_stats(cursor, the_team, the_world)
	else:
		# All looks groovy
		return

def build_team_stats(cursor, the_team, the_world=None):
	current_turn = common.current_turn()
	
	the_stat = stat.Stat()
	
	#	Primary keys
	#------------------------
	the_stat.turn = current_turn
	the_stat.team = the_team.id
	
	#	Team population and slaves
	#------------------------
	the_stat.population	= the_team.get_population(cursor)
	the_stat.slaves		= the_team.get_slaves(cursor)
	
	#	Resources
	#------------------------
	the_stat.resources	= the_team.get_resources(cursor).as_db_string()
	the_stat.upkeep		= float(team_f.get_upkeep(the_team, the_world))
	the_stat.production = team_rules.produce_resources(cursor, the_team, the_world=the_world)[0].as_db_string()
	
	#	Military stuff
	#------------------------
	the_stat.army_size		= team_q.get_army_size(cursor, the_team.id)
	the_stat.navy_size		= team_q.get_navy_size(cursor, the_team.id)
	the_stat.airforce_size	= team_q.get_airforce_size(cursor, the_team.id)
	
	#	Solo units
	#------------------------
	the_stat.operatives	= the_team.operative_count(cursor)
	the_stat.mages		= team_q.get_mage_count(cursor, the_team.id)
	
	#	Other
	#------------------------
	the_stat.land_controlled	= len(mapper_f.team_influence(the_world, the_team.id))
	
	the_stat.city_count			= len(city_q.get_cities_from_team(cursor, the_team.id))
	the_stat.war_losses			= battle_q.get_team_losses(cursor, the_team.id)
	
	#	Specifics
	#------------------------
	# the_stat.temple_count		= stat_q.get_temple_count(cursor, the_team.id)
	
	# Delete (to allow insert)
	delete_stat(cursor, the_team.id, current_turn)
	
	# Insert
	insert_stat(cursor, the_stat)


javascript = """
		function hide_all_sections ()
		{
			$('#overview_div').hide();
			$('#war_losses_div').hide();
			$('#results_div').hide();
			$('#failures_div').hide();
			$('#upkeep_div').hide();
			
			$('#overview_tab').removeClass('ti_tab_selected');
			$('#war_losses_tab').removeClass('ti_tab_selected');
			$('#results_tab').removeClass('ti_tab_selected');
			$('#failures_tab').removeClass('ti_tab_selected');
			$('#upkeep_tab').removeClass('ti_tab_selected');
		}

		function switch_to (div_name)
		{
			hide_all_sections();
			$('#' + div_name + '_div').show();
			$('#' + div_name + '_tab').addClass('ti_tab_selected');
		}
	"""

def headers(team_name, local):
	return common.headers("%s stats" % team_name, css="body {font-size:0.9em;}", javascript=javascript, local_path=local, js_libs=[])

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
		<div class="ti_tab" id="overview_tab" onclick="switch_to('overview');">
			Overview
		</div>
		<div class="ti_tab" id="war_losses_tab" onclick="switch_to('war_losses');">
			War losses
		</div>
		<div class="ti_tab" id="results_tab" onclick="switch_to('results');">
			All results
		</div>
		<div class="ti_tab" id="failures_tab" onclick="switch_to('failures');">
			Failures
		</div>
		<div class="ti_tab" id="upkeep_tab" onclick="switch_to('upkeep');">
			Upkeep
		</div>
	</div>
	""" % {
		"covert_count": report_count_string
	}



def make_team_stats(cursor, the_world, the_team):
	build_team_stats(cursor, the_team, the_world)
	output = []
	
	# Tabs
	output.append(tabs(cursor, the_team))
	
	# Stat table
	output.append(display_stat_table(cursor, the_team.id))
	
	# War history
	output.append(display_team_losses(cursor, the_world, the_team.id))
	
	# Results
	output.append(display_team_results(cursor, the_world, the_team.id))
	
	# Failures
	output.append(display_team_failures(cursor, the_world, the_team.id))
	
	# Upkeep
	output.append(display_team_upkeep(cursor, the_world, the_team.id))
	
	# Onload
	# output.append(common.onload("switch_to('war_losses');"))
	output.append(common.onload("switch_to('results');"))
	
	return "".join(output)

def display_team_losses(cursor, the_world, team_id):
	from queries import battle_q
	
	empty_div = '<div class="ti_section" id="war_losses_div"></div>'
	the_team = the_world.teams()[team_id]
	
	output = ['<div class="ti_section" id="war_losses_div">']
	
	# team_units		= the_team.get_units()
	squad_dict		= the_world.squads()
	team_dict		= the_world.teams()
	unit_dict		= the_world.units()
	campaign_dict	= the_world.campaigns()
	
	# Get a list of all the campaigns this team was part of this turn
	campaign_list = []
	query = """SELECT c.id
		FROM campaign_teams ct, campaigns c
			WHERE ct.team = %d
			AND ct.campaign = c.id
			AND c.turn = %d""" % (the_team.id, common.current_turn())
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		campaign_list.append(str(row['id']))
	
	# No campaigns, no losses
	if campaign_list == []:
		return empty_div
	
	# Now we need a list of all the battles in this campain
	battle_list = []
	battle_dict = {}
	query = "SELECT * FROM battles WHERE campaign in (%s) ORDER BY campaign, start" % ",".join(campaign_list)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in the_world.cursor:
		battle_dict[row['id']] = row
		battle_list.append(str(row['id']))
	
	# No battles, no section of results here!
	if battle_list == []:
		return empty_div
	
	
	#	Losses for other teams
	#------------------------
	output.append("<div style='float:right;width:50%;'><span class='stitle'>Losses across the campaign</span><br /><br />")
	for c in campaign_list:
		losses = campaign_q.get_all_losses(cursor, c)
		
		output.append("<strong>%s</strong><br />" % campaign_dict[int(c)].name)
		
		for t, l in losses.items():
			if l == 0: continue
			output.append("{team}: {losses}<br />".format(
				team = team_dict[t].name,
				losses = common.approx(l),
			))
		
		output.append('<br />')
		
		# print(c, campaign_q.get_all_losses(cursor, c))
	output.append('</div>')
	
	#	Our losses
	#------------------------
	# Now for a list of all squad losses, sort by battle
	query = """SELECT squad, battle, losses
		FROM squad_battle_history
			WHERE battle IN (%s)
				ORDER BY battle""" % ",".join(battle_list)
	try: the_world.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	losses = {"Total":{}}
	for row in the_world.cursor:
		if row['losses'] == 0: continue
		
		if row['battle'] not in losses:
			losses[row['battle']] = {}
		
		the_squad = squad_dict[row['squad']]
		
		if the_squad.team != the_team.id: continue
		if the_squad.unit not in losses[row['battle']]:
			losses[row['battle']][the_squad.unit] = 0
		
		if the_squad.unit not in losses["Total"]:
			losses["Total"][the_squad.unit] = 0
		
		losses[row['battle']][the_squad.unit] += row['losses']
		losses["Total"][the_squad.unit] += row['losses']
	
	last_campaign = -1
	for b, the_battle in battle_dict.items():
		if the_battle['campaign'] != last_campaign:
			last_campaign = the_battle['campaign']
			output.append("<span class='stitle'>%s</span><br />" % campaign_dict[last_campaign].name)
		
		if b == "Total" or b not in losses: continue
		if len(losses[b]) == 0: continue
		output.append("<strong>%s</strong><br />" % the_battle['name'])
		for u, a in losses[b].items():
			output.append("%s: %s<br />" % (unit_dict[u].name, format(a, ',')))
		
		output.append("<br />")
	
	if len(battle_dict) > 1:
		output.append("<br /><strong>Total losses</strong><br />")
		for u, a in losses["Total"].items():
			output.append("%s: %s<br />" % (unit_dict[u].name, format(a, ',')))
	
	output.append('</div>')
	return "".join(output)

def display_stat_table(cursor, team_id, list_size=10):
	# Get stats dict
	stat_dict	= stat_q.get_stats_from_team(cursor, team_id)
	if len(stat_dict) < 1:
		return "The stats for team %d do not exist" % team_id
	
	teams_dict	= team_q.get_all_teams(cursor)
	the_team	= teams_dict[team_id]
	
	output = []
	
	output.append("""
	<div class="ti_section" id="overview_div">
	<table border="0" cellspacing="0" cellpadding="5" style="width:100%;">
		<tr class="row2">
			<th>Turn</th>
			<th>Population</th>
			<th>Slaves</th>
			<th>Resources</th>
			<th>Production</th>
			<th>Upkeep</th>
			<th>Army</th>
			<th>Navy</th>
			<th>Airforce</th>
			<th>Operatives</th>
			<th>Mages</th>
			<th>Land</th>
			<th>Cities</th>
			<th>Losses</th>
		</tr>""")
	
	i = -1
	for k, the_stat in stat_dict.items():
		i += 1
		
		if i > list_size: continue
		
		# Currently
		the_res = res_dict.Res_dict(the_stat.resources)
		materials = the_res.get("Materials")
		if materials < 0:
			resources_string = '<strong class="neg">%s</strong>' % format(int(materials), ',')
		else:
			resources_string = format(int(materials), ',')
		
		# Production
		the_res = res_dict.Res_dict(the_stat.production)
		materials = the_res.get("Materials")
		if materials < 0:
			production_string = '<strong class="neg">%s</strong>' % format(int(materials), ',')
		else:
			production_string = format(int(materials), ',')
		
		output.append("""
		<tr class="row%(count)s">
			<td>Turn %(t)s</td>
			<td>%(population)s</td>
			<td>%(slaves)s</td>
			<td>%(resources)s</td>
			<td>%(production)s</td>
			<td>%(upkeep)s</td>
			<td>%(army_size)s</td>
			<td>%(navy_size)s</td>
			<td>%(airforce_size)s</td>
			<td>%(operatives)s</td>
			<td>%(mages)s</td>
			<td>%(land_controlled)s</td>
			<td>%(city_count)s</td>
			<td>%(war_losses)s</td>
		</tr>
		""" % {
			"count":			i%2,
			"t":				the_stat.turn,
			"population":		common.number_format(the_stat.population),
			"slaves":			common.number_format(the_stat.slaves),
			"resources":		resources_string,
			"production":		production_string,
			"upkeep":			common.number_format(int(the_stat.upkeep)),
			"army_size":		common.number_format(the_stat.army_size),
			"navy_size":		common.number_format(the_stat.navy_size),
			"airforce_size":	common.number_format(the_stat.airforce_size),
			"operatives":		common.number_format(the_stat.operatives),
			"mages":			common.number_format(the_stat.mages),
			"land_controlled":	common.number_format(the_stat.land_controlled),
			"city_count":		common.number_format(the_stat.city_count),
			"war_losses":		common.number_format(the_stat.war_losses),
		})
	
	output.append("</table></div>")
	return "".join(output)

def display_team_results(cursor, the_world, team_id):
	# return '<div class="ti_section" id="results_div">Implimentation will activate next turn</div>'
	
	output = []
	output.append("""
	<div class="ti_section" id="results_div">""")
	
	query = """SELECT content FROM results_log WHERE turn = %d AND team = %d AND failures = False""" % (common.current_turn(), team_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.append(common.bbcode_to_html(row['content']))
	
	output.append("</div>")
	return "".join(output)

def display_team_failures(cursor, the_world, team_id):
	# return '<div class="ti_section" id="failures_div">Implimentation will activate next turn</div>'
	
	output = []
	output.append("""
	<div class="ti_section" id="failures_div">""")
	
	query = """SELECT content FROM results_log WHERE turn = %d AND team = %d AND failures = True""" % (common.current_turn(), team_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		output.append(common.bbcode_to_html(row['content']))
	
	output.append("</div>")
	return "".join(output)

def display_team_upkeep(cursor, the_world, team_id):
	output = []
	breakdown = {}
	sub_total = {}
	output.append("""
	<div class="ti_section" id="upkeep_div">""")
	
	stat_f_amount = 0
	
	# Copy of function: team_f.get_upkeep
	the_team = the_world.teams()[team_id]
	unit_dict = the_world.units()
	army_dict = the_world.armies()
	squad_dict = the_world.squads_from_team(the_team.id)
	
	# Cache iron, makes it faster
	the_team.get_resources(the_world.cursor)#force_requery=True)
	if the_team.resources.get("Iron") > 0:
		has_iron = True
	else:
		has_iron = False
	
	stat_f_amount = 0
	for squad_id, the_squad in squad_dict.items():
		if the_squad.amount < 1: continue
		
		the_unit = unit_dict[the_squad.unit]
		the_army = army_dict[the_squad.army]
		
		# Get Iron/Material cost
		if has_iron:
			unit_cost = the_unit.get_cost(cursor=the_world.cursor, the_world=the_world)['material_upkeep'].get("Materials", 0)
		else:
			unit_cost = the_unit.get_cost(cursor=the_world.cursor, the_world=the_world)['iron_upkeep'].get("Materials", 0)
		
		# Skip it if it's not got any upkeep
		if unit_cost <= 0:
			continue
		
		# If we haven't started on this army then lets start now!
		if the_squad.army not in breakdown:
			breakdown[the_squad.army] = ['<span class="stitle">%s</span><br />' % army_dict[the_squad.army].name]
			sub_total[the_squad.army] = 0
		
		# If it's a ship or airship we don't divide by the divisor
		if the_unit.type_cat == unit.categories.index("Ship") or \
			the_unit.type_cat == unit.categories.index("Airship"):
			temp_cost = (unit_cost * the_squad.amount)
		else:
			temp_cost = (unit_cost * the_squad.amount/military_rules.amount_divisor)
		
		# Now we take into account the army type
		if the_army.garrison > 0:
			temp_cost *= military_rules.garrison_upkeep
			unit_cost *= military_rules.garrison_upkeep
		else:
			temp_cost *= military_rules.army_upkeep
			unit_cost *= military_rules.army_upkeep
		
		stat_f_amount += temp_cost
		
		# Break it down
		breakdown[the_squad.army].append("{squad}: {amount} x {name} @ {price} = {cost}<br />".format(
			squad = the_squad.name,
			amount = the_squad.amount,
			name = the_unit.name,
			price = unit_cost,
			cost = temp_cost,
		))
		sub_total[the_squad.army] += temp_cost
	
	stat_f_amount = team_rules.alter_upkeep(the_world.cursor, the_team, stat_f_amount, the_world)
	
	# We need to confirm that the number we got here is the same as from the function
	team_f_amount = team_f.get_upkeep(the_world.teams()[team_id], the_world)
	
	if stat_f_amount != team_f_amount:
		output.append('<span style="font-weight:bold;color:#F00;">There is an error in the workings: team_f = %d, stat_f = %d</span><br /><br />' % (team_f_amount, stat_f_amount))
	
	# Now for the actual output
	if has_iron:
		output.append("Calcuated with Iron<br /><br />")
	else:
		output.append("Calcuated without Iron<br /><br />")
	
	
	for army_id, the_army in army_dict.items():
		if army_id in breakdown:
			output.append("".join(breakdown[army_id]))
			output.append("<strong>Sub total</strong>: %s<br /><br />" % sub_total[army_id])
	
	output.append("Grand total: %s" % stat_f_amount)
	
	output.append("</div>")
	return "".join(output)