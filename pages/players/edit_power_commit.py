from pages import common
from classes import power

page_data = {
	"Admin":	True,
	"Redirect":	"list_powers",
}

def main(cursor):
	# Power settings
	the_power = power.Power()
	the_power.get_from_form(common.cgi_form.list)
	the_power.update(cursor)
	
	return ""