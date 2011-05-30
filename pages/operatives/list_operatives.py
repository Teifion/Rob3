from pages import common
from queries import team_q, city_q, operative_q

page_data = {
	"Title":	"Operative list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	city_id = int(common.get_val('city', 0))
	
	if team_id < 1 and city_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'list_operatives')
	
	# Handles for later
	city_dict = city_q.get_all_cities(cursor)
	team_dict = team_q.get_all_teams(cursor)
	
	# Build team
	the_team = team_dict[team_id]
	
	if team_id > 0:
		operatives_dict = operative_q.get_operatives_from_team(cursor, team=team_id)
	elif city_id > 0:
		operatives_dict = operative_q.get_operatives_from_city(cursor, city=city_id)
	
	# So we can sort them by team
	team_location = {}
	for o, the_op in operatives_dict.items():
		o_team = city_dict[the_op.city].team
		if o_team not in team_location:
			team_location[o_team] = []
		
		team_location[o_team].append(o)
	
	output = []
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Id</th>
			<th>Size</th>
			
			<th>Stealth</th>
			<th>Observation</th>
			<th>Integration</th>
			<th>Sedition</th>
			<th>Sabotage</th>
			<th>Assassination</th>
			
			<th>Location</th>
			<th>Arrival</th>
			
			<th>&nbsp;</th>
			<th>&nbsp;</th>
		</tr>""")
	
	count = -1
	if len(operatives_dict) > 0:
		for city_team, op_list in team_location.items():
			for operative_id, the_operative in operatives_dict.items():
				
				if the_operative.id not in op_list:
					continue
				
				count += 1
				
				# Is it dead?
				if the_operative.died == 0:
					life_action = '<a href="exec.py?mode=kill_operative&amp;operative=%d" class="block_link">Kill</a>' % operative_id
					
					life_action = '''<a href="#" class="block_link" onclick="$.get('exec.py', {mode: 'kill_operative', operative:%d}, function () {$('#life_%d').html('<div class=\\'block_link\\'>Killed</div>');}); return false;">Kill</a>''' % (operative_id, operative_id)
				else:
					life_action = '<a href="exec.py?mode=revive_operative&amp;operative=%d" class="block_link">Revive (%d)</a>' % (operative_id, the_operative.died)
					
					life_action = '''<a href="#" class="block_link" onclick="$.get('exec.py', {mode: 'revive_operative', operative:%d}, function () {$('#life_%d').html('<div class=\\'block_link\\'>Revived</div>');}); return false;">Revive (%d)</a>''' % (operative_id, operative_id, the_operative.died)
				
				output.append("""
				<tr class="row{row}" id="{operative_id}">
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
					
					<td style="padding: 0px;" id="life_{operative_id}">{life_action}</td>
				
					<td style="padding: 0px;"><a href="web.py?mode=edit_operative&amp;operative={operative_id}" class="block_link">Edit</a></td>
				</tr>
				""".format(
						row = (count % 2),
						
						team_id			= team_id,
						operative_id	= operative_id,
						name		= common.doubleclick_text("operatives", "name", operative_id, the_operative.name, "font-weight:bold"),
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
						
						life_action	= life_action,
		))
	
	# Add unit type
	city_dict = city_q.get_live_cities(cursor)
	names = {}
	for c, the_city in city_dict.items():
		names[c] = the_city.name
	
	if count <= 20:
		onload = common.onload("$('#size').focus();")
	else:
		onload = ''
	
	count += 1
	if team_id > 0:
		output.append("""
		<tr class="row%(row)d">
			<form action="exec.py" method="post" id="new_operative_form" accept-charset="utf-8">
			<input type="hidden" name="mode" value="create_new_operative" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<td style="padding: 1px;">
				<input type="text" name="name" id="name" value="" size="6"/>
			</td>
		
			<td style="padding: 1px;">
				<input type="text" name="size" id="size" value="1" size="3"/>
			</td>
		
			<td style="padding: 1px;">
				<input type="text" name="stealth" id="stealth" value="1" size="3"/>
			</td>
			<td style="padding: 1px;">
				<input type="text" name="observation" id="observation" value="1" size="3"/>
			</td>
			<td style="padding: 1px;">
				<input type="text" name="integration" id="integration" value="1" size="3"/>
			</td>
			<td style="padding: 1px;">
				<input type="text" name="sedition" id="sedition" value="1" size="3"/>
			</td>
			<td style="padding: 1px;">
				<input type="text" name="sabotage" id="sabotage" value="1" size="3"/>
			</td>
			<td style="padding: 1px;">
				<input type="text" name="assassination" id="assassination" value="1" size="3"/>
			</td>
		
			<td style="padding: 1px;">%(location)s</td>
			<td style="padding: 1px;"><input type="text" name="arrival" id="arrival" value="%(arrival)s" size="4"/></td>
			<td colspan="2" style="padding: 0px;"><a class="block_link" onclick="$('#new_operative_form').submit(); return false;" href="#">Add</a></td>
			%(onload)s
			</form>
		</tr>
		""" % {	'row': (count % 2),

				"team_id":		team_id,
				'location':		common.option_box(
					name='city',
					elements=names,
					element_order=city_dict.keys(),
					custom_id="",
				),
				"arrival":	common.current_turn(),
				'onload':	onload,
				})
	
	output.append("</table>")
	
	if team_id > 0:
		page_data['Title'] = "List operatives from %s" % team_dict[team_id].name
	elif city_id > 0:
		page_data['Title'] = "List operatives from %s (%s)" % (city_dict[city_id].name, team_dict[city_dict[city_id].team].name)
	
	return "".join(output)