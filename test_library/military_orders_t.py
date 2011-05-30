import unittest
from classes import res_dict
from orders import military_o
from test_library import orders_t_lib

class Military_squad_orders(unittest.TestCase):
	test_targets = [
		military_o.Military_block,
		military_o.move_squad_order
	]
	w = orders_t_lib.dummy_world()
	
	def test_move_squad_order(self):
		data = {
			"block": military_o.Military_block(
				the_world = orders_t_lib.dummy_world(),
				team = self.w.teams_lookup()['SArkalians'],
				title_name = "Military",
				content = """Move squad: My first squad from My first army to My second army""",
			),
			
			"results": [
				"My first squad moved from My first army to My second army",
			],
			
			"queries":			[
				"-- Moving squad 'My first squad' (ID:0) from army 'My first army' (ID:0) to army 'My second army' (ID:1)",
				"UPDATE squads SET army = '1' WHERE id = 0;"
			],
			"input_response":	[],
			"foreign_results":	{},
			"foreign_queries":	{},
			"foreign_costs":	{},
		}
		
		data['block'].the_world._teams[self.w.teams_lookup()['SArkalians']].resources = res_dict.Res_dict("Materials:10")
		orders_t_lib.test_orders(self, data)
	

class Military_army_orders(unittest.TestCase):
	pass