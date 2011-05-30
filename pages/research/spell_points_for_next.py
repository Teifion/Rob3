from pages import common
from rules import spell_rules

page_data = {
	"Header":	False,
	"Admin":	True,
}

def main(cursor):
	spell_id	= int(common.get_val("spell", 0))
	level		= int(common.get_val("level", 0))
	
	return str(spell_rules.cost_for_next_level(cursor, spell_id, level, in_spell_points=True).get("Spell points"))