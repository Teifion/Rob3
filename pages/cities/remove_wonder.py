import database
from pages import common
from functions import wonder_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_wonders",
}

def main(cursor):
	wonder_id = int(common.get_val('wonder', -1))
	database.query(cursor, wonder_f.delete_wonder(wonder_id))