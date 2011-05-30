import database
from pages import common
from queries import team_q
from functions import player_f
from classes import world

page_data = {
	"Title":	"Orders",
	"Admin":	True,
}

def main(cursor):
	team_id		= int(common.get_val("team", 0))
	turn		= int(common.get_val("turn", -1))
	
	the_world = world.World(cursor)
	the_world.prep_for_orders()
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" %  common.select_team_form(cursor, 'view_orders')
	
	if turn < 1:
		turn = common.current_turn()
	
	# the_team = team_q.get_one_team(cursor, team_id)
	# the_team.get_resources(cursor)
	# the_team.get_spells(cursor)
	# the_team.get_techs(cursor)
	the_team = the_world.teams()[team_id]
	the_orders = the_team.get_orders(cursor, the_world, "normal", turn)
	
	output = ["<div style='padding:1px;'>"]
	player_updates = {}
	
	blocks = []
	for o in the_orders:
		o.split()
		blocks.extend(o.blocks)
	
	# Setup
	for b in blocks:
		b.setup()
	
	# Execution
	for b in blocks:
		b.execute()
	
	for b in blocks:
		# Player activity needs to get updated
		if turn == common.current_turn():
			player_updates[b.post.player] = b.post.team
		
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
	
	# output.append("""
	# Time taken: %(total)s<br /><br />
	# %(joined)s
	# """ % {
	# 	"total":	total_time,
	# 	"joined":	"<br />".join(time_list),
	# })
	# 
	# output.append("""
	# <a href="#" id="all_q_link" style="float: right; padding-right: 10px;" onclick="$('#all_q_div').load('web.py', {'ajax':'True','mode':'run_queries','subject':'Normal orders','queries':$('#all_q_text').val()}); $('#all_q_link').hide(); return false;">Run queries</a>
	# <br />
	# <textarea name="Name" id="Name" rows="8" style="width: 49%%;">%s</textarea>
	# <div style="float: right; width: 49%%; padding-right: 5px;" id="all_q_div">
	# 	<textarea id="all_q_text" name="Name" id="Name" rows="8" style="width: 100%%;">%s</textarea>
	# </div>
	# """ % ("\n".join(total_results), "\n".join(total_queries)))
	
	output.append("</div>")
	
	# Update player activity
	if turn == common.current_turn():
		database.query(cursor, player_f.update_player_activity(player_updates))
	
	page_data['Title'] = "%s normal orders" % the_team.name
	
	return "".join(output)
