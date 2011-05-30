from pages import common
from classes import world
from data_classes import spell
from functions import oh_f, path_f
from lists import resource_list
from rules import unit_rules, spell_rules, tech_rules

class Oh (object):
	"""docstring for Oh"""
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
		# Teams
		team_dict = self.the_world.teams()
		if true_team_list == []:
			true_team_list = team_dict.keys()
		
		# We use the full list of teams so that we don't get key errors later
		for t in team_dict.keys():
			self.caches[t] = {}
		
		# Wonders
		cities_with_wonders	= self.the_world.cities_with_wonders()
		city_dict			= self.the_world.cities()
		
		for c in cities_with_wonders:
			if 'wonder_menu' not in self.caches[city_dict[c].team]:
				self.caches[city_dict[c].team]['wonder_menu'] = []
			
			self.caches[city_dict[c].team]['wonder_menu'].append(
				'<option value="%s">%s</option>' % (
					common.js_name(city_dict[c].name), city_dict[c].name
				)
			)
		
		# Founding
		for c, the_city in city_dict.items():
			if the_city.team not in true_team_list:
				continue
			
			if the_city.dead > 0 or the_city.population < 5000:
				continue
			
			if 'founding_dropdown' not in self.caches[the_city.team]:
				self.caches[the_city.team]['founding_dropdown'] = ['<option value="">All cities</option>']
			
			self.caches[the_city.team]['founding_dropdown'].append(
				'<option value="%s">%s</option>' % (the_city.name, the_city.name)
			)
		
		# Relocation, same as founding minus the first item
		for t in true_team_list:
			self.caches[t]['relocation_dropdown'] = list(self.caches[t].get('founding_dropdown', '<option value=""></option>'))
			del(self.caches[t]['relocation_dropdown'][0])
		
		
		# Army dropdown
		army_dict = self.the_world.armies()
		for army_id, the_army in army_dict.items():
			if the_army.team not in true_team_list: continue
			
			if 'army_list' not in self.caches[the_army.team]:
				self.caches[the_army.team]['army_list'] = []
			
			self.caches[the_army.team]['army_list'].append(
				'<option value="%s">%s</option>' % (the_army.name, the_army.name)
			)
		
		# Unit dropdown
		unit_dict = self.the_world.units()
		for unit_id, the_unit in unit_dict.items():
			if the_unit.team != 0 and the_unit.team not in true_team_list:
				continue
			
			if 'unit_list' not in self.caches[the_unit.team]:
				self.caches[the_unit.team]['unit_list'] = []
			
			self.caches[the_unit.team]['unit_list'].append(
				'<option value="%s">%s %s</option>' % (the_unit.name, the_unit.name, unit_rules.print_unit_cost(the_unit, the_world=self.the_world))
			)
		
		# List of _all_ units
		for t in true_team_list:
			self.caches[t]['all_unit_list'] = list(self.caches[t].get('unit_list', []))
			self.caches[t]['all_unit_list'].extend(self.caches[0]['unit_list'])
		
		# Squad dropdown
		squad_dict = self.the_world.squads()
		for squad_id, the_squad in squad_dict.items():
			if the_squad.team not in true_team_list: continue
			
			if 'squad_list' not in self.caches[the_squad.team]:
				self.caches[the_squad.team]['squad_list'] = []
			
			self.caches[the_squad.team]['squad_list'].append(
				'<option value="%s,%s">%s (%s)</option>' % (common.js_name(the_squad.name), common.js_name(army_dict[the_squad.army].name), the_squad.name, army_dict[the_squad.army].name)
			)
		
		# Operative city dropdown
		city_dict = self.the_world.cities()
		self.caches[0]['operative_city_dropdown'] = []
		for city_id, the_city in city_dict.items():
			if the_city.dead > 0: continue
			if not team_dict[the_city.team].active: continue
			
			self.caches[0]['operative_city_dropdown'].append(
				'<option value="{0}">{1} ({2})</option>'.format(common.js_name(the_city.name), the_city.name.replace('\\', ''), team_dict[the_city.team].name))
		
		# Spell list
		spell_dict = self.the_world.spells()
		for s, the_spell in spell_dict.items():
			if the_spell.name == "NONE": continue
			
			for t in true_team_list:
				if 'spell_list' not in self.caches[t]:
					self.caches[t]['spell_list'] = ['<option value="">&nbsp;</option>']
				
				the_team = team_dict[t]
				
				if s in the_team.spell_levels:
					if the_team.spell_levels[s] >= the_spell.max_level:
						if the_spell.max_level > 0:
							self.caches[t]['spell_list'].append(
								'<option value="" disabled="disabled">%s</option>' % (the_spell.name)
							)
							continue
					
					if the_team.spell_levels[s] > 0:
						points_needed = spell_rules.cost_for_next_level(None,
							the_spell,
							level=the_team.spell_levels[s],
							in_spell_points=True).get("Spell points")
					
						self.caches[t]['spell_list'].append(
							'<option value="%s">%s (%s: %s/%s)</option>' % (
								the_spell.name, the_spell.name, the_team.spell_levels[s], the_team.spell_points[s], points_needed
							)
						)
					else:
						self.caches[t]['spell_list'].append(
							'<option value="%s">%s (%s)</option>' % (
								the_spell.name, the_spell.name, the_team.spell_levels[s]
							)
						)
				else:
					self.caches[t]['spell_list'].append(
						'<option value="%s">%s</option>' % (
							the_spell.name, the_spell.name
						)
					)
		
		# Tech list
		tech_dict = self.the_world.techs()
		for s, the_tech in tech_dict.items():
			if the_tech.name == "NONE": continue
			
			for t in true_team_list:
				if 'tech_list' not in self.caches[t]:
					self.caches[t]['tech_list'] = ['<option value="">&nbsp;</option>']
				
				the_team = team_dict[t]
				
				if s in the_team.tech_levels:
					if the_team.tech_levels[s] >= the_tech.max_level:
						if the_tech.max_level > 0:
							self.caches[t]['tech_list'].append(
								'<option value="" disabled="disabled">%s</option>' % (the_tech.name)
							)
							continue
					
					if the_team.tech_levels[s] > 0:
						points_needed = tech_rules.cost_for_next_level(None,
							the_tech,
							level=the_team.tech_levels[s]).get("Tech points")
					
						self.caches[t]['tech_list'].append(
							'<option value="%s">%s (%s: %s/%s)</option>' % (
								the_tech.name, the_tech.name, the_team.tech_levels[s], the_team.tech_points[s], points_needed
							)
						)
					else:
						self.caches[t]['tech_list'].append(
							'<option value="%s">%s (%s)</option>' % (
								the_tech.name, the_tech.name, the_team.tech_levels[s]
							)
						)
				else:
					self.caches[t]['tech_list'].append(
						'<option value="%s">%s</option>' % (
							the_tech.name, the_tech.name
						)
					)
		
		# Team dropdown list
		for t in true_team_list:
			if 'team_list' not in self.caches[t]:
				self.caches[t]['team_list'] = ['<option value="">&nbsp;</option>']
				self.caches[t]['trade_list'] = ['<option value="">&nbsp;</option>']
			
			for team_id, the_team in team_dict.items():
				if t == team_id or the_team.dead or not the_team.active:
					continue
				
				if path_f.find_trade_route(self.the_world.cursor, the_team.id, t, the_world=self.the_world) != (-1, -1):
					self.caches[t]['trade_list'].append('<option value="%s">%s</option>' % (
						the_team.name, the_team.name)
					)
				
				self.caches[t]['team_list'].append('<option value="%s">%s</option>' % (the_team.name, the_team.name))
		
		# Monster list
		monster_list = []
		for k, v in self.the_world.monsters().items():
			monster_list.append('<option value="%s">%s</option>' % (v.name, v.name))
			
		
		for t in true_team_list:
			self.caches[t]['monster_list'] = monster_list
		
		# Research trade
		master_tier = spell.tiers.index("Master")
		for t in true_team_list:
			if 'spell_trade' not in self.caches[t]:
				self.caches[t]['spell_trade'] = ['<option value="">&nbsp;</option>']
			
			for s, l in team_dict[t].spell_levels.items():
				if l < 1: continue
				
				if spell_dict[s].tier == master_tier: continue
				if not spell_dict[s].tradable: continue
				if spell_dict[s].name == "NONE": continue
				
				self.caches[t]['spell_trade'].append(
					'<option value="%s">%s</option>' % (
						common.js_name(spell_dict[s].name), spell_dict[s].name
					)
				)
		
		for t in true_team_list:
			if 'tech_trade' not in self.caches[t]:
				self.caches[t]['tech_trade'] = ['<option value="">&nbsp;</option>']
			
			for s, l in team_dict[t].tech_levels.items():
				if l < 1: continue
				
				if not tech_dict[s].tradable: continue
				if tech_dict[s].name == "NONE": continue
				
				self.caches[t]['tech_trade'].append(
					'<option value="%s">%s</option>' % (
						common.js_name(tech_dict[s].name), tech_dict[s].name
					)
				)
		
		# Resources dropdowns
		for t in true_team_list:
			team_resource = team_dict[t].resources
			
			if 'boolean_resources' not in self.caches[t]:
				self.caches[t]['boolean_resources'] = ['<option value="">&nbsp;</option>']
				self.caches[t]['discrete_resources'] = ['<option value="">&nbsp;</option>']
			
			for i, r in enumerate(resource_list.data_list):
				if not r.tradable: continue
				
				if r.type == "boolean":
					if team_resource.value[i] < 1: continue
					self.caches[t]['boolean_resources'].append('<option value="%s">%s</option>' % (r.name, r.name))
		
				elif r.type == "discrete":
					if team_resource.value[i] < 1: continue
					self.caches[t]['discrete_resources'].append('<option value="%s">%s</option>' % (r.name, r.name))
		
		# Zip them down into strings
		true_team_list = list(true_team_list)
		true_team_list.append(0)
		for t in true_team_list:
			for k, v in self.caches[t].items():
				if type(v) == list or type(v) == tuple:
					self.caches[t][k] = "".join(v)
	
	def construction_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		city_dict = self.the_world.cities_from_team(the_team.id)
				
		output.append('''<div class="ti_section" id="construction_div">
		<h3 style="clear:both;"><a href="#" onclick="return false;">Construction &amp; Migration</a></h3>''')
		
		construction_java = []
		migration_java = []
		founding_java = []
		relocation_java = []
		
		# City blocks
		for city_id, the_city in city_dict.items():
			if the_city.dead > 0: continue
			
			if the_city.nomadic:
				additions = oh_f.nomadic_city_block(self, the_team, the_city)
				output.append(additions[0])
				load_java.append(additions[1])
				construction_java.append(additions[2])
			
			else:
				additions = oh_f.normal_city_block(self, the_team, the_city)
				output.append(additions[0])
				load_java.append(additions[1])
				migration_java.append(additions[2])
		
		# Founding
		additions = oh_f.founding_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		founding_java.append(additions[2])
		
		# Relocation
		additions = oh_f.relocation_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		relocation_java.append(additions[2])
		
		# Now to run
		run_java.append("""
		function on_change_cities ()
		{
			/* alert('construction'); */
			
			construction_orders = '';
			migration_orders = '';
			founding_orders = '';
			relocation_orders = '';
			supply_demand_orders = '';
			
			construction_materials = 0;
			%(construction_java)s
			
			%(migration_java)s
			
			%(founding_java)s
			
			relocation_materials = 0;
			%(relocation_java)s
			
			if (construction_orders != '')
			{
				construction_orders = '[o]Construction[/o]\\n' + construction_orders + '// Materials spent: ' + construction_materials + '\\n';
			}
			
			construction_orders += '\\n';
			
			if (migration_orders != '')
			{
				migration_orders = '[o]Migration[/o]\\n' + migration_orders;
			}
			
			migration_orders += '\\n';
			
			if (founding_orders != '')
			{
				founding_orders = '[o]Founding[/o]\\n' + founding_orders;
			}
			
			founding_orders += '\\n';
			
			if (relocation_orders != '')
			{
				relocation_orders = '[o]Relocation[/o]\\n' + relocation_orders + '// Materials spent: ' + relocation_materials + '\\n';
			}
			
			if (supply_demand_orders != '')
			{
				supply_demand_orders = '[o]City trade[/o]\\n' + supply_demand_orders + '\\n';
			}
			
			total_orders = construction_orders + migration_orders + founding_orders + relocation_orders + supply_demand_orders;
			$('#city_orders').text(total_orders);
		}
		""" % {
			"construction_java":	"".join(construction_java),
			"migration_java":		"".join(migration_java),
			"founding_java":		"".join(founding_java),
			"relocation_java":		"".join(relocation_java),
		})
		
		# Now call that function when we load up
		# load_java.append("on_change_cities();")
		
		output.append("""<strong>City orders</strong><br />
		<textarea id="city_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def military_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		# Armies
		# caches['unit_list'] = unit_q.get_units_from_team(the_team.id, special_units=True)[0]
		army_dict = self.the_world.armies_from_team(the_team.id)
		# caches['squad_list'] = squad_q.get_squads_from_team(the_team.id)[0]
		
		army_dict		= self.the_world.armies_from_team(the_team.id)
		# squad_dict		= self.the_world.squads_from_team(the_team.id)
		city_dict		= self.the_world.cities()
		
		# Some cached lists
		# Army dropdown
		
		output.append('''<div class="ti_section" id="military_div">
		<h3 style="clear:both;"><a href="#" onclick="return false;">Military management</a></h3>
		<div id="army_help" style="display:none;">
			<ul style="list-style-type: circle;margin-left:25px;">
				<li style="list-style-type: none;"><strong>Armies</strong></li>
				<li>If you don't want to rename an army you can simply leave the text field next to it alone, if the text field is blank then it will be skipped.</li>
				<li>The current location of the army is in the box, if you want to change it then put in new map coordinates. If you edit the location but then decide you want to leave the army where it is then simply leave the box blank.</li>
				<li>You can only delete an army if all the squads in it are empty, the box is displayed regardless so as to provide the option.</li>
				
				<li style="list-style-type: none;">&nbsp;</li>
				<li style="list-style-type: none;"><strong>Squads</strong></li>
				<li>The current name of the squad is displayed in the textbox, to rename the squad you simply enter a new name. If you forget what the name of the squad was and want to leave it as it was then simply leave the text box blank.</li>
				<li>Do <strong>not</strong> enter a negative number into the "amount to add" box, if you want to disband units then select the disband option to the right.</li>
				<li>Moving a squad to another army will not cost money though you shouldn't try to teleport squads across the world without the in game ability to do so ;)</li>
				<li>Moving men from one squad to another is also free though again, try to make sure that you move them to armies you can actually get to. If an army contains two squads of the same name and type then Rob will automatically merge them in the routine checks.</li>
			</ul>
		</div>
		<span id="army_help_link" style="cursor:pointer;" onclick="$('#army_help_link').hide();$('#army_help').show(500);">Show help</span>
		&nbsp;&nbsp;&nbsp;
		<a href="#" onclick="$('.army_order_box').show(500); return false;">Show all armies</a>
		&nbsp;&nbsp;&nbsp;
		<a href="#" onclick="$('.army_order_box').hide(500); return false;">Hide all armies</a>''')
		
		recruit_java = []
		
		
		# Normal armies
		for a, the_army in army_dict.items():
			if the_army.garrison > 0: continue
			
			additions = oh_f.army_block(self, the_team, the_army)
			output.append(additions[0])
			load_java.append(additions[1])
			recruit_java.append(additions[2])
		
		# Garrisons
		for a, the_army in army_dict.items():
			if the_army.garrison <= 0: continue
			
			# Skip garrisons of dead cities, they shouldn't have people in them anyway, right?...
			if the_army.garrison not in city_dict: continue
			if city_dict[the_army.garrison].dead: continue
			
			additions = oh_f.army_block(self, the_team, the_army)
			output.append(additions[0])
			load_java.append(additions[1])
			recruit_java.append(additions[2])
		
		# Relocate squads
		additions = oh_f.relocate_squad_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		# Merge squads
		additions = oh_f.merge_squad_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		# New armies
		additions = oh_f.new_armies(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		# New squads
		additions = oh_f.new_squads(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		output.append("""<strong>Military orders</strong><br />
		<textarea id="military_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		run_java.append("""
		function on_change_military ()
		{
			/* alert('army'); */
			
			total_orders = "";
			
			var army_relocate_orders = "";
			var army_delete_orders = "";
			var army_rename_orders = "";
			var army_recruit_orders = "";
			
			var squad_rename_orders = "";
			var squad_relocate_orders = "";
			var squad_delete_orders = "";
			
			var squad_merge_orders = "";
			
			%(recruit_java)s
			
			if (army_recruit_orders != '')
			{
				total_orders += "" + army_recruit_orders + "\\n\\n";
			}
			
			var new_army_text = $('#new_army_text').text();
			if (new_army_text != '')
			{
				total_orders += "" + new_army_text + "\\n\\n";
			}
			
			var new_squad_text = $('#new_squad_text').text();
			if (new_squad_text != '')
			{
				total_orders += "" + new_squad_text + "\\n\\n";
			}
			
			if (army_relocate_orders != "")
			{
				total_orders += "" + army_relocate_orders + "\\n\\n";
			}
			
			if (army_delete_orders != "")
			{
				total_orders += "" + army_delete_orders + "\\n\\n";
			}
			
			if (army_rename_orders != "")
			{
				total_orders += "" + army_rename_orders + "\\n\\n";
			}
			
			if (squad_rename_orders != "")
			{
				total_orders += "" + squad_rename_orders + "\\n\\n";
			}
			
			if (squad_relocate_orders != "")
			{
				total_orders += "" + squad_relocate_orders + "\\n\\n";
			}
			
			if (squad_merge_orders != "")
			{
				total_orders += "" + squad_merge_orders + "\\n\\n";
			}
			
			if (squad_delete_orders != "")
			{
				total_orders += "" + squad_delete_orders + "\\n\\n";
			}
			
			if (total_orders != "")
			{
				total_orders = "[o]Military[/o]\\n" + clean_text(total_orders);
			}
			
			$('#military_orders').text(total_orders);
		}""" % {
			"recruit_java": "".join(recruit_java),
		})
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def monsters_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append("""<div class="ti_section" id="monsters_div">""")
		
		output.append("""
		<table border="0" cellspacing="0" cellpadding="5">
			<tr>
				<td>Target monster:</td>
				<td>%(monster_dropdown)s</td>
			</tr>
			<tr>
				<td>Area:</td>
				<td><input type="text" id="monster_area" value="" /></td>
			</tr>
			<tr>
				<td>Men:</td>
				<td><input type="text" id="monster_men" value="" /></td>
			</tr>
			<tr>
				<td>Budget:</td>
				<td><input type="text" id="monster_budget" value="" /></td>
			</tr>
			<tr>
				<td>Army:</td>
				<td>%(army_dropdown)s</td>
			</tr>
		</table>
		<br />
		
		&nbsp;&nbsp;&nbsp;Capture instructions:<br />
		<textarea id="monster_text" rows="8" style="width:99%%;"></textarea>
		
		
		<br /><br />
		<strong>Monster orders</strong><br />
		<textarea id="monster_orders" style="width:100%%;" rows="7"></textarea>
		""" % {
			"monster_dropdown": """<select id="monster_target">
				%s
			</select>
			""" % self.caches[the_team.id].get('monster_list', ''),
			
			"army_dropdown":	"""<select id="monster_army">
				%s
			</select>
			""" % self.caches[the_team.id].get('army_list', ''),
		})
		
		run_java.append("""
		function on_change_monsters ()
		{
			var monster_orders = "";
			
			var target = $('#monster_target').val();
			var area = $('#monster_area').val();
			var men = $('#monster_men').val();
			var budget = $('#monster_budget').val();
			var army = $('#monster_army').val();
			var orders = $('#monster_text').val();
			
			if (area != "" && men != "" && budget != "" && orders != "")
			{
				monster_orders = "[o]Monsters[/o]\\n";
				monster_orders += "Map area: " + area + "\\n";
				monster_orders += "Target: " + target + "\\n";
				monster_orders += "Men: " + men + "\\n";
				monster_orders += "Budget: " + budget + "\\n";
				monster_orders += "Army: " + army + "\\n";
				monster_orders += "\\n" + orders + "\\n";
			}
			
			total_orders = monster_orders;
			$('#monster_orders').text(total_orders);
		}
		""")
		
		output.append("</div>")
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def research_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		mundane_java	= []
		magical_java	= []
		
		output.append("""<div class="ti_section" id="research_div">""")
		
		# Mundane
		additions = oh_f.mundane_research(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		mundane_java.append(additions[2])
		
		output.append("<br /><br />")
		
		# Magical
		additions = oh_f.magical_research(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		magical_java.append(additions[2])
		
		output.append("""
			<br /><br />
			<strong>Research orders</strong><br />
			<textarea id="research_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		run_java.append("""
		function on_change_research ()
		{
			/* alert('research'); */
			
			var research_orders = "";
			
			%(mundane)s
			%(magical)s
			
			if (research_orders != "")
			{
				research_orders = "[o]Research[/o]" + research_orders;
			}
			
			total_orders = research_orders;
			$('#research_orders').text(total_orders);
		}""" % {
			"mundane":	"".join(mundane_java),
			"magical":	"".join(magical_java),
		})
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def operative_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('<div class="ti_section" id="operative_div">')
		
		output.append('''
			<h3 style="clear:both;"><a href="#" onclick="return false;">Operative movement</a></h3>
			<div class="order_box">
				To move a cell use the line,.
				<br />
				
				<textarea rows="3" cols="50">[o]Operatives[/o]
Move cell: &lt;name&gt; to &lt;city&gt;</textarea>
				<br />
				
				There is no automated form for this as it caused a huge bloated file and very slow order creation. If you try to recruit a new cell with the same name as another then it will automatically try to reinforce the existing one.
			</div>
			<br /><br />
			''')
		
		recruit_java = []
		
		# Operative reinforcement
		additions = oh_f.reinforce_ops(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		# Operative recruitment
		additions = oh_f.recruit_ops(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		recruit_java.append(additions[2])
		
		output.append("""
			<br /><br />
			<strong>Operative orders</strong><br />
			<textarea id="operative_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		run_java.append("""
		function on_change_operatives ()
		{
			var operative_orders = "";
			var recruitment_orders = "";
			
			%(recruit_java)s
			
			operative_orders = recruitment_orders;
			
			if (operative_orders != "")
			{
				operative_orders = "[o]Operatives[/o]" + operative_orders;
			}
			total_orders = operative_orders;
			$('#operative_orders').text(total_orders);
		}""" % {
			"recruit_java":	"".join(recruit_java),
		})
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def trade_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('<div class="ti_section" id="trade_div">')
		
		research_java = []
		supply_java = []
		resource_java = []
		
		# Research
		additions = oh_f.research_trade_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		research_java.append(additions[2])
		
		# Supply trades
		additions = oh_f.supply_trade_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		supply_java.append(additions[2])
		
		# Resource trades
		additions = oh_f.resource_trade_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		resource_java.append(additions[2])
		
		run_java.append("""
		function on_change_trade ()
		{
			/* alert('trades'); */
	
			total_orders = "";
			trade_orders = "";
		
			%(research_java)s
			%(supply_java)s
			%(resource_java)s
		
			if (trade_orders != "")
			{
				trade_orders = "[o]Trades[/o]" + trade_orders;
			}
		
			total_orders = trade_orders;
		
			$('#trade_orders').text(total_orders);
		}""" % {
			"research_java":	"".join(research_java),
			"supply_java":		"".join(supply_java),
			"resource_java":	"".join(resource_java),
		})
		
		output.append("""<strong>Trade orders</strong><br />
		<textarea id="trade_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		return "".join(output), "".join(load_java), "".join(run_java)
		
	def diplomacy_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('<div class="ti_section" id="diplomacy_div">')
		
		borders_java = []
		
		# Borders
		additions = oh_f.relations_block(self, the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		borders_java.append(additions[2])
		
		run_java.append("""
		function on_change_diplomacy ()
		{
			/* alert('diplomacy'); */
			
			total_orders = "";
			diplomacy_orders = "";
			border_orders = "";
			tax_orders = "";
			
			%(borders_java)s
			
			total_orders = border_orders;
			
			if (tax_orders != "")
			{
				total_orders += "\\n" + tax_orders;
			}
			
			if (total_orders != "")
			{
				total_orders = "[o]Diplomacy[/o]" + total_orders;
			}
			
			$('#diplomacy_orders').text(total_orders);
		}""" % {
			"borders_java":	"".join(borders_java),
		})
		
		output.append("""<strong>Diplomacy orders</strong><br />
		<textarea id="diplomacy_orders" style="width:100%;" rows="7"></textarea>
		</div>""")
		
		return "".join(output), "".join(load_java), "".join(run_java)
	
	def advanced_block(self, the_team):
		output, load_java, run_java = [], [], []
		
		output.append('<div class="ti_section" id="advanced_div">This section is designed to hold more advanced and less frequently used order types.<br /><br />')
		
		output.append("""
		<h3 style="clear:both;"><a href="#" onclick="return false;">Re-equipping</a></h3>
		This needs to be placed under a military heading such as <strong>[o]Military[/o]</strong>.
		<br /><br />
		
		<span class="stitle">Adding</span><br />
		<textarea rows="3" style="width:99%;">Add equipment: {unit name}, {item 1}, {item 2}
Add equipment: Swordsmen, Short sword</textarea>
		<br /><br />
		
		<span class="stitle">Removing</span><br />
		<textarea rows="3" style="width:99%;">Remove equipment: {unit name}, {item 1}, {item 2}
Remove equipment: Swordsmen, Spear</textarea>
		<br /><br />
		
		<span class="stitle">Changing / Replacing</span><br />
		Note that here you must list <strong>all</strong> of the equipment for the unit, not just what you are changing. This order is useful if you want to both add and remove equipment so that you only need to retrain the unit once.
		<textarea rows="3" style="width:99%;">New equipment: {unit name}, {item 1}, {item 2}
New equipment: Swordsmen, Short sword, Good training</textarea>
		<br /><br />
		
		""")
		
		output.append('</div>')
		
		return "".join(output), "".join(load_java), "".join(run_java)
		
		
	def command_block(self, the_team):
		output, load_java, run_java = [], [], []

		output.append('<div class="ti_section" id="command_div">This section is designed to hold special commands for test orders, these are not for normal orders but can allow you to get more information through Rob Requests. All commands found here should be headed by a <strong>[o]Rob command[/o]</strong> heading.<br /><br />')

		output.append("""
		<h3 style="clear:both;"><a href="#" onclick="return false;">Assumption</a></h3>
		Rob can assume that you have traded for a given supply and run all further orders in the test orders with that in mind.
		<textarea rows="4" style="width:99%;">Assume supply: Iron
Assume supply: Stone
Assume supply: Wood</textarea>
		<br /><br />
		
		Additionally you can assume a certain amount of a normal resource like so:
		<textarea rows="4" style="width:99%;">Assume resource: 500 Materials
Assume resource: 500 Ship points
Assume resource: 100 Balloon points</textarea>
		<br /><br />
		
		<h3 style="clear:both;"><a href="#" onclick="return false;">Paths</a></h3>
		Rob can give information on travel times using the pathing system used for colonisation and founding orders. It'll output several travel times for you. As long as there are an even number of number pairs then Rob will try to work out the path.
		<textarea rows="3" style="width:99%;">Path: 170, 1269, 405, 1332// North west Humyti to Tishrashi desert
Path: 273, 1605, 536, 1537, 186, 1264</textarea>
		<br /><br />
		
		<h3 style="clear:both;"><a href="#" onclick="return false;">Overbudget</a></h3>
		By default Rob will try to prevent you going overbudget on materials, using the overbudget command you can disable this. Be careful with this one because when overbudget you generally cannot conduct wars and civilian morale falls fast.
		<textarea rows="3" style="width:99%;">Enable: overbudget
Disable: overbudget</textarea>
		<br /><br />
		
		<h3 style="clear:both;"><a href="#" onclick="return false;">New unit</a></h3>
		You can add units to your TI through rob requests and orders themselves. Be sure to test the order through rob requests and pay attention to the instructions to confirm the adding of the unit. The new unit command needs to be in a <strong>[o]Military[/o]</strong> block.
		<textarea rows="3" style="width:99%;">New unit: {unit name}, {list of equipment}
New unit: Elite swordsmen, Short sword, Elite training, Leather suit</textarea>
		<br /><br />
		
		""")

		output.append('</div>')

		return "".join(output), "".join(load_java), "".join(run_java)
	
	def make_oh(self, team_id):
		the_team = self.the_world.teams()[team_id]
		
		tabs = """
		<div id="tabs" style="border-bottom: 3px solid #EEE; height: 30px;">
			<div class="ti_tab" id="construction_tab" onclick="switch_to('construction');">
				Cities
			</div>
			<div class="ti_tab" id="military_tab" onclick="switch_to('military');">
				Military
			</div>
			<!--
			<div class="ti_tab" id="monsters_tab" onclick="switch_to('monsters');">
				Monsters
			</div>
			-->
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
		
		output = [tabs]
		
		loader_src = '../images/other/loading.gif'
		
		output.append("""
		<div id='loading_div' style='text-align:center;padding-top:20px;'>
			Loading...
			<br /><br />
			<img src='%s'/>
		</div>""" % loader_src)
		
		load_java	= []
		run_java	= []
		
		# CONSTRUCTION - 111
		additions = self.construction_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# MILITARY - 498
		additions = self.military_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# MONSTERS
		# additions = self.monsters_block(the_team)
		# output.append(additions[0])
		# load_java.append(additions[1])
		# run_java.append(additions[2])
		
		# RESEARCH - 52
		additions = self.research_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# OPERATIVES - 221
		additions = self.operative_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# TRADE - 19
		additions = self.trade_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
		# DIPLOMACY - 12
		additions = self.diplomacy_block(the_team)
		output.append(additions[0])
		load_java.append(additions[1])
		run_java.append(additions[2])
		
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
		
		# bytes = len("".join(output))
		# print("")
		# print("<span style='background-color:#FFF;'>Bytes: %s</span>" % format(round(bytes/1000), ','))
		
		# Setup
		output.append(common.onload("on_load_setup();"))
		
		#	JAVASCRIPT
		#------------------------
		javascript = oh_f.javascript("".join(load_java), "".join(run_java))
		
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
	
		output.insert(0, common.headers(title_name="%s order creation form" % the_team.name, css=css, javascript=javascript, local_path=self.local_path))
	
		tabs = tabs.replace('id="', 'id="bottom_')
	
		output.append("""
		%s
		<br /><hr />
		<div style="padding: 5px;">
			<input type="button" id="build_button" value="Create orders" onclick="build_orders();"/><br /><br />
			<strong>Complete orders</strong><br />
			<textarea id="final_output" style="width:100%%;" rows="20"></textarea>
		</div>""" % tabs)
	
		output.append(common.footers())
		
		# Compress some output
		final_output = "".join(output)#.replace("	", "").replace("  ", " ").replace("	 ", " ")
		return final_output
	
	
