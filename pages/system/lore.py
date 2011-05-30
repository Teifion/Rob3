from pages import common
from lore import pages

page_data = {
	"Title":	"Lore",
	"Admin":	True,
	
	# "Header":	False,
}

def main(cursor):
	cat		= common.get_val('cat', "")
	page	= common.get_val('page', "")
	
	page_data['title'] = "Lore: %s.%s" % (cat, page)
	
	try:
		output = pages.get_html(cursor, cat, page, "gm")
	except Exception as e:
		return str(e)
	
	return output