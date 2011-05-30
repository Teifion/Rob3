import urllib.request
from pages import common
from classes import spy_world
# from data import team, team_q, team_f
# from data import ti_f

from functions import ti_f

from queries import team_q, city_q, squad_q, player_q, unit_q
from functions import team_f

page_data = {
	"Title":	"Team info",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id		= int(common.get_val('team', 0))
	post_output = common.get_val('post_output', 0)
	auto_jump	= common.get_val('auto_jump', False)
	dev_mode	= common.get_val('dev_mode', 0)
	recache		= common.get_val('recache', False)
	ajax		= common.get_val('ajax', 0)
	
	output = []
	
	if not ajax:
		output.append("""<div style="padding: 5px;">
		<form style="padding: 5px;" action="web.py" method="get" accept-charset="utf-8">
			<input type="hidden" name="mode" id="mode" value="ti" />
			<table border="0" cellspacing="5" cellpadding="5">
				<tr>
					<td><label for="team">Team:</label></td>
					<td>%(team_option_box)s</td>
					<td><label for="post_output">Post ouput:</label></td>
					<td>%(post_output_checkbox)s</td>
					<td><label for="auto_jump">Auto-jump:</label></td>
					<td>%(auto_jump_checkbox)s</td>
					<td width="10">&nbsp;</td>
					<td><input type="submit" value="Get TI" /></td>
				</tr>
			</table>
		</form>
		<a href="web.py?mode=ti&amp;team=%(last_id)s&amp;post_output=1&amp;auto_jump=1" class="block_link">Update all</a>
		<br />
		
		<a href="web.py?mode=ti&amp;team=%(team_id)s&amp;recache=1" class="block_link">Recache</a>
		<br />""" % {
			"team_option_box":		team_f.structured_list(cursor, default=team_id),
			"post_output_checkbox":	common.check_box('post_output', post_output),
			"auto_jump_checkbox":	common.check_box('auto_jump', auto_jump),
			"last_id":				team_q.get_latest_active_team_id(cursor, skip_irs = True),
			"team_id":				team_id,
		})
	
	
	if team_id < 1:
		return "".join(output)
	
	if post_output:
		output.append(get_bbcode_core(cursor, team_id))
	else:
		output.append(get_ti_core(cursor, team_id, recache, ajax))
	
	if auto_jump:
		new_location = "web.py?mode=ti&post_output=%s&auto_jump=1&team=%d" % (post_output, team_q.get_next_active_team_id(cursor, team_id, skip_irs = True))
		
		if post_output:
			output.append(common.redirect(new_location, 2000))
		else:
			output.append(common.redirect(new_location))
	
	output.append("</div>")
	
	return "".join(output)

def get_bbcode_core(cursor, team_id):
	the_team = team_q.get_one_team(cursor, team_id)
	md5_name = team_f.team_hash(the_team.name)
	
	# bbcode = "".join([headers, output, footers])
	bbcode = ti_f.bbcode_ti(the_team, md5_name)
	
	ti_output = common.bbcode_to_html(bbcode)
	
	# Clean it
	bbcode = bbcode.replace(' ', '\\ ').replace('\n', 'NEWLINE').replace('\t', '')
	bbcode = bbcode.replace("'", 'APOSTRAPH').replace('&', 'AMPASAND')
	bbcode = bbcode.replace("(", '\\(').replace(')', '\\)')
	
	# Send it
	getter_data = "p=%s&mode=postUpdate&post=%d&string=%s" % (common.data['getterPass'], the_team.team_info_first_post, bbcode)
	result = urllib.request.urlopen(common.data['getter_url'], getter_data).read().strip()
	
	return bbcode

def get_ti_core(cursor, team_id, recache, ajax):
	output = []
	
	the_world = spy_world.Spy_world(cursor)
	the_team = the_world.teams()[team_id]
	md5_name = team_f.team_hash(the_team.name)
	
	# Cache it?
	if not recache:
		try:
			# f = open('%s/ti/%s.html' % (common.data['woa_folder'], md5_name))
			f = open('%sti_%s.html' % (common.data['cache_path'], md5_name))
			content = f.read()
			f.close()
			return content
			return '''<a href="web.py?mode=ti&amp;team=%d&amp;recache=True" class="block_link">Recache</a>%s''' % (team_id, content)
		except IOError as e:
			# print(e)
			pass
		except Exception as e:
			raise
	
	# Some caching stuff
	the_world.prep_for_ti()

	# Start of output related stuff
	headers = ti_f.headers(the_team)
	footers = ti_f.footers(the_team)
	js = ti_f.javascript(the_team)
	
	ti_output = ti_f.make_ti(cursor, the_world, the_team)
	
	if ajax:	output.append(headers)
	else:		output.append(js)
	
	output.append(ti_output)
	
	if ajax:	output.append(footers)
	
	output = "".join(output)
	
	# If we can't cache it, no big deal
	try:
		f = open('%sti_%s.html' % (common.data['cache_path'], md5_name), 'w')
		f.write(output)
		f.close()
	except Exception as e:
		pass
	
	return output