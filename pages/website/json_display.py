from pages import common
from json_lib import data_j
import json

page_data = {
	"Header":	False,
	"Admin":	True,
}

def main(cursor):
	data_set = common.get_val('set')
	
	mapping = {
		"buildings":	data_j.buildings,
	}
	
	return str(mapping[data_set](cursor))

