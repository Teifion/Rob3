from pages import common
from functions import system_f

page_data = {
	"Title":	"Items requiring attention",
	"Admin":	True,
}

def handle_interactive(row):
	return '<a href="web.py?mode=interactive_order&order=%d">%s order</a>' % (row['id'], row['title'])

handles = {
	"interactive_order": handle_interactive,
}

def main(cursor):
	output = []
	
	items = system_f.get_warn_list(cursor)
	
	# No items? Send us back.
	if len(items) < 1:
		return "No items requiring your attention, returning you to Rob hom page.%s" % common.redirect("web.py")
	
	output.append("<br /><ul>")
	
	for item_type, row in items:
		output.append("<li>%s</li>" % handles[item_type](row))
	
	output.append("</ul>")
	
	return "".join(output)