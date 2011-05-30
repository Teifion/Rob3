import time, random
from pages import common
from data import mission, mission_f, mission_q
from data import team, team_f
from data import city, city_q
from data import operative
from rules import espionage_rules

def clean_op_list(list_string):
	new_list = list_string.replace(
		"\n0 x grade 1", "").replace(
			"\n0 x grade 2", "").replace(
				"\n0 x grade 3", "").replace(
					"\n0 x grade 4", "")
	
	new_list = new_list.replace("\n\n", "\n").replace("\n\n", "\n")
	
	if new_list == "\n":
		return "No operatives"
	else:
		return new_list
		

mission_id = int(common.get_val("mission", 0))

# No mission ID? Ask for the latest and use that
if mission_id < 1:
	mission_id = mission_q.get_one_pending_mission_id()

# Still no ID, must be no more pending missions
if mission_id < 1:
	print "There are no more pending missions"
	exit()

# We're good, lets get this show on the road!
the_mission = mission.Mission(mission_q.get_one_mission(mission_id))

teams_dict_c		= team.get_teams_dict_c()
city_dict_c			= city.get_city_dict_c()
operatives_dict_c	= operative.get_operatives_dict_c()

the_team = teams_dict_c[the_mission.team]

output = ['<div style="padding:5px;">']

# City target
if mission.mission_types[the_mission.type] in mission.city_targets:
	output.append('<span class="stitle">City type</span><br /><br />')
	
	the_city	= city_dict_c[the_mission.target]
	target_team	= teams_dict_c[the_city.team]
	
	# Header
	output.append("""%(team)s, <strong>%(type)s</strong> at %(target)s <em>(%(target_team)s)</em>""" % {
		"team":			the_team.name,
		"target":		the_city.name,
		"target_team":	target_team.name,
		"type":			mission.mission_types[the_mission.type],
	})

# Nation target
if mission.mission_types[the_mission.type] in mission.team_targets:
	output.append('<span class="stitle">Nation type</span><br /><br />')
	
	target_team	= teams_dict_c[the_mission.target]
	
	# Header
	output.append("""%(team)s, <strong>%(type)s</strong> at %(target)s""" % {
		"team":		teams_dict_c[the_mission.team].name,
		"target":	teams_dict_c[the_mission.target].name,
		"type":		mission.mission_types[the_mission.type],
	})
	
# Get all operatives and counter-ops in the city
# Work out chance to be caught. Factor in skill of operatives, border type and evos
capture_chance	= espionage_rules.capture_chance(the_mission, the_team, target_team)
difficulty		= espionage_rules.difficulty(the_mission, the_team, target_team)


#	MISSION RESULTS
#------------------------
func = mission_f.mission_functions[mission.mission_types[the_mission.type]]

correct_info	= func(the_mission.target, fudge=0)
real_info		= func(the_mission.target, fudge=difficulty)

#	CAPTURE
#------------------------
full_dict	= {'1':0,'2':0,'3':0,'4':0}
caught_dict	= {'1':0,'2':0,'3':0,'4':0}

caught_list = []
for o in the_mission.allied_ops:
	grade = str(operatives_dict_c[o].grade)
	full_dict[grade] += 1
	if random.uniform(0, 100) < capture_chance:
		caught_list.append(str(o))
		caught_dict[grade] += 1

# Write up the caught/present lists
full_losses = """
%(1)d x grade 1
%(2)d x grade 2
%(3)d x grade 3
%(4)d x grade 4""" % full_dict

real_losses = """
%(1)d x grade 1
%(2)d x grade 2
%(3)d x grade 3
%(4)d x grade 4""" % caught_dict

#	LISTING WHAT'S THERE
#------------------------
# Some duplication here incase we change something in the previous section
operative_dict	= {'1':0,'2':0,'3':0,'4':0}
couterspy_dict	= {'1':0,'2':0,'3':0,'4':0}

for o in the_mission.allied_ops:
	grade = str(operatives_dict_c[o].grade)
	operative_dict[grade] += 1

for o in the_mission.enemy_ops:
	grade = str(operatives_dict_c[o].grade)
	couterspy_dict[grade] += 1

# Write up the op/counterspy lists
operative_info = """
%(1)d x grade 1
%(2)d x grade 2
%(3)d x grade 3
%(4)d x grade 4""" % full_dict

counterspy_info = """
%(1)d x grade 1
%(2)d x grade 2
%(3)d x grade 3
%(4)d x grade 4""" % couterspy_dict


#	FORM ELEMENTS
#------------------------
# Selecting which set of info is sent
allied_ops_str_list = [str(x) for x in the_mission.allied_ops]

info_input = common.option_box(
	'info',
	elements = {
		correct_info:	"Correct",
		real_info: 		"Fudged",
		"No information was returned":	"Failure",
	},
	element_order = [correct_info,real_info,"No information was returned"],
	selected = real_info)

# Selecting what losses are used
loss_input = common.option_box(
	'loss',
	elements = {
		",".join(allied_ops_str_list): 	"All",
		",".join(caught_list):				"Real",
		",":								"None",
	},
	element_order = [",".join(allied_ops_str_list), ",".join(caught_list), ","],
	selected = ",".join(caught_list))

#	ACTUAL OUTPUT
#------------------------
output.append("""
<form action="exec.py" method="post" accept-charset="utf-8">
<input type="submit" value="Apply" />
<br /><br />

<span class="stitle">Results</span><br />
<div style="background-color:#EEF;border:1px dotted #00A;padding:5px;width:48%%;float:left;">
	<strong>Correct</strong><br />
	<textarea name="correct_info" rows="8" style="width:100%%;">%(correct_info)s</textarea>
</div>
<div style="background-color:#FEC;border:1px dotted #A60;padding:5px;width:48%%;float:right;">
	<strong>Real (fudged)</strong><br />
	<textarea name="real_info" rows="8" style="width:100%%;">%(real_info)s</textarea>
</div>
<!--<div style="clear:left;">&nbsp;</div>-->

<span class="stitle">Losses</span><br />
<div style="background-color:#FFE;border:1px dotted #AA0;padding:5px;width:48%%;float:left;">
	<strong>Full</strong><br />
	<textarea name="correct_info" rows="8" style="width:100%%;">%(full_losses)s</textarea>
</div>
<div style="background-color:#FFE;border:1px dotted #AA0;padding:5px;width:48%%;float:right;">
	<strong>Real</strong><br />
	<textarea name="real_info" rows="8" style="width:100%%;">%(real_losses)s</textarea>
</div>
<!--<div style="clear:left;">&nbsp;</div>-->

<span class="stitle">Forces present</span><br />
<div style="background-color:#EFE;border:1px dotted #0A0;padding:5px;width:48%%;float:left;">
	<strong>Operatives</strong><br />
	<textarea name="correct_info" rows="8" style="width:100%%;">%(operative_info)s</textarea>
</div>
<div style="background-color:#FEE;border:1px dotted #A00;padding:5px;width:48%%;float:right;">
	<strong>Couterspies</strong><br />
	<textarea name="real_info" rows="8" style="width:100%%;">%(counterspy_info)s</textarea>
</div>
<div style="clear:left;">&nbsp;</div>

	<input type="hidden" name="mode" id="mode" value="handle_mission_commit" />
	<input type="hidden" name="mission" id="mission" value="%(mission_id)s" />
	&nbsp;&nbsp;&nbsp;
	
	Info: %(info_input)s
	&nbsp;&nbsp;&nbsp;
	
	Losses: %(loss_input)s
	&nbsp;&nbsp;&nbsp;
	
	<input type="submit" value="Apply" />
</form>
""" % {
	"correct_info":		correct_info,
	"real_info":		real_info,
	
	"full_losses":		clean_op_list(full_losses),
	"real_losses":		clean_op_list(real_losses),
	
	"operative_info":	clean_op_list(operative_info),
	"counterspy_info":	clean_op_list(counterspy_info),
	
	"info_input":		info_input,
	"loss_input":		loss_input,
	
	"mission_id":		mission_id,
})

# Display all random numbers
# Display reload with it doing better or worse

output.append("</div>")
print "".join(output)