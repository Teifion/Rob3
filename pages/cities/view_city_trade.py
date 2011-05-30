import math
from pages import common
from queries import city_q, mapper_q, team_q, tech_q
from rules import sad_rules

page_data = {
	"Title":	"TODO",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	# Get city Id
	city_id = int(common.get_val('city', 1))
	if city_id < 1: return "No city selected"
	
	# Build city item
	the_city = city_q.get_one_city(cursor, city_id)
	the_team = team_q.get_one_team(cursor, the_city.team)
	tech_dict = tech_q.get_all_techs(cursor)
	
	output.append("""
	<div style="padding:5px;">
	<span class="stitle">{name}</span><br />
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Resource</th>
			<th>Supply</th>
			<th>Demand</th>
		</tr>""".format(
			name = the_city.name,
		))
	
	terrain = mapper_q.get_terrain(cursor, the_city.x, the_city.y)
	team_techs = the_team.get_techs(cursor)[0]
	techs = {}
	for k, v in team_techs.items():
		techs[tech_dict[k].name] = v
	
	for i, r in enumerate(sad_rules.res_list):
		supply = round(sad_rules.supply[r](city=the_city, terrain=terrain, techs=techs), 2)
		demand = round(sad_rules.demand[r](city=the_city, terrain=terrain, techs=techs), 2)
		
		output.append("""
		<tr class="row{i}">
			<td>{res}</td>
			
			<td>{supply}</td>
			<td>{demand}</td>
		</tr>""".format(
			i = i % 2,
			res = r,
			supply = supply,
			demand = demand,
		))
		
	page_data['Title'] = "City trade (%s)" % the_city.name
	output.append("</table></div>")
	return "".join(output)