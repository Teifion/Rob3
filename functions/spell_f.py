import database
from queries import spell_q

def set_spell(spell_id, team_id, points=0, level=0):
	# Delete it
	queries = ["DELETE FROM team_spells WHERE team = %d AND spell = %d;" % (team_id, spell_id)]
	
	# Insert it
	queries.append("INSERT INTO team_spells (spell, team, points, level) values (%d, %d, %d, %d);" % (spell_id, team_id, points, level))
	
	return queries


def spell_option_list(cursor, remove_list=[], default=0):
	output = []
	
	spell_dict = spell_q.get_all_spells(cursor)
	for c, s in spell_dict.items():
		if c in remove_list: continue
		
		if c == default:
			output.append("<option value='%s' selected='selected'>%s</option>" % (c, s.name))
		else:
			output.append("<option value='%s'>%s</option>" % (c, s.name))

	return "".join(output)

def check_row_exists(team_id, spell_id):
	return "INSERT INTO team_spells (team, spell) values (%d, %d);" % (team_id, spell_id)

def research_query(team_id, spell_id, level, points):
	return ["UPDATE team_spells SET level = %d, points = %s WHERE team = %d AND spell = %d;" % (level, points, team_id, spell_id)]

def trade_query(team_id, spell_id):
	return ["UPDATE team_spells SET level = level + 1, points = 0 WHERE team = %d AND spell = %d;" % (team_id, spell_id)]
