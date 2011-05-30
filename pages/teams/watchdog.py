from pages import common
from rules import team_rules
from queries import team_q
# from data import team, team_q
# from rules import team_rules

page_data = {
	"Name":		"list_teams",
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	show_dead_teams		= common.get_val('show_dead')
	show_unqueued_teams	= common.get_val('show_unqueued')
	
	# Get the turn we'll want to get stuff for
	current_turn = common.current_turn()
	
	# Get our list
	team_dict = team_q.get_real_active_teams(cursor, skip_irs=True)
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Team</th>
			<th>Materials</th>
			<th>Food</th>
			<th>Morale</th>
		</tr>""")
	
	count = -1
	for team_id, the_team in team_dict.items():
		count += 1
		
		team_res = the_team.get_resources(cursor)
		
		# TODO - Make it work out the material requirements correctly
		# Materials
		material_amount = int(team_res.get("Materials"))
		if material_amount < 0:
			material_style = "background-color:#AAA;color:#A00; font-weight:bold;"
			if material_amount < -200:
				material_style = "background-color:#000;color:#F00; font-weight:bold;"
		else:
			material_style = ""
		
		# Food
		food_amount = int(team_res.get("Food"))
		needed = team_rules.resource_needed(cursor, "Food", the_team)
		food_ratio = round(food_amount/float(needed), 2)
		
		if food_ratio < 1:
			food_style = "background-color:#AAA;color:#A00; font-weight:bold;"
			if food_ratio < 0.75:
				food_style = "background-color:#000;color:#F00; font-weight:bold;"
		else:
			food_style = ""
			if food_ratio > 1.5:
				food_style = "background-color:#AFA;color:#000; font-weight:bold;"
		
		output.append("""
		<tr class="row%(row)d" id="%(team_id)d">
			<td>%(name)s</td>
			<td style="%(material_style)s">%(materials)s</td>
			<td style="%(food_style)s">%(food)s</td>
			<td>%(morale)s</td>
		</tr>
		""" % {
				'row': (count % 2),
				'board_url': common.data['board_url'],
				
				'team_id':			the_team.id,
				'name':		the_team.name,
				"materials":		material_amount,
				"material_style":	material_style,
				"food":				food_ratio,
				"food_style":		food_style,
				
				"morale":			team_rules.define_nation_morale(team_rules.nation_morale(cursor, the_team)),
		})
	
	output.append("</table>")
	
	return "".join(output)