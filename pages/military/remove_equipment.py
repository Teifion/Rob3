import database
from pages import common
from functions import unit_f

page_data = {
	"Admin":	True,
	"Redirect":	"edit_unit",
}

def main(cursor):
	unit	= int(common.get_val("unit", 0))
	item	= int(common.get_val("item", 0))
	
	database.query(cursor,
		unit_f.remove_equipment(unit=unit, item=item))
	
	# Redirect
	page_data['Redirect'] = 'edit_unit&unit={0:d}'.format(unit)
	return ""