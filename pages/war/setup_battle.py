from pages import common
from classes import battle
from queries import battle_q, city_q, campaign_q, team_q, army_q, squad_q

page_data = {
	"Title":	"Setup battle",
	"Admin":	True,
}

def main(cursor, battle_id = -1):
	battle_id = int(common.get_val('battle', battle_id))
	
	if battle_id < 1:
		return "No battle selected"
	
	the_battle = battle_q.get_one_battle(cursor, battle_id)
	
	# If we're being sent the info from the view_map page then this is the new location we need
	new_location = common.get_val('location', "")
	
	if new_location == "":
		new_location = "%s,%s" % (the_battle.x, the_battle.y)# default value
	
	# Get some other stuff
	cities_dict		= city_q.get_live_cities(cursor)
	team_dict		= team_q.get_all_teams(cursor)
	the_campaign	= campaign_q.get_one_campaign(cursor, the_battle.campaign)
	
	names = {0:"No city"}
	for c, the_city in cities_dict.items():
		names[c] = the_city.name
	
	city_keys = [0]
	city_keys.extend(list(cities_dict.keys()))
	
	output = ["<div style='padding: 5px;'>"]
	
	# output.append('<a href="web.py?mode=perform_battle&amp;battle={0}" class="block_link">Perform</a>'.format(battle_id))
	output.append("""
	<a href="web.py?mode=list_campaigns&amp;turn={turn}" class="block_link" style="display:inline; text-align:left;">Campaigns of this turn</a>
	<a href="web.py?mode=setup_campaign&amp;campaign={campaign_id}" class="block_link" style="display:inline;">Setup campaign</a>
	<a href="web.py?mode=list_battles&amp;campaign={campaign_id}" class="block_link" style="display:inline;">List battles</a>
	<a href="web.py?mode=perform_battle&amp;battle={battle_id}" class="block_link" style="display:inline;">Perform</a>
	<br /><br />
	<!-- PY -->
	<form action="exec.py" method="post" accept-charset="utf-8">
	<!-- PYEND -->
		<input type="hidden" name="mode" value="edit_battle_commit" />
		<input type="hidden" name="id" value="{battle_id}" />
		<input type="hidden" name="campaign" value="{campaign_id}" />
		
		Editing: {name_text}
		<br /><br />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="start">Start:</label></td>
				<td style="padding: 1px;">{battle_start_text}</td>
				
				<td width="5">&nbsp;</td>
				
				<td><label for="duration">Duration:</label></td>
				<td style="padding: 1px;">{battle_duration_text}</td>
			</tr>
			<tr>
				<td style="padding: 0px;">
					<a class="block_link" href="web.py?mode=view_map&amp;new_mode=setup_battle&amp;battle={battle_id}"">Location:</a>
				</td>
				<td style="padding: 1px;">{battle_location_text}</td>
				
				<td>&nbsp;</td>
				<td><label for="city">City:</label></td>
				<td style="padding: 1px;">{city_menu}</td>
			</tr>
			<tr>
				<td><label for="type">Type:</label></td>
				<td style="padding: 1px;">{type}</td>
				
				<td>&nbsp;</td>
				
				<td><label for="result">Result:</label></td>
				<td style="padding: 1px;">{result}</td>
			</tr>
		</table>
		<!-- PY -->
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<!-- PYEND -->
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="battle" id="battle" value="{battle_id}" />
		<input type="hidden" name="mode" id="mode" value="remove_battle" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete battle" onclick="var answer = confirm('Delete {esc_name}?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""".format(
		turn					= common.current_turn(),
		battle_id =				battle_id,
		campaign_id = 			the_battle.campaign,
		name =					the_battle.name,
		esc_name =				common.js_name(the_battle.name),
		name_text =				common.text_box("name", the_battle.name, size=20),
		battle_location_text	= common.text_box("location", new_location, 10),
		battle_start_text		= common.text_box("start", the_battle.start, 3),
		battle_duration_text	= common.text_box("duration", the_battle.duration, 3),
		city_menu				= common.option_box(
			name='city',
			elements=names,
			element_order=city_keys,
			custom_id="",
			selected=the_battle.city,
		),
		
		type = common.option_box("type", elements = battle.battle_types, element_order = [], selected=battle.battle_types[the_battle.type]),
		result = common.option_box("result", elements = battle.result_types, element_order = [], selected=battle.result_types[the_battle.result]),
	))
	
	output.append("</div>")
	
	return "".join(output)