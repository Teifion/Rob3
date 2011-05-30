from pages import common
from functions import spell_f
from queries import team_q, spell_q
from rules import spell_rules

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'list_spells')
	
	# Build team item
	the_team = team_q.get_one_team(cursor, team_id)
	spell_dict = spell_q.get_all_spells(cursor)
	
	output = []
	
	the_team.get_spells(cursor)
	
	output.append("""
	<table style="width: 100%;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>#</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	max_spell_level = 1
	skip_spell_list = {}
	table_dict = {}
	spell_points_spent = 0
	
	for spell_id, spell_level in the_team.spell_levels.items():
		if spell_level not in table_dict:
			table_dict[spell_level]			= []
			skip_spell_list[spell_level]	= []
		max_spell_level = max(max_spell_level, spell_level)
		
		# Total that they've spent
		the_spell = spell_dict[spell_id]
		spell_points_spent += spell_rules.cost_to_get_to_level(cursor, the_spell, spell_level, in_spell_points=True).get("Spell points", 0)
		spell_points_spent += the_team.spell_points[spell_id]
		
		skip_spell_list[spell_level].append(spell_id)
		
		
		table_dict[spell_level].append("""%(name)s <a class="red_link" href="exec.py?mode=set_spell&amp;spell=%(spell_id)s&amp;team=%(team_id)s&amp;level=%(level_down)s&amp;points=0">&nbsp;&lt;&nbsp;</a>
			
			%(points)s/%(points_to_next)s
			
			<a class="green_link" href="exec.py?mode=set_spell&amp;spell=%(spell_id)s&amp;team=%(team_id)s&amp;level=%(level_up)s&amp;points=0">&nbsp;&gt;&nbsp;</a>""" % {
		"name":			the_spell.name,
		"spell_id":		spell_id,
		"team_id":		team_id,
		"points":			the_team.spell_points[spell_id],
		"points_to_next":	spell_rules.cost_for_next_level(cursor, the_spell, spell_level, in_spell_points=True).get("Spell points"),
		"level_down":	spell_level-1,
		"level_up":		spell_level+1,
		})
	
	
	for i in range(0, max_spell_level+1):
		if i not in table_dict:
			table_dict[i] = []
			skip_spell_list[i] = []
		
		output.append("""
		<tr class="row%(row_count)s">
			<td width="15">%(i)s</td>
			<td style="padding: 5px 2px 0 2px;">%(spells)s
			
			<!--
				<form id="spell_form_%(i)s" style="float: right;" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="set_spell" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<input type="hidden" name="points" value="0" />
			<input type="hidden" name="level" value="%(i)s" />
			<a href="#" onclick="$('#spell_form_%(i)s').submit();" class="block_link" style="float: right;">Add</a>
			<select style="float: right;" name="spell">%(new_spell)s</select></form>
			-->
			</td>
		</tr>
		""" % {
			"i":			i,
			"team_id":		team_id,
			"row_count":	(i%2),
			"spells":		", ".join(table_dict[i]),
			"new_spell":	spell_f.spell_option_list(cursor, skip_spell_list[i]),
		})
	
	# Add spells
	output.append("""
	<tr class="row%(row_count)s">
		<td colspan="2">
			<form action="exec.py" method="post" accept-charset="utf-8">
				<input type="hidden" name="mode" value="set_spell" />
				<input type="hidden" name="team" value="%(team_id)s" />
				<select name="spell" id="new_spell">
					%(spell_list)s
				</select>
				&nbsp;&nbsp;
				L: <input type="text" name="level" id="new_level" value="" onblur="$('#points_to_next').load('web.py', {'ajax':'True','mode':'spell_points_for_next','spell':$('#new_spell').val(), 'level':$('#new_level').val()});" size="5"/>
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
		"spell_list":	spell_f.spell_option_list(cursor),
		"onload":		common.onload("$('#new_spell').focus();"),
	})
	
	output.append("</table>")
	
	output.append("<br />&nbsp;&nbsp;&nbsp;Total spell points spent: %d" % spell_points_spent)
	
	return "".join(output)
