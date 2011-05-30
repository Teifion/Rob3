import database
from pages import common
from classes import team
from lists import resource_list
from functions import team_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_teams",
}

def main(cursor):
	# Team settings
	the_team = team.Team()
	the_team.get_from_form(common.cgi_form.list)
	the_team.update(cursor)
	
	# Resources
	res_updates = {}
	
	for k, v in resource_list.data_dict.items():
		form_val = common.get_val('res_%s' % v.name, 0)
		
		if form_val == "True":
			res_updates[k] = 1
		else:
			res_updates[k] = float(form_val)
	
	database.query(cursor, team_f.set_resources(cursor, the_team.id, res_updates))
	return ""