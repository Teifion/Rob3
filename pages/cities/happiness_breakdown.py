import math
from pages import common
from rules import city_rules
from classes import world

page_data = {
	"Title":	"City happiness breakdown",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	city_id = int(common.get_val('city', 0))
	
	output = []
	
	w = world.World(cursor)
	output.append("<br />".join(city_rules.get_happiness(w, w.cities()[city_id], with_breakdown = True)[1]))
	
	return "".join(output)