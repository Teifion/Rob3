from pages import common
from functions import city_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_team",
}

def main(cursor):
	building_id		= int(common.get_val("building", 0))
	completion		= int(common.get_val("completion", 0))
	amount			= int(common.get_val("amount", 0))
	city_id			= int(common.get_val("city", 0))
	
	city_f.set_building(cursor, city_id, building_id, completion, amount)
	
	page_data['Redirect'] = 'edit_city&city={0:d}'.format(city_id)
	return ""