from pages import common
import time
from functions import spy_report_f

def javascript(the_team):
	return """
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
	"""

# Get a list of all the locations we need to make reports for
def location_list(the_world, the_team):
	operative_dict = the_world.operatives_from_team(the_team.id)
	
	locations = set()
	for op_id, the_op in operative_dict.items():
		if the_op.died > 0: continue
		locations.add(the_op.city)
	
	return locations

report_types = ["City buildings", "Armies units"]
def produce_location_report(the_world, the_team, city_id):
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	the_city = city_dict[city_id]
	
	if the_city.dead > 0:
		return []
	
	rep_list = []
	# output.append("""
	# <span class="stitle">Report for %s (%s)</span><br />
	# """ % (the_city.name, team_dict[the_city.team].name))
	
	# Create reports for this
	reports = spy_report_f.generate_report(the_world, the_team.id, city_id, "", radius=1, report_types=report_types)
	
	for r in reports:
		r.team = the_team.id
		r.enemy = city_dict[city_id].team
		r.city = city_id
	
	return reports


def produce_location_report_own_city(the_world, the_team, city_id):
	raise Exception("produce_location_report_own_city called")
	
	city_dict = the_world.cities()
	the_city = city_dict[city_id]
	
	location_info = {}
	
	if the_city.dead > 0:
		return "", {}
	
	# Check it's actually ours
	if the_city.team != the_team.id:
		raise Exception("Tried to call produce_location_report_own_city on a city not your own (%d called for %s [%d] with owner %d)" % (
		the_team.id, the_city.name, the_city.id, the_city.team
	))
	
	output = []
	output.append("""
	<strong>Report for %s</strong><br />
	""" % (the_city.name))
	
	return "".join(output), location_info

def operative_list(the_world, the_team):
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	operatives_dict	= the_world.operatives_from_team(the_team.id)
	reports_dict = {}
	
	if len(operatives_dict) <= 0:
		return 'You have no operatives'
	
	# Location stuff
	team_location = {}
	for o, the_op in operatives_dict.items():
		if the_op.city < 1: continue
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
	
	if recent_deaths == 1:
		cells_str = "cell"
	else:
		cells_str = "cells"
	
	output.append("""
	You have %s cells spread across %s cities. You have lost %s %s in the last 3 turns.<br /><br />""" % (operative_count, len(city_set), recent_deaths, cells_str))
	
	spies_out		= []
	couterspies_out	= []
	for city_id, op_count in city_count.items():
		if city_id < 1: continue
		the_city = city_dict[city_id]
		
		if the_city.team == the_team.id:
			couterspies_out.append("""<li>%s at %s</li>""" % (op_count, city_dict[city_id].name))
		else:
			spies_out.append("""<li>%s at %s</li>""" % (op_count, city_dict[city_id].name))
	
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
	return "".join(output)


def make_report(the_world, the_team):
	output = []
	
	city_dict = the_world.cities()
	team_dict = the_world.teams()
	
	# Tabs
	# output.append(tabs(cursor, the_team))
	
	# Date
	output.append("<h2>Spy report for turn %d</h2><br />\n" % common.current_turn())
	
	# Actual output
	city_dict = the_world.cities()
	locations = location_list(the_world, the_team)
	
	team_output = {}
	
	# Foreign
	# output.append('<span class="stitle">Foreign reports</span><br />')
	for city_id, the_city in city_dict.items():
		if city_id in locations:
			if the_city.team != the_team.id:
				reports = produce_location_report(the_world, the_team, city_id)
				
				for r in reports:
					if r.enemy not in team_output:
						team_output[r.enemy] = []
					
					team_output[r.enemy].append(r)
				
				# output.append(fout)
	
	options = []
	
	for k, v in team_output.items():
		output.append('<span class="stitle" id="%s">%s</span><br />' % (common.js_name(team_dict[k].name), team_dict[k].name))
		# headers.append('<a href="#%s">%s</a>' % (team_dict[k].name, common.js_name(team_dict[k].name)))
		options.append(team_dict[k].name)
		
		last_city = -1
		for r in v:
			if last_city != r.city:
				output.append("<strong id='%s'>%s</strong>" % (common.js_name(city_dict[r.city].name), city_dict[r.city].name))
				options.append(city_dict[r.city].name)
				last_city = r.city
			
			output.append('<div class="spy_report_new">')
			# output.append(common.bbcode_to_html(r))
			output.append(common.bbcode_to_html(r.content))
			output.append("</div>")
	
	form = """
	<div style="cursor: pointer; padding:5px; color: #00A;" onclick=" $(this).hide(500); $('#option_list').show(500);">
		Display jump list
	</div>
	<div id="option_list" style="display:none;">
		%s
		<br /><br />
	</div>
	""" % "<br />".join(['<a href="#%s">%s</a>' % (common.js_name(o), o) for o in options])
	
	output.insert(1, form)
	
	# print("".join(output))
	# print("<br />".join(headers))
	# exit()
	
	# Our cities
	'''
	output.append('<br /><span class="stitle">Internal reports</span><br />')
	for city_id, the_city in the_world.cities_from_team(the_team.id).items():
		output.append(produce_location_report_own_city(the_world, the_team, city_id))
	'''
	# output.append(operative_list(the_world, the_team))
	
	# output.append()
	
	return "".join(output)

