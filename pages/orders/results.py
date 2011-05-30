from pages import common
# from data import team, team_f, team_q, results
from functions import team_f
from queries import team_q
from classes import world

page_data = {
	"Title":	"Team results",
	"Admin":	True,
}

def main(cursor):
	raise Exception("Thought to no longer be used")
	
	team_id = int(common.get_val("team", -1))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>%s</div>" %  common.select_team_form(cursor, 'results')
	
	the_team = team_q.get_one_team(cursor, team_id)
	the_world = world.World(cursor)
	
	output = ['<div style="padding: 5px;">']
	output.append('<span class="stitle">%s results</span>' % the_team.name)
	output.append('<textarea name="results" id="results" rows="13" style="width: 100%;">')
	output.append(team_f.create_results_tail(the_world, the_team))
	output.append('</textarea>Previous results:')
	
	# Now to get the results for the last few turns
	# results_dict = results.get_results_by_team()
	# our_results_dict = results_dict.get(team_id, {})
	# 
	# for t in range(common.current_turn(),common.current_turn()-5,-1):
	# 	if t in our_results_dict:
	# 		output.append("""
	# 		<hr />
	# 		Turn: %d<br />
	# 		%s
	# 		""" % (t, common.bbcode_to_html(our_results_dict[t].strip())))
	
	output.append('<hr /></div>')
	return "".join(output)