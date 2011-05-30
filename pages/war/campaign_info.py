from pages import common
from queries import campaign_q, battle_q, team_q, city_q
from functions import path_f

page_data = {
	"Title":	"Campaign info",
	"Admin":	True,
}

def main(cursor):
	output = ["""<div style="padding: 5px;">"""]
	campaign_id = int(common.get_val('campaign', 0))
	ajax = common.get_val('ajax', 0)
	
	# Used to let us know if there is an issue with the campaign
	errors = False
	
	if campaign_id < 1:
		return "No campaign selected"
	
	if not ajax:
		page_data['Headers'] = False
	
	the_campaign	= campaign_q.get_one_campaign(cursor, campaign_id)
	battle_dict		= battle_q.get_battles_from_campaign(cursor, campaign_id)
	team_dict		= team_q.get_all_teams(cursor)
	city_dict		= city_q.get_all_cities(cursor)
	
	
	output.append("""<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Battle</th>
			<th>Time</th>
			<th>Location</th>
			<th colspan="4">&nbsp;</th>
		</tr>""")
	
	# Display battles
	i = -1
	total_waypoints = []
	for battle_id, the_battle in battle_dict.items():
		i += 1
		
		location = "%d, %d" % (the_battle.x, the_battle.y)
		
		total_waypoints.append((the_battle.x, the_battle.y))
		
		if i == 0:
			days_since = ""
			time_taken = ""
			distance = ""
			
			path_map_link = "&nbsp;"
		else:
			waypoints = ((last_battle.x, last_battle.y), (the_battle.x, the_battle.y))
			b_path = path_f.path(cursor, waypoints, move_speed="Marching", move_type="Medium foot")
			w_path = path_f.path(cursor, waypoints, move_speed="Sailing", move_type="Sail")
			
			if w_path != None:
				if b_path.time_cost > w_path.time_cost:
					b_path = w_path
			
			days_since = "Days since last battle: {0}".format(the_battle.start - (last_battle.start + last_battle.duration))
			time_taken = "Time taken to travel: {0} days".format(int(b_path.time_cost))
			distance = "Distance from last battle: {0}km".format(format(b_path.walk_distance, ','))
			
			# Formatting for time taken?
			if b_path.time_cost > (the_battle.start - (last_battle.start + last_battle.duration)):
				time_taken = "<span class='neg' style='font-weight:bold;'>%s</span>" % time_taken
				days_since = "<span class='neg' style='font-weight:bold;'>%s</span>" % days_since
				errors = True
			
			points = str(waypoints).replace('(', '').replace(')', '')#.replace(',', '%2C')
			path_map_link = '<a href="web.py?mode=path_map&amp;points=%s&amp;move_speed=Marching&amp;move_type=Medium foot" class="block_link">Path link</a>' % points
		
		# Battle start
		start_str = the_battle.start
		dur_str = the_battle.duration
		if (the_battle.start + the_battle.duration) > 365:
			start_str = '<span class="neg" style="font-weight:bold;">%s</span>' % the_battle.start
			dur_str = '<span class="neg" style="font-weight:bold;">%s</span>' % the_battle.duration
			errors = True
		
		output.append("""
		<tr class="row0">
			<td><strong>{name}</strong></td>
			<td>{start} : {duration}</td>
			<td>{location}</td>
			
			<td width="5">&nbsp;</td>
			
			<td colspan="3">
				&nbsp;
			</td>
		</tr>
		<tr class="row1">
			<td colspan="3">
				{days_since}<br />
				{time_taken}<br />
				{distance}<br />
			</td>
			
			<td width="5">&nbsp;</td>
			
			<td colspan="3" style="padding:0px;">
				{path_map_link}
			</td>
		</tr>
		""".format(
			i=i%2,
			
			name=the_battle.name,
			start=start_str,
			duration=dur_str,
			location=location,
			
			days_since = days_since,
			time_taken = time_taken,
			distance = distance,
			
			path_map_link = path_map_link,
			
			id=battle_id,
		))
		
		
		# Use this to record stuff for the next battle
		last_battle = the_battle
	
	if errors:
		error_str = "ERRORS FOUND"
	else:
		error_str = ""
	
	points = str(tuple(total_waypoints)).replace('(', '').replace(')', '')#.replace(',', '%2C')
	output.append("""
	<tr class="row0">
		<td colspan="3" style="font-weight:bold;font-size:1.5em;text-align:center;color:#F00;padding:10px;">
			{error_str}
		</td>
		<td>&nbsp;</td>
		<td colspan="3" style="padding:0px;">
			{path_link}
		</td>
	</tr>""".format(
		path_link = '<a href="web.py?mode=path_map&amp;points=%s&amp;move_speed=Marching&amp;move_type=Medium foot" class="block_link">Path link</a>' % points,
		error_str = error_str,
	))
	
	
	output.append("</table>")
	output.append("</div>")
	
	return "".join(output)
