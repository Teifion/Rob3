from pages import common
from rules import tech_rules
import time

page_data = {
	"Header":	False,
	"Admin":	True,
}

def main(cursor):
	start = time.time()
	
	tech_id		= int(common.get_val("tech", 0))
	level		= int(common.get_val("level", 0))
	
	return str(tech_rules.cost_for_next_level(cursor, tech_id, level).get("Tech points"))