import database
from pages import common
from functions import wonder_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_wonders",
}

def main(cursor):
	name			= common.get_val("name", "")
	city			= int(common.get_val("city", 0))
	point_cost		= int(common.get_val("point_cost", 0))
	material_cost	= int(common.get_val("material_cost", 0))
	description		= common.get_val("description", "")
	
	database.query(cursor,
		wonder_f.new_wonder(name, city, point_cost, material_cost, description))