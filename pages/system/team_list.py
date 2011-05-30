from pages import common
from queries import team_q

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	show_dead_teams		= common.get_val('show_dead')
	show_unqueued_teams	= common.get_val('show_unqueued')
	
	# Get the turn we'll want to get stuff for
	current_turn = common.current_turn()
	
	# Get our list
	team_dict = team_q.get_real_teams(cursor)
	
	output = ['<textarea rows="40" style="width:99%;">']
	
	for team_id, the_team in team_dict.items():
		if the_team.ir or the_team.dead or not the_team.active:
			continue
		
		output.append("%s\n" % the_team.name)
	
	output.append("</textarea>")
	return "".join(output)