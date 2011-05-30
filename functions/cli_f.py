import database
from pages import common
from ftplib import FTP
import urllib.request
from classes import world, spy_world
from functions import team_f, ti_f
from queries import team_q
import signal
import sys
import time

ftp_pass = {
	"data":		"PASSWORD",
	"spyrep":	"PASSWORD",
	'wh':		"PASSWORD",
	"map":		"PASSWORD",
	"gm":		"PASSWORD",
	"voi":		"PASSWORD",
	"orders":	"PASSWORD",
	"stats":	"PASSWORD",
	"ti":		"PASSWORD",
	"to":		"PASSWORD",
	"tmap":		"PASSWORD",
}

padding = "".join([" " for x in range(0, 8*1024)])

class Timeout_exception(Exception):
	def __init__(self, value="Timeout error"):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

class Timeout_function:
	def __init__(self, function, timeout):
		self.timeout	= timeout
		self.function	= function
	
	def handle_timeout(self, signum, frame):
		raise Timeout_exception()
	
	def __call__(self, *args):
		old = signal.signal(signal.SIGALRM, self.handle_timeout)
		signal.alarm(self.timeout)
		try:
			result = self.function(*args)
		finally:
			signal.alarm(0)
			signal.signal(signal.SIGALRM, old)
		signal.alarm(0)
		return result

def progressbar(it, prefix = "", size = 60, with_eta=False):
	"""
	for i in progressbar(range(15), "Computing: ", 40):
		 time.sleep(0.1) # long computation
	"""
	
	count = len(it)
	start_time = time.time()
	
	def _show(_i):
		eta_string = ""
		if _i > 0:
			time_so_far = time.time() - start_time
			time_per_item = time_so_far / _i
			eta = (count - _i) * time_per_item
			
			if with_eta:
				eta_string = "  eta %s" % round(eta, 1)
			
			if eta < 0.1:
				eta_string = "           "
		
		x = int(size*_i/count)
		sys.stdout.write("%s[%s%s] %i/%i%s\r" % (prefix, "#"*x, "."*(size-x), _i, count, eta_string))
		sys.stdout.flush()
	
	_show(0)
	for i, item in enumerate(it):
		yield item
		_show(i+1)
	# sys.stdout.write("".join([" " for i in range(size + 40)]))
	# sys.stdout.flush()
	
	# Cleanup
	time_so_far = time.time() - start_time
	
	if with_eta:
		eta_string = " in %ss" % round(time_so_far, 1)
		
		sys.stdout.write("%s[%s%s] %i/%i%s\r" % (prefix, "#"*size, "."*0, count, count, eta_string))
		sys.stdout.flush()
	
	print()

def upload(ftp_host, ftp_user, ftp_pass, files, delay=2, verbose=True):
	if verbose: print("Connecting")
	ftp = FTP(ftp_host, ftp_user, ftp_pass)
	
	# if verbose:
	print("Connected to %s, uploading %s files" % (ftp_user, len(files)))
	
	for file_name, file_path in progressbar(files.items(), "Uploading: ", 60, True):
		fname = 'STOR %s' % file_name
		data = open(file_path, 'rb')
		
		ftp.storbinary(fname, data)
		time.sleep(int(delay))

	ftp.quit()
	if verbose: print("Disconnected")

def output_to(options, the_world=None, skip_upload=False):
	from functions import to_f
	
	files = {}
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = world.World(cursor)
	else:
		cursor = the_world.cursor
	the_world.prep_for_to()
	
	headers = to_f.headers(the_world)
	footers = to_f.footers(the_world)
	js = to_f.javascript(the_world)
	output = to_f.make_to(the_world)
	
	to_source = "".join([headers, js, output, footers])
	
	# the_to = urllib.request.urlopen(common.data['rob_url'], 'mode=to&dev_mode=0&ajax=1')
	# the_to = urllib.request.urlopen(web_url, 'mode=to&dev_mode=0&ajax=1')
	# to_source = the_to.read()
	
	f = open('%s/to/index.html' % common.data['woa_folder'], 'w')
	f.write(to_source)
	f.write(padding)
	f.close()
	
	files['index.html'] = '%s/to/index.html' % common.data['woa_folder']
	
	if not skip_upload:
		upload("ftp.woarl.com", "to@woarl.com", ftp_pass['to'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Team Overview uploaded[/g]'))

def output_map(options, the_world=None, skip_upload=False):
	from classes import mapper
	from rules import region_data
	
	if the_world != None:
		cursor = the_world.cursor
	else:
		cursor = database.get_cursor()
	files = {}
	
	#	Map Selector
	#------------------------
	from pages.map import map_select
	f = open('%s/map/index.html' % common.data['woa_folder'], 'w')
	f.write(map_select.make_map_select(cursor))
	f.write(padding)
	f.close()
	
	files['index.html'] = '%s/map/index.html' % common.data['woa_folder']
	
	#	Big map
	#------------------------
	the_map = mapper.Map_maker()
	the_map.icon_path = 'images/teamIcons/'
	source_dict = {
		"build":				1,
		"output":				the_map.map_grid(cursor),
	}
	
	map_source = mapper.map_source(source_dict)
	
	f = open('%s/map/latest.html' % common.data['woa_folder'], 'w')
	f.write(map_source)
	f.write(padding)
	
	f = open('%s/map/turn_%d_normal.html' % (common.data['woa_folder'], common.current_turn()), 'w')
	f.write(map_source)
	f.write(padding)
	
	f.close()
	
	files['latest.html'] = '%s/map/latest.html' % common.data['woa_folder']
	files['turn_%d_normal.html' % common.current_turn()] = '%s/map/turn_%d_normal.html' % (common.data['woa_folder'], common.current_turn())
	
	# Now to make all the region maps
	# for r in region_data.region_list:
	for r in progressbar(region_data.region_list, "Creating Maps: ", 60, True):
		the_map = mapper.Map_maker()
		the_map.icon_path = 'images/teamIcons/'
		
		source_dict = region_data.get_source_dict(the_map, r.name)
		source_dict["output"] = the_map.map_grid(cursor)
		source_dict["build"] = 1
		
		map_source = mapper.map_source(source_dict)
		
		f = open('%s/map/latest_%s.html' % (common.data['woa_folder'], r.name.lower()), 'w')
		f.write(map_source)
		f.write(padding)
		f.close()
		
		f = open('%s/map/turn_%s_%s.html' % (common.data['woa_folder'], common.current_turn(), r.name.lower()), 'w')
		f.write(map_source)
		f.write(padding)
		f.close()
		
		files['latest_%s.html' % r.name.lower()] = '%s/map/latest_%s.html' % (common.data['woa_folder'], r.name.lower())
		files['turn_%s_%s.html' % (common.current_turn(), r.name.lower())] = '%s/map/turn_%s_%s.html' % (common.data['woa_folder'], common.current_turn(), r.name.lower())
	
	if not skip_upload:
		upload("ftp.woarl.com", "map@woarl.com", ftp_pass['map'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Map uploaded[/g]'))

def output_ti(options, the_world=None, skip_upload=False):
	from functions import ti_f
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = spy_world.Spy_world(cursor)
	else:
		cursor = the_world.cursor
	
	the_world.prep_for_ti()
	
	team_dict = team_q.get_real_active_teams(cursor)
	# if len(args) == 0:
	# 	team_dict = team_q.get_real_active_teams(cursor)
	# else:
	# 	team_dict = team_q.get_teams_in_list(cursor, team_list=args, by_id=False)
	
	files = {}
	for team_id in progressbar(team_dict.keys(), "Creating TIs: ", 60, True):
	# for team_id in team_dict.keys():
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			
			# Start of output related stuff
			headers = ti_f.headers(the_team)
			footers = ti_f.footers(the_team)
			js = ti_f.javascript(the_team)
			
			output = ti_f.make_ti(cursor, the_world, the_team)
		
			f = open('%s/ti/%s.html' % (common.data['woa_folder'], md5_name), 'w')
			f.write("".join([headers, output, footers]))
			f.write(padding)
			f.close()
			
			files['%s.html' % (md5_name)] = '%s/ti/%s.html' % (common.data['woa_folder'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "ti@woarl.com", ftp_pass['ti'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Team Infos uploaded[/g]'))
	
def output_oh(options, the_world=None, skip_upload=False):
	from classes import oh
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = world.World(cursor)
	else:
		cursor = the_world.cursor
	
	team_dict = team_q.get_real_active_teams(cursor)
	the_oh = oh.Oh(the_world.cursor, the_world)
	the_oh.setup(true_team_list=team_dict.keys())
	# if len(args) == 0:
	# 	team_list, team_dict = team_q.get_real_active_teams()
	# else:
	# 	team_list, team_dict = team_q.get_teams_in_list(team_list=args, by_id=False)
	
	files = {}
	# for team_id in team_dict.keys():
	for team_id in progressbar(team_dict.keys(), "Creating OHs: ", 60, True):
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			
			# # Start of output related stuff
			# headers = ti_f.headers(the_team)
			# footers = ti_f.footers(the_team)
			# js = ti_f.javascript(the_team)
			
			output = the_oh.make_oh(team_id)
		
			f = open('%s/orders/%s.html' % (common.data['woa_folder'], md5_name), 'w')
			# f.write("".join([headers, output, footers]))
			f.write(output)
			f.write(padding)
			f.close()
			
			files['%s.html' % (md5_name)] = '%s/orders/%s.html' % (common.data['woa_folder'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "orders@woarl.com", ftp_pass['orders'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Order helpers uploaded[/g]'))

def output_wh(options, the_world=None, skip_upload=False):
	from classes import wh
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = world.World(cursor)
	else:
		cursor = the_world.cursor
	
	team_dict = team_q.get_real_active_teams(cursor)
	the_wh = wh.Wh(the_world.cursor, the_world)
	the_wh.setup(true_team_list=team_dict.keys())
	
	files = {}
	for team_id in progressbar(team_dict.keys(), "Creating WHs: ", 60, True):
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			
			output = the_wh.make_wh(team_id)
			
			f = open('%s/wh/%s.html' % (common.data['woa_folder'], md5_name), 'w')
			f.write(output)
			f.write(padding)
			f.close()
			
			files['%s.html' % (md5_name)] = '%s/wh/%s.html' % (common.data['woa_folder'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "wh@woarl.com", ftp_pass['wh'], files, options.delay, options.verbose)
		print(database.shell_text('[g]War helpers uploaded[/g]'))
	
def output_tmap(options, the_world=None, skip_upload=False):
	from pages.map import team_map
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = world.World(cursor)
	else:
		cursor = the_world.cursor
	
	team_dict = team_q.get_real_active_teams(cursor)
	# if len(args) == 0:
	# 	team_list, team_dict = team_q.get_real_active_teams()
	# else:
	# 	team_list, team_dict = team_q.get_teams_in_list(team_list=args, by_id=False)
	
	files = {}
	# for team_id in team_dict.keys():
	for team_id in progressbar(team_dict.keys(), "Creating TMaps: ", 60, True):
		the_team = the_world.teams()[team_id]
		md5_name = team_f.team_hash(the_team.name)
		
		html_source = team_map._draw_map(cursor, team_id, build=1)
		
		f = open('%s/tmap/%s.html' % (common.data['woa_folder'], md5_name), 'w')
		f.write(html_source)
		f.write(padding)
		f.close()
		
		files['%s.html' % (md5_name)] = '%s/tmap/%s.html' % (common.data['woa_folder'], md5_name)
	
	if not skip_upload:
		upload("ftp.woarl.com", "tmap@woarl.com", ftp_pass['tmap'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Team maps uploaded[/g]'))

def output_spyrep(options, the_world=None, skip_upload=False):
	from classes import spy_world
	from functions import spyrep_f
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = spy_world.Spy_world(cursor)
	else:
		cursor = the_world.cursor
	
	team_dict = team_q.get_real_active_teams(cursor)
	# if len(args) == 0:
	# 	team_list, team_dict = team_q.get_real_active_teams()
	# else:
	# 	team_list, team_dict = team_q.get_teams_in_list(team_list=args, by_id=False)
	
	files = {}
	# for team_id in team_dict.keys():
	for team_id in progressbar(team_dict.keys(), "Creating Spy reps: ", 60, True):
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			content = ""
			
			try:
				f = open('%sspyrep_%s.html' % (common.data['cache_path'], md5_name))
				content = f.read()
				f.close()
			except IOError as e:
				pass
			except Exception as e:
				raise
			
			if content == "":
				content = spyrep_f.make_report(the_world, the_team)
			
			# Start of output related stuff
			js = spyrep_f.javascript(the_team)
			headers = common.headers("%s spy reports" % the_team.name, local_path=False, javascript=js)
			footers = common.footers(the_team)
			
			html_content = "".join([headers, "<br />", content, footers])
			
			# Try to cache it
			try:
				f = open('%sspyrep_%s.html' % (common.data['cache_path'], md5_name), 'w')
				f.write(content)
				f.close()
			except Exception as e:
				pass
			
			# Save for upload
			f = open('%s/spyrep/%s.html' % (common.data['woa_folder'], md5_name), 'w')
			f.write(html_content)
			f.write(padding)
			f.close()
			files['%s.html' % (md5_name)] = '%s/spyrep/%s.html' % (common.data['woa_folder'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "spyrep@woarl.com", ftp_pass['spyrep'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Spy reports uploaded[/g]'))

def output_stats(options, the_world=None, skip_upload=False):
	from functions import stat_f
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = world.World(cursor)
	else:
		cursor = the_world.cursor
	
	the_world.prep_for_stats()
	
	team_dict = team_q.get_real_active_teams(cursor)
	# if len(args) == 0:
	# 	team_dict = team_q.get_real_active_teams(cursor)
	# else:
	# 	team_dict = team_q.get_teams_in_list(cursor, team_list=args, by_id=False)
	
	files = {}
	# for team_id in team_dict.keys():
	for team_id in progressbar(team_dict.keys(), "Creating Stats: ", 60, True):
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			
			# Start of output related stuff
			headers = stat_f.headers(the_team.name, False)
			footers = common.footers()
			
			output = stat_f.make_team_stats(cursor, the_world, the_team)
			
			f = open('%s/stats/%s.html' % (common.data['woa_folder'], md5_name), 'w')
			f.write("".join([headers, output, footers]))
			f.write(padding)
			f.close()
			
			files['%s.html' % (md5_name)] = '%s/stats/%s.html' % (common.data['woa_folder'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "stats@woarl.com", ftp_pass['stats'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Team stats uploaded[/g]'))

def output_json(options, the_world=None, skip_upload=False):
	output_json_data(options, the_world, skip_upload)
	output_json_ti(options, the_world, skip_upload)
	output_json_map(options, the_world, skip_upload)

def output_json_data(options, the_world=None, skip_upload=False):
	from json_lib import data_j, oh_j
	
	if not the_world:
		cursor = database.get_cursor()
	else:
		cursor = the_world.cursor
	
	# Output the OH.js first
	output = oh_j.get_data(cursor)
	with open('%s/oh_data.js' % (common.data['cache_path']), 'w') as f:
		f.write(output)
		f.write(padding)
	
	# Write a second copy to the Rob3 localhost folder for Rob3 CGI to see
	with open('%s/oh_data.js' % (common.data['rob_fpath']), 'w') as f:
		f.write(output)
		f.write(padding)
	
	files = {
		'oh_data.js': '%s/oh_data.js' % (common.data['cache_path'])
	}
	for d, func in data_j.handle_dict.items():
		output = func(cursor)
		with open('%s/data_%s.json' % (common.data['cache_path'], d), 'w') as f:
			f.write(output)
			f.write(padding)
		
		files['%s.json' % (d)] = '%s/data_%s.json' % (common.data['cache_path'], d)
	
	if not skip_upload:
		upload("ftp.woarl.com", "data@woarl.com", ftp_pass['data'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Data lists uploaded[/g]'))
	

def output_json_ti(options, the_world=None, skip_upload=False):
	from json_lib import ti_j
	
	if not the_world:
		cursor = database.get_cursor()
		the_world = spy_world.Spy_world(cursor)
	else:
		cursor = the_world.cursor
	
	the_world.prep_for_ti()
	
	team_dict = team_q.get_real_active_teams(cursor)
	
	files = {}
	for team_id in progressbar(team_dict.keys(), "Creating JSON TIs: ", 60, True):
	# for team_id in team_dict.keys():
		try:
			the_team = the_world.teams()[team_id]
			md5_name = team_f.team_hash(the_team.name)
			
			# Make actual output
			output = ti_j.make_ti(the_world, the_team)
			
			# Save to DB
			database.query(cursor, ti_f.save_json(team_id, output))
			
			# Save to file
			with open('%s/ti_%s.json' % (common.data['cache_path'], md5_name), 'w') as f:
				f.write(output)
				f.write(padding)
			
			files['%s.json' % (md5_name)] = '%s/ti_%s.json' % (common.data['cache_path'], md5_name)
		
		except Exception as e:
			print("Team name: %s" % the_team.name)
			raise
	
	if not skip_upload:
		upload("ftp.woarl.com", "ti@woarl.com", ftp_pass['ti'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Json team infos uploaded[/g]'))

def output_json_map(options, the_world=None, skip_upload=False):
	from json_lib import mapper_j
	
	if the_world != None:
		cursor = the_world.cursor
	else:
		cursor = database.get_cursor()
	files = {}
	
	# create map
	#------------------------
	the_map = mapper_j.JSON_map_maker()
	map_source = the_map.map_grid(cursor)
	# print(map_source)
	# exit()
	
	with open('%s/map/latest.json' % common.data['woa_folder'], 'w') as f:
		f.write(map_source)
		f.write(padding)
	
	with open('%s/map/turn_%d_normal.json' % (common.data['woa_folder'], common.current_turn()), 'w') as f:
		f.write(map_source)
		f.write(padding)
	
	# Save as files
	files['latest.json'] = '%s/map/latest.json' % common.data['woa_folder']
	files['turn_%d_normal.json' % common.current_turn()] = '%s/map/turn_%d_normal.json' % (common.data['woa_folder'], common.current_turn())
	
	if not skip_upload:
		upload("ftp.woarl.com", "map@woarl.com", ftp_pass['map'], files, options.delay, options.verbose)
		print(database.shell_text('[g]Json map uploaded[/g]'))

def upload_voi(options, files):
	upload("ftp.woarl.com", "voi@woarl.com", ftp_pass['voi'], files, options.delay, options.verbose)
