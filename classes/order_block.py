import re
import database
from classes import res_dict
from pages import common

regexs = {
	"comment_strip":	re.compile(r'//.*$'),
}

def default_line_results(the_line, base_failure=""):
	r = default_multi_line_results(base_failure)
	
	r['input_response']	= "[b]No input_response defined[/b] (%s)" % the_line.content[0:40]
	r["debug"]			= ["Line: %s" % the_line.content]
	r["the_line"]		= the_line
	
	return r

def default_multi_line_results(base_failure=""):
	if base_failure != "":
		base_failure = "%s " % base_failure
	
	return {
		"success":			False,
		"failure":			False,
		"cost":				"",#res_dict.Res_dict(),
		"line_cache":		{},
		"input_response":	"[b]No input_response defined[/b]",
		"results":			[],
		"queries":			[],
		"foreign_queries":	{},
		"foreign_results":	{},
		"foreign_costs":	{},
		"the_line":			None,
		"base_failure":		base_failure,
		"debug":			[],
	}

def success(results):
	the_line = results['the_line']
	
	if the_line == None:
		if str(results['cost']) == "":
			results['input_response'] = "[pos]Success[/pos], no cost"
		else:
			results['input_response'] = "[pos]Success[/pos], cost: %s" % (the_line.content, str(results['cost']))
	else:
		if str(results['cost']) == "":
			results['input_response'] = "%s - [pos]Success[/pos], no cost" % (the_line.content)
		else:
			results['input_response'] = "%s - [pos]Success[/pos], cost: %s" % (the_line.content, str(results['cost']))
	
	results['success'] = True
	return results

def fail(results, reason):
	the_line = results['the_line']
	
	if the_line == None:
		return fail_multi_line(results, reason)
	
	results['input_response'] = "%s - [neg]Failure[/neg], %s" % (the_line.content, reason)
	results['results'] = ["%s%s" % (results['base_failure'], reason)]
	results['success'] = False
	results['failure'] = True
	return results

def fail_multi_line(results, reason):
	results['input_response'] = "[neg]Failure[/neg], %s" % (reason)
	results['results'] = ["%s%s" % (results['base_failure'], reason)]
	results['success'] = False
	results['failure'] = True
	return results

def fail_cost(results, verbose=False):
	the_line = results['the_line']
	
	verbose_str = ""# Used for testing
	if verbose:
		verbose_str = " %s" % str(the_line.the_world._teams[the_line.block.team].resources)
	
	results['input_response'] = "%s - [neg]Too expensive (%s)[/neg]%s" % (the_line.content, str(results['cost']), verbose_str)
	results['results'] = ["%s - [neg]Too expensive (%s)[/neg]%s" % (the_line.content, str(results['cost']), verbose_str)]
	results['success'] = False
	return results

priorities = (	
	"Assertion",
	"Trade",
	"Leader",
	"Normal",
)

class Order_block (object):
	"""Building block of order blocks"""
	background_colour	= "#FFFFFF"
	border_colour		= "#000000"
	
	functions			= ()
	
	def __init__(self, the_world=None, team=-1, title_name="", content=""):
		super(Order_block, self).__init__()
		
		self.msn_order = False
		self.manual_handle = False
		
		# Refs
		self.title_name = title_name
		self.content	= content
		self.the_world	= the_world
		self.team		= team
		self.post		= None
		self.priority	= "Normal"
		self.handled	= False
		
		# Calced
		self.lines				= []
		self.line_cache			= {}# Used to take info from one line for the next
		self.failures			= []# List specifically for listing failures
		
		self.cost				= res_dict.Res_dict()
		self.results			= []# Stuff that's posted to the forum
		self.queries			= []# Stuff that runs through the database
		self.input_response		= []# Echoes back orders with notes
		self.foreign_results	= {}# Results to send to other teams
		self.foreign_queries	= {}# Queries to run for other teams
		self.foreign_costs		= {}# Costs for other teams
		
		self.debug				= []# Debug output
		
		# Not sure about this one...
		self.spy_actions		= []
		
		self.always_debug = False
	
	def affordable(self, cost):
		the_team = self.the_world._teams[self.team]
		
		afford, true_cost = the_team.resources.affordable(cost, the_team.overbudget)
		
		if afford:
			return true_cost
		else:
			return False
	
	def setup(self, msn_order=False):
		"""Splits up the lines ready for reading"""
		order_lines = self.content.split("\n")
		self.msn_order = msn_order
		self.lines = []
		
		for l, the_line in enumerate(order_lines):
			the_line = self.common_mistakes(the_line).strip()
			
			if the_line != "":
				the_line = regexs['comment_strip'].sub('', the_line)
			
			if the_line == "":
				self.lines.append(Empty_line())
			else:
				new_line = Line(self, self.the_world)
				new_line.content = the_line
				self.lines.append(new_line)
		
		self.debug = ["[o]%s[/o]\n" % self.title_name]
		self.failures = ["[o]%s[/o]" % self.title_name]
		
	def common_mistakes(self, text):
		return text
	
	# Implimented by sub-class
	def _execute(self, the_line):
		self.handled = True
		
		if the_line.content == "":
			self.input_response.append("")
			self.results.extend([""])
			return
		
		found_regex = False
		for regex, proof_func in self.functions:
			if found_regex: break
			
			temp_content = the_line.content
			
			# Enable debug mode on an order by starting the line with an exclamation mark
			debug = False
			if the_line.content[0] == "!":
				debug = True
				temp_content = the_line.content[1:len(the_line.content)]
			
			# Leave the above block in because it removes debug lines
			if self.always_debug:
				debug = True
			
			result = regex.search(temp_content)
			
			if result == None:
				continue
			
			found_regex = True
			the_line.content = temp_content
			
			line_result = proof_func(the_line, result.groupdict(), debug)
			
			# DEBUG STUFF
			# if the_line.the_world._cities[974].buildings != {'0':None}:
			# 	print(the_line.content, ",", the_line.block.title_name, ",", the_line.block.team)
			# if the_line.the_world._cities[974].buildings == {'0':None}:
			# 	print("\nChanged!")
			# 	print(the_line.content, ",", the_line.block.title_name, ",", the_line.block.team)
			# 	the_line.the_world.cursor.execute("ROLLBACK")
			# 	the_line.the_world.cursor.execute("ROLLBACK")
			# 	exit()
			
			if debug:
				if line_result['success']:
					line_result['debug'].insert(1, "Succeeded")
				self.debug.append("\n".join(line_result['debug']))
			
			if line_result['input_response'] != None:
				self.input_response.append(line_result['input_response'])
			
			if line_result['results'] != None:
				self.results.extend(line_result['results'])
			
			if line_result['success'] == True:
				self.cost += line_result['cost']
				
				self.queries.extend(line_result['queries'])
				
				for k, v in line_result['foreign_results'].items():
					if k not in self.foreign_results: self.foreign_results[k] = []
					self.foreign_results[k].extend(v)
				
				for k, v in line_result['foreign_queries'].items():
					if k not in self.foreign_queries: self.foreign_queries[k] = []
					self.foreign_queries[k].extend(v)
				
				for k, v in line_result['foreign_costs'].items():
					if k not in self.foreign_costs: self.foreign_costs[k] = res_dict.Res_dict()
					self.foreign_costs[k] += v
			else:
				self.failures.extend(line_result['results'])
			
			self.line_cache = line_result['line_cache']
			
		if not found_regex and the_line.content != "":
			self.input_response.append("%s - [neg]No match found[/neg]" % the_line.content)
			self.results.extend(["%s - [neg]No match found[/neg]" % the_line.content])
	
	def execute(self):
		for l in self.lines:
			try:
				self._execute(l)
			except Exception as e:
				print(l.content)
				raise
		
		if self.cost.value == {}:
			self.results.insert(0, "[o]%s[/o]" % (self.title_name))
		else:
			self.results.insert(0, "[o]%s[/o] - Cost: %s" % (self.title_name, str(self.cost)))

class Multiline_order_block (Order_block):
	# def __init__(self, the_world=None, team=-1, title_name="", content=""):
	# 	super(Multiline_order_block, self).__init__(the_world, team, title_name, content)
	# 	
	# 	self.msn_order = False
	# 	self.manual_handle = False
	# 	
	# 	# Refs
	# 	self.title_name = title_name
	# 	self.content	= content
	# 	self.the_world	= the_world
	# 	self.team		= team
	# 	self.post		= None
	# 	self.priority	= "Normal"
	# 	self.handled	= False
	# 	
	# 	# Calced
	# 	self.lines				= []
	# 	self.line_cache			= {}# Used to take info from one line for the next
	# 	self.failures			= []# List specifically for listing failures
	# 	
	# 	self.cost				= res_dict.Res_dict()
	# 	self.results			= []# Stuff that's posted to the forum
	# 	self.queries			= []# Stuff that runs through the database
	# 	self.input_response		= []# Echoes back orders with notes
	# 	self.foreign_results	= {}# Results to send to other teams
	# 	self.foreign_queries	= {}# Queries to run for other teams
	# 	self.foreign_costs		= {}# Costs for other teams
	# 	
	# 	self.debug				= []# Debug output
	# 	
	# 	# Not sure about this one...
	# 	self.spy_actions		= []
	# 	
	# 	self.always_debug = False
	
	# def affordable(self, cost):
	# 	the_team = self.the_world._teams[self.team]
	# 	
	# 	afford, true_cost = the_team.resources.affordable(cost, the_team.overbudget)
	# 	
	# 	if afford:
	# 		return true_cost
	# 	else:
	# 		return False
	
	def setup(self, msn_order=False):
		"""Splits up the lines ready for reading"""
		order_lines = self.content.split("\n")
		self.msn_order = msn_order
		self.lines = []
		
		for l, the_line in enumerate(order_lines):
			the_line = self.common_mistakes(the_line).strip()
			self.lines.append(the_line)
		
		self.debug = ["[o]%s[/o]\n" % self.title_name]
		self.failures = ["[o]%s[/o]" % self.title_name]
	
	# def common_mistakes(self, text):
	# 	return text
	
	# Multiline executes as one
	def _execute(self):
		self.handled = True
		
		# Enable debug mode on an order by starting the line with an exclamation mark
		debug = False
		if self.lines[0][0] == "!":
			debug = True
			self.lines[0] = self.lines[0][1:len(self.lines[0])]
		
		# Leave the above block in because it removes debug lines
		if self.always_debug:
			debug = True
		
		result = self.ml_check()
		
		if debug:
			if result['success']:
				result['debug'].insert(1, "Succeeded")
			self.debug.append("\n".join(result['debug']))
		
		if result['input_response'] != None:
			self.input_response.append(result['input_response'])
		
		if result['results'] != None:
			self.results.extend(result['results'])
		
		if result['success'] == True:
			self.cost += result['cost']
			
			self.queries.extend(result['queries'])
			
			for k, v in result['foreign_results'].items():
				if k not in self.foreign_results: self.foreign_results[k] = []
				self.foreign_results[k].extend(v)
			
			for k, v in result['foreign_queries'].items():
				if k not in self.foreign_queries: self.foreign_queries[k] = []
				self.foreign_queries[k].extend(v)
			
			for k, v in result['foreign_costs'].items():
				if k not in self.foreign_costs: self.foreign_costs[k] = res_dict.Res_dict()
				self.foreign_costs[k] += v
		else:
			self.failures.extend(result['results'])
		
		self.line_cache = result['line_cache']
	
	def approve(self, team, title, content, turn=-1):
		if turn < 1:
			turn = common.current_turn()
		
		return ["""INSERT INTO interactive_orders (team, turn, title, content) values ({team}, {turn}, '{title}', '{content}');""".format(
			team = team,
			turn = turn,
			title = title,
			content = database.escape(content),
		)]
	
	def execute(self):
		self._execute()
	
class Interactive_order_block (Multiline_order_block):
	def __init__(self, *args, **kwargs):
		super(Interactive_order_block, self).__init__(*args, **kwargs)
		self.interactivity = {}
		self.page = None
	
	def try_query(self, *queries):
		if self.the_world.cursor == None:
			raise Exception("Interactive_order_block.the_world.cursor is None")
		
		for q in queries:
			if type(q) == list or type(q) == tuple:
				self.try_query_list(*q)
			else:
				self.the_world.cursor.execute("BEGIN")
				try:
					self.cursor.execute(q)
				except Exception as e:
					self.the_world.cursor.execute("ROLLBACK")
				else:
					self.the_world.cursor.execute("COMMIT")
	
	def try_query_list(self, *queries):
		for q in queries:
			self.the_world.cursor.execute("BEGIN")
			try:
				self.the_world.cursor.execute(q)
			except Exception as e:
				self.the_world.cursor.execute("ROLLBACK")
			else:
				self.the_world.cursor.execute("COMMIT")
	
	def ml_check(self, *args, **kwargs):
		raise Exception("Not implimented, args: %s, kwargs: %s" % (args, kwargs))
	
	def interactive_setup(self, *args, **kwargs):
		raise Exception("Not implimented, args: %s, kwargs: %s" % (args, kwargs))
	
	def interactive_execution(self, *args, **kwargs):
		raise Exception("Not implimented, args: %s, kwargs: %s" % (args, kwargs))


class Line (object):
	def __init__(self, block, the_world):
		super(Line, self).__init__()
		
		self.content			= ""
		
		self.block				= block
		self.the_world			= the_world
	
	def try_query(self, *queries):
		for q in queries:
			if type(q) == list or type(q) == tuple:
				self.try_query_list(*q)
			else:
				self.the_world.cursor.execute("BEGIN")
				try:
						self.the_world.cursor.execute(q)
				except Exception as e:
					self.the_world.cursor.execute("ROLLBACK")
				else:
					self.the_world.cursor.execute("COMMIT")
	
	# Try some queries, ignore exceptions
	def try_query_list(self, *queries):
		for q in queries:
			self.the_world.cursor.execute("BEGIN")
			try:
				self.the_world.cursor.execute(q)
			except Exception as e:
				self.the_world.cursor.execute("ROLLBACK")
			else:
				self.the_world.cursor.execute("COMMIT")


class Empty_line (Line):
	def __init__(self):
		super(Empty_line, self).__init__(None, None)
