from pages import common
from rules import unit_rules
from queries import team_q, army_q, city_q
from classes import army

page_data = {
	"Title":	"Army list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	text_location = common.get_val('location', "")
	
	# Build team
	the_team = team_q.get_one_team(cursor, team_id)
	cities_dict = city_q.get_cities_from_team(cursor, team=team_id, include_dead=0)
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" %  common.select_team_form(cursor, 'list_armies')
		exit()
	
	armies_dict = army_q.get_armies_from_team(cursor, team=team_id, include_garrisons=1)
	
	output = []
	output.append("""
	<table border="0" cellspacing="0" cellpadding="5" style="width: 100%;">
		<tr class="row2">
			<th>Army</th>
			<th>Location</th>
			<th>Base</th>
			<th>Size</th>
			<th>&nbsp;</th>
			<th>&nbsp;</th>
		</tr>""")
	
	names = {}
	
	if len(armies_dict) > 0:
		count = -1
		
		# for team_id, team in team_dict.items():
		for army_id, the_army in armies_dict.items():
			count += 1
			
			city_location = the_army.garrison
			
			if the_army.garrison > 0:
				location = "Garrison"
			
			else:
				location = "%s, %s" % (the_army.x, the_army.y)
			
			if the_army.base in cities_dict:
				base_name = cities_dict[the_army.base].name
			else:
				base_name = "N/A"
			
			output.append("""
			<tr class="row%(row)d" id="%(army_id)d">
				<td><strong>%(name)s</strong></td>
				<td>%(location)s</td>
				<td>%(base)s</td>
				<td>%(size)s</td>
				
				<td style="padding: 0px;">
					<a class="block_link" id="show_squads_%(army_id)d" href="#" onclick="$('#div_%(army_id)d').load('web.py', {'mode':'list_squads', 'ajax':'True', 'army':'%(army_id)d'}, function () {$('#tr_%(army_id)d').fadeIn(0); $('#show_squads_%(army_id)d').fadeOut(0); $('#hide_squads_%(army_id)d').fadeIn(0);}); return false;">Show squads</a>
				<a id="hide_squads_%(army_id)d" style="display:none;" class="block_link" href="#" onclick="$('#tr_%(army_id)d').fadeOut(0); $('#show_squads_%(army_id)d').fadeIn(0); $('#hide_squads_%(army_id)d').fadeOut(0); return false;">Hide squads</a></td>
				
				<td style="padding: 0px;"><a class="block_link" href="web.py?mode=edit_army&amp;army=%(army_id)d">Edit army</a></td>
			</tr>
			<tr style="display: none;" id="tr_%(army_id)d">
				<td colspan="5" style="padding: 0 10px 10px 10px;">
					<div id="div_%(army_id)d">
						&nbsp;
					</div>
				</td>
			</tr>
			""" % {	'row': (count % 2),
					
					"army_id":		army_id,
					"name":			common.doubleclick_text("armies", "name", army_id, the_army.name, "font-weight:bold", size=18),
					"base":			base_name,
					"location":		location,
					"size":			the_army.get_size(cursor),
					})
	
	# Add new army thingie
	names = {}
	for c, the_city in cities_dict.items():
		names[c] = the_city.name
	
	count += 1
	output.append("""
	<tr class="row%(row)d">
		<form action="exec.py" id="add_army_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" value="add_army" />
		<input type="hidden" name="team" value="%(team_id)s" />
		<td style="padding: 1px;"><input type="text" id="new_name" name="name" value="" /></td>
		<td>&nbsp;</td>
		<td style="padding: 1px;">
			%(city_location)s
			&nbsp;&nbsp;&nbsp;
			%(text_location)s
		</td>
		<td style="padding: 0px;"><a href="web.py?mode=view_map&amp;new_mode=list_armies&amp;team=%(team_id)s" class="block_link">Pick location</a></td>
		<td colspan="2" style="padding: 0px;"><a class="block_link" href="#" onclick="$('#add_army_form').submit(); return false;">Add</a></td>
		</form>
		%(onload)s
	</tr>
	""" % {	'row': (count % 2),
			
			"team_id":			team_id,
			'city_location':	common.option_box(
				name='city_location',
				elements=names,
				element_order=cities_dict.keys(),
				custom_id="",
			),
			
			"text_location":	common.text_box("text_location", text_location, custom_id=""),
			"onload":			common.onload("$('#new_name').focus();")
			})	
	
	output.append("</table>")
	
	return "".join(output)