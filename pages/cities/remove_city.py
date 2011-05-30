import database
from pages import common
from functions import city_f
from queries import city_q

page_data = {
	"Admin":	True,
	"Redirect":	"list_cities",
}

def main(cursor):
	city_id = int(common.get_val('city', -1))
	the_city = city_q.get_one_city(cursor, city_id)
	database.query(cursor, city_f.delete_city(city_id))
	
	# Redirect
	page_data['Redirect'] = 'list_cities&team={0:d}'.format(the_city.team)
