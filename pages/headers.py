"""
Used to print out the admin headers
"""

import database
from pages import common
from functions import player_f, mission_f, system_f

from rules import region_data

def main(cursor, page_dict):#css="", javascript="", local_path=True):
	current_turn = common.current_turn()
	output = []
	
	# Region data
	region_table = []
	for r in region_data.region_list:
		region_table.append("""
		<tr>
			<td><a class="nav_link" href="web.py?mode=view_region&amp;region=%s">%s</a>&nbsp;&nbsp;</td>
			<td><a class="nav_link" href="web.py?mode=edit_map&amp;region=%s">Terrain</a>&nbsp;&nbsp;</td>
		</tr>
		""" % (r.name.lower(), r.name, r.name.lower()))
	
	# Print out headers
	output.append("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
	<html>
		<head>
			<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
			<link rel="stylesheet" href="media/admin.css" type="text/css" media="screen" charset="utf-8" />
			<script src="media/jquery.js" type="text/javascript" charset="utf-8"></script>
			<script src="media/jquery-ui.js" type="text/javascript" charset="utf-8"></script>""")
		
	# mission_requests = mission_f.count_mission_requests(cursor)
	# if mission_requests > 0:
	# 	mission_string = " (%s)" % mission_requests
	# else:
	# 	mission_string = ""
	
	warn_count = system_f.get_warn_count(cursor)
	
	if warn_count > 0:
		warnings = """
		<a style="position:absolute;background-color:#C3C;padding:5px;color:#FFF;left:50px;display:block;text-decoration:none;" href="web.py?mode=warnings">
			%d item%s require%s your attention
		</a>""" % (warn_count, ("s" if warn_count > 1 else ""), ("" if warn_count > 1 else "s"))
	else:
		warnings = ""
	
	output.append("""
			<title>{title}</title>
			<style type="text/css" media="screen">
				{css}
			</style>
			<script type="text/javascript" charset="utf-8">
				{javascript}
			</script>
		</head>
		<body>
		<div style="position:absolute;background-color:#66F;padding:5px;color:#FFF;">
			Rob 3
		</div>
		{warnings}
		<div class="headerNav">
			<div class="headerLogo">
				&nbsp;
			</div>
			<ul>
				<li><a href="web.py?mode=list_teams&amp;all_teams=True">Teams</a></li>
				<li><a href="web.py?mode=list_players">Players</a></li>
				<li><a href="web.py?mode=view_map">Map</a></li>
				<li><a href="web.py?mode=to&amp;dev_mode=1&amp;ajax=1">TO</a></li>
				<li><a href="web.py?mode=list_artefacts">Artefacts</a></li>
				<li><a href="web.py?mode=list_powers">Powers</a></li>
				<li><a href="web.py?mode=list_campaigns">Campaigns</a></li>
				<li><a href="web.py?mode=spy_reports">Spy reports</a></li>
				<li><a href="web.py?mode=list_wonders">Wonders</a></li>
				<li><a href="web.py?mode=turn_stats&amp;turn={turn}">Stats</a></li>
			
				<li>&nbsp;&nbsp;&nbsp;&nbsp;</li>
			
				<li><a href="{board}web.py">Board</a></li>
			</ul>
		</div>
			""".format(
				title=page_dict.get('Title', "Rob3"),
				css = page_dict.get('CSS', ""),
				javascript = page_dict.get('javascript', ""),
				turn = current_turn,
				board = common.data['board_url'],
				warnings = warnings
			))
	
	# It might be under Team Id
	team = int(common.get_val('team', 0))
	
	if team < 1:
		team = common.get_val('team_id', 0)
	
	# Maybe it's a page that has team stuff on it
	if team < 1:
		if common.data['mode'] == 'edit_unit':
			unit_id = int(common.get_val('unit', 0))
			if unit_id > 0:
				query = "SELECT team FROM units WHERE id = %d LIMIT 1" % unit_id
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
			
		if common.data['mode'] == 'edit_army':
			army_id = int(common.get_val('army', 0))
			if army_id > 0:
				query = "SELECT team FROM armies WHERE id = %d LIMIT 1" % army_id
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
		
		if common.data['mode'] == 'list_squads':
			army_id = int(common.get_val('army', 0))
			if army_id > 0:
				query = "SELECT team FROM armies WHERE id = %s LIMIT 1" % int(army_id)
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
		
		if common.data['mode'] == 'edit_player':
			player_id = int(common.get_val('player', 0))
			if player_id > 0:
				query = "SELECT team FROM players WHERE id = %d LIMIT 1" % player_id
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
		
		if common.data['mode'] == 'edit_squad':
			squad_id = int(common.get_val('squad', 0))
			if squad_id > 0:
				query = "SELECT team FROM squads WHERE id = %d LIMIT 1" % squad_id
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
		
		if common.data['mode'] == 'edit_city':
			city_id = int(common.get_val('city', 0))
			if city_id > 0:
				query = "SELECT team FROM cities WHERE id = %d LIMIT 1" % city_id
				try: cursor.execute(query)
				except Exception as e:
					raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
				for row in cursor:
					team = row['team']
	
	if team > 0:
		query = "SELECT forum_url_id, orders_topic, intorders_topic, name FROM teams WHERE id = %s LIMIT 1;" % team
		try:
			cursor.execute(query)
		except Exception as e:
			print("Query: %s\n" % query)
			raise e
	
		row = cursor.fetchone()
		if row == None: exit('Error')
		team_data = {}
		team_data['team_id']			= team
		team_data['forum_url_id']		= row['forum_url_id']
		team_data['orders_topic']		= row['orders_topic']
		team_data['intorders_topic']	= row['intorders_topic']
		team_data['name']			= row['name']
		
		output.append("""
			<div class="subheaderNav"> 
				<ul>
					<li><strong>%(name)s:&nbsp;&nbsp;</strong></li>
					<li><a href="web.py?mode=list_cities&amp;team=%(team_id)d">Cities</a></li>
					<li><a href="web.py?mode=list_spells&amp;team=%(team_id)d">Magic</a></li>
					<li><a href="web.py?mode=list_techs&amp;team=%(team_id)d">Tech</a></li>
					<li><a href="web.py?mode=list_units&amp;team=%(team_id)d">Military</a></li>
					<li><a href="web.py?mode=list_armies&amp;team=%(team_id)d">Armies</a></li>
					<li><a href="web.py?mode=list_operatives&amp;team=%(team_id)d">Ops</a></li>
					<li><a href="web.py?mode=list_artefacts&amp;team=%(team_id)d">Artefacts</a></li>
					<li><a href="web.py?mode=list_players&amp;team=%(team_id)d">Players</a></li>
					<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</li>
					<li><a href="web.py?mode=team_stats&amp;team=%(team_id)d">Stats</a></li>
					<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</li>""" % team_data)
	
		output.append("""
					<li><a href="web.py?mode=view_orders&amp;team=%s&amp;turn=%s">Orders</a></li>
			""" % (team, current_turn))
	
		output.append("""
					<li><a href="web.py?mode=view_intorders&amp;team=%s&amp;turn=%s">Int Orders</a></li>
			""" % (team, current_turn))
	
		output.append("""
					<li><a href="web.py?mode=ti&amp;turn=%s&amp;team=%s">Team Info</a></li>
					<li><a href="web.py?mode=results&amp;team=%s">Results</a></li>
					<li><a href="%sviewforum.php?f=%s">Forum</a></li>
				
					<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</li>
				
					<li><a href="web.py?mode=edit_team&team=%s">Edit</a></li>
				</ul>
			</div>""" % (current_turn, team, team, common.data['board_url'], team_data['forum_url_id'], team))

	output.append("""
			<div class="page">
				<div class="sideNav">
					<ul>
						<li class="navHeading">Turn sequence</li>
						<li><a href="web.py?mode=watchdog">Team watchdog</a></li>
						<li><a href="web.py?mode=new_cities">New cities</a></li>
						<li><a href="web.py?mode=mass_results">Mass results</a></li>
						
						<li>&nbsp;</li>
						<li><a href="web.py?mode=analyse_order">Analyse order</a></li>
						<li><a href="web.py?mode=trade_matrix">Trade matrix</a></li>
						<li><a href="web.py?mode=trade_view">Trade preview</a></li>
					</ul>
					<div class="navDrop">
						&nbsp;
					</div>
					<ul>
						<li class="navHeading">Utilities</li>
						<li><a href="web.py?mode=path_map">Path map</a></li>
						
						<!--
						<li><a href="web.py?mode=edit_map&amp;grid_size=10">Map editor</a></li>
						<li><a href="web.py?mode=terrain_map&amp;grid_size=10">Map terrain view</a></li>
						<li><a href="web.py?mode=supplies_map&amp;grid_size=10">Map supplies</a></li>
						<li><a href="web.py?mode=coord_map&amp;grid_size=10">Map coordinates</a></li>
						-->
						<li><a href="web.py?mode=team_map">Team map</a></li>
						<li><a href="web.py?mode=gm_map">GM map</a></li>
						<li><a href="web.py?mode=team_list">Team list</a></li>
						
						<li>&nbsp;</li>
						<li><a href="web.py?mode=test_orders">Test orders</a></li>
						<li><a href="web.py?mode=view_relations">Team relations</a></li>
					</ul>
					<div class="navDrop">
						&nbsp;
					</div>
					<ul>
						<li class="navHeading">System</li>
						<li><a href="web.py?mode=rebuild_unit_equipment">Rebuild unit equipment</a></li>
						<li><a href="web.py?mode=map_select">Map select</a></li>
						<li>&nbsp;</li>
						<li><a href="web.py?mode=get_teams">Get teams</a></li>
						<li><a href="web.py?mode=get_players">Get players</a></li>
						<li>&nbsp;</li>
						<li><a href="web.py?mode=evo_points">Evo points</a></li>
						<li><a href="web.py?mode=di">DI points</a></li>
						<li>&nbsp;</li>
						<li><a href="web.py?mode=queries_log">Queries log</a></li>
						<li><a href="web.py?mode=direct_query">Direct query</a></li>
						<li><a href="web.py?mode=surplus_accounts">Surplus accounts</a></li>
					</ul>
				
					<div class="navDrop">
						&nbsp;
					</div>
					<ul>
						<li class="navHeading">Map regions</li>
						<table border="0" cellspacing="0" cellpadding="3">
							%(region_table)s
						</table>
					</ul>
				
					<div class="navDrop">
						&nbsp;
					</div>
					<ul>
						<li class="navHeading">Script pages</li>
						<li><a href="web.py?mode=orders_helper">Orders helper</a></li>
						<li><a href="web.py?mode=war_helper">War helper</a></li>
					</ul>
					
					<div class="navDrop">
						&nbsp;
					</div>
					<ul>
						<li class="navHeading">Lists</li>
						<li><a href="web.py?mode=building_list">Building list</a></li>
						<li><a href="web.py?mode=equipment_list">Equipment list</a></li>
						<li><a href="web.py?mode=evolution_list">Evolution list</a></li>
						<li><a href="web.py?mode=deity_list">Deity list</a></li>
						<li><a href="web.py?mode=spell_list">Spell list</a></li>
						<li><a href="web.py?mode=tech_list">Tech list</a></li>
						
						<li>&nbsp;</li>
						<li><a href="web.py?mode=deity_matrix">Deity like/dislike</a></li>
					</ul>
				</div>
				<div class="content" id="content">
					<span id="ajax_target"></span>""" % {
						"region_table":	"".join(region_table),
					})
	
	return "".join(output)

def footers(page_dict):
	return """
					<div style="clear: both; height: 0px;">
						&nbsp;
					</div>
				</div><!-- Content -->
				<div class="footer">
					&nbsp;
				</div>
			</div><!-- Page -->
		</body>
	</html>"""
	
	return """
	<br /><br />
	Queries: %s<br />
	Unique queries: %s<br />
	Time taken: %s seconds
					<div style="clear: both; height: 0px;">
						&nbsp;
					</div>
				</div><!-- Content -->
				<div class="footer">
					&nbsp;
				</div>
			</div><!-- Page -->
		</body>
	</html>
	""" % (len(cursor.query_list), len(set(cursor.query_list)), round(time.time() - start_time, 2))
