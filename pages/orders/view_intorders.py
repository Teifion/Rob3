import database
from pages import common
from functions import player_f, order_post_f
from queries import team_q
from classes import world

page_data = {
	"Title":	"Orders",
	"Admin":	True,
}

def main(cursor):
	team_id		= int(common.get_val("team", 0))
	turn		= int(common.get_val("turn", -1))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'view_orders')
	
	if turn < 1: turn = common.current_turn()
	
	the_world = world.World(cursor)
	player_dict = the_world.players()
	
	the_team = team_q.get_one_team(cursor, team_id)
	the_orders = the_team.get_orders(cursor, the_world, "international", turn)
	
	# output = ["<div style='padding: 5px; font-size: 14px; line-height: 17px;'>"]
	output = ["<div style='padding: 5px;'>"]
	player_updates = {}
	
	for o in the_orders:
		player_updates[o.player] = o.team
		
		if o.content == "Orders placeholder": continue
		
		output.append('<br /><hr />Post: <a href="http://woarl.com/board/viewtopic.php?p=%s#p%s">%s</a><br />' % (o.post_id, o.post_id, o.post_id))
		output.append('Poster: <a href="http://woarl.com/board/memberlist.php?mode=viewprofile&u=%d">%s</a> - ' % (o.player, player_dict[o.player].name))
		output.append('<a href="web.py?mode=edit_player&amp;player=%d">Local edit</a><br />' % (o.player))
		
		output.append(common.bbcode_to_html(o.content.replace('<span class="stitle">', '<hr /><span class="stitle">')))
	
	output.append("</div>")
	
	# Update player activity
	if turn == common.current_turn():
		database.query(cursor, player_f.update_player_activity(player_updates))
	
	# print "<br />".join(output)
	page_data['Title'] = "%s International orders" % the_team.name
	return "".join(output)