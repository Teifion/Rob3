from pages import common
from queries import city_q, operative_q
from functions import team_f

page_data = {
	"Title":	"Edit operative",
	"Admin":	True,
}

def main(cursor):
	operative_id = int(common.get_val('operative'))
	
	the_operative = operative_q.get_one_operative(cursor, operative_id)
	
	city_dict = city_q.get_live_cities(cursor)
	
	names = {}
	for c, the_city in city_dict.items():
		names[c] = the_city.name
	
	output = []
	
	output.append("<div style='padding: 5px;'>")
	
	output.append("""
	<form action="exec.py" id="the_operative_form" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_operative_commit" />
		<input type="hidden" name="id" id="id" value="{operative_id}" />
		<input type="hidden" name="team" id="team" value="{team}" />
		
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="name">Identifier:</label></td>
				<td style="padding: 1px;">{name}</td>
		
				<td width="5">&nbsp;</td>
				
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				
				<td width="5">&nbsp;</td>
				
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td><label for="location">Location:</label></td>
				<td style="padding: 1px;">{city_select}</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="arrival">Arrival:</label></td>
				<td style="padding: 2px;">{arrival}</td>
				
				<td width="5">&nbsp;</td>
				
				<td><label for="size">Size:</label></td>
				<td style="padding: 2px;">{size}</td>
			</tr>
			<tr>
				<td><label for="stealth">Stealth:</label></td>
				<td style="padding: 2px;">{stealth}</td>
				
				<td>&nbsp;</td>
				
				<td><label for="observation">Observation:</label></td>
				<td style="padding: 2px;">{observation}</td>
				
				<td>&nbsp;</td>
				
				<td><label for="integration">Integration:</label></td>
				<td style="padding: 2px;">{integration}</td>
			</tr>
			<tr>
				<td><label for="sedition">Sedition:</label></td>
				<td style="padding: 2px;">{sedition}</td>
				
				<td>&nbsp;</td>
				
				<td><label for="sabotage">Sabotage:</label></td>
				<td style="padding: 2px;">{sabotage}</td>
				
				<td>&nbsp;</td>
				
				<td><label for="assassination">Assassination:</label></td>
				<td style="padding: 2px;">{assassination}</td>
			</tr>
			<tr>
				<td colspan="8" style="padding: 0;">
					<a class="block_link" href="#" onclick="$('#the_operative_form').submit();">Apply changes</a>
				</td>
			</tr>
		</table>
	</form>
	<form id="delete_form" action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="operative" id="operative" value="{operative_id}" />
		<input type="hidden" name="mode" id="mode" value="remove_operative" />
		<input style="float:right; margin-right:100px;" type="button" value="Delete operative" onclick="var answer = confirm('Delete operative?')
		if (answer) $('#delete_form').submit();" />
	</form>
	<br /><br />""".format(
		operative_id	= operative_id,
		team			= the_operative.team,
		size			= common.text_box("size", the_operative.size),
		arrival			= common.text_box("arrival", the_operative.arrival, size=3),
		name		= common.text_box("name", the_operative.name),
		
		stealth			= common.text_box("stealth", the_operative.stealth, size=3),
		observation		= common.text_box("observation", the_operative.observation, size=3),
		integration		= common.text_box("integration", the_operative.integration, size=3),
		sedition		= common.text_box("sedition", the_operative.sedition, size=3),
		sabotage		= common.text_box("sabotage", the_operative.sabotage, size=3),
		assassination	= common.text_box("assassination", the_operative.assassination, size=3),
		
		city_select		= common.option_box(
			name='city',
			elements=names,
			element_order=city_dict.keys(),
			custom_id="",
			selected=the_operative.city
		),
	))
	
	output.append("</div>")
	
	return "".join(output)