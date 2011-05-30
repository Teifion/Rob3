from pages import common
from data import battle, battle_f, battle_q
from data import army
from data import squad
from data import unit
from data import team
from data import evolution

battle_id	= int(common.get_val("battle", -1))
team_1		= int(common.get_val("t1", -1))
team_2		= int(common.get_val("t2", -1))

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

if team_1 not in participants or team_2 not in participants:
	print "The selected teams are not in this battle"
	exit()

participants = [team_1, team_2]

# Create output list
output = ['<div style="padding: 5px;">']

# Titles
output.append("""<span class="stitle">%(name)s</span> - <a href="web.py?mode=edit_battle&amp;battle=%(battle_id)s">Edit</a> - <a href="web.py?mode=view_battle&amp;battle=%(battle_id)s">View</a><br /><br />
""" % {
	"name":	the_battle.name,
	"battle_id":	battle_id,
})

for team_id in participants:
	the_team = teams_dict_c[team_id]
	
	output.append("""<div id="team_container_%(team_id)s" style="float:left; width:47%%;">
	<span class="stitle">%(name)s</span>
	""" % {
			"team_id":		team_id,
			"name":	the_team.name,
		})
	
	#	ORDER BY UNIT TYPE
	#------------------------
	team_units = the_team.get_units()
	unit_count = {}
	
	for unit_id, amount in team_units.items():
		unit_count[unit_id] = 0
	
	for s in squads:
		if squad_dict_c[s].team != team_id: continue
		unit_count[squad_dict_c[s].unit] += squad_dict_c[s].amount
	
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%%">
		<tr class="row2">
			<th>Unit</th>
			<th>Equipment</th>
			<th>Amount</th>
			<th>Losses</th>
		</tr>
	""")
	
	# Unit row
	count = -1
	for unit_id, amount in team_units.items():
		count += 1
		output.append("""
		<tr class="row%(count)s">
			<td>%(name)s</td>
			<td>%(equipment)s</td>
			<td>%(amount)s</td>
			<td>%(losses)s</td>
		</tr>
		""" % {
			"count":		count%2,
			"name":	unit_dict_c[unit_id].name,
			"equipment":	unit_dict_c[unit_id].equipment_string,
			"amount":		unit_count[unit_id],
			"losses":		0,
			"unit_id":		unit_id,
		})
	
	# Evos row
	evo_output = []
	
	the_team.get_evolutions()
	for evolution_id in the_team.evolutions:
		the_evo = evolution_dict_c[evolution_id]
		
		evo_output.append("""<strong>%(level)sx %(evo_name)s</strong><br />""" % {
			"level":	the_team.evolutions[evolution_id],
			"evo_name":	the_evo.name,
		})
	
	
	count += 1
	output.append("""
	<tr class="row%(count)s">
		<td colspan="5" style="padding:0px;">
			<div id="show_evos_%(team_id)s">
				<a href="#" class="block_link" onclick="$('#show_evos_%(team_id)s').hide(); $('#evos_%(team_id)s').fadeIn(250); return false;">Evos</a>
			</div>
			<div id="evos_%(team_id)s" style="display:none;">
				<a href="#" class="block_link" onclick="$('#show_evos_%(team_id)s').fadeIn(250); $('#evos_%(team_id)s').hide();return false;">Hide</a><br />
				
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
				<a href="#" onclick="$('#compare_form_%(team_id)s').submit();">Compare</a>
			</form>
		</td>
	</tr>
	""" % {
		"count":		count%2,
		"team_id":		team_id,
		"battle_id":	battle_id,
		"team_list":	common.option_box("t2", elements=teams_dict, element_order=participants)
	})
	
	output.append("</table>")
	
	output.append("</div>")
	
	# Spacer between columns
	output.append("<div style='float:left;width:50px;'>&nbsp;</div>")


output.append("</div>")

print "".join(output)