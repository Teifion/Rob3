import time
import database
from pages import common
from queries import team_q

def headers(the_world):
	# Makes printing those flashy links that much easier
	def linkfade(link_name):
		return '''class="clear_link" onmouseover="$('#%sLinkInfo').fadeIn(250);" onmouseout="$('#%sLinkInfo').fadeOut(250);"''' % (link_name, link_name)
	
	return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<title>World of Arl Team Overview</title>
		<script type="text/javascript" src="../includes/jquery.js" charset="utf-8"></script>
		<link rel="stylesheet" href="../styles.css" type="text/css" media="screen" title="no title" charset="utf-8" />
		<style type="text/css" media="screen">
			.team_row, .team_row_hover
			{
				font-size:			1em;
				cursor:				pointer;
				border-bottom:		1px solid #50A;
				padding:			3px;
				background-color:	#CCF;
			}
			
			.team_row:hover
			{
				color:				#FFF;
				background-color:	#000;
			}
			
			.team_row_hover
			{
				color:				#FFF;
				background-color:	#000;
			}
			
			.team_icon, .team_icon_hover
			{
				background-color:	#FFF;
				float:				left;
				padding:			3px;
				border:				1px solid #FFF;
			}
			
			.team_icon:hover, .team_icon_hover
			{
				background-color:	#000;
				border:				1px solid #00A;
			}
			
			.war_row td
			{
				border-bottom:		1px dotted #000;
			}
		</style>
		%(javascript)s
	</head>
	<body id="order_form" onload="">
		<div class="page">
			<div class="header">
			<div id="logo">
				<a id="woaLogo" href="../"></a>
			</div>
			<ul>
				<li id="registerLink"><a href="http://woarl.com/board/ucp.php?mode=register" %(linkfade_register)s>Register</a></li>
				<li id="loginLink"><a href="http://woarl.com/board/ucp.php?mode=login" %(linkfade_login)s>Login</a></li>
				<li id="contactLink"><a href="../pages/general/contact.html" %(linkfade_contact)s>Contact</a></li>
				<li id="aboutLink"><a href="../pages/general/about.html" %(linkfade_about)s>About</a></li>
				<li id="blogLink"><a href="http://woarl.com/blog/" %(linkfade_blog)s>Blog</a></li>
				<li id="guideLink"><a href="../pages/general/starting.html" %(linkfade_guide)s>Guide</a></li>
				<li id="homeLink"><a href="../" %(linkfade_home)s>Home</a></li>
			</ul>
			<div id="infoLinkWrapper">
				<div id="homeLinkInfo">&nbsp;</div>
				<div id="guideLinkInfo">&nbsp;</div>
				<div id="blogLinkInfo">&nbsp;</div>
				<div id="aboutLinkInfo">&nbsp;</div>
				<div id="contactLinkInfo">&nbsp;</div>
				<div id="loginLinkInfo">&nbsp;</div>
				<div id="registerLinkInfo">&nbsp;</div>
			</div>
		</div>
		<!-- 852px width normally, 20px padding -->
		<div class="contentWide">
		""" % {
			"javascript":			javascript(the_world),
			"linkfade_register":	linkfade('register'),
			"linkfade_login":		linkfade('login'),
			"linkfade_contact":		linkfade('contact'),
			"linkfade_about":		linkfade('about'),
			"linkfade_blog":		linkfade('blog'),
			"linkfade_guide":		linkfade('guide'),
			"linkfade_home":		linkfade('home'),
		}

def footers(the_world):
	"""docstring for footers"""
	return """</div><!-- content -->
			<div class="clear">
				&nbsp;
			</div>
			</div><!-- page -->
			
			<div class="footer">
			<br />
			Game copyright <a href="http://woarl.com/blog">Teifion Jordan</a>, all rights reserved.<br />
			If you want to use these game rules for your own game, please contact Teifion, all player written stories and cultures are property of their authors
			</div><!-- footer -->
			%s
		</body>
	</html>""" % common.data['analytics']

def javascript(the_world):
	return ""
	return """
	<script type="text/javascript" charset="utf-8">
		function hide_all_sections ()
		{
			$('#evolutions_div').hide();
			$('#resources_div').hide();
			$('#deities_div').hide();
			$('#units_div').hide();
			$('#armies_div').hide();
			$('#operatives_div').hide();
			$('#techs_div').hide();
			$('#spells_div').hide();
			$('#chosen_div').hide();
			$('#cities_div').hide();
			
			$('#evolutions_tab').removeClass('ti_tab_selected');
			$('#resources_tab').removeClass('ti_tab_selected');
			$('#deities_tab').removeClass('ti_tab_selected');
			$('#units_tab').removeClass('ti_tab_selected');
			$('#armies_tab').removeClass('ti_tab_selected');
			$('#operatives_tab').removeClass('ti_tab_selected');
			$('#techs_tab').removeClass('ti_tab_selected');
			$('#spells_tab').removeClass('ti_tab_selected');
			$('#chosen_tab').removeClass('ti_tab_selected');
			$('#cities_tab').removeClass('ti_tab_selected');
		}
		
		function switch_to_evolutions ()
		{
			hide_all_sections();
			$('#evolutions_div').show();
			$('#evolutions_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_resources ()
		{
			hide_all_sections();
			$('#resources_div').show();
			$('#resources_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_deities ()
		{
			hide_all_sections();
			$('#deities_div').show();
			$('#deities_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_units ()
		{
			hide_all_sections();
			$('#units_div').show();
			$('#units_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_armies ()
		{
			hide_all_sections();
			$('#armies_div').show();
			$('#armies_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_operatives ()
		{
			hide_all_sections();
			$('#operatives_div').show();
			$('#operatives_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_techs ()
		{
			hide_all_sections();
			$('#techs_div').show();
			$('#techs_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_spells ()
		{
			hide_all_sections();
			$('#spells_div').show();
			$('#spells_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_chosen ()
		{
			hide_all_sections();
			$('#chosen_div').show();
			$('#chosen_tab').addClass('ti_tab_selected');
		}
		
		function switch_to_cities ()
		{
			hide_all_sections();
			$('#cities_div').show();
			$('#cities_tab').addClass('ti_tab_selected');
		}
	</script>
	"""


def make_to(the_world):
	output = []
	
	dev_mode = int(common.get_val("dev_mode", 0))
	if dev_mode == 1:	file_path = "http://localhost/woa/map/images/teamIcons/"
	else:				file_path = "../map/images/teamIcons/"
	
	# TODO stats
	# TODO compare teams
	
	team_dict 		= the_world.teams()
	cities_dict		= the_world.cities()
	player_dict		= the_world.players()
	artefacts_dict	= the_world.artefacts()
	deity_dict		= the_world.deities()
	evolution_dict	= the_world.evolutions()
	
	current_turn = common.current_turn()
	
	output.append("""Last updated: %s<br />
	Click a team name on the left or on their icon on the right to display team information.""" % time.strftime("%H:%M %A %d %B", time.localtime()))
	
	# output.append("")# This will be replaced with a teamcount
	
	output.append("""<noscript> <span style='color: #A00;'>If you are seeing this then you do not have javascript enabled. You need to have javascript enabled for this page to work correctly.</span></noscript>
	<br /><br />
	<div onmouseout='$("#name_div").html("&nbsp;");'>""")
	
	image_menu	= []
	text_menu	= []
	team_divs	= []
	
	count = -1
	team_count = 0
	
	real_team_dict = team_q.get_real_active_teams(the_world.cursor, skip_irs=False)
	
	last_team_ir = False
	
	for team_id in real_team_dict.keys():
		the_team = team_dict[team_id]
		
		# Teams that don't need to appear on the TO
		if the_team.hidden: continue
		count += 1
		
		# How many player teams?
		if the_team.ir == 0: team_count += 1
		
		
		#	MENUS
		#------------------------
		js = "$('#team_display').hide(1, function() {$('#team_display').html($('#team_%(team_id)s').html()); $('#team_display').show(1);});" % {"team_id":team_id}
		
		#	IMAGE MENU
		#------------------------
		if the_team.ir != last_team_ir:
			count = 0
			image_menu.append("""<tr>
			<td colspan="9">&nbsp;</td>
			</tr>""")
		
		column_number = count % 9
		
		if column_number == 0:
			image_menu.append("""</tr><tr>""")
		
		image_menu.append("""<td style="padding:1px;">
		<div class="team_icon"
			onmousedown="%(js)s"
			onmouseover="$('#name_div').html('%(js_name)s'); $('#team_list_%(team_id)s').addClass('team_row_hover'); $('#team_list_%(team_id)s').removeClass('team_row');"
			onmouseout="$('#team_list_%(team_id)s').removeClass('team_row_hover'); $('#team_list_%(team_id)s').addClass('team_row');"
		id="team_selector_%(team_id)s">
				<img src="%(file_path)s%(clean_name)s_to.png" alt="%(name)s logo" width="64" height="64" style="cursor: pointer;"/>
			</div></td>
		""" % {
			"team_id":		team_id,
			"file_path":	file_path,
			"js":			js,
			"name":			the_team.name,
			"clean_name":	the_team.clean_name(),
			"js_name":		common.js_name(the_team.name),
		})
		
		#	TEXT MENU
		#------------------------
		if the_team.ir != last_team_ir:
			text_menu.append("""<div class="team_row" style="text-align:center;">
			<br />
			<strong>Indigenous races</strong>
			</div>
			""")
			last_team_ir = the_team.ir
			
		
		text_menu.append("""<div id="team_list_%(team_id)s" class="team_row"
			onclick="%(js)s"
			onmouseover="$('#name_div').html('%(js_name)s'); $('#team_selector_%(team_id)s').addClass('team_icon_hover'); $('#team_selector_%(team_id)s').removeClass('team_icon');"
			onmouseout="$('#team_selector_%(team_id)s').removeClass('team_icon_hover'); $('#team_selector_%(team_id)s').addClass('team_icon');">
				%(name)s
			</div>""" % {
			"team_id":		team_id,
			"clean_name":	the_team.clean_name(),
			"js":			js,
			"name":	the_team.name,
			"js_name":		common.js_name(the_team.name),
		})
		
		
		#	ACTUAL TEAM INFO
		#------------------------
		this_team = []
		
		ir_text = ""
		if the_team.ir: ir_text = "<span style='font-size: 0.8em;'>(Indigenous race)</span>"
		
		# TEAM HEADER
		this_team.append("""
		<img src="%(file_path)s%(clean_name)s_to.png" alt="%(name)s logo" width="64" height="64" style="padding-right: 10px;" />
		<div style="width: 300px; float: left;">
			<span class="stitle">%(name)s %(ir_text)s</span>
			<br />
		""" % {
			"file_path":	file_path,
			"clean_name":	the_team.clean_name(),
			"name":	the_team.name,
			"ir_text":		ir_text,
		})
		
		# LEADER
		if the_team.leader_id > 0:
			this_team.append("""<strong>Leader</strong>: <a class="clear_link" href="http://woarl.com/board/memberlist.php?mode=viewprofile&u=%(leader_id)s">%(name)s</a>
			<br />""" % {
				"leader_id":	the_team.leader_id,
				"name":			player_dict[the_team.leader_id].name
			})
		else:
			this_team.append('<span class="neg">Teifion has not added a team leader!</span><br />')
		
		# Players
		team_players = the_world.players_from_team(the_team.id)
		seconds = []
		for p, the_player in team_players.items():
			if the_player.id != the_team.leader_id:
				if the_player.last_posted >= common.current_turn() - 4:
					seconds.append(
						'<a class="clear_link" href="http://woarl.com/board/memberlist.php?mode=viewprofile&u={0}">{1}</a>'.format(
							p, the_player.name
						)
					)
		
		if len(seconds) > 0:
			this_team.append("""<strong>Seconds</strong>: %s<br />""" % ", ".join(seconds))
		
		
		# CULTURE
		if the_team.culture_topic > 0:
			this_team.append("""<strong>Culture</strong>: <a class="clear_link" href="http://woarl.com/board/viewtopic.php?t=%s">Link</a>
			<br />""" % the_team.culture_topic)
		else:
			this_team.append('<span class="neg">Teifion has not added a team culture link!</span><br />')
		
		# SIZE
		this_team.append("<strong>Size</strong>: %s<br />" % common.approx(the_team.get_size(the_world.cursor)))
		
		# START TURN
		if the_team.join_turn > 0:
			this_team.append("<strong>Started</strong>: Turn %s<br />" % the_team.join_turn)
		else:
			this_team.append('<span class="neg">Teifion has not added a start turn for this team</span><br />')
		
		# Deities
		try:
			deity_string = ", ".join([deity_dict[d].name for d in the_team.get_deities(the_world.cursor).keys()])
		except Exception:
			raise
		
		if deity_string != "":
			this_team.append("<strong>Deities</strong>: %s<br />" % deity_string)
		
		#	EVOLUTIONS
		#-----------------------
		this_team.append('<br /><strong>Evolutions</strong><br />')
		total_points = 0
		
		for evolution_id in the_team.evolutions:
			the_evo = evolution_dict[evolution_id]
			if the_team.evolutions[evolution_id] == 0: continue
			
			total_points += (the_evo.cost_per_level * the_team.evolutions[evolution_id])
			
			if the_evo.max_level == 1 and the_team.evolutions[evolution_id] == 1:
				this_team.append("""%(evo_name)s [%(cost)s] - <em style="font-size:0.9em;">%(description)s</em><br />""" % {
					"evo_name":		the_evo.name,
					"cost":	   		the_evo.cost_per_level * the_team.evolutions[evolution_id],
					"description":	the_evo.description,
				})
			else:
				if the_team.evolutions[evolution_id] < 1:
					# 1-
					this_team.append("""<span class="neg">%(level)sx</span> %(evo_name)s [%(cost)s]
					<br />""" % {
						"level":	the_team.evolutions[evolution_id],
						"evo_name":	the_evo.name,
						"cost":		the_evo.cost_per_level * the_team.evolutions[evolution_id],
					})
				else:
					# 1+
					this_team.append("""<span class="pos">%(level)sx</span> %(evo_name)s [%(cost)s]
					<br />""" % {
						"level":	the_team.evolutions[evolution_id],
						"evo_name":	the_evo.name,
						"cost":		the_evo.cost_per_level * the_team.evolutions[evolution_id],
					})
		
		this_team.append("&nbsp;&nbsp;&nbsp;Total points spent: %s<br />" % total_points)
		
		#	CITIES
		#------------------------
		this_team.append('<br /><strong>Cities</strong><br />')
		team_cities = the_world.cities_from_team(the_team.id)#city_q.get_cities_from_team(team=the_team.id, include_dead=0)
		
		for city_id, the_city in team_cities.items():
			if the_city.dead > 0: continue
			this_team.append('<a href="http://woarl.com/map/latest.html#mv_%s">%s</a><br />' % (the_city.name.replace(' ', '').replace("'", "").lower(), the_city.name))
		
		#	ARTIFACTS
		#------------------------
		artefacts_list = []
		for c, the_city in team_cities.items():
			if len(the_city.artefacts) > 0:
				artefacts_list.extend(the_city.artefacts)
		
		if len(artefacts_list) > 0:
			this_team.append('<br /><strong>Artefacts</strong><br />')
			
			for a in artefacts_list:
				this_team.append("%s <em>(%s)</em><br />" % (artefacts_dict[a].name, cities_dict[artefacts_dict[a].city].name))
		
		# End of left float
		this_team.append("</div>")
		
		
		#	START OF WAR DIV
		#------------------------
		'''
		this_team.append("""<div style="width: 300px; float: left; padding-left: 50px;">
			<div style="text-align: center; font-size: 1.2em; font-weight: bold;">Battle history</div>
			<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<th>Turn</th>
				<th>War</th>
				<th>Losses</th>
			</tr>
		""")
		
		battle_order, battle_dict = battle_q.get_battles_from_team(team_id, since_turn=common.current_turn()-5)
		squads_order, squads_dict = squad_q.get_squads_from_team(team_id)
		
		# Run all relevant DB queries for these squads
		for s in squads_order: squads_dict[s].get_battles()
		
		w_count = 0
		for b in battle_order:
			# if count > 10: continue
			w_count += 1
			
			the_battle = battle_dict[b]
			
			battle_losses = 0
			for s in squads_order: battle_losses += squads_dict[s].losses.get(b, 0)
			
			this_team.append("""
			<tr>
				<td>%(turn)s</td>
				<td>%(name)s</td>
				<td>%(losses)s</td>
			</tr>""" % {
				"turn":			the_battle.turn,
				"name":	the_battle.name,
				"losses":		common.approx(battle_losses),
			})
		
		this_team.append("</table></div>")
		'''
		this_team.append("</div>")
	
		team_divs.append("""<div id="team_%s" style="display: none;" class="team_display">
			%s
		<br />
		</div>
		""" % (team_id, "".join(this_team)))
	
	
	output.append("""
		<div style="width: 140px; float: left; padding-right: 10px; margin-left: -5px;">
			<div class="team_row" style="text-align:center;">
				<strong>Player teams</strong>
			</div>
			%s
		<br />
		</div>""" % "".join(text_menu))
	
	output.append("""<table border="0" cellspacing="0" cellpadding="0" style="margin:0 auto;"><tr>""")
	output.append("".join(image_menu))
	output.append("""</tr></table>""")
	
	output.append("""</div>
	<div style="clear: right;">&nbsp;</div>
	<div id="name_div" style="color: #555; text-align: center; font-weight: bold; font-size: 1.2em;">
		&nbsp;
	</div>
	<br />
	
	<div id="team_display" style="display: none;">
		&nbsp;
		<span style="clear:left;"></span>
	</div>
	<div id="all_teams" style="display: none;">
	""")
	
	output.append("".join(team_divs))
	
	output.append('</div>')
	
	# Autoloads the ZO
	# output.append(common.onload("$('#team_display').html($('#team_35').html()); $('#team_display').show();"))
	# output.append(common.onload("$('#team_display').html($('#team_41').html()); $('#team_display').show();"))
	# output.append(common.onload("$('#team_display').html($('#team_75').html()); $('#team_display').show();"))
	
	output.insert(1, ' %s player teams in action.' % team_count)
	
	return "".join(output)