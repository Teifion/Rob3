import database
from pages import common
from functions import team_f
from queries import team_q

page_data = {
	"Admin":	True,
	"Redirect":	"view_borders",
}

def main(cursor):
	team_id = int(common.get_val("team", 0))
	default_border = int(common.get_val("default_border_state", 0))
	
	team_dict = team_q.get_real_active_teams(cursor, skip_irs=False)
	the_team = team_dict[team_id]
	
	queries = [
		"DELETE FROM team_borders WHERE host = %d" % team_id,
		"UPDATE teams SET default_borders = %d WHERE id = %d;" % (default_border, team_id),
	]
	insertions = []
	
	# Get a list of states
	for t, other_team in team_dict.items():
		if t == the_team.id: continue
		
		state = int(common.get_val("border_state_%d" % t, -1))
		if state >= 0:
			insertions.append("(%d, %d, %d)" % (team_id, t, state))
	
	# Add insertions to list
	if len(insertions) > 0:
		queries.append("INSERT INTO team_borders (host, visitor, state) values %s;" % ",".join(insertions))
		
	# print("")
	# print(common.print_post_data())
	# print("<br /><br />")
	# print("<br />".join(queries))
	# exit()
	
	database.query(cursor, queries)
	
	page_data['Redirect'] = 'view_borders&team={0:d}'.format(team_id)
	return ""