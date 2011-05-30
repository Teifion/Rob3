from pages import common
from queries import team_q, deity_q

page_data = {
	"Title":	"DI points",
	"Admin":	True,
}

def main(cursor):
	team_dict = team_q.get_real_active_teams(cursor)
	deity_dict = deity_q.get_all_deities(cursor)
	
	team_q.mass_get_team_deities(cursor, team_dict)
	
	# Stores lists of teams
	deities = {}
	
	# Make blank lists
	for d in deity_dict.keys():
		deities[d] = []
	
	# Find out who follows who
	for t, the_team in team_dict.items():
		for d, v in the_team.deities.items():
			deities[d].append(the_team.name)
	
	output = []
	for d, the_deity in deity_dict.items():
		if len(deities[d]) == 0: continue
		
		# Deity name and follower list
		if len(deities[d]) > 1:
			output.append("[b]%s[/b] %s followers (%s)" % (the_deity.name, len(deities[d]), ", ".join(deities[d])))
		else:
			output.append("[b]%s[/b] 1 follower (%s)" % (the_deity.name, deities[d][0]))
		
		output.append("Objective: %s" % the_deity.objective)
		output.append("DI: %s" % the_deity.di)
		output.append("Chosen follower: \n")
	
	return '&nbsp;<textarea rows="40" style="width:99%%;">%s</textarea>' % "\n".join(output)
