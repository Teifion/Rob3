"""
This is not designed to be called as a web-page, it's a terminal script.

82 - 1279969267
83 - 1280571856 (should be 1279968771)

1280571856-1279968771
"""

import os
import time
import re
import database
import collections
from classes import spy_world, order_block, res_dict
from pages import common
from functions import system_f, order_post_f, operative_f, results_f, cli_f
from functions import team_f, power_f, artefact_f, player_f, army_f, stat_f
from queries import team_q

def main(options):
	orders_str = ""
	if not options.local:
		while orders_str == "":
			orders_input = input("Orders closing text (default 'Turn %d approaches'): " % (common.current_turn() + 2))
		
			if orders_input == "":
				orders_str = "Turn %d approaches" % (common.current_turn() + 2)
			else:
				orders_str = orders_input
			
			orders_input = input("Confirm that you are happy with '%s': " % orders_str)
			if orders_input.lower() not in ["y", "yes"]:
				orders_str = ""
	# orders_str = "IGNORE"
	
	start_time = time.time()
	cursor = database.get_cursor()
	the_world = spy_world.Spy_world(cursor)
	cursor.track_queries = True
	team_dict = the_world.active_teams()
	turn = common.current_turn()
	
	cursor.execute("BEGIN")
	#	Timestamp
	#------------------------
	print(database.shell_text("Updating timestamp"), end="")
	try:
		database.query(cursor,
			system_f.add_turn_timestamp(common.current_turn()+2))
		
		# Refresh timestamp
		common.data['current_turn'] += 1
		turn = common.data['current_turn']
	except Exception as e:
		print(database.shell_text(" - [r]Failure[/r]"))
		raise
	
	print(database.shell_text(" - [g]Done[/g]"))
	
	#	Close orders
	#------------------------
	print(database.shell_text("Closing orders"), end="")
	try:
		result = order_post_f.close_orders(cursor, orders_str, test_mode=options.verbose)
	except Exception as e:
		print(database.shell_text(" - [r]Failure[/r]"))
		raise
	
	print(database.shell_text(" - [g]Done[/g]"))
	
	#	Get orders
	#------------------------
	print(database.shell_text("Downloading orders:"))
	for team_id, the_team in team_dict.items():
		try:
			if the_team.orders_topic > 0:
				order_post_f.get_orders(cursor, the_team.orders_topic, turn, team_id,
					recache=True, delay=options.delay)
			
			if the_team.intorders_topic > 0:
				order_post_f.get_orders(cursor, the_team.intorders_topic, turn, team_id,
					recache=True, delay=options.delay)
			
			print(database.shell_text("%s - [g]Done[/g]" % the_team.name))
		except Exception as e:
			print(database.shell_text("[r]ERROR[/r]"))
			print("Failure downloading orders for %s" % the_team.name)
			raise
	
	cursor.execute("COMMIT")
	print(database.shell_text("\nNow run [g]rob preorders[/g]"))

def pre_orders(options):
	start_time = time.time()
	cursor = database.get_cursor()
	the_world = spy_world.Spy_world(cursor)
	team_dict = the_world.active_teams()
	
	#	Stats first, it's used for some favour stuff
	#------------------------
	for team_id, the_team in team_dict.items():
		stat_f.build_team_stats(the_world.cursor, the_team, the_world)
	
	# Now to assign the stats
	team_q.mass_get_team_stats(the_world.cursor, team_dict, common.current_turn())
	
	#	Pre orders - Teams
	#------------------------
	cursor.execute("BEGIN")
	print(database.shell_text("Team pre-orders"), end="")
	for team_id, the_team in team_dict.items():
		try:
			team_f.pre_orders(the_world, the_team)
		except Exception as e:
			cursor.execute("ROLLBACK")
			print(database.shell_text(" - [r]Failure[/r]"))
			print("Failure running pre-orders for %s" % the_team.name)
			print(database.shell_text("[r]Re run as 'rob3 start -l True[/r]'"))
			raise
	
	print(database.shell_text(" - [g]Done[/g]"))
	
	#	Pre orders - System
	#------------------------
	print(database.shell_text("System pre-orders"), end="")
	try:
		# Army history
		army_f.location_history(the_world)
		
		# Player history
		player_f.turn_history(the_world)
		
		# Power history
		power_f.turn_history(the_world)
		
		# Artefact history
		artefact_f.turn_history(the_world)
		
		# Operatives catching
		operative_f.catch_operatives(the_world)
		
		# Border history
		team_f.border_history(the_world)
	
	except Exception as e:
		cursor.execute("ROLLBACK")
		print(database.shell_text(" - [r]Failure[/r]"))
		print(database.shell_text("[r]Re run as 'rob3 start -l True[/r]'"))
		raise
	
	cursor.execute("COMMIT")
	print(database.shell_text("\nNow run [g]rob orders[/g]"))


def run_orders(options):
	start_time = time.time()
	cursor = database.get_cursor()
	cursor.track_queries = True
	the_world = spy_world.Spy_world(cursor)
	team_dict = the_world.active_teams()
	
	#	Run orders
	#------------------------
	print(database.shell_text("Running orders"), end="")
	queries, orders, debug = [], ["Team orders\n"], []
	the_world.prep_for_orders()
	
	try:
		player_updates = {}
		the_orders = order_post_f.get_turn_orders(cursor, the_world)
		
		blocks = []
		# for o in the_orders:
		for o in cli_f.progressbar(the_orders, "Splitting: ", 60, True):
			o.split()
			blocks.extend(o.blocks)
		
		# Setup
		# for b in blocks:
		for b in cli_f.progressbar(blocks, "Setting up: ", 60, True):
			b.setup()
			b.always_debug = True
		
		# Execution, in order of priority
		for priority in order_block.priorities:
			c = 0
			
			for b in blocks:
				if b.priority != priority:
					continue
				
				try:
					b.execute()
				except Exception as e:
					print("")
					print(b.title_name)
					print(the_world.teams()[b.team].name)
					print("\n".join(cursor.queries[-5:-1]))
					print("")
					raise
		
		# Ensure we've handled all blocks
		for b in blocks:
			if not b.handled:
				raise Exception("Block with priority '%s' not handled" % b.priority)
		
		team_output = {}
		manual_output = {}
		team_debug = {}
		team_failures = {}
		for b in cli_f.progressbar(blocks, "Running Blocks: ", 60, True):
		# for b in blocks:
			if b.team not in team_output:
				team_output[b.team] = []
			
			if b.team not in team_debug:
				team_debug[b.team] = []
			
			if b.team not in team_failures:
				team_failures[b.team] = []
			
			if b.team not in manual_output:
				manual_output[b.team] = []
			
			# Player activity needs to get updated
			player_updates[b.post.player] = b.post.team
			
			# team_output[b.team].append("[o]%s[/o]" % b.title_name)
			team_output[b.team].append("\n".join(b.results))
			team_output[b.team].append("")
			
			if b.manual_handle:
				manual_output[b.team].append("\n".join(b.results))
				manual_output[b.team].append("")
			
			# Failures
			if len(b.failures) > 0:
				team_failures[b.team].append("\n".join(b.failures))
				team_failures[b.team].append("")
			
			# Debug
			team_debug[b.team].append(b.debug[0])
			team_debug[b.team].append("\n---\n".join(b.debug[1:len(b.debug)]))
			team_debug[b.team].append("")
			
			# Foreign results
			for team_id, res in b.foreign_results.items():
				if team_id not in team_output:
					team_output[team_id] = []
				team_output[team_id].insert(0, "")
				team_output[team_id].insert(0, "\n".join(res))
			
			# Queries
			for team_id, fqueries in b.foreign_queries.items():
				queries.extend(fqueries)
			
			queries.extend(b.queries)
		
		
		
		for team_id, the_team in team_dict.items():
			if the_team.ir: continue
			
			orders.append("""# %s
######################################################################
[fullbox=#EEF,#AAF][h4]Turn %d Results[/h4][/fullbox]

[url=http://woarl.com/stats/%s.html]Rob results[/url]

""" % (the_team.name, common.current_turn(), team_f.team_hash(the_team.name)))
			
			if team_id in team_output:
				if team_id in manual_output:
					# orders.extend(team_output[team_id])
					orders.extend(manual_output[team_id])
			
			if team_id in team_debug:
				debug.extend(team_debug[team_id])
		
		# Update player activity
		database.query(cursor,
			player_f.update_player_activity(player_updates))
		
		# Save results
		results_f.save_results(cursor, team_output)
		results_f.save_failures(cursor, team_failures)
		
		# Now we work out the costs
		team_costs = {}
		for t, the_team in team_dict.items():
			r = res_dict.Res_dict(the_team.resources)
			queries.extend(r.make_set_queries(t))
		
		# Write queries to file
		f = open('%s/script_output/queries.sql' % common.data['server_fpath'], 'w')
		f.write("\n".join(queries))
		f.close()
		
		# Write orders to file
		f = open('%s/script_output/orders.txt' % common.data['server_fpath'], 'w')
		f.write("\n".join(orders))
		f.close()
		
		# Write debug to file
		f = open('%s/script_output/debug.txt' % common.data['server_fpath'], 'w')
		f.write("Team orders\n\n")
		f.write("\n".join(debug))
		f.close()
		
	except Exception as e:
		print(database.shell_text("[r]Failure[/r]"))
		print(database.shell_text("[r]Re run as 'rob3 start -l True[/r]'"))
		raise
	
	# print(database.shell_text(" - [g]Done[/g]"))
	# os.system('mate %s' % '%s/queries.sql' % common.data['server_fpath'])
	# os.system('mate %s' % '%s/orders.txt' % common.data['server_fpath'])
	
	# Failable orders
	failable = (
		re.compile(r'DELETE FROM squads WHERE id = [0-9]*;?'),
	)
	
	failed_queries = []
	
	#	Execute order queries
	#------------------------
	# print(database.shell_text("Executing order queries"), end="")
	for q in cli_f.progressbar(queries, "Running queries: ", 60, True):
	# for q in queries:
		if q == '': continue
		if q[0:2] == '--': continue
		
		try:
			cursor.execute(q)
		except Exception as e:
			ignorable = False
			
			for f in failable:
				if f.search(q) != None:
					ignorable = True
					failed_queries.append(q)
			
			if not ignorable:
				for f in failable:
					print("")
					print(f.search(q))
					print("")
			
				cursor.execute('ROLLBACK')
				print(database.shell_text(" - [r]Failure[/r]"))
				print("Query: %s\n" % q)
				print(database.shell_text("[r]Re run as 'rob3 start -l True'[/r]"))
				raise
	
	# print(database.shell_text(" - [g]Done[/g]"))
	
	if len(failed_queries) > 0:
		print("Failed queries")
		print("\n".join(failed_queries))
	
	# Build up a dict of the queries
	query_dict = {}
	for q in cursor.queries:
		if q in ("BEGIN", "COMMIT", "ROLLBACK"): continue
		
		if q not in query_dict:
			query_dict[q] = 0
		
		query_dict[q] += 1
	
	# What's our most popular query?
	pop_count, pop_query = 0, ""
	for q, c in query_dict.items():
		if c > pop_count:
			pop_count = c
			pop_query = q
	
	print("\n\n--- Info ---")
	print("Time taken: %s" % str(round(time.time() - start_time, 3))[0:5])
	print("Queries: %d" % len(cursor.queries))
	print("Uniques: %d" % len(set(cursor.queries)))
	print("Most queried: %s (%d)" % (pop_query, pop_count))
	
	#	Verbose mode
	#------------------------
	if options.verbose:
		cursor.execute("ROLLBACK")
		print("Rolled back")
	else:
		cursor.execute("COMMIT")
		print("Startup scripts executed")
		os.system("open %s/script_output/orders.txt" % common.data['server_fpath'])
		
		# print("\n".join(cursor.queries))
