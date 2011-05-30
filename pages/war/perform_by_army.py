from pages import common
# from data import battle, battle_f, battle_q
# from data import team, team_f, team_q
# from data import city, city_q
# from data import army, army_q
from queries import battle_q, campaign_q, team_q, army_q, squad_q, unit_q
from queries import evolution_q
from classes import unit

page_data = {
	"Title":	"Perform battle",
	"Admin":	True,
}

short_weapon_categories = (
	'Melee',
	'Ranged',
	'Both',
	'N/A',
)

short_armour_categories = (
	'&nbsp;',
	'Leather',
	'Mail',
	'Plate',
)

short_move_categories = (
	'Foot',
	'Mule',
	'Horse',
	'Fly',
	'Boat',
	'Ball',
)

short_training_categories = (
	'Low',
	'Norm',
	'High',
)

def draw_unit(the_battle, unit_count, unit_losses, the_unit, the_army, lookahead, row_count):
	output = []
	
	# Form JS
	form_js = """$('#ajax_target').load('web.py', {mode: 'add_army_loss', ajax: 'True', battle: %(battle_id)d, army: %(army_id)d, unit: %(unit_id)d, amount: $('#amount_for_%(army_id)d_%(unit_id)d').attr('value')}, function ()
	{
		var loss			= parseInt($('#amount_for_%(army_id)d_%(unit_id)d').attr('value').replace(',', ''));
		var current_loss	= parseInt($('#losses_%(army_id)d_%(unit_id)d').html().replace(',', ''));
		var current_amount	= parseInt($('#amount_%(army_id)d_%(unit_id)d').html().replace(',', ''));
		
		$('#amount_%(army_id)d_%(unit_id)d').html(current_amount - loss);
		$('#losses_%(army_id)d_%(unit_id)d').html(current_loss + loss);
		
		$('#amount_for_%(army_id)d_%(unit_id)d').attr('value', '');
		$('#amount_for_%(army_id)d_%(ahead)d').focus();
	});
	return false;""" % {
		"battle_id":	the_battle.id,
		"unit_id":		the_unit.id,
		"army_id":		the_army.id,
		"ahead":		lookahead,
	};
	
	return """
	<tr class="row{count}" id="row_{army_id}_{unit_id}">
		<td style='font-weight:bold;'>{unit_name}</td>

		<td>{weapon_cat}</td>
		<td>{armour_cat}</td>
		<td>{move_cat}</td>
		<td>{training_cat}</td>

		<td>{equipment}</td>
		<td>{total}</td>
		<td id="amount_{army_id}_{unit_id}">{amount}</td>
		<td id="losses_{army_id}_{unit_id}">{losses}</td>
		<td id="losses_cent_{army_id}_{unit_id}">{losses_cent}%</td>
		<td style="padding:1px;">
			<form action="web.py" method="post" id="" onsubmit="{form_js}" accept-charset="utf-8">
				<input type="hidden" name="mode" value="add_army_loss" />
				<input type="hidden" name="battle" value="{battle_id}" />
				<input type="hidden" name="unit" value="{unit_id}" />
				<input type="hidden" name="army" value="{army_id}" />
				<input type="text" onfocus="{on_focus}" onblur="{on_blur}" name="amount" id="amount_for_{army_id}_{unit_id}" value="" size="5"/>
			</form>
		</td>
	</tr>
	""".format(
		count		= row_count % 2,
		form_js		= form_js,
		army_id		= the_army.id,
		unit_id		= the_unit.id,
		unit_name	= the_unit.name,
		equipment	= the_unit.equipment_string,
		total		= common.number_format(unit_count.get(the_unit.id, 0) + unit_losses.get(the_unit.id, 0)),
		amount		= common.number_format(unit_count.get(the_unit.id, 0)),
		losses		= common.number_format(unit_losses.get(the_unit.id, 0)),
		losses_cent	= round(unit_losses.get(the_unit.id, 0)/(unit_count.get(the_unit.id, 0) + unit_losses.get(the_unit.id, 0))*100),
		battle_id	= the_battle.id,
		team_id		= the_army.team,
		# unit_id		= the_squad.unit,
		on_focus	= "$('#row_{0}_{1}').addClass('row3');".format(the_army.id, the_unit.id),
		on_blur		= "$('#row_{0}_{1}').removeClass('row3');".format(the_army.id, the_unit.id),
		
		weapon_cat		= "",
		armour_cat		= "",
		move_cat		= "",
		training_cat	= "",

		# xweapon_cat		= short_weapon_categories[unit_dict[unit_id].weapon_cat],
		# xarmour_cat		= short_armour_categories[unit_dict[unit_id].armour_cat],
		# xmove_cat		= short_move_categories[unit_dict[unit_id].move_cat],
		# xtraining_cat	= short_training_categories[unit_dict[unit_id].training_cat],
	)

def draw_army(the_battle, squad_dict, unit_dict, the_army):
	output = []
	row_count = 0
		
	# Build dictionaries/lists
	team_units = []
	for k, v in unit_dict.items():
		if v.team == the_army.team or v.team == 0:
			team_units.append(k)
	
	total_count = {}
	unit_count = {}
	unit_losses = {}
	
	transport_lost = 0
	transport_capacity = 0
	army_size = 0
	
	for unit_id in team_units:
		unit_count[unit_id] = 0
		unit_losses[unit_id] = 0
	
	for s in the_army.squads:
		the_squad = squad_dict[s]
		
		unit_count[the_squad.unit] += the_squad.amount
		army_size += the_squad.amount
		unit_losses[the_squad.unit] += the_battle.losses.get(the_squad.id, 0)
	
	# Build look-ahead
	lookahead = {}
	last_unit = -1
	for u in team_units:
		if unit_count[u] == 0 and unit_losses[u] == 0:
			continue
		lookahead[last_unit] = u
		last_unit = u
	
	if lookahead == {}:
		return None
	
	lookahead[last_unit] = 0
	
	for unit_id in team_units:
		the_unit = unit_dict[unit_id]
		# if unit_dict[the_squad.unit].type_cat == unit.categories.index("Ship") and ships == False:
		# 	continue
		
		if unit_count[unit_id] == 0 and unit_losses[unit_id] == 0:
			continue
		
		row_count += 1
		# the_battle, the_unit, the_army, lookahead, row_count
		output.append(draw_unit(the_battle, unit_count, unit_losses, the_unit, the_army, lookahead[unit_id], row_count))
	
	return """
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%">
		<tr>
			<td colspan="11"><span class="stitle">{army_name}</span></td>
		</tr>
		<tr class="row2">
			<th>Unit: Squad</th>
			<th colspan="4">&nbsp;</th>
			<th>Equipment</th>
			<th>Total</th>
			<th>Amount</th>
			<th colspan="2">Losses</th>
			<th>&nbsp;</th>
		</tr>
		{squad_data}
	</table>
	""".format(army_name = the_army.name, squad_data = "".join(output))

def main(cursor, battle_id=-1):
	battle_id = int(common.get_val('battle', battle_id))
	ships = int(common.get_val('ships', True))
	
	if battle_id < 1:
		return "No battle selected"
	
	the_battle = battle_q.get_one_battle(cursor, battle_id)
	
	# Get some other stuff
	team_dict		= team_q.get_all_teams(cursor)
	the_campaign	= campaign_q.get_one_campaign(cursor, the_battle.campaign)
	
	output = ["""	
	<div style='padding: 5px;'>
	<a href="web.py?mode=list_campaigns&amp;turn={turn}" class="block_link" style="display:inline; text-align:left;">Campaigns of this turn</a>
	<a href="web.py?mode=setup_campaign&amp;campaign={c.id}" class="block_link" style="display:inline;">Setup campaign</a>
	<a href="web.py?mode=list_battles&amp;campaign={c.id}" class="block_link" style="display:inline;">List battles</a>
	<a href="web.py?mode=setup_battle&amp;battle={b.id}" class="block_link" style="display:inline;">Setup battle</a>
	<a href="web.py?mode=perform_battle&amp;battle={b.id}" class="block_link" style="display:inline;">By unit</a>
	<br /><br />
	
	<span class="stitle">{c.name} - {b.name}</span> - <a href="web.py?mode=perform_battle&amp;battle={b.id}&amp;ships=0">No ships</a>
	
	<br />
	<a href="#" onclick="$('.show_evo_wedge').show(); $('.evo_wedge').hide(); return false;">Hide evo wedges</a>
	 - 
	<a href="#" onclick="$('.show_evo_wedge').hide(); $('.evo_wedge').show(); return false;">Show evo wedges</a>
	""".format(
		c = the_campaign,
		b = the_battle,
		turn = common.current_turn(),
	)]
	
	#	Now for some stuff about the participants
	#------------------------
	the_campaign.get_sides_basic(cursor)
	the_campaign.get_armies_basic(cursor)
	the_battle.get_losses(cursor)
	the_battle.get_squads(cursor)
	
	team_list = []
	for s in range(1, the_campaign.sides+1):
		for t in the_campaign.sides_basic[s]:
			team_list.append(t)
	
	unit_dict = unit_q.get_units_from_team_list(cursor, team_list, special_units=True)
	
	evolution_dict = evolution_q.get_all_evolutions(cursor)
	
	# Sort squads by team
	# Doing this makes it O(2n) rather than O(t*n)
	army_dict = army_q.get_armies_from_list(cursor, the_battle.armies)
	squad_dict = squad_q.get_all_squads(cursor)
	squad_q.mass_get_squads(cursor, army_dict)
	armies_by_team = {}
	
	for army_id, the_army in army_dict.items():
		if the_army.team not in armies_by_team: armies_by_team[the_army.team] = []
		armies_by_team[the_army.team].append(army_id)
	
	for s in range(1, the_campaign.sides+1):
		teams_on_side = the_campaign.sides_basic[s]
		
		if len(teams_on_side) > 0:
			output.append('''<table border="1" cellspacing="0" cellpadding="5" width="100%">
			<tr>
				<td class="stitle" colspan="2">{s}</td>
			</tr>'''.format(s=s))
			
			for i, team_id in enumerate(teams_on_side):
				if team_id not in armies_by_team:
					armies_by_team[team_id] = []
				
				# Table tags for team cell
				if i % 2 == 0:	output.append('<tr><td>')
				else:			output.append('<td>')
				
				the_team = team_dict[team_id]
				
				# Team header
				output.append('''
				<span class="stitle">{name}</span>
				 - 
				<a href="web.py?mode=list_units&amp;team={id}">Military</a>
				 - 
				<a href="web.py?mode=list_armies&amp;team={id}">Armies</a>
				 - 
				<a href="#" onclick="$(this).parent().hide(); return false;">Hide</a>
				'''.format(
					name=the_team.name,
					id=team_id,
				))
				
				# Armies
				for army_id in armies_by_team[team_id]:
					the_army = army_dict[army_id]
					
					army_output = draw_army(the_battle, squad_dict, unit_dict, the_army)
					
					if army_output != None:
						output.append(army_output)
						output.append("<tr><td colspan='1'>&nbsp;</td></tr>")
				
				# Evos row
				evo_output = []
				
				the_team.get_evolutions(cursor)
				for evolution_id in the_team.evolutions:
					the_evo = evolution_dict[evolution_id]
				
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
				
				count = 0
				output.append("""
				<tr class="row%(count)s">
					<td colspan="11" style="padding:0px;">
						<div id="show_evos_%(team_id)s" style="display:nnone;" class="show_evo_wedge">
							<a href="#" class="block_link" onclick="$('#show_evos_%(team_id)s').hide(); $('#evos_%(team_id)s').fadeIn(250);return false;">Evos</a>
						</div>
						<div id="evos_%(team_id)s" style="display:none;" class="evo_wedge">
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
				
				# End of team units
				output.append("</table>")
				
				
				# Table tags for team cell
				if i % 2 == 0:	output.append('</td>')
				else:			output.append('</td></tr>')
			
			# Not sure that we need to adhere to W3C specs for tables...
			# if i % 2 == 0:	output.append('<td>&nbsp;</td></tr>')
			
			output.append("</table><br />")
		else:
			output.append('No teams on side {s}'.format(s=s))
	
	# Field for the ids of the armies listed that we need to sort out
	# output.append('</table><br />')
	
	output.append("</div>")
	
	page_data['Title'] = "Perform by army - %s" % the_battle.name
	return "".join(output)
