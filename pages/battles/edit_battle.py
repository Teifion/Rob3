from pages import common
from data import battle, battle_f, battle_q
from data import team, team_f, team_q
from data import city, city_q
from data import army, army_q

battle_id = int(common.get_val('battle', 0))

if battle_id < 1:
	print "No battle selected"
	exit()

the_battle = battle.Battle(battle_q.get_one_battle(battle_id))

# If we're being sent the info from the view_map page then this is the new location we need
new_location = common.get_val('location', "")

if new_location == "":
	new_location = "%s,%s" % (the_battle.x, the_battle.y)# default value


# Build the city selector
city_list, cities_dict = city_q.get_live_cities()

names = {}
for c in city_list:
	names[c] = cities_dict[c].name

city_list.insert(0,0)
names[0] = "&nbsp;&nbsp;&nbsp;None"

output = ["<div style='padding: 5px;'>"]

output.append("""
<a href="web.py?mode=list_battles&amp;turn=%(battle_turn)s" class="block_link" style="text-align:left;">Wars of this turn</a>
<br />
<form action="exec.py" method="post" accept-charset="utf-8">
	<input type="hidden" name="mode" id="mode" value="edit_battle_commit" />
	<input type="hidden" name="id" id="id" value="%(battle_id)s" />
	
	Editing: %(name_text)s
	<br /><br />
	
	<table border="0" cellspacing="5" cellpadding="5">
		<tr>
			<td><label for="turn">Turn:</label></td>
			<td style="padding: 1px;">%(battle_turn_text)s</td>
		
			<td width="5">&nbsp;</td>
			
			<td>City</td>
			<td style="padding: 1px;">%(battle_city_select)s</td>
			
			
			<td width="5">&nbsp;</td>
			
			<td style="padding: 0px;">
				<a class="block_link" href="web.py?mode=view_map&amp;new_mode=edit_battle&amp;battle=%(battle_id)s"">Location:</a>
			</td>
			<td style="padding: 1px;">%(battle_location_text)s</td>
		</tr>
	</table>
	<br />
	<input type="submit" value="Perform edit" />
</form>
<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
	<input type="hidden" name="battle" id="battle" value="%(battle_id)s" />
	<input type="hidden" name="mode" id="mode" value="remove_battle" />
	<input style="float:right; margin-right:100px;" type="button" value="Delete battle" onclick="var answer = confirm('Delete %(esc_name)s?')
	if (answer) $('#delete_form').submit();" />
</form>
<br /><br />""" % {
	"battle_id":					battle_id,
	"name":					the_battle.name,
	"esc_name":				common.js_name(the_battle.name,),
	"battle_turn":					the_battle.turn,
	"name_text":				common.text_box("name", the_battle.name, size=20),
	"battle_turn_text":				common.text_box("turn", the_battle.turn, size=5),
	"battle_city_select":			common.option_box(
		name='city',
		elements=names,
		element_order=city_list,
		custom_id="",
		selected=the_battle.city,
	),
	"battle_location_text":			common.text_box("location", new_location, 10),
})

#	Now for the participants of the battle
#------------------------
teams_dict		= team.get_teams_dict()
army_dict		= army.get_army_dict()
participants	= the_battle.get_participants()

output.append("""
<hr />
<form action="exec.py" method="post" id="add_team_form" accept-charset="utf-8">
	<input type="hidden" name="mode" value="add_team_battle" />
	<input type="hidden" name="battle" id="battle" value="%s" />
	%s
	&nbsp;&nbsp;<input type="submit" value="Add team" />
</form>
<br />""" % (battle_id, team_f.structured_list(include_irs = True, field_name="team", skip=participants)))


#	TEAM DISPLAY
#------------------------
for t, s in participants.items():
	# Styling the public/secret link correctly
	if s:
		public_display	= ""
		secret_display	= "display: none;"
	else:
		public_display	= "display: none;"
		secret_display	= ""
	
	# Outputting the containing div and table header
	output.append("""
	<div style="float: left; width: 49%%; border: 1px solid #AAA;" id="team_div_%(t)s">
		<table border="0" cellspacing="0" cellpadding="5">
			<tr class="row2">
				<th colspan="3">
					<a href="#" id="team_public_%(t)s"
						onclick="$('#ajax_target').load('web.py', {mode:'battle_team_public', team:%(t)s, battle:%(battle_id)s, ajax:1}); %(show_hide)s return false;" class="mini_link" style="%(public_display)s">Make public</a>
					<a href="#" id="team_secret_%(t)s"
						onclick="$('#ajax_target').load('web.py', {mode:'battle_team_secret', team:%(t)s, battle:%(battle_id)s, ajax:1}); %(show_hide)s return false;" class="mini_link" style="%(secret_display)s'">Make secret</a>
						 - 
						<strong style="font-size:1.1em;">%(name)s</strong>
						 - 
						<a class="mini_link" href="exec.py?mode=remove_team_battle&amp;team=%(t)s&amp;battle=%(battle_id)s" onclick="var answer = confirm('Remove %(name)s?'); if (!answer) return false;">Remove</a>
						 - 
						<a class="mini_link" href="web.py?mode=list_units&amp;team=%(t)d">Military</a>
						 - 
						<a class="mini_link" href="web.py?mode=list_armies&amp;team=%(t)d">Armies</a>
				</th>
			</tr>
	""" % {
		"t":			t,
		"name":	teams_dict[t],
		"battle_id":	battle_id,
		
		"public_display":	public_display,
		"secret_display":	secret_display,
		
		"show_hide":	"$('#team_public_%s').toggle(); $('#team_secret_%s').toggle();" % (t, t),
	})
	
	# List all the armies involved here
	count = -1
	armies_list = battle_f.armies_in_battle(battle_id, t)
	for a in armies_list:
		count += 1
		
		output.append("""
		<tr class="row%(count)s">
			<td>%(name)s</td>
			<td>&nbsp;</td>
			<td style="padding:0;"><a class="block_link" href="exec.py?mode=remove_army_from_battle&amp;army=%(army_id)s&amp;battle=%(battle_id)s">Remove</a></td>
			<!--<td style="padding:0;"><a class="block_link" href="#" onclick="">Edit</a></td>-->
		</tr>
		""" % {
			"count":		count%2,
			"name":	army_dict[a],
			"army_id":		a,
			"battle_id":	battle_id,
		})
	
	# And armies yet to be involved
	armies_order, armies_dict_c = army_q.get_armies_from_team(t, True)
	army_select = []
	
	for a in armies_order:
		if a in armies_list: continue
		army_select.append('<option value="%s">%s</option>' % (a, army_dict[a]))
	
	if army_select != []:
		count += 1
		output.append("""
		<tr class="row%(count)s">
			<form action="exec.py" id="add_army_form_%(t)s" method="post" accept-charset="utf-8">
			<td style="padding:1px;">
				<input type="hidden" name="mode" value="add_army_to_battle" />
				<input type="hidden" name="team" value="%(t)s" />
				<input type="hidden" name="battle" value="%(battle_id)s" />
				<select name="army">
					%(army_select)s
				</select>
			</td>
			<td>&nbsp;</td>
			<td style="padding:0;"><a class="block_link" href="#" onclick="$('#add_army_form_%(t)s').submit(); return false;">Add army</a></td>
			</form>
		</tr>
		""" % {
			"count":		count%2,
			"army_select":	"".join(army_select),
			"t":			t,
			"battle_id":	battle_id,
		})
	
	# Close table and container
	output.append("</table></div>")

output.append('<div style="clear:left;">&nbsp;</div><a href="web.py?mode=view_battle&amp;battle=%s" class="block_link">View battle</a>' % battle_id)

output.append("</div>")

print "".join(output)