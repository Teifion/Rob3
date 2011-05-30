import database
from queries import tech_q

def set_tech(tech_id, team_id, points=0, level=0):
	# Delete it
	queries = ["DELETE FROM team_techs WHERE team = %d AND tech = %d;" % (team_id, tech_id)]
	
	# Insert it
	queries.append("INSERT INTO team_techs (tech, team, points, level) values (%d, %d, %d, %d);" % (tech_id, team_id, points, level))
	
	return queries


def tech_option_list(cursor, remove_list=[], default=0):
	output = []
	
	tech_dict = tech_q.get_all_techs(cursor)
	for c, s in tech_dict.items():
		if c in remove_list: continue
		
		if c == default:
			output.append("<option value='%s' selected='selected'>%s</option>" % (c, s.name))
		else:
			output.append("<option value='%s'>%s</option>" % (c, s.name))
	
	return "".join(output)

def check_row_exists(team_id, tech_id):
	return "INSERT INTO team_techs (team, tech) values (%d, %d);" % (team_id, tech_id)

def research_query(team_id, tech_id, level, points):
	return ["UPDATE team_techs SET level = %d, points = %d WHERE team = %d AND tech = %d;" % (level, points, team_id, tech_id)]

def trade_query(team_id, tech_id):
	return ["UPDATE team_techs SET level = level + 1, points = 0 WHERE team = %d AND tech = %d;" % (team_id, tech_id)]
