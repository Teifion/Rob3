from data import path
from data import team
from data import resource_f
from data import mapper_q, city
from data import deity, deity_f

#	City supply testing
#------------------------
# print mapper_q.get_resource_at_x_y(121, 1168, 25)



#	Res_dict testing
#------------------------
# my_resources_str	= "Spell points:50,Light points:200"

# No swap needed
# my_cost_str			= "Spell points:50,(Spell points:Light points)(Materials:Fart points)"

# res_dict.Res_dict("Materials:3,Balloon points:20,(Balloon points:Ship points)")
# Materials:6,Balloon points:45,(Ship points:Balloon points)

# Standard straight out swap
# my_cost_str			= "Spell points:150,(Spell points:Light points)(Materials:Fart points)"

# Swap it with something you don't have
# my_cost_str			= "Spell points:250,(Spell points:Abjuration points)"

# Swap where the swap_target also has a cost
# my_cost_str			= "Spell points:50,Light points:75(Spell points:Light points)"
# my_cost_str			= "Spell points:130,Light points:50(Spell points:Light points)"

# Swap where it has too high a cost to be split over both
# my_cost_str			= "Spell points:150,Light points:150(Spell points:Light points)"

# Swap where you have to split it over both
# my_cost_str			= "Spell points:250,(Spell points:Light points)"

# my_dict = res_dict.Res_dict(my_resources_str)
# 
# print "Resources:", resource_f.make_cost_string(my_dict), "<br />"
# print "Origional cost:", my_cost_str, "<br />"
# 
# r = my_dict.affordable(my_cost_str)
# 
# if r[0]:
# 	print "Cost: ", resource_f.make_cost_string(r[1])
# else:
# 	print "Not affordable"





#	Stuff for pathfinding testing
#------------------------
team_dict = {
	"Aybabtu":		75,
	"Azmodizzar":	60,
	"Calidi":		26,
	"Daninia":		72,
}

# print """<a href="#" id="show_a" onclick="$('#show_a').hide(200);$('#results_div').show(200);">Show path output</a><div id="results_div" style="display:none;">"""

# results = path.path(waypoints=[(180, 1170), (180, 1200)], move_speed="Marching", move_type="Medium foot", output="Item")

# results = path.path(waypoints=[(70, 1170), (190, 1180)], move_speed="Marching", move_type="Medium foot", output="Item")

# Long distance over Cayim
results = path.path(waypoints=[(180, 1160), (770, 1640)], move_speed="Marching", move_type="Medium foot", output="Item")

# results = path.path(waypoints=[(-820, 2090), (-710, 2190)], move_speed="Marching", move_type="Medium foot", output="Item")

# results = path.path(waypoints=[(-10, 910), ( -90, 910)], move_speed="Marching", move_type="Medium foot", output="Item")

# results = path.path(waypoints=[(20, 940), (170, 950)], move_speed="Colonists", move_type="Colonists", output="Item")

# Tests across water
# results = path.path(waypoints=[(-360, 814), (-238, 796)], move_speed="Colonists", move_type="Colonists", output="Item")

# Test from Rayti to the north side of an Indis island, they should sail around it, not walk across it
# results = path.path(waypoints=[(40, 920), (-174, 737)], move_speed="Colonists", move_type="Colonists", output="Item")

# results = path.path(waypoints=[(-182, 844), (-188, 808)], move_speed="Colonists", move_type="Colonists", output="Item")

# print '</div>'

if results[0].fastest_path == None:
	print "<br />No path found"

print "<br />Time: ", results[0].travel_time
print "<br />Total steps: ", results[0].total_steps
print "<br />Map units: ", results[0].map_units, " (%skm)" % (results[0].map_units*10)
print "<br />Tile list: ", results[0].tile_list
print "<br />Tile times: ", results[0].tile_time
print "<br />Partial: ", results[0].partial_debug
print "<br />Full: ", results[0].full_debug

tile_list_html = ":".join(["(%s,%s)" % (x[0],x[1]) for x in results[0].tile_list])

print """
<a class="block_link" style="text-align: left;" href="colour_map&list=%s">Map</a>
<form action="web.py" method="post" accept-charset="utf-8">
	<input type="hidden" name="mode" value="colour_map" />
	<input type="hidden" name="list" value="%s" />
	
	<input type="submit" value="Display" />
</form>
""" % (tile_list_html, tile_list_html)

# http://localhost:8888/cgi-bin/teibuilder/colour_map&list=(80,1170):(90,1160)


#	Deity like/dislike/hate
#------------------------
# print deity_f.find_attitude("Arl", "Trchkithin")
