#!/usr/bin/env python3

import queries

import os
import time
import sys
from multiprocessing import Process
from optparse import OptionParser
from pages import common
from classes import spy_world, world
import database
from functions import cli_f
import urllib.request, urllib.parse

# Padding
padding = "".join([" " for x in range(0, 8*1024)])

if __name__ == '__main__':
	os.system('clear')

def main():
	last_check = time.time()
	
def tests(options):
	print("Running tests")
	# import tests as tests_module
	# tests_module.main()
	
	if options.verbose:
		tests_path = "%s/tests.py -v" % common.data['server_fpath']
	else:
		tests_path = "%s/tests.py" % common.data['server_fpath']
		
	
	os.system('clear; python3 %s;' % tests_path)


twitter_username = "TWITTERNAME"
twitter_password = "PASSWORD"
def tweet(options):
	import base64
	
	def encode_credentials(username, password):
		byte_creds = '{}:{}'.format(username, password).encode('utf-8')
		return base64.b64encode(byte_creds).decode('utf-8')
	
	message = " ".join(sys.argv[2:len(sys.argv)])
	
	encoded_msg = urllib.parse.urlencode({'status': message})
	credentials = encode_credentials(twitter_username, twitter_password)
	request = urllib.request.Request('http://api.twitter.com/1/statuses/update.json')
	request.add_header('Authorization', 'Basic ' + credentials)
	urllib.request.urlopen(request, encoded_msg)
	
	print("Tweeted: %s" % message)

def cli_help(options):
	print("""msg
start, preorders, orders
sync, fix
check, test, report
int_topics, result_topics, new_cities
worker
all
to, ti, oh, map, tmap, wh, spyrep""")

def path_test(options):
	from test_library import basic_path_test
	basic_path_test.main()

def world_test(options):
	import world_test
	world_test.main()

def start(options, part):
	from pages.system import start as sys_start
	
	if options.verbose:
		print("Verbose mode")
	else:
		# exit("Script must be run in verbose mode")
		a = input("Run start script?: ")
		if a.lower() not in ["y", "yes"]:
			exit()
		else:
			print("Running start script")
	
	if part == "download":		sys_start.main(options)
	elif part == "pre_orders":	sys_start.pre_orders(options)
	elif part == "run_orders":		sys_start.run_orders(options)
	else:
		raise Exception("No mode found")
	
def sync(options, fix=False):
	import sync as sync_module
	if options.verbose:
		print(sync_module.main(fix=fix, show_fixes=True))
	else:
		print(sync_module.main(fix=fix))

def continents(options):
	import sync as sync_module
	print(sync_module.build_map())

def check(options):
	from checks import main_check
	main_check.main(check_all=options.all, verbose=options.verbose)

def reports(options):
	from reports import main_reports
	main_reports.main(options.verbose)

def find_requests(options):
	from queries import team_q
	from functions import request_f
	cursor = database.get_cursor()
	
	team_dict = team_q.get_real_active_teams(cursor)
	topic_list = []
	lookup = {}
	for k, v in team_dict.items():
		if v.request_topic > 0:
			topic_list.append(str(v.request_topic))
			lookup[str(v.request_topic)] = v.id
	
	topic_list = ",".join(topic_list)
	# print(topic_list)
	getter_data = "p=%s&mode=find_request_topics&topic_list=%s" % (common.data['getterPass'], topic_list)
	
	topics_to_read = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip().decode('utf-8')
	
	topic_list = topics_to_read.split("\n")
	
	if len(topic_list) < 1:
		if options.verbose:
			print(database.shell_text("No requests found"))
		return
	
	teams_to_read = []
	for t in topic_list:
		if t == '': continue
		teams_to_read.append(lookup[t])
	
	for t in teams_to_read:
		print(request_f.msn_run_orders(database.get_cursor(), t))
		time.sleep(options.delay)
	
	if options.verbose:
		print(database.shell_text("[g]Ran %d requests[/g]" % len(teams_to_read)))
	
	

def profile(options):
	from profile_library import profiler
	
	try:
		x = options.suite
	except Exception as e:
		print("No suite supplied to profile, select with -s")
		exit()
	
	if options.verbose:
		profiler.view(options)
	else:
		profiler.run(options)

def backup(options):
	file_path = "%s/backup/turn_%s.sql" % (common.data['server_fpath'], common.current_turn())
	args = "-h localhost -U postgres"
	
	os.system("pg_dump %s rob3 -f %s" % (args, file_path))
	
	if options.verbose:
		print(database.shell_text("[g]Database backed up[/g]"))
	
	# file_path = "%s/backup/rob2_%s.sql" % (common.data['server_fpath'], common.current_turn())
	# os.system("pg_dump %s rob2 -f %s" % (args, file_path))

def test_all(options):
	options.all = True
	
	tests(options)
	
	options.verbose = True
	
	the_world = spy_world.Spy_world(database.get_cursor())
	cli_f.output_ti(options, the_world, skip_upload=True)
	cli_f.output_to(options, the_world, skip_upload=True)
	cli_f.output_stats(options, the_world, skip_upload=True)
	cli_f.output_map(options, the_world, skip_upload=True)
	cli_f.output_wh(options, the_world, skip_upload=True)
	cli_f.output_oh(options, the_world, skip_upload=True)
	cli_f.output_spyrep(options, the_world, skip_upload=True)
	cli_f.output_tmap(options, the_world, skip_upload=True)
	cli_f.output_json(options, skip_upload=True)
	
	funcs = (
		the_world.relations,
		the_world.border_history,
		# the_world.prep_for_orders(self):,
		# the_world.prep_for_to(self):,
		# the_world.prep_for_stats(self):,
		# the_world.prep_for_oh(self):,
		# the_world.prep_for_ti(self):,
		# the_world.prep_for_start(self):,
		# the_world.building_requirements(self):,
		# the_world._lookup(self, name, lower=False, force_requery=False):,
		the_world.artefacts_lookup,
		the_world.armies_lookup,
		the_world.buildings_lookup,
		the_world.cities_lookup,
		the_world.campaigns_lookup,
		the_world.deities_lookup,
		the_world.equipment_lookup,
		the_world.evolutions_lookup,
		the_world.operatives_lookup,
		the_world.powers_lookup,
		the_world.spells_lookup,
		the_world.techs_lookup,
		the_world.teams_lookup,
		the_world.squads_lookup,
		the_world.units_lookup,
		the_world.wonders_lookup,
		# the_world._build_lookup_from_team(self, name, force_requery=False):,
		# the_world._lookup_all_from_team(self, name, force_requery=False):,
		# the_world._lookup_from_team(self, name, team_id, force_requery=False):,
		# the_world.armies_lookup_from_team(self, team_id, force_requery=False):,
		# the_world.units_lookup_from_team(self, team_id, force_requery=False):,
		# the_world._dict(self, name, force_requery=False):,
		the_world.armies,
		the_world.artefacts,
		the_world.buildings,
		the_world.cities,
		the_world.campaigns,
		the_world.deities,
		the_world.equipment,
		the_world.evolutions,
		the_world.kills,
		the_world.servants,
		the_world.operatives,
		the_world.powers,
		the_world.players,
		the_world.spells,
		the_world.techs,
		the_world.squads,
		the_world.teams,
		the_world.units,
		# the_world.json_ti(self, team, turn, force_requery=False),
		the_world.wonders,
		# the_world._build_from_team(self, name, force_requery=False):,
		# the_world._all_from_team(self, name, force_requery=False):,
		# the_world._from_team(self, name, team_id, force_requery=False):,
		# the_world.armies_from_team(self, team_id, force_requery=False):,
		# the_world.cities_from_team(self, team_id, force_requery=False):,
		# the_world.kills_from_turn(self, team_id, force_requery=False):,
		# the_world.kills_from_camp(self, team_id, force_requery=False):,
		# the_world.players_from_team(self, team_id, force_requery=False):,
		# the_world.operatives_from_team(self, team_id, force_requery=False):,
		# the_world.squads_from_team(self, team_id, force_requery=False):,
		# the_world.units_from_team(self, team_id, force_requery=False):,
		# the_world.squads_lookup_from_army(self, army_id, force_requery=False):,
		the_world.cities_with_wonders,
		the_world.cities_with_artefacts,
		the_world.active_teams,
		the_world.live_cities,
		# the_world.live_cities_from_team(self, team_id, force_requery=False):,,
		
		# armies_by_base(self, base, force_requery=False)
		# armies_in_area(self, area, radius=10, force_requery=False)
		# operatives_in_area(self, area, radius=10, force_requery=False)
		# operatives_in_city(self, city_id, force_requery=False)
		# cities_in_area(self, area, radius=10, force_requery=False)
		# race_difference(self, race_1, race_2)
	)
	
	for f in cli_f.progressbar(funcs, "Testing world: ", 60, True):
		f()
	

def check_all(options):
	options.all = True
	options.verbose = True
	check(options)

def output_all(options, nightly=False):
	start_time = time.time()
	
	print(database.shell_text("''Running tests''"))
	tests(options)
	
	print(database.shell_text("''Running checks''"))
	check_all(options)
	
	print(database.shell_text("''Building world''"))
	the_world = spy_world.Spy_world(database.get_cursor())
	
	cli_f.output_ti(options, the_world)
	cli_f.output_to(options, the_world)
	cli_f.output_stats(options, the_world)
	cli_f.output_map(options, the_world)
	cli_f.output_wh(options, the_world)
	cli_f.output_oh(options, the_world)
	cli_f.output_spyrep(options, the_world)
	cli_f.output_tmap(options, the_world)
	cli_f.output_json(options)
	
	print(database.shell_text("''Completed in %s seconds (delay of %s)''" % (int(time.time() - start_time), options.delay)))

def db_convert(options):
	import db_convert as db_convert_module
	db_convert_module.main()
	
	# Now fix and check
	sync(options, fix=True)
	check(options)

def int_topics(options):
	from functions import team_f
	team_f.open_int_orders(database.get_cursor())

def result_topics(options):
	from functions import team_f
	team_f.open_results(database.get_cursor())

def new_cities(options):
	from queries import city_q
	city_dict = city_q.get_new_cities(database.get_cursor())
	
	for city_id, the_city in city_dict.items():
		cmd = "open http://localhost/rob3/web.py?mode=view_map\\&{map_link}".format(
			map_link = the_city.map_link_args().replace('&amp;', '\\&'),
		)
		os.system(cmd)

def ops_catching():
	from functions import operative_f
	the_world = spy_world.Spy_world(database.get_cursor())
	the_world.cursor.execute("BEGIN")
	operative_f.catch_operatives(the_world, verbose=True)
	the_world.cursor.execute("ROLLBACK")
	exit("Exit()")

# Script that runs in the background
def worker(options):
	import socket, imp
	
	tests(options)
	print("Worker running")
	options.verbose = True
	options.delay = 7
	
	last_upload = time.time()
	
	backup(options)
	try:
		while True:
			imp.reload(database)
			
			update_function = cli_f.Timeout_function(urllib.request.urlopen, 20)
			requests_function = cli_f.Timeout_function(find_requests, 30)
			try:
				requests_function(options)
			except cli_f.Timeout_exception:
				print("Timeout for find_requests")
			except urllib.request.URLError as e:
				print("URL request error")
			except Exception as e:
				raise
			
			# Upload twice a day
			if time.time() - last_upload > 60*60*12:
				check(options)
				"""
				the_world = spy_world.Spy_world(database.get_cursor())
				cli_f.output_to(options, the_world)
				cli_f.output_map(options, the_world)
				cli_f.output_ti(options, the_world)
				cli_f.output_stats(options, the_world)
				cli_f.output_oh(options, the_world)
				cli_f.output_spyrep(options, the_world)
				cli_f.output_tmap(options, the_world)
				"""
				
				try:
					getter_results = update_function(common.data['rob_url'], "mode=get_players").read()
				except cli_f.Timeout_exception:
					print("Timeout for get_players")
				
				try:
					getter_results = update_function(common.data['rob_url'], "mode=get_teams").read()
				except cli_f.Timeout_exception:
					print("Timeout for get_teams")
				
				last_upload = time.time()
			
			time.sleep(60*2)
			
	except KeyboardInterrupt as e:
		print(database.shell_text("[c]Exiting from keyboard interrupt[/c]"))
		exit()
		
	except Exception as e:
		raise
		

def learn(options):
	from functions import city_f, trade_f
	from classes import world
	from rules import sad_rules
	import sys
	
	from functions import bpnn
	from functions import neural_f
	
	# print("  {result:6} {target:6} {diff:6} {percent:6} {current:8}          ".format(
	# 	result = "Res",
	# 	target = "Targ",
	# 	diff = "Diff",
	# 	percent = "Perc",
	# 	current = "Curr",
	# ))
	
	def test_func(inputs, max_count = 100):
		totals = {}
		sad_rules.supply_factor = inputs
		
		w = world.World(database.get_cursor())
		city_f.apply_city_matrix(w)
		
		for r in sad_rules.res_list:
			totals[r] = 0
		
		# for i in cli_f.progressbar(range(0, max_count), prefix = "", size = 60, with_eta=True):
		for i in range(0, max_count):
			res = trade_f.supply_and_demand(w)
			
			for r in sad_rules.res_list:
				totals[r] += (res['production'][r][0]/res['demand'][r][0])
		
		# Get average
		avg = {}
		for r in sad_rules.res_list:
			avg[r] = totals[r]/max_count
		
		return avg
	
	inputs = dict(sad_rules.supply_factor)
	
	targets = {
		# Basics (90%)
		"Grain":			0.90,
		"Linen":			0.90,
		"Wool":				0.90,
		
		# Nice (40%)
		"Pottery":			0.40,
		"Olives":			0.40,
		"Wine":				0.40,
		"Dairy":			0.40,
		"Meat":				0.40,
		"Salt":				0.40,
		
		# Luxury (15%)
		"Silk":				0.15,
		"Furs":				0.15,
		"Gems":				0.15,
		"Glass":			0.15,
		"Precious metals":	0.15,
		"Spices":			0.15,
		
		# Exotic (0-1%)
	}
	
	mapping = {}
	
	
	NN = neural_f.NN(test_func, inputs, targets, mapping, cycles=10000)
	NN.train()
	# neural_f.train(test_func, inputs, targets, mapping)
	
	# trade_f.print_reports(w, res)

def trade_real(options):
	from functions import city_f, trade_f, sad_f
	from classes import world
	from rules import sad_rules
	import sys
	
	w = world.World(database.get_cursor())
	city_f.apply_city_matrix(w)
	
	res = sad_f.supply_and_demand(w)
	
	# trade_f.print_reports(w, res, ['res_summary', 'res_surplus', 'res_demand', 'res_producers', 'production', 'demand', 'wealth'])
	# sad_f.print_reports(w, res, ['res_summary', 'demand', 'wealth'])
	
	total_sat = 0
	big_sat = 0
	big_count = 0
	wealth = 0
	for k, v in w.live_cities().items():
		total_sat += v.satisfaction()
		wealth += v.wealth
		
		if v.size > 15000:
			big_sat += v.satisfaction()
			big_count += 1
	
	print("Avg wealth: %s" % (wealth/len(w.live_cities())))
	print("Average: %s" % (total_sat/len(w.live_cities())))
	print("Big average: %s" % (big_sat/big_count))
		

def trade_build(options):
	from functions import trade_f
	from classes import world
	
	w = world.World(database.get_cursor())
	trade_f.build_distance_matrix(w, verbose=True)

def build_site(options):
	from lore import builder, page_saver
	
	cursor = database.get_cursor()
	page_saver.rebuild_pages(cursor)
	builder.build(cursor, options.verbose)

def get_lore(options):
	from data_classes import lore_entry
	from lore import pages
	
	if len(sys.argv) < 3:
		print("Usage: $rob lore <cat> <page> <type:html/bbcode/plain>")
		exit()
	
	cursor = database.get_cursor()
	
	try:
		category = sys.argv[2]
		page = sys.argv[3]
		
		if len(sys.argv) > 4:
			formatting = sys.argv[4]
		else:
			formatting = "plaintext"
		
		if len(sys.argv) > 5:
			level = sys.argv[5].lower()
		else:
			level = "public"
	except Exception as e:
		raise
	
	if formatting == "html":
		print(pages.get_html(cursor, category, page, level))
	elif formatting == "bbcode":
		print(pages.get_bbcode(cursor, category, page, level))
	elif formatting == "plain" or formatting == "plaintext":
		print(pages.get_plaintext(cursor, category, page, level))
	

def build_voi(options):
	from functions import voi_f
	w = world.World(database.get_cursor())
	
	files = voi_f.build_turn(w)
	cli_f.upload_voi(options, files)

def build_voi_battle(options):
	options.delay = 0
	options.verbose = True
	
	from functions import voi_f
	battle = " ".join(sys.argv[2:len(sys.argv)])
	
	files = voi_f.build_battle(world.World(database.get_cursor()), battle=battle)
	cli_f.upload_voi(options, files)

def build_voi_campaign(options):
	options.delay = 0
	options.verbose = True
	
	from functions import voi_f
	campaign = " ".join(sys.argv[2:len(sys.argv)])
	
	files = voi_f.build_campaign(world.World(database.get_cursor()), campaign=campaign)
	cli_f.upload_voi(options, files)

def build_voi_forum(options):
	from functions import voi_f
	w = world.World(database.get_cursor())
	voi_f.update_topic_new(w)
	voi_f.update_topic_old(w)

func_dict = {
	"site":	build_site,
	"lore":	get_lore,
	
	"voi":	build_voi,
	"voib":	build_voi_battle,
	"voic":	build_voi_campaign,
	"voif":	build_voi_forum,
}

if __name__ == '__main__':
	# exit('Compiled correctly')
	
	parser = OptionParser()
	parser.add_option("-m", "--mode", dest="mode", default="")
	parser.add_option("-v", "--verbose", dest="verbose", default=False)
	parser.add_option("-s", "--suite", dest="suite", default="")
	parser.add_option("-t", "--team", dest="team", default="")
	parser.add_option("-p", "--player", dest="player", default="")
	parser.add_option("-d", "--delay", dest="delay", default=2)
	parser.add_option("-l", "--local", dest="local", default=False)
	parser.add_option("-a", "--all", dest="all", default=False)
	
	(options, args) = parser.parse_args()
	
	# By default you don't need to specify -m for mode
	if options.mode == "" and len(args) > 0: options.mode = args[0]
	
	if options.mode.lower() == "tests":				tests(options)
	elif options.mode.lower() == "test":			tests(options)
	elif options.mode.lower() == "msg":			tweet(options)
	
	elif options.mode.lower() == "h":				cli_help(options)
	elif options.mode.lower() == "help":			cli_help(options)
	
	elif options.mode.lower() == "pathtest":		path_test(options)
	elif options.mode.lower() == "ptest":			path_test(options)
	
	elif options.mode.lower() == "world_test":		world_test(options)
	elif options.mode.lower() == "wtest":			world_test(options)
	
	elif options.mode.lower() == "start":			start(options, "download")
	elif options.mode.lower() == "preorders":		start(options, "pre_orders")
	elif options.mode.lower() == "orders":			start(options, "run_orders")
	
	elif options.mode.lower() == "trade":			trade(options)
	elif options.mode.lower() == "learn":			learn(options)
	elif options.mode.lower() == "trade_build":		trade_build(options)
	
	elif options.mode.lower() == "sync":			sync(options)
	elif options.mode.lower() == "fix":				sync(options, fix=True)
	elif options.mode.lower() == "continents":		continents(options)
	elif options.mode.lower() == "convert":			db_convert(options)
	elif options.mode.lower() == "check":			check(options)
	elif options.mode.lower() == "checkall":		check_all(options)
	
	elif options.mode.lower() == "report":			reports(options)
	elif options.mode.lower() == "reports":			reports(options)
	elif options.mode.lower() == "int_topics":		int_topics(options)
	elif options.mode.lower() == "result_topics":	result_topics(options)
	elif options.mode.lower() == "new_cities":		new_cities(options)
	elif options.mode.lower() == "profile":			profile(options)
	
	elif options.mode.lower() == "spyrep":			cli_f.output_spyrep(options)
	elif options.mode.lower() == "stats":			cli_f.output_stats(options)
	elif options.mode.lower() == "map":				cli_f.output_map(options)
	elif options.mode.lower() == "tmap":			cli_f.output_tmap(options)
	elif options.mode.lower() == "ti":				cli_f.output_ti(options)
	elif options.mode.lower() == "oh":				cli_f.output_oh(options)
	elif options.mode.lower() == "wh":				cli_f.output_wh(options)
	elif options.mode.lower() == "to":				cli_f.output_to(options)
	elif options.mode.lower() == "json":			cli_f.output_json(options)
	elif options.mode.lower() == "all":				output_all(options)
	elif options.mode.lower() == "nightly":			output_all(options, nightly=True)
	
	elif options.mode.lower() == "testall":			test_all(options)
	
	elif options.mode.lower() == "backup":			backup(options)
	
	elif options.mode.lower() == "requests":		requests(options)
	elif options.mode.lower() == "fr":				find_requests(options)
	
	elif options.mode.lower() == "worker":			worker(options)
	elif options.mode.lower() == "trade":			trade(options)
	
	elif options.mode.lower() == "qtest":# quickly test something
		cursor = database.get_cursor()
		
		# from queries import city_q, battle_q
		# city_dict = city_q.get_live_cities(cursor)
		# battle_dict = battle_q.get_all_battles(cursor)
		# 
		# output = []
		# 
		# for k, v in battle_dict.items():
		# 	for i, c in city_dict.items():
		# 		if v.x == c.x:
		# 			if v.y == c.y:
		# 				output.append("UPDATE battles SET city = %d WHERE id = %d;" % (i, k))
		# 
		# 
		# print("\n".join(output))
		
		
		
		
	
	# Just for testing the capture of operatives
	elif options.mode.lower() == "ops":
		ops_catching()
	
	# Quick and dirty calc for testing res dicts
	elif options.mode.lower() == "restest":
		from classes import res_dict
		
		spell_cost = res_dict.Res_dict("Destruction points:100,(Spell points:Destruction points)")
		team_res = res_dict.Res_dict("Destruction points:20,Spell points:20")
		
		results = team_res.affordable(spell_cost, overbudget_list=[""], verbose=True)
		
		print("")
		print(results[0])
		print(str(res_dict.Res_dict(results[1])))
	
	else:
		# Try the func dict
		if options.mode.lower() in func_dict:
			func_dict[options.mode.lower()](options)
		else:
			# Standard mode
			try:
				print("No mode of %s found, running interactive mode" % options.mode)
				main()
			except KeyboardInterrupt:
				exit("Exiting from keyboard interrupt")
