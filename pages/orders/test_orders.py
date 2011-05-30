import database
from pages import common
from queries import team_q
from functions import team_f, request_f
from rules import team_rules
from classes import world

page_data = {
	"Title":	"Test orders",
	"Admin":	True,
}

def main(cursor):
	team_id		= int(common.get_val("team", 0))
	orders_str	= common.get_val("orders", "")#.replace("’", "'")
	msn_mode	= int(common.get_val("msn_mode", 0))
	
	if team_id < 1 or orders_str == "":
		return """
		<div style='padding: 5px;'>
			<form action="web.py" id="select_team_form" method="post" accept-charset="utf-8">
				<input type="hidden" name="mode" id="mode" value="test_orders" />
				<label for="msn_mode">MSN mode:</label> <input type="checkbox" id="msn_mode" name="msn_mode" value="1" />
				Team: %s
				<!--
				<a class="block_link" href="#" onclick="$('#select_team_form').submit(); return false;">Run orders</a>
				-->
				<input type="submit" value="Run orders" />
				<br />
				<textarea name="orders" rows="8" style="width: 100%%;">[o]Rob command[/o]
Enable: Overbudget

</textarea>
			</form>
		</div>%s""" % (
			team_f.structured_list(cursor, field_id="team"),
			common.onload("$('#team').focus();"),
		)
	
	the_world = world.World(cursor)
	the_world.prep_for_orders()
	
	the_team = the_world.teams()[team_id]
	produced_resources, new_resources = team_rules.produce_resources(cursor, the_team, the_world, force_requery=True)
	the_team.resources = new_resources
	blocks = request_f.convert_orders(the_world, the_team, orders_str)
	
	output = ["<div style='padding:1px;'>"]
	
	output.append("Running with resources: %s" % str(the_team.resources))
	
	# Setup
	for b in blocks:
		b.setup(msn_order=msn_mode)
	
	# Execution
	for b in blocks:
		b.execute()
	
	debug = []
	for i, b in enumerate(blocks):
		# if b.cost.as_string() != "":
		# 	b.results = b.results.replace("{COST}", " - [neg]Cost: %s[/neg]" % b.cost.as_string())
		# else:
		# 	b.results = b.results.replace("{COST}", "")
		# 
		# # Trade queries are done differently
		# if b.order_type != "trades":
		# 	total_queries.append(b.queries)
		# 	total_results.append(b.results.strip())
		# 	total_results.append("")# To create a gap
		
		if len(b.debug) > 1:
			debug.append(b.debug[0])
			debug.append("\n---\n".join(b.debug[1:len(b.debug)]))
		
		output.append("""
		<div class="orders" style="border-color:{border};background-color:{background};">
			<strong>{title}</strong>: {cost}<br />
			{response}
			<br />
			
			<div style="float: left; width: 50%;">
				<textarea rows="6" style="float:left;width:99%;">{results}</textarea>
			</div>
			
			<div style="float: left; width: 50%;">
				<textarea rows="6" style="float:right;width:99%;">{queries}</textarea>
				<br />
				<a href="web.py?mode=direct_query">Direct query</a>
			</div>
			<div style="clear: left;">
				&nbsp;
			</div>
		</div>
		""".format(
			title		= b.title_name,
			cost		= str(b.cost),
			response	= common.bbcode_to_html("<br />".join(b.input_response)),
			results		= "\n".join(b.results),
			queries		= "\n".join(b.queries),
			
			border		= b.border_colour,
			background	= b.background_colour,
		))
	
	if debug != []:
		output.insert(2, '<br /><strong>Debug:</strong><br /><textarea name="debug" id="debug" rows="6" cols="80">%s</textarea><br />' % "".join(debug))
	
	output.append("Finishing with resources: %s" % str(the_team.resources))
	output.append("</div>")
	
	return "".join(output)
