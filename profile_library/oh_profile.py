import time
from classes import world, oh
from functions import team_f
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
	
	# Setup the World
	the_oh = oh.Oh(the_world=the_world)
	the_oh.local_path = True
	the_oh.setup(true_team_list=team_list)
	
	print("Caches setup")
	
	t_output = []
	for t in team_list:
		the_team = the_world._teams[t]
		
		try:
			team_start = time.time()
			
			output = the_oh.make_oh(t)
			
			md5_name = team_f.team_hash(the_team.name)
			f = open('%soh_%s.html' % (common.data['cache_path'], md5_name), 'w')
			f.write(output)
			f.close()
			
			t_output.append(output)
			
			print("Made for %s in %s" % (the_world._teams[t].name, round(time.time() - team_start, 3)))
		except Exception as e:
			print("Error in making OH for team '%s'" % the_world._teams[t].name)
			raise
		
	
	return "".join(t_output)
	
main.args = ['options']