import cProfile
import pstats
import pages
import time
import database

cursor = database.get_cursor()
cursor.track_queries = True


def run(options):
	try:
		if options.suite == "map":	import pages.map.view_map as the_page
		elif options.suite == "check":	from checks import main_check as the_page
		elif options.suite == "trade":	from profile_library import trade_profile as the_page
		elif options.suite == "sad": from profile_library import sad_profile as the_page
		elif options.suite == "ti":	from profile_library import ti_profile as the_page
		elif options.suite == "oh":	from profile_library import oh_profile as the_page
		elif options.suite == "wh":	from profile_library import wh_profile as the_page
		elif options.suite == "to":	import pages.system.to as the_page
		else:
			print("Suite '%s' not found, run as 'rob profile -s <suite>'" % options.suite)
			exit()
	except Exception as e:
		raise
	
	start_time = time.time()
	cache = {}
	
	try:
		arg_list = ['cursor']
		args = the_page.main.args
		
		if 'options' in args: arg_list.append('options')
		
		run_str = 'cache["output"]=the_page.main(%s)' % (",".join(arg_list))
	except Exception as e:
		# Normal main functions will just get called normally
		run_str = 'cache["output"]=the_page.main(cursor)'
	
	cProfile.runctx(run_str,
		{"the_page":the_page, "cursor":cursor, "options":options},
		{"cache":cache},
		"print_stats"
	)
	
	# Build up a dict of the queries
	query_dict = {}
	f = open('profile_queries.sql', 'w')
	for q in cursor.queries:
		if q in ("BEGIN", "COMMIT", "ROLLBACK"): continue
		
		f.write(q)
		f.write("\n")
		if q not in query_dict:
			query_dict[q] = 0
		
		query_dict[q] += 1
	f.close()
	
	
	# What's our most popular query?
	pop_count, pop_query = 0, ""
	for q, c in query_dict.items():
		if c > pop_count:
			pop_count = c
			pop_query = q
	
	
	
	
	try:
		print("Size: %s bytes" % format(len(cache['output']), ','))
	except Exception as e:
		pass
	
	print("Time taken: %s" % str(round(time.time() - start_time, 3))[0:5])
	print("Queries: %d" % len(cursor.queries))
	print("Uniques: %d" % len(set(cursor.queries)))
	print("Most queried: %s (%d)" % (pop_query, pop_count))
	print("View stats with: rob profile -v True")


def view(options):
	p = pstats.Stats("print_stats")
	# p.strip_dirs()
	
	p.sort_stats('cumulative')
	# p.sort_stats('time')
	# p.print_stats(r'(classes|queries|pages|functions|rules|orders)', 35)
	p.print_stats(35)
	