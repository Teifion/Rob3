import database
from pages import common
from functions import spell_f

page_data = {
	"Admin":	True,
	"Redirect":	"list_spells",
}

def main(cursor):
	spell_id	= int(common.get_val("spell", 0))
	team		= int(common.get_val("team", 0))
	level		= int(common.get_val("level", 0))
	points		= int(common.get_val("points", 0))
	
	database.query(cursor, spell_f.set_spell(spell_id=spell_id, team_id=team, level=level, points=points))
	
	page_data['Redirect'] = "list_spells&team=%s" % team
	return ""