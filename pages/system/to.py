from pages import common
# from queries import team_q
from functions import to_f#, team_f
from classes import world

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	post_output = int(common.get_val('post_output', 0))
	dev_mode	= common.get_val('dev_mode', 0)
	ajax		= common.get_val('ajax', 0)
	
	the_world = world.World(cursor)
	the_world.prep_for_to()
	
	headers = to_f.headers(the_world)
	footers = to_f.footers(the_world)
	js = to_f.javascript(the_world)
	output = to_f.make_to(the_world)
	
	content = []
	
	if dev_mode == "1":
		headers = headers.replace('../styles.css', 'http://localhost/woa/styles.css').replace('../includes/jquery.js', '%sjquery.js' % common.data['media_path'])
	
	if ajax:	content.append(headers)
	else:		content.append(js)
	
	content.append(output)
	
	if ajax:	content.append(footers)
	
	return "".join(content)