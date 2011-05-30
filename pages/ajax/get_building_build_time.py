from pages import common
from queries import building_q

page_data = {
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	b = int(common.get_val("building", 0))
	
	return str(building_q.get_one_building(cursor, b).build_time)