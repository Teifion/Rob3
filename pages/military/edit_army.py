from pages import common
# from data import army, army_q
# from data import team_f, city_q
from queries import army_q, city_q
from functions import team_f

page_data = {
	"Title":	"Edit army",
	"Admin":	True,
}

def main(cursor):
	army_id = int(common.get_val('army', 0))
	garrison_id = int(common.get_val('garrison', 0))
	
	if army_id < 1 and garrison_id > 0:
		the_army = army_q.get_one_garrison(cursor, garrison_id)
	else:
		the_army = army_q.get_one_army(cursor, army_id)
	
	# If we're being sent the info from the view_map page then this is the new location we need
	new_location = common.get_val('location', "")
	
	if new_location == "":
		new_location = "%s,%s" % (the_army.x, the_army.y)# default value
		last_location = "%s,%s" % (the_army.old_x, the_army.old_y)
	
	if the_army.garrison > 0:
		new_location = """
		<td><label for="garrison">Garrison:</label></td>
		<td>%s</td>
		""" % (city_q.get_one_city(cursor, the_army.garrison).name)
	else:
		new_location = """
		<td style="padding: 0px;"><a href="web.py?mode=view_map&new_mode=edit_army&amp;army=%s" class="block_link">Location:</a></td>
		<td style="padding: 1px;">%s</td>""" % (the_army.id, common.text_box("location", new_location))
	
	output = []
	
	output.append("""<div style="float: right; width: 50%%;">
		<strong>Squads in army</strong>
		<div id="army_squads">
			
		</div>
	</div>""")
	
	output.append("<div style='padding: 5px;'>")
	
	if the_army.base > 0:
		base_name = "%s (%d)" % (city_q.get_one_city(cursor, the_army.base).name, the_army.base)
	else:
		base_name = "None"
	
	output.append("""
	<form action="exec.py" id="the_army_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_army_commit" />
		<input type="hidden" name="id" id="id" value="%(army_id)s" />
		
		Editing: %(name_text)s
		<br /><br />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="team">Team:</label></td>
				<td style="padding: 1px;">%(owner_select)s</td>
				
				<td width="5">&nbsp;</td>
				
				%(location)s
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				
				<td width="5">&nbsp;</td>
				
				<td>Last location:</td>
				<td>%(last_location)s</td>
			</tr>
			<tr>
				<td>Base:</td>
				<td>%(base)s</td>
				
				<td width="5">&nbsp;</td>
				
				<td>Distance:</td>
				<td>%(distance)s</td>
			</tr>
			<tr>
				<td colspan="5" style="padding: 0;"><a class="block_link" href="#" onclick="$('#the_army_form').submit();">Apply changes</a></td>
			</tr>
		</table>
	</form>
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="army" id="army" value="%(army_id)s" />
		<input type="hidden" name="mode" id="mode" value="remove_army" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete army" onclick="var answer = confirm('Delete %(name_safe)s?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""" % {
		"name_safe":		common.js_name(the_army.name),
		"army_id":			the_army.id,
		"name":				the_army.name,
		"name_text":		common.text_box("name", the_army.name),
		"owner_select":		team_f.structured_list(cursor, default=the_army.team),
		"location":			new_location,
		"last_location":	last_location,
		"base":				base_name,
		"distance":			the_army.distance,
	})
	
	output.append(common.onload("$('#army_squads').load('web.py', {'mode':'list_squads','army':'%d', 'ajax':'True'});" % int(the_army.id)))
	
	output.append("</div>")
	
	page_data['Title'] = "Edit army %s" % the_army.name
	return "".join(output)