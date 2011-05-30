from lore import pages
import string
from queries import deity_q

def standard_page(cursor, cat, page, **kwargs):
	source = pages.get_html(cursor, cat, page, level="public")
	
	return source