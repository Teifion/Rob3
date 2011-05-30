import collections
from pages import common
from classes import world
from data_classes import spell
from functions import path_f
from functions import oh_f_new as oh_f
from lists import resource_list
from rules import unit_rules, spell_rules, tech_rules
from json_lib import ti_j
import json

tabs = """
<div id="tabs" style="border-bottom: 3px solid #EEE; height: 30px;">
	<div class="ti_tab" id="construction_tab" onclick="switch_to('construction');">
		Cities
	</div>
	<div class="ti_tab" id="military_tab" onclick="switch_to('military');">
		Military
	</div>
	<div class="ti_tab" id="research_tab" onclick="switch_to('research');">
		Research
	</div>
	<div class="ti_tab" id="operative_tab" onclick="switch_to('operative');">
		Operatives
	</div>
	<div class="ti_tab" id="trade_tab" onclick="switch_to('trade');">
		Trades
	</div>
	<div class="ti_tab" id="diplomacy_tab" onclick="switch_to('diplomacy');">
		Diplomacy
	</div>
	<div class="ti_tab" id="advanced_tab" onclick="switch_to('advanced');">
		Advanced
	</div>
	<div class="ti_tab" id="command_tab" onclick="switch_to('command');">
		Commands
	</div>
</div>
"""

wrappers = """
<div class="ti_section" id="construction_div">
	
</div>
<div class="ti_section" id="military_div">
	
</div>
<div class="ti_section" id="research_div">
	
</div>
<div class="ti_section" id="operative_div">
	
</div>
<div class="ti_section" id="trade_div">
	
</div>
<div class="ti_section" id="diplomacy_div">
	
</div>
<div class="ti_section" id="advanced_div">
	%(advanced)s
</div>
<div class="ti_section" id="command_div">
	%(command)s
</div>
""" % {
	"advanced":	oh_f.advanced_text,
	"command":	oh_f.command_text,
}

class Oh (object):
	def __init__(self, cursor=None, the_world=None):
		super(Oh, self).__init__()
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
		pass
	
	def city_tab(self, the_team):
		city_dict = self.the_world.live_cities_from_team(the_team.id)
		
		cities = collections.OrderedDict()
		fixed_cities = []
		nomadic_cities = []
		for i, c in city_dict.items():
			cities[i] = oh_f.normal_city_block(self, the_team, c)
			if c.nomadic:
				nomadic_cities.append(i)
			else:
				fixed_cities.append(i)
		
		return """
		cities = {cities};
		city_list = {city_list};
		fixed_cities = {fixed_cities};
		nomadic_cities = {nomadic_cities};
		""".format(
			cities = json.dumps(cities),
			city_list = json.dumps(list(cities.keys())),
			fixed_cities = json.dumps(fixed_cities),
			nomadic_cities = json.dumps(nomadic_cities),
		)
	
	def military_tab(self, the_team):
		army_dict = self.the_world.armies_from_team(the_team.id)
		squad_dict = self.the_world.squads_from_team(the_team.id)
		unit_dict = self.the_world.units_from_team(the_team.id)
		global_unit_dict = self.the_world.units_from_team(0)
		
		units = collections.OrderedDict()
		for i, u in unit_dict.items():
			units[i] = {
				"name":	u.name,
			}
		
		for i, u in global_unit_dict.items():
			units[i] = {
				"name":	u.name,
			}
		
		armies = collections.OrderedDict()
		for i, a in army_dict.items():
			armies[i] = oh_f.army_block(self, the_team, a)
		
		squads = collections.OrderedDict()
		for i, s in squad_dict.items():
			squads[i] = oh_f.squad_block(self, the_team, s)
			squads[i]['army'] = army_dict[s.army].name
		
		return """
		units = {units};
		unit_list = {unit_list};
		armies = {armies};
		army_list = {army_list};
		squads = {squads};
		squad_list = {squad_list};
		""".format(
			armies = json.dumps(armies),
			army_list = json.dumps(list(armies.keys())),
			
			units = json.dumps(units),
			unit_list = json.dumps(list(units.keys())),
			
			squads = json.dumps(squads),
			squad_list = json.dumps(list(squads.keys())),
		)
	
	def research_tab(self, the_team):
		output = []
		return "".join(output)
	
	def operative_tab(self, the_team):
		output = []
		return "".join(output)
	
	def trade_tab(self, the_team):
		output = []
		return "".join(output)
		
	def diplomacy_tab(self, the_team):
		output = []
		return "".join(output)
	
	def make_oh(self, team_id):
		the_team = self.the_world.teams()[team_id]
		
		output = [tabs]
		
		# loader_src = '../images/other/loading.gif'
		
		# output.append("""
		# <div id='loading_div' style='text-align:center;padding-top:20px;'>
		# 	Loading...
		# 	<br /><br />
		# 	<img src='%s'/>
		# </div>""" % loader_src)
		
		js_data	= []
		
		# CONSTRUCTION
		js_data.append(self.city_tab(the_team))
		
		# MILITARY - 498
		js_data.append(self.military_tab(the_team))
		
		# RESEARCH - 52
		js_data.append(self.research_tab(the_team))
		
		# OPERATIVES - 221
		js_data.append(self.operative_tab(the_team))
		
		# TRADE - 19
		js_data.append(self.trade_tab(the_team))
		
		# DIPLOMACY - 12
		js_data.append(self.diplomacy_tab(the_team))
		
		"""
		# ADVANCED
		additions = self.advanced_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# COMMANDS
		additions = self.command_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		"""
		
		#	JAVASCRIPT
		#------------------------
		# javascript = oh_f.javascript
		javascript = ""
		
		
		if self.local_path:
			data_lib = 'http://woarl.com/data/oh_data.js'
			data_lib = 'oh_data.js'
		else:
			data_lib = '../data/oh_data.js'
		
		#	HEADER AND FOOTER
		#------------------------
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
		}"""
		
		output.insert(0, common.headers(title_name="%s order creation form" % the_team.name, css=css, javascript=javascript, local_path=self.local_path))
		
		output.append(wrappers)
		
		output.append("""
		<div id='loading_div' style='text-align:center;padding-top:20px;'>
			Loading...
		</div>
		%s
		<br /><hr />
		<div style="padding: 5px;">
			<input type="button" id="build_button" value="Create orders" onclick="build_orders();"/><br /><br />
			<strong>Complete orders</strong><br />
			<textarea id="final_output" style="width:100%%;" rows="20"></textarea>
		</div>""" % tabs.replace('id="', 'id="bottom_'))
		
		# JS libs
		output.append("""
		<script type="text/javascript" charset="utf-8" src="%s"></script>
		<script type="text/javascript" charset="utf-8">
			%s
		</script>
		<script type="text/javascript" charset="utf-8" src="oh_new.js"></script>
		""" % (
			data_lib,
			"".join(js_data),
		))
		
		# And to get the ball rolling!
		output.append(common.onload("on_load_setup();"))
		
		output.append(common.footers())
		
		# Compress some output
		final_output = "".join(output)#.replace("	", "").replace("  ", " ").replace("	 ", " ")
		return final_output
	
	
