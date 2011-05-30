import re
from classes import order_block

def todo_order(the_line, groups, debug=False):
	results = order_block.default_line_results(the_line)
	
	results['input_response'] = None
	results['results'] = [the_line.content]
	results['success'] = True
	results['debug'] = []
	return results

class Unknown_block (order_block.Order_block):
	background_colour	= "#FFEEEE"
	border_colour		= "#AA0000"
	
	functions = (
		(re.compile(r'(?P<content>.*)'),	todo_order),
	)
	
	def __init__(self):
		super(Unknown_block, self).__init__()
		self.manual_handle = True
	
	def execute(self):
		super(Unknown_block, self).execute()
		self.results[0] = "[o]%s[/o] - TODO" % self.title_name
		self.input_response = ["These orders will be passed on to Teifion to handle manually. If this is not the intention then you can try altering the title of the orders."]