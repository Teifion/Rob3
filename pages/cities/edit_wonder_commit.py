from pages import common
from classes import wonder

page_data = {
	"Admin":	True,
	"Redirect":	"list_wonders",
}

def main(cursor):
	the_wonder = wonder.Wonder()
	the_wonder.get_from_form(common.cgi_form.list)
	the_wonder.update(cursor)
	
	return ""