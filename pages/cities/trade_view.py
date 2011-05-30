from queries import city_q, mapper_q
from functions import trade_f
from rules import sad_rules, map_data

page_data = {
	"Title":	"Trade preview",
	"Admin":	True,
	"CSS":		".sideNav{display:none;}.content{margin-right:0;}",
}

# Output using webkit2png
# webkit2png -W 1600 -H 300 -o trade_view.png -F http://localhost/rob3/web.py?mode=trade_view

def approx(n):
	if n < 1000:		return 1000
	if n < 10000:		return int(round(n, -3))
	if n < 100000:		return int(round(n, -4))
	if n < 1000000:		return int(round(n, -4))
	if n < 10000000:	return int(round(n, -5))
	if n < 100000000:	return int(round(n, -6))

def main(cursor):
	output = []
	
	city_list = (
	# Aracnia
	1215,
	
	# Holm
	830,
	
	# Chiark (Crown)
	849,
	
	# Reeth (Dan)
	62,
	
	# Wetworks (Exion)
	1221,
	
	# Cassel (HEM)
	1058,
	
	# Sierlith (Luprasic)
	595,
	)
	city_dict = city_q.get_all_cities(cursor)
	
	output.append("""<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>City</th>
			<th>Terrain</th>
			<th>&nbsp;</th>
			<th colspan='2'>
				{cols}
			</th>
		</tr>""".format(
			cols = "</th><th>&nbsp;</th><th colspan='2'>".join(sad_rules.res_list),
		))
	
	for i, c in enumerate(city_list):
		the_city = city_dict[c]
		
		the_city.size = approx(the_city.size)
		
		terrain = mapper_q.get_terrain(cursor, the_city.x, the_city.y)
		techs = {}
		
		cols = []
		for r in sad_rules.res_list:
			s = round(sad_rules.supply[r](city=the_city, terrain=terrain, techs=techs), 2)
			d = round(sad_rules.demand[r](city=the_city, terrain=terrain, techs=techs), 2)
			
			cols.append("<td style='text-align:center;'>%s</td>" % s)
			cols.append("<td style='text-align:center;'>%s</td>" % d)
			cols.append("<td>|</td>")
		
		cols.pop()
		
		output.append("""
		<tr class="row{i}">
			<td>{name} ({size}k)</td>
			<td>{terrain}</td>
			<td>|</td>
			{cols}
		</tr>
		""".format(
			i = i%2,
			name = the_city.name,
			size = int(the_city.size/1000),
			terrain = map_data.terrain[terrain].title(),
			cols = "".join(cols),
		))
	
	output.append("</table>")
	
	return "".join(output)