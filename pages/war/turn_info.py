from pages import common
from queries import campaign_q, battle_q, team_q, city_q
from functions import path_f

page_data = {
	"Title":	"Turn info",
	"Admin":	True,
}

def main(cursor):
	return ""
	
	output = ["""<div style="padding: 5px;">"""]
	
	ajax = common.get_val('ajax', 0)
	
	if not ajax:
		page_data['Headers'] = False
	
	battle_dict		= battle_q.get_battles_from_turn(cursor, common.current_turn())
	team_dict		= team_q.get_all_teams(cursor)
	city_dict		= city_q.get_all_cities(cursor)
	
	output.append("""<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Battle</th>
			<th>Time</th>
			<th>Location</th>
		</tr>""")
	
	# Display battles
	i = -1
	for battle_id, the_battle in battle_dict.items():
		i += 1
		
		location = "%d, %d" % (the_battle.x, the_battle.y)
		
		if i == 0:
			days_since = ""
			time_taken = ""
			distance = ""
		else:
			waypoints = ((last_battle.x, last_battle.y), (the_battle.x, the_battle.y))
			b_path = path_f.path(cursor, waypoints, move_speed="Marching", move_type="Medium foot")
			
			
			days_since = "Days since last battle: {0}".format(the_battle.start - last_battle.ended)
			time_taken = "Time taken to travel: {0} days".format(b_path.time_cost)
			distance = "Distance from last battle: {0}km".format(format(b_path.walk_distance, ','))
		
		output.append("""
		<tr class="row0">
			<td><strong>{name}</strong></td>
			<td>{start} : {ended}</td>
			<td>{location}</td>
		</tr>
		<tr class="row1">
			<td colspan="3">
				{days_since}<br />
				{time_taken}<br />
				{distance}<br />
			</td>
		</tr>
		""".format(
			i=i%2,
			
			name=the_battle.name,
			start=the_battle.start,
			ended=the_battle.ended,
			location=location,
			
			days_since = days_since,
			time_taken = time_taken,
			distance = distance,
			
			id=battle_id,
		))
		
		
		# Use this to record stuff for the next battle
		last_battle = the_battle
	
	
	
	
	output.append("</table></div>")
	
	return "".join(output)
