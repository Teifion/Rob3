import math
from pages import common
from queries import city_q, team_q
from rules import sad_rules

page_data = {
	"Title":	"Ctiy matrix",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	city_id = int(common.get_val('city', 1))
	if city_id < 1: return "No city selected"
	
	# Build city item
	team_dict = team_q.get_all_teams(cursor)
	city_dict = city_q.get_live_cities(cursor)
	if city_id not in city_dict:
		return "You must select live cities"
	
	the_city = city_dict[city_id]
	
	output.append("""
	<div style="padding:5px;">
	<span class="stitle">{name}</span><br />
	<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Partner</th>
			<th colspan="2">Distance</th>
		</tr>""".format(
			name = the_city.name,
		))
	
	query = """SELECT city_2, distance FROM trade_distances WHERE city_1 = %d ORDER BY distance ASC""" % city_id
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for i, row in enumerate(cursor):
		if city_dict[row['city_2']].team == the_city.team:
			style = "color: #070;font-weight:bold;"
		else:
			style = "color: #007;"
			
		tr_row = i % 2
		
		output.append("""
		<tr class="row{tr_row}">
			<td><a class="clear_link" href="web.py?mode=view_city_matrix&amp;city={partner_id}">{partner}</a> (<em style="{style}">{team}</em>)</td>
			<td>{distance}</td><td><em>{real_distance}</em></td>
		</tr>
		""".format(
			tr_row = tr_row,
			style = style,
			partner_id = row['city_2'],
			partner = city_dict[row['city_2']].name,
			team = team_dict[city_dict[row['city_2']].team].name,
			
			distance = row['distance'],
			real_distance = int(sad_rules.reverse_trade_distance(row['distance'])),
		))
	
	page_data['Title'] = "City matrix (%s)" % the_city.name
	output.append("</table></div>")
	return "".join(output)