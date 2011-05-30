import unittest
from classes import res_dict
from orders import research_o
from test_library import orders_t_lib

class Research_orders(unittest.TestCase):
	test_targets = [
		research_o.research_order, research_o.research_tech, research_o.research_spell,
		research_o.Research_block,
	]
	w = orders_t_lib.dummy_world()
	
	def test_basic_research(self):
		data = {
			"block": research_o.Research_block(
				the_world = orders_t_lib.dummy_world(),
				team = self.w.teams_lookup()['SArkalians'],
				title_name = "Research",
				content = """Economy
Fireball""",
			),
			
			"results": [
				"Economy was researched to 100 out of 160 points towards level 1",
				"Fireball is now level 1",
			],
			
			"queries":			[
				'-- Tech research Economy to 0.100 for team:0',
				'UPDATE team_techs SET level = 0, points = 100 WHERE team = 0 AND tech = 1;',
				'-- Spell research Fireball to 1.0 for team:0',
				'UPDATE team_spells SET level = 1, points = 0 WHERE team = 0 AND spell = 40;',
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[self.w.teams_lookup()['SArkalians']].resources = res_dict.Res_dict("Materials:100,Tech points:100,Spell points:100")
		orders_t_lib.test_orders(self, data)
	
	def test_research_comment_issue(self):
		data = {
			"block": research_o.Research_block(
				the_world = orders_t_lib.dummy_world(),
				team = self.w.teams_lookup()['SArkalians'],
				title_name = "Research",
				content = """Economy //Comment
Fireball //Comment""",
			),

			"results": [
				"Economy was researched to 100 out of 160 points towards level 1",
				"Fireball is now level 1",
			],

			"queries":			[
				'-- Tech research Economy to 0.100 for team:0',
				'UPDATE team_techs SET level = 0, points = 100 WHERE team = 0 AND tech = 1;',
				'-- Spell research Fireball to 1.0 for team:0',
				'UPDATE team_spells SET level = 1, points = 0 WHERE team = 0 AND spell = 40;',
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}

		data['block'].the_world._teams[self.w.teams_lookup()['SArkalians']].resources = res_dict.Res_dict("Materials:100,Tech points:100,Spell points:100")
		orders_t_lib.test_orders(self, data)