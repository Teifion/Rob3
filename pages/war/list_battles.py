from pages import common
from classes import battle
from queries import campaign_q, battle_q, team_q, city_q

page_data = {
	"Title":	"Battle list",
	"Admin":	True,
}

def main(cursor, campaign_id = -1):
	output = ["""<div style="padding: 5px;">"""]
	
	campaign_id	= int(common.get_val('campaign', campaign_id))
	battle_id	= int(common.get_val('battle', 0))
	ajax = common.get_val('ajax', 0)
	
	if campaign_id < 1:
		if battle_id < 1:
			return "No campaign selected"
		else:
			the_battle = battle_q.get_one_battle(cursor, battle_id)
			campaign_id = the_battle.campaign
	
	the_campaign	= campaign_q.get_one_campaign(cursor, campaign_id)
	battle_dict		= battle_q.get_battles_from_campaign(cursor, campaign_id)
	team_dict		= team_q.get_all_teams(cursor)
	city_dict		= city_q.get_all_cities(cursor)
	
	if not ajax:
		output.append("""
		<div style="float:right;border:0px solid #000; width: 50%;">
			<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
				<input type="hidden" name="campaign" id="campaign" value="{id}" />
				<input type="hidden" name="mode" id="mode" value="remove_campaign" />
				<input style="float:right; margin-right:100px;" type="button" value="Delete campaign" onclick="var answer = confirm('Delete {esc_name}?')
				if (answer) $('#delete_form').submit();" />
			</form>
			<div id="campaign_info">
				&nbsp;
			</div>
			&nbsp;
		</div>
		
		<a href="web.py?mode=list_campaigns&amp;turn={turn}" class="block_link" style="display:inline; text-align:left;">Campaigns of this turn</a>
		<a href="web.py?mode=setup_campaign&amp;campaign={camp}" class="block_link" style="display:inline;">Setup campaign</a>
		<br /><br />
		
		<span class="stitle">{name}</span>
		<br /><br />
		<table border="0" cellspacing="0" cellpadding="5">
		""".format(
			turn			= common.current_turn(),
			camp			= the_campaign.id,
			name			= the_campaign.name,
			id				= campaign_id,
			esc_name		= common.js_name(the_campaign.name),
		))
		
	else:
		output.append("""<table border="0" cellspacing="0" cellpadding="5" width="100%">""")
	
	output.append("""
		<tr class="row2">
			<th>Battle</th>
			<th>Time</th>
			<th>Location</th>
			<th>Type</th>
			<th>Result</th>
			<th>&nbsp;</th>
			<th colspan="2">Perform</th>
		</tr>""")
	
	# Display battles
	i = -1
	for battle_id, the_battle in battle_dict.items():
		i += 1
		
		location = "%d, %d" % (the_battle.x, the_battle.y)
		city_link = ""
		
		if the_battle.city > 0:
			city_link = '<!-- PY --> <a href="web.py?mode=edit_city&amp;city=%d">Edit city</a><!-- PYEND -->' % the_battle.city
		
		
		output.append("""
		<tr class="row{i}">
			<td>{name} ({battle_id}){city_link}</td>
			<td>{start} : {duration}</td>
			<td>{location} &nbsp; {city}</td>
			<td>{type}</td>
			<td>{result}</td>
			<td style="padding:0px;"><a href="web.py?mode=setup_battle&amp;battle={battle_id}" class="block_link">Setup</a></td>
			<td style="padding:0px;"><a href="web.py?mode=perform_battle&amp;battle={battle_id}" class="block_link">By unit</a></td>
			<td style="padding:0px;"><a href="web.py?mode=perform_by_army&amp;battle={battle_id}" class="block_link">By army</a></td>
		</tr>
		""".format(
			i=i%2,
			city_link = city_link,
			name=common.doubleclick_text("battles", "name", battle_id, the_battle.name, label_style="font-weight:bold;"),
			start=common.doubleclick_text("battles", "start", battle_id, the_battle.start, size=2),
			duration=common.doubleclick_text("battles", "duration", battle_id, the_battle.duration, size=2),
			location=location,
			battle_id=battle_id,
			city = city_dict[the_battle.city].name,
			
			type = battle.battle_types[the_battle.type],
			result = battle.result_types[the_battle.result],
		))
		
	
	if ajax:
		onload = ""
	else:
		onload = common.onload("$('#form_city').focus();")
	
	# Add new battle
	i += 1
	output.append("""
	<tr class="row{i}">
		<form action="exec.py" id="add_battle_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_battle" />
		<input type="hidden" name="campaign" value="{campaign_id}" />
		<td style="padding: 1px;"><input type="text" name="name" id="new_name" value="" /></td>
		<td style="padding: 1px;">
			<input type="text" name="start" value="-1" size="2"/>
			<input type="text" name="duration" value="" size="2"/>
		</td>
		<td style="padding: 1px;">
			<input type="text" name="location" value="" size="8"/>
		</td>
		
		<td style="padding: 1px;">
			{type}
		</td>
		<td>&nbsp;</td>
		
		<td colspan="3" style="padding: 0px;">
			<!--<a class="block_link" href="#" onclick="$('#add_battle_form').submit();">Add</a>-->
			<input type="submit" value="Add" />
		</td>
		</form>
	</tr>""".format(
		i=i%2,
		campaign_id=campaign_id,
		type = common.option_box("type", elements = battle.battle_types, element_order = [], custom_id = ""),
	))
	
	# Add by city
	city_dict = city_q.get_cities_for_dropdown(cursor)
	keys, names = [], {}
	for c, the_city in city_dict.items():
		if the_city.dead > 0: continue
		if not team_dict[the_city.team].active: continue
		
		keys.append(c)
		names[c] = the_city.name
	
	i += 1
	output.append("""
	<tr class="row{i}">
		<form action="exec.py" id="add_battle_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_battle" />
		<input type="hidden" name="campaign" value="{campaign_id}" />
		<td style="padding: 1px;">{city_list}</td>
		<td style="padding: 1px;">
			<input type="text" name="start" value="-1" size="2"/>
			<input type="text" name="duration" value="" size="2"/>
		</td>
		<td>
			&nbsp;
		</td>
		
		<td style="padding: 1px;">
			{type}
		</td>
		<td>&nbsp;</td>
		
		<td colspan="3" style="padding: 0px;">
			<!--<a class="block_link" href="#" onclick="$('#add_battle_form').submit();">Add</a>-->
			<input type="submit" value="Add" />
		</td>
		</form>
		{onload}
	</tr>
	</table>
	<br /><br />
	""".format(
		i=i%2,
		campaign_id=campaign_id,
		onload=onload,
		city_list = common.option_box(
			name='city',
			elements=names,
			element_order=keys,
			custom_id="form_city",
		),
		type = common.option_box("type", elements = battle.battle_types, element_order = [], custom_id = ""),
	))
	
	
	# Chosen kills
	output.append("""
	<div style="float:right;border:0px solid #000; width: 60%;">
		<div id="player_kills">
			&nbsp;
		</div>
	</div>
	""")
	
	
	# Now for moving all the armies
	output.append("""
	<!-- PY -->
	<table border="0" cellspacing="0" cellpadding="5">
	<!--
		<tr class="row2">
			<th>Team</th>
			<th colspan="3">Move</th>
			<th>&nbsp;</th>
		</tr>
	-->""")
	
	the_campaign.get_sides_full(cursor)
	for s in range(1, the_campaign.sides+1):
		teams_on_side = the_campaign.sides_full[s]
		
		if len(teams_on_side) > 0:
			i = 0
			output.append("<tr class='row2'><td colspan='5' style='text-align:center;'>Side %d</td></tr>" % s)
			
			for t in teams_on_side:
				i += 1
				
				output.append("""
				<tr class="row{i}">
					<td>{team}</td>
					<td style='padding:0px;'>
						<!--
						<a class="block_link" href="#" onclick="$.get('exec.py', {{mode: 'move_armies', team:{team_id}, campaign:{campaign}, location: ''}}, function () {{$('#ajax_result_{team_id}').html('Moved to location of final battle').val());}}); return false;">Final battle</a>
						-->
						<a class="block_link" href="exec.py?mode=move_armies&team={team_id}&campaign={campaign}">Final battle</a>
					</td>
					<td style='padding:0px;'>
						<a class="block_link" href="#" onclick="$.get('exec.py', {{mode: 'move_armies', team:{team_id}, campaign:{campaign}, location: $('#location_{team_id}').value}}, function () {{$('#ajax_result_{team_id}').html('Moved to ' + $('#location_{team_id}').val());}}); return false;">Location:</a>
					</td>
					<td style="padding:2px;">
						<form action="exec.py" method="post" accept-charset="utf-8" id="team_form_{team_id}">
							<input type="hidden" name="mode" value="move_armies" />
							<input type="hidden" name="team" value="{team_id}" />
							<input type="hidden" name="campaign" value="{campaign}" />
							<input type="text" name="location" id="location_{team_id}" value="" size="6"/>
						</form>
					</td>
					<td id="ajax_result_{team_id}">
						&nbsp;
					</td>
				</tr>
				""".format(
					i = i % 2,
					team_id = t['team'],
					team = team_dict[t['team']].name,
					campaign = campaign_id,
				))
	output.append("</table><!-- PYEND -->")
	
	output.append("</div><!-- PY -->%s<!-- PYEND -->" % common.onload("""
		$('#campaign_info').load('web.py',{'mode':'campaign_info','ajax':'True','campaign':'%d'});
		$('#player_kills').load('web.py',{'mode':'player_kills','ajax':'True','campaign':'%d'});
	""" % (campaign_id, campaign_id)))
	
	if ajax:
		output.append("<br />")
	
	return "".join(output)