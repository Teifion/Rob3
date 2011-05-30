from pages import common
from classes import world
from data_classes import spell, tech
from functions import wh_f, path_f
from lists import resource_list
from rules import unit_rules, spell_rules, tech_rules

class Wh (object):
	def __init__(self, cursor=None, the_world=None):
		super(Wh, self).__init__()
		self.cursor = cursor
		self.caches = {}
		
		self.local_path = False
		
		if the_world:
			self.the_world = the_world
			self.cursor = the_world.cursor
		else:
			self.the_world = world.World(cursor)
		
		self.the_world.prep_for_oh()
	
	# Sets up caches
	def setup(self, true_team_list=[]):
		# Teams
		team_dict = self.the_world.teams()
		if true_team_list == []:
			true_team_list = team_dict.keys()
		
		# We use the full list of teams so that we don't get key errors later
		for t in team_dict.keys():
			self.caches[t] = {}
		
		# Team dropdown list
		for t in true_team_list:
			if 'team_list' not in self.caches[t]:
				self.caches[t]['team_list'] = []
				self.caches[t]['trade_list'] = []
			
			for team_id, the_team in team_dict.items():
				if t == team_id or the_team.dead or not the_team.active:
					continue
				
				if path_f.find_trade_route(self.the_world.cursor, the_team.id, t, the_world=self.the_world) != (-1, -1):
					self.caches[t]['trade_list'].append('<option value="%s">%s</option>' % (
						the_team.name, the_team.name)
					)
				
				self.caches[t]['team_list'].append('<option value="%s">%s</option>' % (the_team.name, the_team.name))
		
		# World city menu
		city_dict = self.the_world.cities()
		self.caches[0]['world_city_menu'] = []
		for city_id, the_city in city_dict.items():
			if the_city.dead > 0: continue
			if not team_dict[the_city.team].active: continue
			
			self.caches[0]['world_city_menu'].append(
				'<option value="{0}">{1} ({2})</option>'.format(common.js_name(the_city.name), the_city.name.replace('\\', ''), team_dict[the_city.team].name))
		
		# Army dropdown
		army_dict = self.the_world.armies()
		for army_id, the_army in army_dict.items():
			if the_army.team not in true_team_list: continue
			if the_army.garrison > 0: continue
			
			if 'army_list' not in self.caches[the_army.team]:
				self.caches[the_army.team]['army_list'] = []
			
			self.caches[the_army.team]['army_list'].append(
				'<option value="%s">%s</option>' % (the_army.name, the_army.name)
			)
		
		# Zip them down into strings
		true_team_list = list(true_team_list)
		true_team_list.append(0)
		for t in true_team_list:
			for k, v in self.caches[t].items():
				if type(v) == list or type(v) == tuple:
					self.caches[t][k] = "".join(v)
	
	def overview_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('''
		<div class="ti_section" style="padding:0px;" id="overview_div">
			<div class="wh_row">
				<label for="war_name">Order name:</label>
				<input type="text" id="war_name" value="" size="40"/>
			</div>
			<div class="wh_row">
				<label for="target_team">Targets:</label> (chronological order where possible)<br />
				<select id="target_team_1">
					<option value="">&nbsp;</option>
					{team_target}
				</select><br />
				<select id="target_team_2">
					<option value="">Loading...</option>
				</select><br />
				<select id="target_team_3">
					<option value="">Loading...</option>
				</select>
			</div>
			<div class="wh_row">
				<label for="target_city">City targets:</label> (chronological order where possible)<br />
				<select id="target_city_1">
					<option value="">&nbsp;</option>
					{city_target}
				</select><br />
				<select id="target_city_2">
					<option value="">Loading...</option>
				</select><br />
				<select id="target_city_3">
					<option value="">Loading...</option>
				</select><br />
				<select id="target_city_4">
					<option value="">Loading...</option>
				</select><br />
				<select id="target_city_5">
					<option value="">Loading...</option>
				</select>
			</div>
			<div class="wh_row">
				<label for="depart_time">Departure time:</label>
				<select id="depart_time">
					<option value="early">early</option>
					<option value="mid">mid</option>
					<option value="late">late</option>
				</select>
				<select id="depart_month">
					<option value="January">January</option>
					<option value="Feburary">Feburary</option>
					<option value="March">March</option>
					<option value="April">April</option>
					<option value="May">May</option>
					<option value="June">June</option>
					<option value="July">July</option>
					<option value="August">August</option>
					<option value="September">September</option>
					<option value="October">October</option>
					<option value="November">November</option>
					<option value="December">December</option>
				</select>
			</div>
			<div class="wh_row">
				<label for="objectives">Objectives:</label> (one per line, chronological order where possible)<br />
				<textarea id="objectives" rows="6" style="width:99%;"></textarea>
			</div>
		
			<div class="wh_row">
				<label for="expected_allies_1">Expected allies:</label><br />
				<select id="expected_allies_1">
					<option value="">Loading...</option>
				<select id="expected_allies_2">
					<option value="">Loading...</option>
				</select><br />
				<select id="expected_allies_3">
					<option value="">Loading...</option>
				</select>
			</div>
		</div>
		'''.format(
			team_target = self.caches[the_team.id].get('team_list', ''),
			city_target = self.caches[0].get('world_city_menu', ''),
		))
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def units_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('''
		<div class="ti_section" style="padding:0px;" id="units_div">
			<div class="wh_row">
				<label for="armies_1">Armies:</label><br />
				<select id="armies_1">
					{armies}
				</select><br />
				<select id="armies_2">
					<option value="">Loading...</option>
				</select><br />
				<select id="armies_3">
					<option value="">Loading...</option>
				</select><br />
				<select id="armies_4">
					<option value="">Loading...</option>
				</select><br />
				<select id="armies_5">
					<option value="">Loading...</option>
				</select><br />
				<select id="armies_6">
					<option value="">Loading...</option>
				</select><br />
				<select id="armies_7">
					<option value="">Loading...</option>
				</select>
			</div>
		</div>
		'''.format(
			armies = self.caches[the_team.id].get('army_list', ''),
		))
		
		return "".join(output), "".join(load_java), "".join(run_java)
		
	def plan_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('''
		<div class="ti_section" style="padding:0px;" id="plan_div">
			<div class="wh_row">
				<label for="timeline">Timeline:</label><br />
				<textarea id="timeline" rows="8" style="width:99%;"></textarea>
			</div>
			<div class="wh_row">
				<label for="plan">Actual plan:</label><br />
				<textarea id="plan" rows="30" style="width:99%;"></textarea>
			</div>
			<div class="wh_row">
				<label for="reminders">Overall reminders:</label><br />
				<textarea id="reminders" rows="15" style="width:99%;"></textarea>
			</div>
			<div class="wh_row">
				<label for="finally">Finally / Dividing the spoils:</label><br />
				<textarea id="finally" rows="15" style="width:99%;"></textarea>
			</div>
		</div>
		'''.format(
		))
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def feedback_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('''
		<div class="ti_section" style="padding:0px;" id="feedback_div">
			<div class="wh_row">
				<label for="feedback">Feedback:</label> (one line per item you want specific feedback on)<br />
				<textarea id="feedback" rows="12" style="width:99%;"></textarea>
			</div>
		</div>
		'''.format(
		))
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def make_wh(self, team_id):
		the_team = self.the_world.teams()[team_id]
		
		tabs = """
		<div id="tabs" style="border-bottom: 3px solid #EEE; height: 30px;">
			<div class="ti_tab" id="overview_tab" onclick="switch_to('overview');">
				Overview
			</div>
			<div class="ti_tab" id="units_tab" onclick="switch_to('units');">
				Units
			</div>
			<div class="ti_tab" id="plan_tab" onclick="switch_to('plan');">
				Plan
			</div>
			<div class="ti_tab" id="feedback_tab" onclick="switch_to('feedback');">
				Feedback
			</div>
		</div>
		"""
		
		output = [tabs]
		
		load_java	= []
		run_java	= []
		
		# OVERVIEW
		additions = self.overview_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# UNITS
		additions = self.units_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# PLAN
		additions = self.plan_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# FEEDBACK
		additions = self.feedback_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# bytes = len("".join(output))
		# print("")
		# print("<span style='background-color:#FFF;'>Bytes: %s</span>" % format(round(bytes/1000), ','))
		
		# Setup
		output.append(common.onload("on_load_setup();"))
		
		#	JAVASCRIPT
		#------------------------
		javascript = wh_f.javascript("".join(load_java), "".join(run_java))
		
		#	HEADER AND FOOTER
		#------------------------
		# 892px for .content
		# container has 10px padding so left with 872px
		# 872/2 = 436
		# order_box has 5px side margin, becomes 426 yet somehow only 414 works...
		css = """
		.order_box, .order_box_half
		{
			border:1px solid #600;
			background-color:#FFEFEF;
			margin:10px 5px;
			padding:5px;
		}
	
		.order_box_half
		{
			width: 414px;
			float: left;
		}
		"""
	
		output.insert(0, common.headers(title_name="%s war helper" % the_team.name, css=css, javascript=javascript, local_path=self.local_path))
	
		tabs = tabs.replace('id="', 'id="bottom_')
	
		output.append("""
		%s
		<br /><hr />
		<div style="padding: 5px;">
			<input type="button" id="build_button" value="Create orders" onclick="build_orders();"/><br /><br />
			<strong>Complete orders</strong><br />
			<textarea id="final_output" style="width:99%%;" rows="20"></textarea>
		</div>""" % "")#tabs)
	
		output.append(common.footers())
		
		# Compress some output
		final_output = "".join(output)#.replace("	", "").replace("  ", " ").replace("	 ", " ")
		return final_output
	
	
