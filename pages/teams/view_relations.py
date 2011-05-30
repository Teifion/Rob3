import database
from pages import common
from queries import team_q
from classes import team

page_data = {
	"Admin":	True,
	"Redirect":	"View relations",
}

def main(cursor):
	team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
	relations = team_q.get_relations(cursor)
	
	output = []
	
	# Now the actual set of borders
	output.append('''
	<div style="overflow: scroll;">
		<table border="0" cellspacing="0" cellpadding="5" style="width:100%; overflow: scroll;">
			<tr class='row2'>
				<th>&nbsp;</th>''')
	
	for t1, team1 in team_dict.items():
		output.append('<th>%s</th>' % team1.name[0:6])
	
	output.append('</tr>')
	
	# Data
	i = 1
	for t1, team1 in team_dict.items():
		i += 1
		output.append("<tr class='row%d'><td style='font-weight:bold;'>%s</td>" % (i % 2, team1.name[0:15]))
		
		for t2, team2 in team_dict.items():
			if t1 == t2:
				output.append('<td>&nbsp;</td>')
				continue
			
			output.append("""
			<td style="padding:0px;">
				<a class="block_link" href="web.py?mode=edit_relations&amp;t1={t1}&amp;t2={t2}">{other}</a>
			</td>
			""".format(
				other = team2.name[0:5],
				t1 = t1,
				t2 = t2,
			))
	
	# Close form
	output.append("</table></div>")
	return "".join(output)