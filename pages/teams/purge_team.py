import database
from pages import common
from queries import city_q, army_q, squad_q

page_data = {
	"Title":	"Purge team",
	"Admin":	True,
}

def main(cursor):
	team_id = int(common.get_val('team', 0))
	confirm = int(common.get_val('confirm', 0))
	
	if team_id < 1:
		return "<div style='padding: 5px;'>{0}</div>".format(common.select_team_form(cursor, 'purge_team'))
	
	if confirm == 0:
		return """
		<form action="web.py" method="post" accept-charset="utf-8" style="padding: 10px;">
			<input type="hidden" name="mode" id="mode" value="purge_team" />
			<input type="hidden" name="team" id="team" value="{0}" />
			<input type="hidden" name="confirm" id="confirm" value="1" />
			Are you sure?<br /><br />
			<input type="submit" value="Purge team" />
		</form>
		""".format(team_id)
	
	# Query the DB for some info
	city_dict = city_q.get_cities_from_team(cursor, team_id, include_dead=True)
	army_dict = army_q.get_armies_from_team(cursor, team_id, include_garrisons=True)
	squad_dict = squad_q.get_squads_from_team(cursor, team_id)
	
	# Turn the dictionaries into lists
	city_list = [str(c) for c in city_dict]
	army_list = [str(a) for a in army_dict]
	squad_list = [str(s) for s in squad_dict]
	
	queries = []
	
	if len(army_list) > 0:
		# Wipe squads
		queries.append("DELETE FROM squads WHERE army IN (%s)" % ",".join(army_list))
		queries.append("DELETE FROM army_monsters WHERE army IN (%s)" % ",".join(army_list))
		queries.append("DELETE FROM campaign_armies WHERE army IN (%s)" % ",".join(army_list))
		
		# Wipe armies
		queries.append("DELETE FROM armies WHERE id IN (%s)" % ",".join(army_list))
	
	if len(city_list) > 0:
		# Wipe buildings
		queries.append("DELETE FROM city_buildings WHERE city IN (%s)" % ",".join(city_list))
		
		# Wipe garrisons
		# queries.append("DELETE FROM armies WHERE garrison IN (%s)" % ",".join(city_list))
		
		# Wipe cities
		queries.append("UPDATE operatives SET city = 0 WHERE city IN (%s)" % ",".join(city_list))
		queries.append("DELETE FROM cities WHERE id IN (%s)" % ",".join(city_list))
		
		# Wipe buildings
		queries.append("DELETE FROM city_buildings WHERE city IN (%s)" % ",".join(city_list))
	
	if len(squad_list) > 0:
		# Wipe squad battle history
		queries.append("DELETE FROM squad_battle_history WHERE squad IN (%s)" % ",".join(squad_list))
	
	# Operatives
	queries.append("DELETE FROM operatives WHERE team = %s" % team_id)
	
	# Spy reports
	queries.append("DELETE FROM spy_reports WHERE team = %s" % team_id)
	
	# Resources
	queries.append("UPDATE team_resources SET amount = 0 WHERE team = %d" % int(team_id))
	queries.append("UPDATE team_resources SET amount = 1500 WHERE team = %d AND resource = 0" % int(team_id))
	queries.append("UPDATE team_resources SET amount = 300 WHERE team = %d AND resource = 1" % int(team_id))
	
	database.query_batch(cursor, queries)
	
	
	return "<br />".join(queries)

