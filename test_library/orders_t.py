import unittest
from classes import res_dict
from orders import construction_o
from test_library import orders_t_lib

# class Unicode_orders(unittest.TestCase):
# 	test_targets = []
# 	
# 	w = orders_t_lib.dummy_world()
# 	
# 	def test_construction(self):
# 		data = {
# 			"block": construction_o.Construction_block(
# 				the_world = orders_t_lib.dummy_world(),
# 				team = self.w.teams_lookup()['Úñíçódéß'],
# 				title_name = "Construction",
# 				content = """Build University at Úñíçódé""",
# 			),
# 			
# 			"results": [
# 				"Úñíçódé is 25% of the way through it's University",
# 			],
# 			
# 			"queries":			[],
# 			"input_response":	[],
# 			"foreign_results":	{},
# 			"foreign_queries":	{},
# 			"foreign_costs":	{},
# 		}
# 		
# 		data['block'].the_world._teams[self.w.teams_lookup()['Úñíçódéß']].resources = res_dict.Res_dict("Materials:10")
# 		orders_t_lib.test_orders(self, data)
# 	
