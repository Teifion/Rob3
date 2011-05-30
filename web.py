#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3

print("Content-type: text/html; charset=utf-8")
print("")

import cgitb
cgitb.enable()

import database
import traceback
import os
import sys
import time
import imp
import re

page_list = []
page_dict = {}

from pages import common, headers
import pages

class HTTP404 (object):
	page_data = {
		'Title':	"HTTP 404",
	}
	def __init__(self):
		super(HTTP404, self).__init__()
	
	def main(self, *args, **kwargs):
		return "404 for %s" % common.get_val('mode')
		
		
		

def html_headers(cursor, page_dict):
	if page_dict.get("Admin", False):
		return headers.main(cursor, page_dict)
	
	# Makes printing those flashy links that much easier
	def linkfade(link_name):
		return '''class="clear_link" onmouseover="$('#%sLinkInfo').fadeIn(250);" onmouseout="$('#%sLinkInfo').fadeOut(250);"''' % (link_name, link_name)
	
	title_name = page_dict["Title"]
	
	output = []
	
	if page_dict.get('Remote path', False):
		jquery_path = "../includes/jquery.js"
		css_path	= "../styles.css"
	else:
		jquery_path = 'media/jquery.js'
		css_path	= "media/styles.css"
	
	return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
	<html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<title>{title_name}</title>
		<script type="text/javascript" src="{jquery_path}" charset="utf-8"></script>
		<link rel="stylesheet" href="{css_path}" type="text/css" media="screen" title="no title" charset="utf-8" />
		<script type="text/javascript" charset="utf-8">
			{javascript}
		</script>
		<style type="text/css" media="screen">
			{css}
		</style>
	</head>
	<body id="body">
		<div class="page">
			<div class="header">
			<div id="logo">
				<a id="woaLogo" href="../"></a>
			</div>
			<ul>
				<li id="registerLink"><a href="http://woarl.com/board/ucp.php?mode=register" {linkfade_register}>Register</a></li>
				<li id="loginLink"><a href="http://woarl.com/board/ucp.php?mode=login" {linkfade_login}>Login</a></li>
				<li id="contactLink"><a href="../pages/general/contact.html" {linkfade_contact}>Contact</a></li>
				<li id="aboutLink"><a href="../pages/general/about.html" {linkfade_about}>About</a></li>
				<li id="blogLink"><a href="http://woarl.com/blog/" {linkfade_blog}>Blog</a></li>
				<li id="guideLink"><a href="../pages/general/starting.html" {linkfade_guide}>Guide</a></li>
				<li id="homeLink"><a href="../" {linkfade_home}>Home</a></li>
				{reload_link}
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
		<div class="contentWide" style="padding: 0px; width: 892px;">
		""".format(
			title_name			= title_name,
			javascript			= page_dict.get('javascript', ''),
			css					= page_dict.get("css", ""),
			linkfade_register	= linkfade('register'),
			linkfade_login		= linkfade('login'),
			linkfade_contact	= linkfade('contact'),
			linkfade_about		= linkfade('about'),
			linkfade_blog		= linkfade('blog'),
			linkfade_guide		= linkfade('guide'),
			linkfade_home		= linkfade('home'),
			jquery_path			= jquery_path,
			css_path			= css_path,
			reload_link			= "",#'<li id="reload"><a href="/reload">Reload</a></li>',
		)


def html_footers(cursor, page_dict, with_analytics=True):
	if page_dict.get("Admin", False):
		return headers.footers(page_dict)
	
	if with_analytics:
		analytics = common.data['analytics']
	else:
		analytics = ""
	
	return """
	</div><!-- content -->
			<div class="clear">
				&nbsp;
			</div>
			</div><!-- page -->
			
			<div class="footer">
			<br />
			Game copyright <a href="http://woarl.com/blog">Teifion Jordan</a>, all rights reserved.<br />
			If you want to use these game rules for your own game, please contact Teifion, all player written stories and cultures are property of their authors
			</div><!-- footer -->
			{0}
		</body>
	</html>""".format(analytics)


# Default to list_teams
common.data['mode'] = common.get_val('mode', 'list_teams')

m = common.data['mode']


# Teams
if	m == "list_teams":	import pages.teams.list_teams as the_page
elif m == "view_borders":	import pages.teams.view_borders as the_page
elif m == "view_relations":	import pages.teams.view_relations as the_page
elif m == "edit_relations":	import pages.teams.edit_relations as the_page
elif m == "edit_team":	import pages.teams.edit_team as the_page
elif m == 'ti':			import pages.teams.ti as the_page
elif m == 'spyrep':		import pages.teams.spyrep as the_page
elif m == 'watchdog':	import pages.teams.watchdog as the_page

elif m == 'get_teams':	import pages.teams.get_teams as the_page
elif m == 'purge_team':	import pages.teams.purge_team as the_page

# Military
elif m == 'list_units':				import pages.military.list_units as the_page
elif m == 'list_armies':			import pages.military.list_armies as the_page
elif m == 'list_squads':			import pages.military.list_squads as the_page
elif m == 'edit_unit':				import pages.military.edit_unit as the_page
elif m == 'edit_army':				import pages.military.edit_army as the_page
elif m == 'edit_squad':				import pages.military.edit_squad as the_page
elif m == 'edit_army_monster':		import pages.military.edit_army_monster as the_page

# Operatives
elif m == 'list_operatives':		import pages.operatives.list_operatives as the_page
elif m == 'edit_operative':			import pages.operatives.edit_operative as the_page

# Players
elif m == 'list_players':			import pages.players.list_players as the_page
elif m == 'get_players':			import pages.players.get_players as the_page
elif m == 'edit_player':			import pages.players.edit_player as the_page
elif m == 'player_kills':			import pages.players.player_kills as the_page

elif m == 'all_achievements':		import pages.players.all_achievements as the_page

elif m == 'all_powers':				import pages.players.all_powers as the_page
elif m == 'list_powers':			import pages.players.list_powers as the_page
elif m == 'edit_power':				import pages.players.edit_power as the_page

# Reseach
elif m == 'list_spells':			import pages.research.list_spells as the_page
elif m == 'list_techs':				import pages.research.list_techs as the_page

elif m == 'tech_points_for_next':	import pages.research.tech_points_for_next as the_page
elif m == 'spell_points_for_next':	import pages.research.spell_points_for_next as the_page

# Cities
elif m == 'list_cities':	import pages.cities.list_cities as the_page
elif m == 'new_cities':		import pages.cities.new_cities as the_page
elif m == 'edit_city':		import pages.cities.edit_city as the_page

elif m == 'list_wonders':	import pages.cities.list_wonders as the_page
elif m == 'new_wonder':		import pages.cities.new_wonder as the_page
elif m == 'edit_wonder':	import pages.cities.edit_wonder as the_page

elif m == 'view_city_trade':	import pages.cities.view_city_trade as the_page
elif m == 'view_city_matrix':	import pages.cities.view_city_matrix as the_page

elif m == 'trade_view':		import pages.cities.trade_view as the_page
elif m == 'trade_matrix':	import pages.cities.trade_matrix as the_page
elif m == 'happiness_breakdown':	import pages.cities.happiness_breakdown as the_page

# Espionage missions
# elif m == 'list_missions':			import pages.mission.list_missions as the_page
# elif m == 'latest_missions':			import pages.mission.latest_missions as the_page
# elif m == 'edit_mission':			import pages.mission.edit_mission as the_page
# elif m == 'handle_mission':			import pages.mission.handle_mission as the_page

# Spy reports
elif m == 'spy_reports':			import pages.operatives.spy_reports as the_page
elif m == 'generate_report':		import pages.operatives.generate_report as the_page
# elif m == 'list_reports':			import pages.mission.list_reports as the_page
# elif m == 'latest_reports':			import pages.mission.latest_reports as the_page
# elif m == 'edit_report':				import pages.mission.edit_report as the_page
# elif m == 'handle_report':			import pages.mission.handle_report as the_page

# Battles
# elif m == 'compare_teams':			import pages.battles.compare_teams as the_page
# elif m == 'battle_team_public':		import pages.battles.battle_team_public as the_page
# elif m == 'battle_team_secret':		import pages.battles.battle_team_secret as the_page

# Campaigns
elif m == 'list_campaigns':				import pages.war.list_campaigns as the_page
elif m == 'setup_campaign':				import pages.war.setup_campaign as the_page
elif m == 'campaign_info':				import pages.war.campaign_info as the_page
elif m == 'turn_info':					import pages.war.turn_info as the_page

elif m == 'add_team_to_campaign':		import pages.war.add_team_to_campaign as the_page

elif m == 'campaign_team_public':		import pages.war.campaign_team_public as the_page
elif m == 'campaign_team_secret':		import pages.war.campaign_team_secret as the_page

# Battles
elif m == 'list_battles':				import pages.war.list_battles as the_page
elif m == 'setup_battle':				import pages.war.setup_battle as the_page
elif m == 'perform_battle':				import pages.war.perform_battle as the_page
elif m == 'perform_by_army':			import pages.war.perform_by_army as the_page

elif m == 'add_battle':					import pages.war.add_battle as the_page
elif m == 'add_unit_loss':				import pages.war.add_unit_loss as the_page
elif m == 'add_army_loss':				import pages.war.add_army_loss as the_page
elif m == 'add_squad_loss':				import pages.war.add_squad_loss as the_page


# New battle GUI
elif m == 'analyse_order':				import pages.order_gui.analyse_order as the_page

# Stats
elif m == 'turn_stats':				import pages.stats.turn_stats as the_page
elif m == 'team_stats':				import pages.stats.team_stats as the_page
elif m == 'stat_stats':				import pages.stats.stat_stats as the_page

# Map
# elif m == 'create_map':				import pages.map.create_map as the_page
elif m == 'edit_map':				import pages.map.edit_map as the_page
# elif m == 'terrain_map':				import pages.map.edit_map as the_page
# elif m == 'coord_map':				import pages.map.coord_map as the_page
# elif m == 'colour_map':				import pages.map.colour_map as the_page
elif m == 'view_map':					import pages.map.view_map as the_page
elif m == 'view_region':				import pages.map.view_region as the_page
# elif m == 'value_map':				import pages.map.value_map as the_page
elif m == 'edit_map_ajax':			import pages.map.edit_map_ajax as the_page
# elif m == 'map_continents':			import pages.map.map_continents as the_page
elif m == 'team_map':				import pages.map.team_map as the_page
elif m == 'gm_map':					import pages.map.gm_map as the_page
elif m == 'map_select':				import pages.map.map_select as the_page
elif m == 'path_map':				import pages.map.path_map as the_page

# Deities
elif m == 'deity_matrix':			import pages.deities.deity_matrix as the_page

# System
elif m == 'lore':					import pages.system.lore as the_page


elif m == 'warnings':				import pages.system.warnings as the_page
elif m == 'rebuild_unit_equipment':	import pages.system.rebuild_unit_equipment as the_page
# elif m == 'system_checks':			import pages.system.check; web.system.check.run()
elif m == 'timestamps':				import pages.system.timestamps as the_page
elif m == 'edit_one_field':			import pages.system.edit_one_field as the_page
elif m == 'to':						import pages.system.to as the_page
elif m == 'direct_query':			import pages.system.direct_query as the_page
elif m == 'msn':					import pages.system.msn_handler as the_page
elif m == 'msn_instructions':		import pages.system.msn_instructions as the_page
elif m == 'surplus_accounts':		import pages.system.surplus_accounts as the_page
# elif m == 'test':					import pages.system.test as the_page

elif m == 'evo_points':				import pages.system.evo_points as the_page
elif m == 'di':						import pages.system.di as the_page

# elif m == 'water_cities':			import pages.system.water_cities as the_page

# elif m == 'queries_log':				import pages.system.queries_log as the_page

elif m == 'list_spells_summary':	import pages.system.list_spells_summary as the_page
elif m == 'trait_display':			import pages.system.display_traits as the_page
elif m == 'beast_display':			import pages.system.beast_display as the_page
elif m == 'deity_display':			import pages.system.deity_display as the_page
elif m == 'deity_summary':			import pages.system.deity_summary as the_page
elif m == 'tech_display':			import pages.system.tech_display as the_page
elif m == 'ship_display':			import pages.system.ship_display as the_page
elif m == 'airship_display':		import pages.system.airship_display as the_page
elif m == 'evo_display':			import pages.system.evo_display as the_page
elif m == 'building_display':		import pages.system.building_display as the_page
elif m == 'unit_designer':			import pages.system.unit_designer as the_page
elif m == 'full_unit_designer':		import pages.system.full_unit_designer as the_page

elif m == 'team_list':				import pages.system.team_list as the_page
# elif m == 'graph_stats':				import pages.system.graph_stats as the_page

# Orders
elif m == 'close_orders':			import pages.orders.close_orders as the_page
# elif m == 'close_orders_half':			import pages.orders.close_orders_half as the_page
elif m == 'get_orders':				import pages.orders.get_orders as the_page
# elif m == 'trades':					import pages.orders.trades as the_page
elif m == 'view_orders':				import pages.orders.view_orders as the_page
elif m == 'interactive_order':		import pages.orders.interactive_order as the_page
elif m == 'view_intorders':			import pages.orders.view_intorders as the_page
elif m == 'test_orders':			import pages.orders.test_orders as the_page
# elif m == 'get_requests':			import pages.orders.get_requests as the_page
# elif m == 'run_request':				import pages.orders.run_request as the_page
elif m == 'results':					import pages.orders.results as the_page
# elif m == 'mass_results':			import pages.orders.mass_results as the_page

# elif m == 'pre_orders':				import pages.orders.pre_orders as the_page

elif m == 'orders_helper':			import pages.orders.orders_helper as the_page
elif m == 'orders_helper_new':		import pages.orders.orders_helper_new as the_page
elif m == 'war_helper':				import pages.orders.war_helper as the_page

# Lists
elif m == 'building_list':			import pages.data_lists.building_list as the_page

# Artefacts
elif m == 'list_artefacts':			import pages.artefacts.list_artefacts as the_page
elif m == 'edit_artefact':			import pages.artefacts.edit_artefact as the_page

# Ajax
elif m == 'get_building_build_time':	import pages.ajax.get_building_build_time as the_page
elif m == 'run_queries':				import pages.ajax.run_queries as the_page

# Website
elif m == 'spell_display':			import pages.website.spell_display as the_page
elif m == 'json':					import pages.website.json_display as the_page

# 404
else:								the_page = HTTP404()

output = []

cursor = database.get_cursor()
page_results = the_page.main(cursor)
ajax = bool(common.get_val('ajax', False))

if the_page.page_data.get("Header", True) and page_results != "" and ajax != True:
	output.append(html_headers(cursor, the_page.page_data))

output.append(page_results)

if the_page.page_data.get("Header", True) and page_results != "" and ajax != True:
	output.append(html_footers(cursor, the_page.page_data, False))


def _print_ignoring_error(text):
	text = re.sub(r"""[^a-zA-Z0-9! 	*$@?_#\-'"+<>()\[\]:=,.;/&\\{}%\n]""", "<strong style='color:#F00;'>*</strong>", text)
	print(text)


output = common.de_unicode("".join(output))

try:
	print(output)
except UnicodeEncodeError as e:
	ignore_uni_errror = common.get_val("iue", 0)
	
	f = open('/Library/WebServer/Documents/rob3/rob_out.html', 'w', encoding='utf-8')
	content = f.write(output)
	f.close()
	
	if ignore_uni_errror:
		_print_ignoring_error(output)
	
	o = output
	
	# Used to recover from a unicode error
	# print(common.redirect('http://localhost/rob3/rob_out.html'))
	# exit()
	
	print("Unicode error at character %d, Ignore errors by adding '&iue=1', <a href='http://localhost/rob3/rob_out.html'>alternately view raw</a><br />" % e.start)
	print("%s<strong style='color:red;'>*</strong>%s" % (o[e.start-300:e.start].replace("<", "&lt;").replace(">", "&gt;"), o[e.start+1:e.start+20].replace("<", "&lt;").replace(">", "&gt;")))
	print("<br />")
	print(e.start, "<br />")
	print(dir(e))
	exit()
except Exception as e:
	raise


# # User
# page_list.append(pages.user.index)
# 
# # Teams
# page_list.append(pages.teams.list_teams)
# page_list.append(pages.teams.add_deity)
# page_list.append(pages.teams.edit_team)
# 
# # HTTP
# page_list.append(pages.http.http_400)
# page_list.append(pages.http.http_401)
# page_list.append(pages.http.http_403)
# page_list.append(pages.http.http_404)
# page_list.append(pages.http.http_500)
