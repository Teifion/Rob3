from pages import common
from classes import city
from queries import city_q, building_q
from functions import team_f, building_f
from rules import city_rules

page_data = {
	"Title":	"Edit city",
	"Admin":	True,
}

def main(cursor):
	# Get city Id
	city_id = int(common.get_val('city', 1))
	if city_id < 1: return "No city selected"
	
	# Build city item
	the_city = city_q.get_one_city(cursor, city_id)
	
	# Get buildings list
	building_dict = building_q.get_all_buildings(cursor)
	
	# If we're being sent the info from the view_map page then this is the new location we need
	new_location = common.get_val('location', "")
	
	if new_location == "":
		new_location = "%s,%s" % (the_city.x, the_city.y)# default value
	
	output = []
	
	output.append("""<div style="float: right; width: 50%;">
		<strong>Happiness</strong>
		<div id="happiness">
			
		</div>
	</div>""")
	
	output.append("""<div style='padding: 5px;'>
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_city_commit" />
		<input type="hidden" name="id" id="id" value="%(city_id)s" />
		
		Editing: %(name_text)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="web.py?mode=edit_army&amp;garrison=%(city_id)s">Edit garrison</a>
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="web.py?mode=list_operatives&amp;city=%(city_id)s">Operatives</a>
		<br /><br />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="team">Team:</label></td>
				<td colspan="4" style="padding: 1px;">%(owner_select)s</td>
				
				<td width="5">&nbsp;</td>
				
				<td>&nbsp;</td>
				<td colspan="6">&nbsp;</td>
			</tr>
			<tr>
				<td><label for="size">Size:</label></td>
				<td style="padding: 1px;">%(city_population_text)s</td>
				
				<td width="5">&nbsp;</td>
				
				<td><label for="slaves">Slaves:</label></td>
				<td style="padding: 1px;">%(city_slaves_text)s</td>
				
				<td width="5">&nbsp;</td>
				<td style="padding: 0px;">
					<a class="block_link" href="web.py?mode=view_map&amp;new_mode=edit_city&amp;city=%(city_id)s"">Location:</a>
				</td>
				<td style="padding: 1px;">%(city_location_text)s</td>
				
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><label for="port">Port:</label></td>
				<td>%(city_port_checkbox)s</td>
				
				<td><label for="nomadic">Nomadic:</label></td>
				<td>%(city_nomadic_checkbox)s</td>
				
				<td><label for="dead">Dead:</label></td>
				<td>%(city_dead)s</td>
				
				<td><label for="secret">Secret:</label></td>
				<td>%(city_secret_checkbox)s</td>
				
				<td><label for="founded">Founded:</label></td>
				<td>%(founded_text)s</td>
			</tr>
			<tr>
				<td colspan="10">&nbsp;&nbsp;&nbsp;Description:<br />
					%(city_description_textarea)s
				</td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="city" id="city" value="%(city_id)s" />
		<input type="hidden" name="mode" id="mode" value="remove_city" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete city" onclick="var answer = confirm('Delete %(name_safe)s?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""" % {
		"city_id":						city_id,
		"name":					the_city.name,
		"name_text":				common.text_box("name", the_city.name, size=20),
		"owner_select":					team_f.structured_list(cursor, default=the_city.team, field_name="team"),
		# "city_location_text":			common.text_box("location", "%s,%s" % (the_city.x, the_city.y), 10),
		"city_location_text":			common.text_box("location", new_location, 10),
		
		"city_population_text":			common.text_box("population", the_city.population, 10),
		"city_slaves_text":				common.text_box("slaves", the_city.slaves, 10, warn_on = lambda x:(True if int(x) < 0 else False)),
		"city_port_checkbox":			common.check_box("port", the_city.port),
		"city_dead":					common.text_box("dead", the_city.dead, 5),
		"city_nomadic_checkbox":		common.check_box("nomadic", the_city.nomadic),
		"city_secret_checkbox":			common.check_box("secret", the_city.secret),
		"city_description_textarea":	'<textarea name="description" id="description" rows="4" cols="40">%s</textarea>' % the_city.description,
		
		"founded_text":					the_city.founded,
		
		"name_safe":				common.js_name(the_city.name),
	})
	
	
	#	Buildings
	#----------------------
	the_city.get_buildings(cursor)
	
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Building</th>
		<th>Progress</th>
		<th>Amount</th>
		<th>&nbsp;</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	counter = -1
	building_remove_list = []
	for building_id, completion in the_city.buildings.items():
		counter += 1
		
		building_remove_list.append(building_id)
		
		output.append("""
		<tr class="row%(row)d">
			<form id="b_%(building_id)s" action="exec.py" method="get" accept-charset="utf-8">
				<input type="hidden" name="mode" value="set_building" />
				<input type="hidden" name="city" value="%(city_id)s" />
				<input type="hidden" name="building" value="%(building_id)s" />
				<td><label for="%(building_name)s">%(building_name)s</label></td>
				<td style="padding: 1px;">
					%(building_completion_text)s/%(building_build_time)s
				</td>
				<td style="padding: 1px;">
					%(building_amount_text)s
				</td>
				<td style="padding: 0px;">
					<!--<a class="block_link" href="#" onclick="$('#b_%(building_id)s').submit();">Edit</a>-->
					<input type="submit" value="Edit" />
				</td>
				<td style="padding: 0px;">
					<a class="block_link" href="exec.py?mode=set_building&amp;building=%(building_id)d&amp;city=%(city_id)d&amp;completion=0&amp;amount=0">Remove</a>
				</td>
			</form>
		</tr>""" % {'row':						(counter % 2),
					'building_name':			building_dict[building_id].name,
					'building_id':				building_id,
					'building_build_time':		building_dict[building_id].build_time,
					'city_id':					city_id,
					"building_completion_text":	common.text_box("completion", the_city.buildings[building_id], size=4),
					"building_amount_text":		common.text_box("amount", the_city.buildings_amount[building_id], size=3),
					})
	
	output.append("""
		<tr class="row%(row)d">
		<form id="city_add_building_form" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="set_building" />
			<input type="hidden" name="city" value="%(city_id)s" />
			<td style="padding:1px;">
				<select id="new_building" name="building" onchange="$('#building_completion_span').load('web.py', {mode: 'get_building_build_time', building: document.getElementById('new_building').value, ajax:'True'});">
					%(building_option_box)s
				</select>
			</td>
			<td style="padding:1px;">
				%(building_completion_text)s/<span id="building_completion_span">000</span>
			</td>
			<td style="padding:1px;">
				%(building_amount_text)s
			</td>
			<td style="padding: 0px;" colspan="2">
				<input type="submit" value="Add" />
				<!--<a href="#" onclick="$('#city_add_building_form').submit();" class="block_link">Add</a>-->
			</td>
		</tr>
		</form>
	</table>
	%(onload)s
	""" % {	'row':						((counter+1) % 2),
			'city_id':					the_city.id,
			'building_option_box':		building_f.building_option_list(cursor, building_remove_list),
			"building_completion_text":	common.text_box("completion", 0, size=4),
			"building_amount_text":		common.text_box("amount", 0, size=3),
			"onload":					common.onload("$('#new_building').focus();"),
			})
	
	output.append(common.onload("$('#building_completion_span').load('web.py', {mode: 'get_building_build_time', building: document.getElementById('new_building').value, 'ajax':1});"))
	
	output.append("<strong>Wonder construction speed</strong>")
	output.append("<ul>")
	
	# Work out city points
	cities_dict = city_q.get_cities_from_team(cursor, the_city.team)
	total_points = 0
	for city_id2, city2 in cities_dict.items():
		if city2.team != the_city.team: continue
		if city2.dead == True: continue
		
		points = city_rules.wonder_build_rate(city2, the_city)
		if points > 0:
			output.append("<li>%s: %s</li>" % (city2.name, points))
			total_points += points
	
	output.append("<li><em>Total: %s</em></li>" % total_points)
	output.append("</ul>")
	
	output.append(common.onload("$('#happiness').load('web.py', {'mode':'happiness_breakdown','city':'%d', 'ajax':'True'});" % int(the_city.id)))
	
	# output.append('''<img src="%simages/grid_25.png" width="0" height="0" onload="">''' % common.data['media_path'])
	output.append("</div>")
	
	page_data['Title'] = "Edit city (%s)" % the_city.name
	return "".join(output)

