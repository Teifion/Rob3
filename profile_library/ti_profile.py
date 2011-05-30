import time
from classes import world
from functions import ti_f, team_f
from queries import player_q, team_q, city_q, squad_q, unit_q
from pages import common

def main(cursor, options):
	the_world = world.World(cursor)
	team_dict = the_world.teams()
	
	team_list = []
	
	# Work out our team
	try:
		t = options.team
		
		if t != "":
			for t, the_team in team_dict.items():
				if the_team.name.lower() == options.team.lower():
					team_list = [t]
			
			if team_list == []:
				raise Exception()
		else:
			raise Exception()
	except Exception as e:
		team_list = [t for t in team_dict.keys() if (team_dict[t].active and not team_dict[t].ir)]
	
	# Some caching stuff
	the_world.cities()
	the_world.armies()
	the_world.players()
	the_world.units()
	
	player_q.mass_get_player_powers(cursor, the_world._players)
	
	team_q.mass_get_team_deities(cursor, the_world._teams)
	team_q.mass_get_team_spells(cursor, the_world._teams)
	team_q.mass_get_team_techs(cursor, the_world._teams)
	team_q.mass_get_team_resources(cursor, the_world._teams)
	team_q.mass_get_team_evolutions(cursor, the_world._teams)
	
	city_q.mass_get_city_buildings(cursor, the_world._cities)
	city_q.mass_get_city_artefacts(cursor, the_world._cities)
	city_q.mass_get_city_wonders(cursor, the_world._cities)
	
	unit_q.mass_get_unit_equipment(cursor, the_world._units)
	
	squad_q.mass_get_squads(cursor, the_world._armies)
	
	print("Caches setup")
	
	t_output = []
	for t in team_list:
		the_team = the_world._teams[t]
		
		headers = ti_f.headers(the_team)
		footers = ti_f.footers(the_team)
		js = ti_f.javascript(the_team)
		
		try:
			team_start = time.time()
			
			ti_output = ti_f.make_ti(cursor, the_world, the_team)
			
			output = "".join([js, ti_output])
			
			md5_name = team_f.team_hash(the_team.name)
			try:
				f = open('%sti_%s.html' % (common.data['cache_path'], md5_name), 'w')
				f.write(output)
				f.close()
			except Exception as e:
				pass
			
			t_output.append(output)
			
			print("Made for %s in %s" % (the_world._teams[t].name, round(time.time() - team_start, 3)))
		except Exception as e:
			print("Error in making TI for team '%s'" % the_world._teams[t].name)
			raise
		
	
	return "".join(t_output)
	
main.args = ['options']