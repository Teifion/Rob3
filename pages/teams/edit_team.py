from pages import common
from classes import team, res_dict
from functions import resource_f, deity_f, evolution_f, team_f, trait_f
from queries import team_q, deity_q, evolution_q, trait_q

from lists import resource_list

page_data = {
	"Title":	"Edit team",
	"Admin":	True,
}

def main(cursor):
	# Get team Id
	team_id = int(common.get_val('team', 0))
	if team_id < 1: return "No team selected"
	
	# Build team item
	the_team = team_q.get_one_team(cursor, team_id)
	
	# Get some properties
	the_team.get_population(cursor)
	
	# Lists
	trait_dict = trait_q.get_all_traits(cursor)
	deity_dict = deity_q.get_all_deities(cursor)
	evolution_dict = evolution_q.get_all_evolutions(cursor)
	
	# Is the join turn set?
	if the_team.join_turn == 0:
		the_team.join_turn = common.current_turn()
	
	# First row of check_boxes
	output = ["<div style='padding: 5px;'>"]

	output.append("""
	<span class="stitle">%(name)s</span>
	&nbsp;&nbsp;&nbsp;
	Population: %(team_population)s

	<br /><br />
	<form action="exec.py" method="post" accept-charset="utf-8">
		<input type="hidden" name="mode" id="mode" value="edit_team_commit" />
		<input type="hidden" name="id" id="id" value="%(team_id)d" />
	
		<input type="hidden" name="requestTime" id="requestTime" value="' . $the_team->requestTime . '" />
	
		<label for="active">Active:</label>&nbsp;&nbsp;
		%(active_check_box)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

		<label for="ir">IR:</label>&nbsp;&nbsp;
		%(ir_check_box)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

		<label for="hidden">Hidden:</label>&nbsp;&nbsp;
		%(hidden_check_box)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	
		<label for="not_a_team">Not a team:</label>&nbsp;&nbsp;
		%(not_a_team_check_box)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

		<label for="dead">Dead:</label>&nbsp;&nbsp;
		%(dead_check_box)s
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

		<label for="not_in_queue">Not in queue:</label>&nbsp;&nbsp;
		%(not_in_queue_check_box)s
		<br />
		""" % {	'team_id':					team_id,
				'name':				the_team.name,
				'team_population':			common.number_format(the_team.population),
				'active_check_box':			common.check_box('active', the_team.active),
				'ir_check_box':				common.check_box('ir', the_team.ir),
				'hidden_check_box':			common.check_box('hidden', the_team.hidden),
				'not_a_team_check_box':		common.check_box('not_a_team', the_team.not_a_team),
				'dead_check_box':			common.check_box('dead', the_team.dead),
				'not_in_queue_check_box':	common.check_box('not_in_queue', the_team.not_in_queue),
				})

	# Row 1
	output.append("""
		<table border="0" cellspacing="5" cellpadding="5" style="width:100%%;">
			<tr>
				<td><label for="forum_url_id">Forum URL id:</label></td>
				<td>%(forum_text_box)s</td>
		
				<td width="5">&nbsp;</td>
		
				<td><label for="orders_topic">Orders topic:</label></td>
				<td>%(orders_text_box)s</td>
		
				<td width="5">&nbsp;</td>
		
				<td><label for="intorders_topic">Int Orders topic:</label></td>
				<td>%(intorders_text_box)s</td>
			</tr>""" % {'forum_text_box':		common.text_box('forum_url_id', the_team.forum_url_id, warn_on = lambda x:(True if x < 0 else False)),
						'orders_text_box':		common.text_box('orders_topic', the_team.orders_topic, warn_on = lambda x:(True if x < 0 else False)),
						'intorders_text_box':	common.text_box('intorders_topic', the_team.intorders_topic, warn_on = lambda x:(True if x < 0 else False)),
						})


	# Row 2
	output.append("""
			<tr>
				<td><label for="results_topic">Results topic:</label></td>
				<td>{results_topic}</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="teaminfo_topic">Team info topic:</label></td>
				<td>{teaminfo_topic}</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="team_info_first_post">Team info first post:</label></td>
				<td>{team_info_first_post}</td>
			</tr>""".format(
			results_topic			= common.text_box('results_topic', the_team.results_topic, warn_on = lambda x:(True if x < 0 else False)),
			teaminfo_topic			= common.text_box('teaminfo_topic', the_team.teaminfo_topic, warn_on = lambda x:(True if x < 0 else False)),
			team_info_first_post	= common.text_box('team_info_first_post', the_team.team_info_first_post, warn_on = lambda x:(True if x < 0 else False)),
			))

	# Row 3
	output.append("""
			<tr>
				<td><label for="request_topic">Request topic:</label></td>
				<td>%(request_topic)s</td>
			
				<td width="5">&nbsp;</td>
			
				<td><label for="leader_id">Leader:</label></td>
				<td>%(leader_id)s</td>
			
				<td width="5">&nbsp;</td>
		
				<td>Culture topic:</td>
				<td>%(culture_topic)s</td>
			</tr>""" % {'leader_id':		common.text_box('leader_id', the_team.leader_id, warn_on = lambda x:(True if x < 1 else False)),
						'request_topic':	common.text_box('request_topic', the_team.request_topic, warn_on = lambda x:(True if x < 1 else False)),
						'culture_topic':	common.text_box('culture_topic', the_team.culture_topic, warn_on = lambda x:(True if x < 1 else False)),
					})
	
	output.append("""
	<tr>
		<td><label for="default_borders">Default borders:</label></td>
		<td>%(default_borders)s</td>
		
		<td width="5">&nbsp;</td>
		
		<td><label for="default_taxes">Default taxes:</label></td>
		<td>%(default_taxes)s</td>
		
		<td width="5">&nbsp;</td>
		
		<td><label for="evo_points">Evo points:</label></td>
		<td>%(evo_points)s</td>
	</tr>
	<tr>
		<td colspan="8" style="padding:0px;border-bottom:3px #EEE double;"></td>
	</tr>
	""" % {
		"default_borders":		common.option_box("default_borders", elements=team.border_states, selected=team.border_states[the_team.default_borders]),
		"default_taxes":		common.text_box('default_taxes', the_team.default_taxes, warn_on = lambda x:(True if int(x) < 0 else False), size=4),
		"evo_points":			common.text_box('evo_points', the_team.evo_points, warn_on = lambda x:(True if int(x) < 0 else False)),
	})
	
	output.append("""
			<!--
			<tr>
				<td>Previous resources:</td>
				<td>%(previous_resources)s</td>
			</tr>
			-->
	""" % {
		"previous_resources":	the_team.previous_resources,
		})
	
	# End row
	output.append("""
			<tr>
				<td>Join turn:</td>
				<td>%(join_turn)s</td>

				<td width="5">&nbsp;</td>

				<td>Primary:</td>
				<td>%(primary_colour)s</td>
			
				<td width="5">&nbsp;</td>

				<td>Secondary:</td>
				<td>%(secondary_colour)s</td>
			</tr>
		</table>
		<br />
	
		<input type="submit" value="Perform edit" />
		<input style="float:right; margin-right:100px;" type="button" value="Purge team" onclick="setTimeout('document.location=\\'web.py?mode=purge_team&team=%(team_id)s\\'', 0);"/>
	<a class="block_link" href="web.py?mode=ti&amp;post_output=1&amp;team=%(team_id)s">Update my TI</a>

	<br />""" % {
		"team_id":				team_id,
		'join_turn':			common.text_box('join_turn', the_team.join_turn),
		'previous_resources':	common.text_box('previous_resources', the_team.previous_resources, size=56),
	
		"primary_colour":		common.text_box('primary_colour', the_team.primary_colour),
		"secondary_colour":		common.text_box('secondary_colour', the_team.secondary_colour),
		})
		
	#	Resources
	#------------------------
	the_team.get_resources(cursor)
	
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Resource</th>
		<th>Amount</th>
	</tr>
	""")
	
	counter = -1
	for res_id, the_res in resource_list.data_dict.items():
		if the_res.category == resource_list.category['Map terrain feature']:
			continue
		
		# If it's not set then we need to give it a default
		if not res_id in the_team.resources.value:
			the_team.resources.value[res_id] = 0
		
		counter += 1
		
		output.append("""
		<tr class="row%(row)d">
			<td><label for="res_%(res_name)s">%(res_name)s</label></td>
			<td style="padding:1px;">%(res_amount)s</td>
		</tr>""" % {'row':			(counter % 2),
					'res_name':		the_res.name,
					'res_amount':	resource_f.print_form_element(res_id, the_team.resources[res_id])
					})
	
	output.append("</table></form>")# Subsequent forms are for other stuff
	
	#	Deities
	#----------------------
	the_team.get_deities(cursor)
	
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Deity</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	counter = -1
	for deity_id, team_favour in the_team.deities.items():
		counter += 1
		
		output.append("""
		<tr class="row%(row)d">
			<td><label for="%(name)s">%(name)s</label></td>
			<td style="padding: 0px;">
				<a class="block_link" href="exec.py?mode=remove_deity&amp;deity=%(deity_id)d&amp;team=%(team_id)d">Remove</a>
			</td>
		</tr>""" % {'row':			(counter % 2),
					'name':	deity_dict[deity_id].name,
					'deity_id':		deity_id,
					'team_id':		team_id
					})
	
	output.append("""
		<tr class="row%(row)d">
		<form id="team_add_deity_form" action="exec.py?mode=add_deity" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="add_deity" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<td style="padding:1px;">
				<select name="deity">
					%(deity_option_box)s
				</select>
			</td>
			<td style="padding: 2px;">
				<input type="submit" value="Add" />
				<!--<a href="#" onclick="$('#team_add_deity_form').submit(); return false;" class="block_link">Add</a>-->
			</td>
		</tr>
		</form>
	</table>
	""" % {	'row':				((counter+1) % 2),
			'team_id':			the_team.id,
			'deity_option_box': deity_f.deity_option_list(cursor, the_team.deities)})
	
	
	#	Evolutions
	#-------------------
	the_team.get_evolutions(cursor)
	
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Evolution</th>
		<th>&nbsp;</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	counter = -1
	for evo_id, evo_level in the_team.evolutions.items():
		counter += 1
		
		output.append("""
		<tr class="row%(row)d">
			<form id="edit_evo_%(evolution_id)s" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="set_evolution" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<input type="hidden" name="evolution" value="%(evolution_id)s" />
			<td><label for="%(name)s">%(name)s</label></td>
			<td style="padding:1px;">
				%(text_box)s
			</td>
			</form>
			<td style="padding: 0px;">
				<a class="block_link" href="exec.py?mode=set_evolution&amp;evolution=%(evolution_id)d&amp;team=%(team_id)d">Remove</a>
			</td>
		</tr>""" % {'row':				(counter % 2),
					'name':				evolution_dict[evo_id].name,
					'evolution_level':	evo_level,
					'evolution_id':		evo_id,
					'team_id':			team_id,
					
					"text_box": common.text_box("evolution_level", evo_level, custom_id="", size=3,
						warn_on = lambda e: (True if evolution_dict[evo_id].min_level > e or e > evolution_dict[evo_id].max_level else False)),
					})
	
	output.append("""
		<tr class="row%(row)d">
		<form id="team_add_evolution_form" action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="set_evolution" />
			<input type="hidden" name="team" value="%(team_id)d" />
			<td style="padding:1px;">
				<select name="evolution">
					%(evolution_option_box)s
				</select>
			</td>
			<td style="padding:1px;">
				%(evolution_level)s
			</td>
			<td style="padding: 0px;">
				<a href="#" onclick="$('#team_add_evolution_form').submit();" class="block_link">Add</a>
			</td>
		</tr>
		</form>
	</table>
	""" % {	'row':				((counter+1) % 2),
			'team_id':			the_team.id,
			'evolution_level':	common.text_box('evolution_level', 0, 4),
			'evolution_option_box': evolution_f.evolution_option_list(cursor, the_team.evolutions)})
	
	
	#	Traits
	#----------------------
	the_team.get_traits(cursor)
	
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Trait</th>
		<th>&nbsp;</th>
	</tr>
	""")
	
	counter = -1
	for trait_id in the_team.traits:
		counter += 1
		
		output.append("""
		<tr class="row%(row)d">
			<td><label for="%(name)s">%(name)s</label></td>
			<td style="padding: 0px;">
				<a class="block_link" href="exec.py?mode=remove_trait&amp;trait=%(trait_id)d&amp;team=%(team_id)d">Remove</a>
			</td>
		</tr>""" % {'row':			(counter % 2),
					'name':			trait_dict[trait_id].name,
					'trait_id':		trait_id,
					'team_id':		team_id
					})
	
	output.append("""
		<tr class="row%(row)d">
		<form id="team_add_trait_form" action="exec.py?mode=add_trait" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="add_trait" />
			<input type="hidden" name="team" value="%(team_id)s" />
			<td style="padding:1px;">
				<select name="trait">
					%(trait_option_box)s
				</select>
			</td>
			<td style="padding: 2px;">
				<input type="submit" value="Add" />
				<!--<a href="#" onclick="$('#team_add_trait_form').submit(); return false;" class="block_link">Add</a>-->
			</td>
		</tr>
		</form>
	</table>
	""" % {	'row':				((counter+1) % 2),
			'team_id':			the_team.id,
			'trait_option_box': trait_f.trait_option_list(cursor, the_team.traits)})
	
	
	# Hashes
	output.append("""
	<table style="float:left; margin-right: 25px;" border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Turn</th>
		<th>Hash</th>
	</tr>
	""")

	for i, t in enumerate(range(common.current_turn(), common.current_turn()-5, -1)):
		output.append("""
		<tr class="row{i}">
			<td>{t}</td>
			<td>{hash}</td>
		</tr>""".format(
			i = i % 2,
			t = t,
			hash = team_f.team_hash(the_team.name, turn=t),
	))
	
	output.append("</table>")
	
	
	

	
	output.append("</div>")
	page_data['Title'] = "Edit team (%s)" % the_team.name
	return "".join(output)