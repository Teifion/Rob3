import urllib.request
from pages import common
from queries import stat_q, team_q
from functions import team_f, stat_f
from classes import res_dict, world
# from data import stat, stat_f
# from data import team, team_f
# from data import resource_f

page_data = {
	"Title":	"Team stats",
	"Admin":	True,
}

def main(cursor):
	team_id = int(common.get_val("team", 0))
	
	output = []
	
	output.append(stat_f.display_stat_table(cursor, team_id, list_size=10))
	
	return "".join(output)

# from pages import common
# from classes import world
# # from data import team, team_q, team_f
# # from data import ti_f
# 
# from functions import ti_f
# 
# from queries import team_q, city_q, squad_q, player_q, unit_q
# from functions import team_f

def main(cursor):
	# Get team Id
	team_id		= int(common.get_val('team', 0))
	recache		= common.get_val('recache', False)
	
	output = []
	
	output.append("""<div style="padding: 5px;">
	<form style="padding: 5px;" action="web.py" method="get" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="team_stats" />
		<table border="0" cellspacing="5" cellpadding="5">
			<tr>
				<td><label for="team">Team:</label></td>
				<td>%(team_option_box)s</td>
				<td width="10">&nbsp;</td>
				<td><input type="submit" value="Get stats" /></td>
			</tr>
		</table>
	</form>
	<a href="web.py?mode=team_stats&amp;team=%(team_id)s&amp;recache=1" class="block_link">Recache</a>
	<br />""" % {
		"team_option_box":		team_f.structured_list(cursor, default=team_id),
		"last_id":				team_q.get_latest_active_team_id(cursor, skip_irs = True),
		"team_id":				team_id,
	})
	
	if team_id < 1:
		return "".join(output)
	
	ajax = False
	output.append(get_stat_core(cursor, team_id, recache, ajax))
	# output.append("</div>")
	
	return "".join(output)

def get_stat_core(cursor, team_id, recache, ajax):
	output = []
	
	the_world = world.World(cursor)
	the_team = the_world.teams()[team_id]
	md5_name = team_f.team_hash(the_team.name)
	
	# Cache it?
	if not recache:
		try:
			f = open('%sstat_%s.html' % (common.data['cache_path'], md5_name))
			content = f.read()
			f.close()
			return content
			return '''<a href="web.py?mode=stat&amp;team=%d&amp;recache=True" class="block_link">Recache</a>%s''' % (team_id, content)
		except IOError as e:
			pass
		except Exception as e:
			raise
	
	# Some caching stuff
	the_world.prep_for_stats()
	
	# Start of output related stuff
	headers = stat_f.headers(the_team.name, True)#common.headers("%s stats" % the_team.name, css="", javascript=stat_f.javascript, local_path=True, js_libs=[])#stat_f.headers(the_team)
	footers = common.footers()
	
	stat_output = stat_f.make_team_stats(cursor, the_world, the_team)
	
	if ajax:	output.append(headers)
	else:		output.append("""
	<script type="text/javascript" charset="utf-8">
		%s
	</script>
	""" % stat_f.javascript)
	
	output.append(stat_output)
	
	if ajax:	output.append(footers)
	
	output = "".join(output)
	
	# If we can't cache it, no big deal
	try:
		f = open('%sstat_%s.html' % (common.data['cache_path'], md5_name), 'w')
		f.write(output)
		f.close()
	except Exception as e:
		pass
	
	return output