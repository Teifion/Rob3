# -*- coding: utf-8 -*-

import time
from pages import common
import urllib.request
import re
import database
from queries import system_q
from classes import order_post

# Gets all the normal orders for the turn
def get_turn_orders(cursor, the_world=None, turn=-1):
	if turn < 1:
		turn = common.current_turn()
	
	order_results = []
	topic_list = []
	team_dict = the_world.teams()
	for t, the_team in team_dict.items():
		if the_team.orders_topic > 0:
			topic_list.append(str(the_team.orders_topic))
			
	topic_list = ",".join(topic_list)
	
	query = """SELECT * FROM orders WHERE topic in (%s) AND turn = %d""" % (topic_list, turn)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		order_results.append(order_post.Order_post(the_world, row))
	
	if len(order_results) > 0:
		return order_results
	
	raise Exception("No orders for turn = %d" % turn)

def get_orders(cursor, topic_id, turn, team, recache=False, delay=0):
	"""Gets the list of orders from the database, if it's not there it goes after the post cache"""
	if recache:
		orders_string = download_orders(cursor, topic_id, turn, recache)
		time.sleep(float(delay))
	
	else:
		order_results = []
		
		query = """SELECT * FROM orders WHERE topic = %d AND turn = %d""" % (topic_id, turn)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			order_results.append(order_post.Order_post(row))
		
		if len(order_results) > 0:
			return order_results
	
	# If we are still going then it means that there were no orders in that list
	orders_string = download_orders(cursor, topic_id, turn)
	time.sleep(float(delay))
	
	# Now to convert the bulk orders into individual items
	return convert_string_to_posts(cursor, orders_string, turn, team, topic_id)

def convert_string_to_posts(cursor, post_string, turn, team, topic):
	"""Takes the great big text of orders and """
	# Yes it's misspelt, consider it something to help prevent mistakes
	posts = re.findall(r"-POST_SEPERATOR-(.*?)-END OF POST-", post_string, re.DOTALL)
	
	# print("")
	# print("""<textarea name="Name" id="Name" rows="8" cols="40">%s</textarea>""" % post_string)
	# exit()
	
	results = []
	
	for p in posts:
		p = p.strip()
		
		# print(post_string)
		
		# Get post info
		post_id		= int(re.search(r"^post id:([0-9]*)$", p, re.MULTILINE).groups()[0])
		poster_id	= int(re.search(r"^poster id:([0-9]*)$", p, re.MULTILINE).groups()[0])
		
		# Get post contents
		content = re.search(r"-START OF ORDER %d-(.*?)-END OF ORDER %d-" % (post_id, post_id), p, re.DOTALL).groups()[0]
		
		if content == "Orders placeholder":
			continue
		
		# print(post_id, content.strip()[0:70], "<br />")
		
		temp_result = order_post.Order_post(None)
		temp_result.post_id = post_id
		temp_result.team	= team
		temp_result.turn	= turn
		temp_result.topic	= topic
		temp_result.player	= poster_id
		temp_result.content = content.strip()
		
		# print "<hr /><strong>%s</strong><br />%s" % (post_id, results[-1].build_insert())
		# continue
		
		# The placeholder of this will have been downloaded, we need to delete it
		query = """DELETE FROM orders WHERE post_id = %d""" % post_id
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		query = """INSERT INTO orders (post_id, turn, team, topic, player, content)
			values
			({post_id}, {turn}, {team}, {topic}, {player}, '{content}');""".format(
				post_id = post_id,
				turn = turn,
				team = team,
				topic = topic,
				player = poster_id,
				content = database.escape(content.strip()),
		)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		results.append(temp_result)
	
	return results

def check_orders_cache(cursor, topic_id, turn_number):
	query = """SELECT content FROM post_cache
		WHERE topic = %d AND turn = %d LIMIT 1;""" % (topic_id, turn_number)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return row['content']

def download_orders(cursor, topic_id, turn_number, recache=False):
	"""Goes after the post cache, if it's not there it DL's it"""
	# Cache
	if not recache:
		cache = check_orders_cache(cursor, topic_id, turn_number)
		if cache != None:
			return cache
	
	# Need to work out from and till
	turn_dict = system_q.get_all_turns(cursor)
	
	# Allow 300 seconds leeway
	time_from = turn_dict[turn_number] - 300
	time_till = turn_dict[turn_number+1] + 300
	
	getter_data = "p=%s&mode=posts&topic=%d&from=%d&till=%d" % (
		common.data['getterPass'], topic_id, time_from, time_till)
	
	orders_result = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	
	# We used to use this to blott out UTF-8 characters - Now we do again!
	regex = r"""[^a-zA-Z0-9! *$@?_#\-'"+<>()\[\]:=,.;/&\\{}%\n]"""
	orders_result = re.sub(regex.encode('utf-8'), b'', orders_result)
	
	"""
	Test code
	
	getter_data = "p=123qwfpgjluy_098&mode=posts&topic=3222&till=1280571856&from=1278780343"
	orders_result = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	orders_result = orders_result.decode('utf-8')
	print(orders_result)
	
	"""
	
	orders_result = convert_donwloaded_orders(orders_result)
	
	# Delete it first, just incase
	query = """DELETE FROM post_cache WHERE topic = %d AND turn = %d""" % (topic_id, turn_number)
	try: cursor.execute(query)
	except Exception as e:
		print("Query: %s\n" % query)
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Delete order cache too
	query = """DELETE FROM orders WHERE topic = %d AND turn = %d""" % (topic_id, turn_number)
	try: cursor.execute(query)
	except Exception as e:
		print("Query: %s\n" % query)
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Save it to the database
	query = """INSERT INTO post_cache (topic, turn, content)
		values
		(%d, %d, '%s');""" % (topic_id, turn_number, database.escape(orders_result))
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	return orders_result

def convert_donwloaded_orders(orders_result):
	"""In go the orders from the board, out comes something for the database"""
	
	# If left as bytes we need it back as a str
	if type(orders_result) == bytes:
		orders_result = orders_result.decode('utf-8')
	
	# Currently no string modifacation is needed, this function is here incase it becomes needed
	return orders_result

def close_orders(cursor, closing_text, test_mode=False):
	args		= [];
	arg_count	= -1;
	
	query = "SELECT name, orders_topic, intorders_topic, forum_url_id, leader_id FROM teams WHERE active = True"
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	for row in cursor:
		if row['orders_topic'] != 0 and row['forum_url_id'] != 0:
			arg_count += 1
			args.append("t%(arg_count)s=%(orders_topic)s&f%(arg_count)s=%(forum_url)s" % {
				"arg_count":	arg_count,
				"orders_topic":	row['orders_topic'],
				"forum_url":	row['forum_url_id'],
			})
			if row['leader_id'] != 0:
				args.append("l%s=%s" % (arg_count, row['leader_id']))
		
		if row['intorders_topic'] != 0 and row['forum_url_id'] != 0:
			arg_count += 1
			args.append("t%(arg_count)s=%(intorders_topic)s&f%(arg_count)s=%(forum_url)s" % {
				"arg_count":		arg_count,
				"intorders_topic":	row['intorders_topic'],
				"forum_url":		row['forum_url_id'],
			})
			if row['leader_id'] != 0:
				args.append("l%s=%s" % (arg_count, row['leader_id']))
	
	args.append("pCount=%s" % arg_count)
	
	getter_data = "p=%s&mode=makePosts&time=%d&postContent=%s&%s" % (common.data['getterPass'], time.time(), closing_text.replace(' ', '%20'), "&".join(args))
	
	if not test_mode:
		reply = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	else:
		return "Close data: %s" % getter_data
	
	return True