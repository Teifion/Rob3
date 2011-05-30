import database
from pages import common
from functions import tech_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_techs",
}

def main(cursor):
	tech_id		= int(common.get_val("tech", 0))
	team		= int(common.get_val("team", 0))
	level		= int(common.get_val("level", 0))
	points		= int(common.get_val("points", 0))
	
	database.query(cursor, tech_f.set_tech(tech_id=tech_id, team_id=team, level=level, points=points))
	
	page_data['Redirect'] = "list_techs&team=%s" % team
	return ""