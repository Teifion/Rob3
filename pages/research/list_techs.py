from pages import common
from functions import tech_f
from queries import team_q, tech_q
from rules import tech_rules

page_data = {
	"Title":	"Tech list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'list_techs')
	
	# Build team item
	the_team = team_q.get_one_team(cursor, team_id)
	tech_dict = tech_q.get_all_techs(cursor)
	
	output = []
	
	the_team.get_techs(cursor)
	
	output.append("""
	<table style="width: 100%;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>#</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	max_tech_level = 1
	skip_tech_list = {}
	table_dict = {}
	tech_points_spent = 0
	
	for tech_id, tech_level in the_team.tech_levels.items():
		if tech_level not in table_dict:
			table_dict[tech_level]			= []
			skip_tech_list[tech_level]	= []
		max_tech_level = max(max_tech_level, tech_level)
		
		# Total that they've spent
		the_tech = tech_dict[tech_id]
		tech_points_spent += tech_rules.cost_to_get_to_level(cursor, the_tech, tech_level).get("Tech points", 0)
		tech_points_spent += the_team.tech_points[tech_id]
		
		skip_tech_list[tech_level].append(tech_id)
		
		table_dict[tech_level].append("""%(name)s <a class="red_link" href="exec.py?mode=set_tech&amp;tech=%(tech_id)s&amp;team=%(team_id)s&amp;level=%(level_down)s&amp;points=0">&nbsp;&lt;&nbsp;</a>
			
			%(points)s/%(points_to_next)s
			
			<a class="green_link" href="exec.py?mode=set_tech&amp;tech=%(tech_id)s&amp;team=%(team_id)s&amp;level=%(level_up)s&amp;points=0">&nbsp;&gt;&nbsp;</a>""" % {
		"name":			the_tech.name,
		"tech_id":		tech_id,
		"team_id":		team_id,
		"points":			the_team.tech_points[tech_id],
		"points_to_next":	tech_rules.cost_for_next_level(cursor, the_tech, tech_level).get("Tech points"),
		"level_down":	tech_level-1,
		"level_up":		tech_level+1,
		})
	
	
	for i in range(0, max_tech_level+1):
		if i not in table_dict:
			table_dict[i] = []
			skip_tech_list[i] = []
		
		output.append("""
		<tr class="row%(row_count)s">
			<td width="15">%(i)s</td>
			<td style="padding: 5px 2px 0 2px;">%(techs)s
			
			<!--
				<form id="tech_form_%(i)s" style="float: right;" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="set_tech" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<input type="hidden" name="points" value="0" />
			<input type="hidden" name="level" value="%(i)s" />
			<a href="#" onclick="$('#tech_form_%(i)s').submit();" class="block_link" style="float: right;">Add</a>
			<select style="float: right;" name="tech">%(new_tech)s</select></form>
			-->
			</td>
		</tr>
		""" % {
			"i":			i,
			"team_id":		team_id,
			"row_count":	(i%2),
			"techs":		", ".join(table_dict[i]),
			"new_tech":		tech_f.tech_option_list(cursor, skip_tech_list[i]),
		})
	
	# Add techs
	output.append("""
	<tr class="row%(row_count)s">
		<td colspan="2">
			<form action="exec.py" method="post" accept-charset="utf-8">
				<input type="hidden" name="mode" value="set_tech" />
				<input type="hidden" name="team" value="%(team_id)s" />
				<select name="tech" id="new_tech">
					%(tech_list)s
				</select>
				&nbsp;&nbsp;
				L: <input type="text" name="level" id="new_level" value="" onblur="$('#points_to_next').load('web.py', {'ajax':'True','mode':'tech_points_for_next','tech':$('#new_tech').val(), 'level':$('#new_level').val()});" size="5"/>
				&nbsp;&nbsp;
				P: <input type="text" name="points" value="" size="5" />/<span id="points_to_next">0</span>
				<input type="submit" value="Add" />
			</form>
		</td>
	</tr>
	%(onload)s
	""" % {
		"team_id":		team_id,
		"row_count":	((i+1)%2),
		"tech_list":	tech_f.tech_option_list(cursor),
		"onload":		common.onload("$('#new_tech').focus();"),
	})
	
	output.append("</table>")
	
	output.append("<br />&nbsp;&nbsp;&nbsp;Total tech points spent: %d" % tech_points_spent)
	
	return "".join(output)
