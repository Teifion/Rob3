from pages import common
from data import battle, battle_f, battle_q
from data import army
from data import squad
from data import unit
from data import team, team_f
from data import evolution

battle_id	= int(common.get_val("battle", -1))
order_by	= common.get_val("order", "Unit_type")

# No battle, no lunch
if battle_id < 1:
	print "No battle selected"
	exit()

# Lists/Dicts
teams_dict_c	= team.get_teams_dict_c()
teams_dict		= team.get_teams_dict()
army_dict_c		= army.get_army_dict_c()
squad_dict_c	= squad.get_squad_dict_c()
unit_dict_c		= unit.get_unit_dict_c()

evolution_list		= evolution.get_evolution_list()
evolution_dict_c	= evolution.get_evolution_dict_c()

# Get specifics
the_battle		= battle.Battle(battle_q.get_one_battle(battle_id))
participants	= the_battle.get_participants()
armies			= the_battle.get_armies()
squads			= the_battle.get_squads()

# Create output list
output = ['<div style="padding: 5px;">']

# "Order by" links
order_by_link = """
Order by: <a href="view_battle&amp;battle=%(b)s&amp;order=Unit_type"{ut}>Unit type</a> - 
<a href="view_battle&amp;battle=%(b)s&amp;order=Army"{a}>Army</a>
<br /><br />
""" % {"b": battle_id}

if order_by == "Army":
	order_by_link = order_by_link.replace("{a}", 'class="blue_link"')

elif order_by == "Unit_type":
	order_by_link = order_by_link.replace("{ut}", 'class="blue_link"')

else:
	print "Unknonw order_by type of '%s' in web.battles.view_battle" % order_by
	exit()

order_by_link = order_by_link.replace("{a}", "").replace("{ut}", "")

# Titles
output.append("""<span class="stitle">%(name)s</span> - <a href="web.py?mode=edit_battle&amp;battle=%(battle_id)s">Edit</a><br />
%(order_by)s
""" % {
	"name":	the_battle.name,
	"battle_id":	battle_id,
	"order_by":		order_by_link,
})

for team_id in participants:
	the_team = teams_dict_c[team_id]
	
	army_size = 0
	
	output.append("""<div id="team_container_%(team_id)s" style="float:left; width:47%%;">
	<span class="stitle">%(name)s</span>
	 - 
	<a href="list_units&amp;team=%(team_id)s">Military</a>
	 - 
	<a href="list_armies&amp;team=%(team_id)s">Armies</a>
	""" % {
			"team_id":		team_id,
			"name":	the_team.name,
		})
	
	#	FIRST PASS FOR SOME STUFF
	#------------------------
	team_units = the_team.get_units()
	unit_count = {}		
	unit_losses = {}
	
	# transport_dict = team_f.team_transport_types(team_id)
	transport_lost = 0
	
	for unit_id, amount in team_units.items():
		unit_count[unit_id] = 0
		unit_losses[unit_id] = 0
	
	for s, l in squads.items():
		if squad_dict_c[s].team != team_id: continue
		unit_count[squad_dict_c[s].unit] += squad_dict_c[s].amount
		army_size += squad_dict_c[s].amount
		unit_losses[squad_dict_c[s].unit] += l
	
	transport_capacity = team_f.team_sea_transport_capacity(team_id, unit_count)
	
	
	#	ORDER BY ARMY
	#------------------------
	if order_by == "Army":
		pass
	
	#	ORDER BY UNIT TYPE
	#------------------------
	elif order_by == "Unit_type":
		# for unit_id, amount in team_units.items():
		# 	unit_count[unit_id] = 0
		# 	unit_losses[unit_id] = 0
		# 
		# for s, l in squads.items():
		# 	if squad_dict_c[s].team != team_id: continue
		# 	unit_count[squad_dict_c[s].unit] += squad_dict_c[s].amount
		# 	unit_losses[squad_dict_c[s].unit] += l
		
		output.append("""
		<table border="0" cellspacing="0" cellpadding="5" style="width: 100%%">
			<tr class="row2">
				<th>Unit</th>
				<th>Equipment</th>
				<th>Amount</th>
				<th>Losses</th>
				<th>&nbsp;</th>
			</tr>
		""")
		
		# Unit row
		count = -1
		for unit_id, amount in team_units.items():
			if unit_count[unit_id] == 0 and unit_losses[unit_id] == 0:
				continue
			
			count += 1
			
			# Form JS
			form_js = """$('#ajax_target').load('web.py', {mode: 'add_unit_loss', ajax: 'True', battle: %(battle_id)s, unit: %(unit_id)s, team: %(team_id)s, amount: $('#amount_for_%(unit_id)s_%(team_id)s').attr('value')}, function ()
			{
				var loss			= parseInt($('#amount_for_%(unit_id)s_%(team_id)s').attr('value').replace(',', ''));
				var current_loss	= parseInt($('#losses_%(unit_id)s_%(team_id)s').html().replace(',', ''));
				var current_amount	= parseInt($('#amount_%(unit_id)s_%(team_id)s').html().replace(',', ''));
				
				$('#amount_%(unit_id)s_%(team_id)s').html(current_amount - loss);
				$('#losses_%(unit_id)s_%(team_id)s').html(current_loss + loss);
				
				$('#amount_for_%(unit_id)s_%(team_id)s').attr('value', '');
			});
			return false;""" % {
				"battle_id":	battle_id,
				"team_id":		team_id,
				"unit_id":		unit_id,
			};
			
			# function add_unit_amount_%(unit_id)s ()
			# {
			# 	$('#amountFor_team').removeAttr('value');
			# 	$('#spanAddUnitFor_team').load('ajax.php', {mode: 'getUnitsNotInWar', team: $team, war: $warId});
			# });
			
			output.append("""
			<tr class="row%(count)s">
				<td>%(name)s</td>
				<td>%(equipment)s</td>
				<td id="amount_%(unit_id)s_%(team_id)s">%(amount)s</td>
				<td id="losses_%(unit_id)s_%(team_id)s">%(losses)s</td>
				<td style="padding:1px;">
					<form action="exec.pyy" method="post" id="" onsubmit="%(form_js)s" accept-charset="utf-8">
						<input type="hidden" name="mode" id="mode" value="add_unit_loss" />
						<input type="hidden" name="battle" id="battle" value="%(battle_id)s" />
						<input type="hidden" name="unit" id="unit" value="%(unit_id)s" />
						<input type="hidden" name="team" id="team" value="%(team_id)s" />
						<input type="text" name="amount" id="amount_for_%(unit_id)s_%(team_id)s" value="" size="5"/>
					</form>
				</td>
			</tr>
			""" % {
				"count":		count%2,
				"form_js":		form_js,
				"name":	unit_dict_c[unit_id].name,
				"equipment":	unit_dict_c[unit_id].equipment_string,
				"amount":		common.number_format(unit_count[unit_id]),
				"losses":		common.number_format(unit_losses[unit_id]),
				"battle_id":	battle_id,
				"team_id":		team_id,
				"unit_id":		unit_id,
			})
		
		# Size row
		count += 1
		output.append("""
		<tr class="row%(count)s">
			<td colspan="2">
				Military size:
			</td>
			<td colspan="3">
				%(size)s
			</td>
		</tr>
		""" % {
			"count":	count%2,
			"size":		common.number_format(army_size),
		})
		
		# Transport row
		count += 1
		output.append("""
		<tr class="row%(count)s">
			<td colspan="2">
				Transport capacity:
			</td>
			<td colspan="3">
				%(capacity)s
			</td>
		</tr>
		""" % {
			"count":		count%2,
			"capacity":		common.number_format(transport_capacity),
		})
		
		# Evos row
		evo_output = []
		
		the_team.get_evolutions()
		for evolution_id in the_team.evolutions:
			the_evo = evolution_dict_c[evolution_id]
			
			if the_team.evolutions[evolution_id] == 0: continue
			if not the_evo.combat_relevant: continue
				
			
			if the_evo.max_level == 1 and the_team.evolutions[evolution_id] == 1:
				evo_output.append("""<strong>%(evo_name)s</strong><br />""" % {
					"evo_name":	the_evo.name,
				})
			else:
				evo_output.append("""<strong>%(level)sx %(evo_name)s</strong><br />""" % {
					"level":	the_team.evolutions[evolution_id],
					"evo_name":	the_evo.name,
				})
		
		count += 1
		output.append("""
		<tr class="row%(count)s">
			<td colspan="5" style="padding:0px;">
				<div id="show_evos_%(team_id)s" style="display:none;" >
					<a href="#" class="block_link" onclick="$('#show_evos_%(team_id)s').hide(); $('#evos_%(team_id)s').fadeIn(250);return false;">Evos</a>
				</div>
				<div id="evos_%(team_id)s" style="display:nnone;">
					<a href="#" class="block_link" onclick="$('#show_evos_%(team_id)s').fadeIn(250); $('#evos_%(team_id)s').hide(); return false;">Hide</a><br />
					
					%(evo_output)s
				</div>
			</td>
		</tr>
		""" % {
			"count":		count%2,
			"team_id":		team_id,
			"evo_output":	"".join(evo_output)
		})
		
		# Compare teams row
		count += 1
		
		output.append("""
		<tr class="row%(count)s">
			<td colspan="5">
				<form action="web.py" id="compare_form_%(team_id)s" method="get" accept-charset="utf-8">
					<input type="hidden" name="mode" value="compare_teams" />
					<input type="hidden" name="battle" value="%(battle_id)s" />
					<input type="hidden" name="t1" value="%(team_id)s" />
					%(team_list)s - 
					<a href="#" onclick="$('#compare_form_%(team_id)s').submit(); return false;">Compare</a>
				</form>
			</td>
		</tr>
		""" % {
			"count":		count%2,
			"team_id":		team_id,
			"battle_id":	battle_id,
			"team_list":	common.option_box("t2", elements=teams_dict, element_order=participants)
		})
		
		output.append("</table><br /><br />")
	
	output.append("</div>")
	
	# Spacer between columns
	output.append("<div style='float:left;width:50px;'>&nbsp;</div>")


output.append("</div>")

print "".join(output)