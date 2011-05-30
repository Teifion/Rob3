import database
from functions import intorder_f, order_post_f
from queries import intorder_q, team_q
from classes import world
from pages import common

page_data = {
	"Title":	"Analyse order",
	"Admin":	True,
}

"""
UPDATE orders SET content = '[o]The Daemons Hand[/o]

[rob][b]Forces[/b]

Sharyk
Central Reserves
Southern Garrison
Gate Guarders
The Navy
Aracnar forces

[b]Plan[/b]

The objective of this attack is to remove the port cities of Zatoka, Przystan, Kruel and Empires Edge, to remove the ability of any of Raytis current enemies to attack us.[/rob]

[b]Chronology[/b]

-The forces will gather for the assault at the start of the year at the Sharyzen city of Shearwater Cliff.
-They will then proceed south and mount an assault on the Valnor port city of Zatoka, followed by Przystan. See the Valnor attack orders below.
-Afterwards, they are to head back up and around to attack the Orc port of Kruel. See Kruel attack orders below
-Following this, the army is to attack the Luprasic port of Empires Edge. See the Luprasic attack orders below.
-Finally, the Orc city of Nasgrak Fortress is to be attacked. See Nasgrak Fortress attacks below.
-In case of attacks at see, see the Naval Engagement orders below.

[b]Valnor attack[/b]

The Valnor city of Zatoka will be the first target of this turns attack. Upon approaching the city, all Sharyzen ships are to remain back while the Sharyzen soldiers fly forward and attack and burn and ships in the harbour, disabling the ships first by destroying their rigging and preventing them from fleeing the harbour, before cutting them adrift and pushing them away from the docks before finally setting them alight. This will free the docks and allow the Aracnar forces to use them for disembarking.
After the ships have been destroyed, the Shrikes will seize the docks and any Gates preventing the Aracnar ground forces from gaining access to the city. They will then open the gates as the Aracnar troops land, letting the Aracnar troops storm the city.
Inside the walls, the Aracnar are to be left to handle the bulk of the house to house fighting. Any conflicts taking place in the streets however, are to be supported by Sharyzen skirmishers who will land on the rooftops and attack any enemies in the streets below.
Each time they reach another set of walls, the Shrikes are to seize the gates and open them.
While ideally I would prefer the city to be destroyed, if it is decided that its impossible to do so and still have sufficient forces to complete the rest of the campaign then simply destroying the harbour (removing any Shipyards) and any and all ships, before then moving on to the next target will be acceptable.
These tactics are to be repeated on the city of Przystan.
Note that I am willing to accept over excessive casualties so long as all four targets are destroyed.

Kruel Attack
' WHERE post_id = 49809;

"""


def main(cursor):
	team_id		= int(common.get_val("team", 0))
	turn		= int(common.get_val("turn", -1))
	
	turn = 81
	team_id = 83# Clan
	team_id = 71# Shrikes
	# team_id = 72# Daninia
	
	# Defaults
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" % common.select_team_form(cursor, 'view_orders')
	
	if turn < 1:
		turn = common.current_turn()
	
	# Build some handles
	the_world = world.World(cursor)
	player_dict = the_world.players()
	
	the_team = team_q.get_one_team(cursor, team_id)
	the_orders = the_team.get_orders(cursor, the_world, "international", turn)
	
	output = ["<div style='padding: 5px;'>"]
	player_updates = {}
	
	# Make sure we have the orders in place
	for o in the_orders:
		intorder_f.create_default(cursor, o)
	
	# Bulk get
	intorders = intorder_q.get_orders_from_posts(cursor, [o.post_id for o in the_orders])
	intorder_q.mass_get_parents(cursor, intorders)
	
	for i, o in intorders.items():
		# if o.parent.content == "Orders placeholder": continue
		
		sections = o.split()
		
		for s in sections:
			output.append("""
			<div class="intorder">
				<a href="http://woarl.com/board/memberlist.php?mode=viewprofile&amp;u={player.id}">{player.name}</a>:
				<a href="http://woarl.com/board/viewtopic.php?p={the_order.post_id}#p{the_order.post_id}">{the_order.post_id}</a>
				<br />
				
				{content}
			</div>""".format(
				intorder = o,
				player = player_dict[o.parent.player],
				the_order = o.parent,
				s = s,
				
				content = common.bbcode_to_html(s.content),
			))
		
		
		# output.append('<br /><hr />Post: <a href="http://woarl.com/board/viewtopic.php?p=%s#p%s">%s</a><br />' % (o.parent.post_id, o.parent.post_id, o.parent.post_id))
		# output.append('Poster: <a href="http://woarl.com/board/memberlist.php?mode=viewprofile&u=%s">%s</a><br />' % (o.parent.player, player_dict[o.parent.player].name))
		# 
		# output.append(common.bbcode_to_html(o.parent.content.replace('{SMILIES_PATH}', 'http://woarl.com/board/images/smilies')))
		# 
		# output.append(str(the_order.parent.topic))
		# output.append("<br />")
	
	output.append("</div>")
	
	# TODO update player activity
	
	# print "<br />".join(output)
	page_data['Title'] = "%s International orders" % the_team.name
	return "".join(output)