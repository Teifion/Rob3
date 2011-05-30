import math
from pages import common
from queries import city_q
from rules import city_rules
from classes import city

page_data = {
	"Title":	"City list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	
	text_location = common.get_val('location', "")
	
	if team_id < 1:
		return "<div style='padding: 5px;'>{0}</div>".format(common.select_team_form(cursor, 'list_cities'))
	
	cities_dict = city_q.get_cities_from_team(cursor, team = team_id, include_dead = True)
	
	# Work out city points
	total_points = 0
	for city_id, the_city in cities_dict.items():
		if the_city.dead == True: continue
		total_points += the_city.point_value()
	
	output = []
	
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>City name</th>
			<th colspan="3">Location</th>
			<th>Port</th>
			<th>Secret</th>
			<th>Dead</th>
			<th>Nomadic</th>
			
			<th>Overlap</th>
			
			<th>Wonder speed</th>
			<th>Population</th>
			<th>Slaves</th>
			<th>Happiness</th>
			
			<th colspan="2">&nbsp;</th>
		</tr>""")
	
	# Work out how fast it can build wonders
	city_wonder_speed = {}
	for c1, city1 in cities_dict.items():
		city_wonder_speed[c1] = math.floor((city1.population + city1.slaves)/1000)
		c1_loc = (cities_dict[c1].x, cities_dict[c1].y)
		
		for c2, city2 in cities_dict.items():
			if city2.dead: continue
			
			if c2 != c1:
				amount = city_rules.wonder_build_rate(city2, city1)
				city_wonder_speed[c1] += amount
		
		city_wonder_speed[c1] = common.number_format(int(city_wonder_speed[c1]))
	
	count = -1
	if len(cities_dict) > 0:
		for city_id, the_city in cities_dict.items():
			count += 1
			
			city_share = 0
			if not the_city.dead:
				if total_points > 0:
					city_share = round(the_city.point_value()/total_points*100,1)
			
			# Happiness
			happiness = city.happiness_str(the_city.happiness)
			
			if happiness == "Rebellious":
				happiness = '<span style="font-weight:bold;color:#A00;">Rebellious</span>'
			
			if happiness == "Utopian":
				happiness = '<span style="font-weight:bold;color:#0A0;">Utopian</span>'
			
			output.append("""
			<tr class="row%(row)d" id="%(city_id)d">
				<td>%(name)s</td>
		
				<td>%(x)s</td>
				<td>%(y)s</td>
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=view_map&amp;%(map_link)s">Map link</a></td>
				
				<td style="text-align: center;">%(port)s</td>
				<td style="text-align: center;">%(secret)s</td>
				<td style="text-align: center;">%(dead)s</td>
				<td style="text-align: center;">%(nomadic)s</td>
				
				<td>%(overlap)s</td>
				
				<td>%(wonder_speed)s</td>
				<td>%(population)s</td>
				<td>%(slaves)s</td>
				
				<td>%(happiness)s</td>
				
				<!--<td style="padding: 0px;"><a class="block_link" href="web.py?mode=view_city_trade&amp;city=%(city_id)d">City trade</a></td>-->
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=view_city_matrix&amp;city=%(city_id)d">City matrix</a></td>
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_city&amp;city=%(city_id)d">Edit city</a></td>
			</tr>
			""" % {	'row': (count % 2),
			
					'city_id': the_city.id,
					'name': common.doubleclick_text("cities", "name", the_city.id, the_city.name, "font-weight:bold"),
					'x': common.doubleclick_text("cities", "x", the_city.id, the_city.x, ""),
					'y': common.doubleclick_text("cities", "y", the_city.id, the_city.y, ""),
					"map_link":	the_city.map_link_args(),
					
					'port': common.bstr(the_city.port),
					'secret': common.bstr(the_city.secret),
					'dead': "" if the_city.dead < 1 else common.doubleclick_text("cities", "dead", the_city.id, the_city.dead, "", size=3),
					'nomadic': common.bstr(the_city.nomadic),
				
					'overlap': the_city.overlap,
				
					'population': common.doubleclick_text("cities", "population", the_city.id, the_city.population, ""),
					'slaves': common.doubleclick_text("cities", "slaves", the_city.id, the_city.slaves, ""),
				
					"wonder_speed": city_wonder_speed[the_city.id],
					"happiness":	happiness,
				})


	# Add new city
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_city_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_city" />
		<input type="hidden" name="team" value="%(team_id)s" />
		<td style="padding: 1px;"><input type="text" name="name" id="new_name" value="" /></td>
		<td style="padding: 0px;" colspan="2">
			<a href="web.py?mode=view_map&amp;new_mode=list_cities&amp;team=%(team_id)s" class="block_link">Location:</a>
		</td>
		<td colspan="1" style="padding:1px;">
			%(location)s
		</td>
		<td style="padding: 2px;"><input type="checkbox" name="port" value="True" /></td>
		<td style="padding: 2px;"><input type="checkbox" name="secret" value="True" /></td>
		<td style="padding: 2px;"><input type="text" name="dead" id="dead" value="0" size="3"/></td>
		<td style="padding: 2px;"><input type="checkbox" name="nomadic" value="True" /></td>
	
		<td>&nbsp;</td>
		
		<td>&nbsp;</td>
	
		<td style="padding: 1px;"><input type="text" name="population" value="" size="10"/></td>
		<td style="padding: 1px;"><input type="text" name="slaves" value="" size="10"/></td>
	
		<td style="padding: 2px;" colspan="3"><input type="submit" value="Add" /></td>
		<!--
		<td style="padding: 0px;" colspan="3"><a class="block_link" href="#" onclick="$('#add_city_form').submit();">Add</a></td>
		-->
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),

			"team_id":	team_id,
			"location": common.text_box("text_location", text_location, custom_id="", size="7"),
			"onload":	common.onload("$('#new_name').focus();"),
			})


	output.append("</table>")

	return "".join(output)