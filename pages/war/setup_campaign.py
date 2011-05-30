from pages import common
from queries import campaign_q, team_q, army_q, battle_q, city_q
from functions import team_f
from classes import city

page_data = {
	"Title":	"Edit campaign",
	"Admin":	True,
}

def grab_armies(cursor, coords, radius):
	result = city.city_coords.search(coords)
	if result != None:
		x = int(result.groups()[0])
		y = int(result.groups()[1])
	else:
		raise Exception("No match found on '%s'" % coords)
	
	# Copied from spy_world.Spy_world
	cities_in_area = []
	armies_in_area = []
	
	# Get cities in the area
	query = """SELECT id FROM cities
		WHERE x > {minx} AND x < {maxx}
			AND y > {miny} AND y < {maxy} AND dead < 1""".format(
		minx = x - radius,
		maxx = x + radius,
		miny = y - radius,
		maxy = y + radius,
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		cities_in_area.append(row['id'])
	
	# Now for armies
	if len(cities_in_area) > 0:
		sql_extra = "OR garrison IN (%s)" % ",".join([str(c) for c in cities_in_area])
	else:
		sql_extra = ""
	
	# Get armies query
	query = """SELECT name FROM armies
		WHERE x > {minx} AND x < {maxx}
			AND y > {miny} AND y < {maxy} {sql_extra}""".format(
		minx = x - radius,
		maxx = x + radius,
		miny = y - radius,
		maxy = y + radius,
		sql_extra = sql_extra,
	)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		armies_in_area.append(row['name'])
	
	return "\n".join(armies_in_area)
	# 578, 1371

def main(cursor, campaign_id=-1):
	output = ['<div style="padding: 5px;">']
	
	grab_coords = common.get_val('coords', '')
	radius = int(common.get_val('radius', 10))
	
	if grab_coords != '' and radius > 0:
		# 138, 1224
		grabbed_armies = grab_armies(cursor, grab_coords, radius)
	else:
		grabbed_armies = ""
	
	campaign_id = int(common.get_val('campaign', campaign_id))
	if campaign_id < 1:
		return "No city selected"
	
	# Get stuff from DB
	the_campaign = campaign_q.get_one_campaign(cursor, campaign_id)
	team_dict = team_q.get_all_teams(cursor)
	city_dict = city_q.get_cities_for_dropdown(cursor)
	battle_dict = battle_q.get_battles_from_campaign(cursor, campaign_id)
	
	if len(battle_dict) < 1:
		return common.redirect("web.py?mode=list_battles&campaign=%d" % campaign_id)
	
	# last_battle = battle_dict[list(battle_dict.keys())[-1]]
	last_battle = battle_q.get_last_battle_from_campaign(cursor, campaign_id)
	if not last_battle:
		return common.redirect("web.py?mode=list_battles&campaign=%d" % campaign_id)
	
	# coords_cities
	coords_cities = ['<select name="coords">']
	for city_id, the_city in city_dict.items():
		if city_id == last_battle.city:
			coords_cities.append("<option value='%s,%s' selected='selected'>%s</option>" % (the_city.x, the_city.y, the_city.name))
		else:
			coords_cities.append("<option value='%s,%s'>%s</option>" % (the_city.x, the_city.y, the_city.name))
	
	coords_cities.append("</select>")
	coords_cities = "".join(coords_cities)
	
	output.append("""
	<a href="web.py?mode=list_campaigns&amp;turn={turn}" class="block_link" style="display:inline; text-align:left;">Campaigns of this turn</a>
	<a href="web.py?mode=list_battles&amp;campaign={id}" class="block_link" style="display:inline;">List battles</a>
	<a href="web.py?mode=perform_battle&amp;battle={last_battle}" class="block_link" style="display:inline;">Last battle</a>
	<br /><br />
	<form action="exec.py" id="mass_add_army_form" method="post" accept-charset="utf-8" style="display:block; float:right; border: 0px solid #000; margin-right:20px;">
		<strong>Mass add units</strong><br />
		<input type="hidden" name="mode" value="mass_add_armies" />
		<input type="hidden" name="campaign" value="{id}" />
		{team_list}
		<br />
		<textarea name="army_names" rows="10" cols="40">{grabbed_armies}</textarea>
		<br />
		<input type="submit" value="Add armies" />
		<br /><br />
	</form>
	
	<form action="web.py" id="grab_armies_form_cities" method="get" accept-charset="utf-8" style="display:block; float:right; border: 0px solid #000; margin-right:20px;">
		<strong>Grab armies</strong><br />
		<input type="hidden" name="mode" value="setup_campaign" />
		<input type="hidden" name="campaign" value="{id}" />
		<label for="coords">Coords: </label>{coords_cities}<br />
		<label for="radius">Radius: </label><input type="text" name="radius" id="radius" value="10" /><br />
		<input type="submit" value="Grab armies" />
		<br /><br />
	</form>
	
	<form action="web.py" id="grab_armies_form" method="get" accept-charset="utf-8" style="display:block; float:right; border: 0px solid #000; margin-right:20px;">
		<strong>Grab armies</strong><br />
		<input type="hidden" name="mode" value="setup_campaign" />
		<input type="hidden" name="campaign" value="{id}" />
		<label for="coords">Coords: </label><input type="text" name="coords" id="coords" value="{default_coods}" /><br />
		<label for="radius">Radius: </label><input type="text" name="radius" id="radius" value="10" /><br />
		<input type="submit" value="Grab armies" />
		<br /><br />
	</form>
	
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="setup_campaign_commit" />
		<input type="hidden" name="id" id="id" value="{id}" />
		
		Editing: {name_text}
		<br /><br />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="turn">Turn:</label></td>
				<td style="padding: 1px;">{turn_text}</td>
				
				<td width="5">&nbsp;</td>
				
				<td><label for="turn">Sides:</label></td>
				<td style="padding: 1px;">{sides_text}</td>
			</tr>
		</table>
		<br />
		<input type="submit" value="Perform edit" />
	</form>
	<br /><br />""".format(
		id =					campaign_id,
		name =					the_campaign.name,
		turn =					the_campaign.turn,
		name_text =				common.text_box("name", the_campaign.name, size=20),
		turn_text =				common.text_box("turn", the_campaign.turn, size=5),
		sides_text =			common.text_box("sides", the_campaign.sides, size=5),
		team_list				= team_f.structured_list(cursor, include_irs=True),
		grabbed_armies			= grabbed_armies,
		last_battle				= last_battle.id,
		coords_cities			= coords_cities,
		default_coods			= "%s, %s" % (last_battle.x, last_battle.y),
	))
	
	# Sides and teams
	side_form = ['<select id="side_menu">']
	
	for s in range(1, the_campaign.sides+1):
		side_form.append('<option value="{s}">{s}</option>'.format(s=s))
	
	side_form.append("</select>")
	side_form = "".join(side_form)
	
	# Form JS
	js = """
	var side = $("#side_menu").attr("value");
	var team_id = $("#new_team").attr("value");
	var team_name = $("#new_team :selected").text();
	
	team_list_content = $("#team_list_" + side).html();
	
	if (team_list_content != "")
	{
		$("#team_list_" + side).html(team_list_content + ", " + team_name);
	}
	else
	{
		$("#team_list_" + side).html(team_name);
	}
	
	$("#ajax_target").load("exec.py", {mode: "add_team_to_campaign", campaign: %s, side: side, team: team_id});
	$("#new_team").focus();
	return false;
	""" % campaign_id
	
	js = js.replace("\t", "").replace("\n", "")
	
	output.append('''
	<form action="" onsubmit='{js}' method="post" accept-charset="utf-8">
		{team_list}
		{side}
		
		<input type="submit" value="Add" />
	</form>
	
	<!-- PY -->
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="edit_campaign_armies" />
		<input type="hidden" name="campaign" value="{c}" />
		<input type="submit" value="Apply armies" />
		<!-- PYEND -->
		<table border="0" cellspacing="0" cellpadding="5" style="width:99%">
			<tr class="row2">
				<th width="15">#</th>
				<th>Teams</th>
			</tr>
	'''.format(
		c=campaign_id,
		team_list=team_f.structured_list(cursor, include_irs=True, field_id="new_team"),
		side=side_form,
		js=js,
	))
	
	army_ids = []
	
	the_campaign.get_sides_full(cursor)
	the_campaign.get_armies_full(cursor)
	campaign_armies = campaign_q.get_campaign_armies_from_turn(cursor, the_campaign.turn)
	teams_on_side_str = []
	for s in range(1, the_campaign.sides+1):
		teams_on_side = the_campaign.sides_full[s]
		
		if len(teams_on_side) > 0:
			teams_on_side_str = ['<table border="0" cellspacing="0" cellpadding="5" width="100%">']
			for t in teams_on_side:
				where = "campaign=%d and team=%d" % (campaign_id, t['team'])
				
				# Display "make secret" or "make public"
				public_display, secret_display = "", ""
				if t['secret']:	secret_display	= "display: none;"
				else:			public_display	= "display: none;"
				
				teams_on_side_str.append("""
				<tr id="team_row_{t}" class="row1">
					<td width="100">{name}</td>
					<td width="65">
						{started}
						-&gt;
						{finished}
					</td>
					<td>{remove}</td>
					<td>
					<a href="#" id="team_public_{t}"
						onclick="$('#ajax_target').load('web.py', {{mode:'campaign_team_public', team:{t}, campaign:{c}}}); {show_hide} return false;" class="mini_link" style="{public_display}">Make public</a>
					<a href="#" id="team_secret_{t}"
						onclick="$('#ajax_target').load('web.py', {{mode:'campaign_team_secret', team:{t}, campaign:{c}}}); {show_hide} return false;" class="mini_link" style="{secret_display}'">Make secret</a>
					</td>
				</tr>
				""".format(
					t = t['team'],
					c = campaign_id,
					name=team_dict[t['team']].name,
					started=common.doubleclick_text_full("campaign_teams", "started", where, t['started'], size=2),
					finished=common.doubleclick_text_full("campaign_teams", "finished", where, t['finished'], size=2),
					remove='''<a href="#" onclick='$("#ajax_target").load("exec.py", {mode: "remove_team_from_campaign", campaign: %d, team: %d, side: %d}); $("#team_row_%d").hide(); return false;'>Remove</a>''' % (campaign_id, t['team'], s, t['team']),
					
					show_hide = "$('#team_public_%d').toggle(); $('#team_secret_%d').toggle();" % (t['team'], t['team']),
					
					public_display = public_display,
					secret_display = secret_display,
				))
				
				# Now to put in the armies form
				army_form = []
				garrison_form = []
				
				team_armies = army_q.get_armies_from_team(cursor, t['team'], include_garrisons=True)
				# the_campaign.get_armies_full
				for army_id, the_army in team_armies.items():
					selected = False
					start_finish = ""
					
					if army_id in the_campaign.armies_full:
						selected = True
						where = "campaign=%d and army=%d" % (campaign_id, army_id)
						
						start_finish = "%s -&gt; %s" % (
							common.doubleclick_text_full("campaign_armies", "started", where, the_campaign.armies_full[army_id]['started'], size=2),
							common.doubleclick_text_full("campaign_armies", "finished", where, the_campaign.armies_full[army_id]['finished'], size=2))
					
					# Is it selected?
					if selected:
						checked = "checked='checked'"
						rclass = "selected_army"
					else:
						checked = ""
						rclass = ""
					
					# Is it being used elsewhere this turn?
					elsewhere = "<td>&nbsp;</td>"
					if army_id in campaign_armies:
						if campaign_id in campaign_armies[army_id]:
							elsewhere_count = len(campaign_armies[army_id]) - 1
						else:
							elsewhere_count = len(campaign_armies[army_id])
						
						if elsewhere_count == 1:
							elsewhere = "<td style='background-color:#700;'>&nbsp;</td>"
						elif elsewhere_count == 2:
							elsewhere = "<td style='background-color:#B00;'>&nbsp;</td>"
						elif elsewhere_count > 2:
							elsewhere = "<td style='background-color:#F00;'>&nbsp;</td>"
					
					army_s = '''<tr id="row_{a}" class="{rclass}">
					<td><label for="a_{a}" style="width:100%; display:block;">{name}</label></td>
					<td><input type="checkbox" name="a_{a}" id="a_{a}" value="True" onchange="if ($('#a_{a}').attr('checked')) {{$('#row_{a}').addClass('selected_army');}} else {{$('#row_{a}').removeClass('selected_army');}}" {checked}/></td>
					<td>{start_finish}&nbsp;&nbsp;</td>
					{elsewhere}
					</tr>'''.format(
						a = army_id,
						name = the_army.name,
						# cb = common.check_box("a_%d" % army_id, checked=selected),
						start_finish=start_finish,
						checked = checked,
						rclass = rclass,
						elsewhere = elsewhere,
					)
					
					if the_army.garrison:
						garrison_form.append(army_s)
					else:
						army_form.append(army_s)
					
					army_ids.append(army_id)
				
				
				teams_on_side_str.append("""
				<tr>
					<td colspan="4">
						<table border="0" cellspacing="0" cellpadding="0">
							<tr>
								<td width="300">
									<table border="0" cellspacing="0" cellpadding="3">
										{armies}
									</table>
								</td>
								<td>
									<table border="0" cellspacing="0" cellpadding="3">
										{garrisons}
									</table>
								</td>
								<td>
									&nbsp;
								</td>
							</tr>
						</table>
					</td>
				</tr>""".format(
					armies = "".join(army_form), 
					garrisons = "".join(garrison_form),
					
					c_id = campaign_id,
					team = t['team'],
				))
			
			teams_on_side_str.append("</table>")
		
		output.append("""
		<tr>
			<td colspan="2"><hr /></td>
		</tr>
		<tr>
			<td><strong>{s}</strong></td>
			<td>
				{teams}
				<br />
				<span id="team_list_{s}"></span>
			</td>
		</tr>
		""".format(
			s=s,
			teams="".join(teams_on_side_str),
			# teams=", ".join([team_dict[t].name for t in teams_on_side]),
		))
	
	# Field for the ids of the armies listed that we need to sort out
	output.append('<input type="hidden" name="army_ids" value="%s" />' % ",".join([str(a) for a in army_ids]))	
	output.append('<!-- PY --><tr><td colspan="2"><input type="submit" value="Apply armies" /></td></tr><!-- PYEND -->')
	output.append('''</table>
	<!-- PY --></form><!-- PYEND -->
	<br />''')
	
	# Delete button
	output.append("""
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="campaign" id="campaign" value="{id}" />
		<input type="hidden" name="mode" id="mode" value="remove_campaign" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete campaign" onclick="var answer = confirm('Delete {esc_name}?')
		if (answer) $('#delete_form').submit();" />
	</form>""".format(
		id =					campaign_id,
		esc_name =				common.js_name(the_campaign.name),
	))
	
	output.append(common.onload("$('#new_team').focus();"))
	output.append('<a href="web.py?mode=list_battles&amp;campaign=%d" class="block_link">List battles</a>' % campaign_id)
	output.append("</div>")
	
	return "".join(output)
