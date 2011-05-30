import urllib.request
from pages import common
from classes import spy_world
from functions import spyrep_f, team_f

page_data = {
	"Title":	"Team spy report",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id		= int(common.get_val('team', 0))
	post_output = common.get_val('post_output', '')
	auto_jump	= int(common.get_val('auto_jump', 0))
	recache		= common.get_val('recache', 1)
	ajax		= common.get_val('ajax', 0)
	
	output = []
	
	if team_id < 1:
		raise Exception("No team selected")
		
	the_world = spy_world.Spy_world(cursor)
	the_team = the_world.teams()[team_id]
	md5_name = team_f.team_hash(the_team.name)
	
	if not recache:
		try:
			f = open('%sspyrep_%s.html' % (common.data['cache_path'], md5_name))
			content = f.read()
			f.close()
			return '''<a href="web.py?mode=spyrep&amp;team=%d&amp;recache=True" class="block_link">Recache</a>%s''' % (team_id, content)
		except IOError as e:
			pass
		except Exception as e:
			raise
	
	# Start of output related stuff
	js = spyrep_f.javascript(the_team)
	headers = common.headers("%s spy reports" % the_team.name, local_path=True, javascript=js)
	footers = common.footers(the_team)
	
	report_output = spyrep_f.make_report(the_world, the_team)
	
	if ajax:	output.append(headers)
	# else:		output.append(js)
	
	output.append(report_output)
	
	if ajax:	output.append(footers)
	
	output.append("</div>")
	output = "".join(output)
	
	# If we can't cache it, no big deal
	try:
		f = open('%sspyrep_%s.html' % (common.data['cache_path'], md5_name), 'w')
		f.write(output)
		f.close()
	except Exception as e:
		pass
	
	# Inject a recache link here so it's not cached and thus picked up by the batch script
	recache_link = """<div style="padding: 5px;">
		<a href="web.py?mode=spyrep&amp;team=%(team_id)s&amp;recache=True" class="block_link">Recache</a>
		<br />""" % {
			"team_id":				team_id,
		}
	
	return "%s%s" % (recache_link, output)
