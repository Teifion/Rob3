from pages import common
from classes import order_post, world
from functions import order_post_f
from queries import team_q
from rules import team_rules
import urllib.request
import re

def convert_orders(the_world, the_team, orders_string, player_id=0):
	"""docstring for convert_orders"""
	post_data = {
		"post_id":	0,
		"team":		the_team.id,
		"turn":		common.current_turn(),
		"topic":	0,
		"player":	player_id,
		"content":	orders_string,
	}
	
	the_post = order_post.Order_post(the_world, row=post_data)
	the_post.team_ref = the_team
	the_post.split()
	# the_post.match()
	
	return the_post.blocks

def msn_run_orders(cursor, team_id):
	the_team = team_q.get_one_team(cursor, team_id)
	
	# Get orders
	getter_data = "p=%s&mode=latest_rr&topic=%s" % (common.data['getterPass'], the_team.request_topic)
	orders_str = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	# print(common.data['getter_url'], getter_data)
	# return orders_str.decode('utf-8')
	
# 	orders_str = b"""-POST_SEPERATOR-                                                                                                                                                                             
# -START OF POST-
# post id:48143
# poster id:2
# -START OF ORDER 48143-
# 
# [o]Construction[/o]
# Build 25k Fortifications at Ashkar
# Build Border forts at Candor
# 
# [o]Military[/o]
# 
# Select army: Expeditionary fleet
# Reinforce squad: the Divine Wind, 100
# 
# [o]Research[/o]
# Architecture
# Covert training
# Dazzle
# Fireball
# 
# -END OF ORDER 48143-
# -END OF POST-
# """
	
	orders_str = orders_str.decode('utf-8')
	orders_str = re.sub(r'-END OF ORDER [0-9]*-', '', orders_str)
	orders_str = orders_str.replace('-END OF POST-', '')
	
	# Prep world
	the_world = world.World(cursor)
	the_world.prep_for_orders()
	
	the_team = the_world.teams()[team_id]
	produced_resources, new_resources = team_rules.produce_resources(cursor, the_team, the_world, force_requery=True)
	the_team.resources = new_resources
	
	blocks = convert_orders(the_world, the_team, orders_str)
	output = []
	
	# Setup
	for b in blocks:
		b.setup(msn_order=True)
	
	# Execution
	for b in blocks:
		b.execute()
	
	for b in blocks:
		output.append("""
[o]{name}[/o]
{input}\n
[fullbox={background},{border}]{results}[/fullbox]
""".format(
			name=b.title_name,
			cost=str(b.cost),
			input="\n".join(b.input_response).strip(),
			results="\n".join(b.results).strip(),
			background=b.background_colour,
			border=b.border_colour,
		))
	
	# return "".join(output)
	post_request_result(the_team, "".join(output))
	return "Orders run (%s)" % the_team.name

def post_request_result(the_team, results):
	results = results.replace(' ', '\\ ').replace('\n', 'NEWLINE').replace('\t', ' ')
	results = results.replace('(', '\\(').replace(')', '\\)')
	results = results.replace("'", 'APOSTRAPH').replace('&', 'AMPASAND')
	
	# Time to grab content from online
	getter_data = "p=%s&mode=requestReply&forum=%d&topic=%s&content=%s" % (common.data['getterPass'], the_team.forum_url_id, the_team.request_topic, results)
	reply = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	return reply