import re
from decimal import Decimal
import database
from lists import resource_list
from functions import res_dict_f
import inspect

def lineno():
	"""Returns the current line number in our program."""
	return inspect.currentframe().f_back.f_lineno

operator = {
		"+": lambda a,b: a+b,
		"-": lambda a,b: a-b,
		"*": lambda a,b: a*b,
		"/": lambda a,b: a/b,
		"=": lambda a,b: b,
}

re_cache = {
	"Amount":				re.compile(r"^-?[0-9]"),
	"Swappable_start":		re.compile(r"\("),
	"Swappable_block":		re.compile(r"\((.*?):(.*?)\)"),
	"Swappable_operands":	re.compile(r'^(.*)([-+/*=])(.*)$'),
}

for r in resource_list.data_list:
	re_cache["Initial_search_{0}".format(r.name)] = re.compile(
		r"{0}:(-?[^,]*?)(,|\(|$)".format(r.name),
		re.IGNORECASE)

class Res_dict (object):
	"""docstring for Res_dict"""
	def __init__(self, input_value=""):
		super(Res_dict, self).__init__()
		self.value = {}
		self.swappables = []
		self.conditionals = {}
		self.overbudget = []
		
		# Now we build our value
		if type(input_value) == str:
			if input_value == "":
				return
			
			for i, r in resource_list.data_dict.items():
				result = re_cache["Initial_search_{0}".format(r.name)].search(input_value)
				# print(input_value)
				if result == None: continue
				
				res = result.groups()[0]
				self.value[i] = res
				
				# Now get the conditionals
				self.conditionals = {}
				
				for k, v in self.value.items():
					if re_cache['Amount'].search(str(v)) == None:
						self.conditionals[k] = v
						self.value[k] = 0
					else:
						self.value[k] = float(v)
			
			# Are there any swappables?
			if re_cache['Swappable_start'].search(input_value) != None:
				results = re_cache['Swappable_block'].findall(input_value)
				
				for r in results:
					resource_0_id = -1
					resource_1_id = -1
					
					for res_id, the_res in resource_list.data_dict.items():
						if r[0].lower() == the_res.name.lower():
							resource_0_id = res_id
						
						if r[1].lower() == the_res.name.lower():
							resource_1_id = res_id
					
					if resource_0_id > 0 and resource_1_id > 0:
						self.swappables.append((resource_0_id,resource_1_id))
		
		elif type(input_value) == dict:
			self.value = input_value
		
		elif type(input_value) == Res_dict:
			self.value			= input_value.value
			self.swappables		= input_value.swappables
			self.conditionals	= input_value.conditionals
			self.overbudget		= input_value.overbudget
		
		else:
			raise Exception("Unable to handle input class of {0}".format(input_value.__class__))
	
	def __str__(self):
		return self.as_string()
	
	def __repr__(self):
		return self.as_string()
		return self.value
	
	# http://docs.python.org/3.1/reference/datamodel.html#basic-customization
	# object.__lt__(self, other)
	# object.__le__(self, other)
	# object.__eq__(self, other)
	def __eq__(self, other):
		if type(other) != Res_dict:
			raise TypeError("Cannot compare with non Res_dict")
		
		return self.as_string() == other.as_string()
		
	# object.__ne__(self, other)
	# object.__gt__(self, other)
	# object.__ge__(self, other)
	
	def __get_cost_value(self, other, allow_numbers=False):
		"""Returns a Cost_dict for the math functions
		
		This function handles things such as flatteing etc"""
		
		if type(other) in (str, dict):
			return Res_dict(other)
		
		elif type(other) == Res_dict:
			other.flatten(self.value)
			return other
		
		elif type(other) in (int, float):
			if not allow_numbers:
				raise TypeError
			else:
				return other
		
	def __add__(self, other):
		other = self.__get_cost_value(other)
		new_value = Res_dict()
		for i, r in resource_list.data_dict.items():
			if i not in self.value and i not in other.value:
				continue
			
			try:
				new_value.value[i] = self.value.get(i, 0) + other.value.get(i, 0)
			except Exception as e:
				print("")
				print("self.value: %s<br />" % str(self.value))
				print("other.value: %s<br /><br />" % str(other.value))
				
				print("self.value.get: %s<br />" % str(self.value.get(i, 0)))
				print("other.value.get: %s<br />" % str(other.value.get(i, 0)))
				raise
			
		
		return new_value
	
	def __sub__(self, other):
		# First we make sure it's in the right format
		other = self.__get_cost_value(other)
		
		# Now we get the true cost via the affordable function
		# If it's not affordable then we don't bother with swappables
		afford, real_cost = self.affordable(other)
		if afford:
			other = Res_dict(real_cost)
		
		new_value = Res_dict()
		for i, r in resource_list.data_dict.items():
			if i in self.value or i in other.value:
				new_value.value[i] = self.value.get(i, 0) - other.value.get(i, 0)
		
		return new_value
	
	def __mul__(self, other):
		other = self.__get_cost_value(other, True)
		new_value = Res_dict()
		for i, r in resource_list.data_dict.items():
			if type(other) == Res_dict:
				if i in self.value or i in other.value:
					new_value.value[i] = self.value.get(i, 0) * other.value.get(i, 0)
			
			elif type(other) in (int, float):
				if i in self.value:
					new_value.value[i] = self.value[i] * other
				
		return new_value
	
	def __truediv__(self, other):
		if type(other) == int:
			if other == 0:
				raise ZeroDivisionError()
		
		other = self.__get_cost_value(other, True)
		new_value = Res_dict()
		for i, r in resource_list.data_dict.items():
			if type(other) == Res_dict:
				if i in self.value and i in other.value:
					new_value.value[i] = self.value.get(i, 0) / other.value.get(i, 1)
				elif i in self.value:
					new_value.value[i] = self.value[i]
					
			elif other.__class__ == int or other.__class__ == float:
				if i in self.value:
					new_value.value[i] = self.value[i] / other
			
		return new_value
	
	# Allows us to access this as if it were a dictionary
	def __getitem__(self, key):
		if type(key) == str:
			return self.value[res_dict_f.get_id(key)]
		else:
			return self.value[key]
	
	def set(self, key, value):
		if type(key) == str:
			key = res_dict_f.get_id(key)
		self.value[key] = value
	
	def get(self, key, default = 0):
		if type(key) == str:
			key = res_dict_f.get_id(key)
		
		try:
			v = self.value.get(key, default)
		except Exception as e:
			raise
		
		# Cast it to an int if we can for printing purposes
		if type(v) == float:
			if v == int(v):
				return int(v)
		
		# We have it, yay!
		return v
	
	def flatten(self, host_resources="", reset_conditionals=True):
		"""Runs through all the conditionals and turns them into constant values
		
		host_resources is the resources of whatever will be buying this, conditionals rely on this
		"""
		
		if host_resources.__class__ != Res_dict:
			host = Res_dict(host_resources)
		else:
			host = host_resources
		
		for r, v in self.conditionals.items():
			result = re_cache['Swappable_operands'].search(v)
			
			if result == None: continue
			
			res_id		= res_dict_f.get_id(result.groups()[0])
			op			= result.groups()[1]
			amount		= float(result.groups()[2])
			
			# If the host has it then we'll apply the change
			if host.value.get(r, 0) > 0:
				self.value[res_id] = operator[op](self.value[res_id], amount)
		
		# This stops it applying them more than once by mistake
		if reset_conditionals: self.conditionals = {}
		 
		return self
	
	def invert(self):
		for k, v in self.value.items():
			self.value[k] = -v
		
		return self
	
	def affordable(self, cost, overbudget_list=None, verbose=False):
		"""Checks to see if you can pay the price
		
		other is a Res_dict"""
		
		# Ensure that our input is what we want
		if type(cost) != Res_dict: cost = Res_dict(cost)
		cost.flatten(self.value)
		
		# Turn overbudget into a list of integers
		if overbudget_list == None:
			overbudget_list = self.overbudget
		
		overbudget = []
		for o in overbudget_list:
			overbudget.append(res_dict_f.get_id(o))
			
		cant_afford = []
		actual_cost = {}
		
		if verbose:
			print("")
			print("%d: Cost = %s" % (lineno(), cost.value))
			print("%d: Host: %s" % (lineno(), self.value))
		
		for k, r in resource_list.data_dict.items():
			# Set this to 0 so that we don't need to worry about it later
			actual_cost[k] = 0
			
			# Are we not being billed for this or billed zero?
			if cost.get(k, 0) <= 0:
				actual_cost[k] = cost.get(k, 0)
				continue
			
			# If you are allowed to be overbudget on this resource we won't even check it
			if k in overbudget:
				if verbose:
					if self.value[k] > cost.value[k]:
						print("%d: Allowed overbudget on %s" % (lineno(), r.name))
					else:
						print("%d: Can afford %s, can go overbudget" % (lineno(), r.name))
				actual_cost[k] = cost.value[k]
				continue
			
			# We set this to zero to stop null-exception errors
			if k not in self.value:
				self.value[k] = 0
			
			# We can afford this!
			if cost.value[k] <= self.value[k]:
				if verbose:
					print("%d: Can afford %s (%s < %s)" % (lineno(), r.name, cost.value[k], self.value[k]))
				actual_cost[k] += cost.value[k]
				continue
			
			# We can't afford this :(
			if self.value[k] < cost.value[k]:
				
				if verbose:
					print("%d: Can't afford %s" % (lineno(), r.name))
				
				# All is not lost, it may be swappable!
				replacement_k = -1
				
				# Work out amounts now to save duplicating lots of lines of code
				if k not in actual_cost: actual_cost[k] = 0
				
				amount_needed = cost.value[k] - self.value[k]
				k_amount_used = cost.value[k] - amount_needed
				
				# We can't afford this outright, it may however be swappable
				for s in cost.swappables:
					temp_k = -1
					
					# Is it in this swappable block?
					if k not in s:			continue
					
					# Have we already handled it?
					if replacement_k > 0:	continue
					
					# What are we swapping with? One of them is k, the other is it's swap partner
					if s[0] == k:	temp_k = s[1]
					else:			temp_k = s[0]
					
					# temp_k is now what we're looking to swap with
					
					# First lets see if we can go overbudget on temp_k
					if temp_k in overbudget or resource_list.data_list[temp_k].name in overbudget:
						if verbose:
							print("%d: Going overbudget on %s, found in overbudget" % (lineno(),
								resource_list.data_list[temp_k].name))
						
						replacement_k = temp_k
					
					# Failing that we could just see if we can afford it
					elif self.value.get(temp_k, 0) >= amount_needed:
						if verbose:
							print("%d: Going overbudget on %s, found in we had enough spare" % (lineno(),
								resource_list.data_list[temp_k].name))
						
						replacement_k = temp_k
						
					# If we've found a replacement, we need to alter the costs
					if replacement_k > 0:
						if replacement_k not in actual_cost:
							actual_cost[replacement_k] = 0
						
						actual_cost[replacement_k] += amount_needed
						actual_cost[k] += k_amount_used
						continue
				
				# We've gotten this far, that means no solution was found
				if replacement_k < 1:
					if verbose:
						print("%d: Could not find a swap for %s, could not afford cost" % (lineno(),
							resource_list.data_list[k].name))
					return False, {}
		
		return True, actual_cost
	
	def as_string(self):
		"""A sensical string such as: X Materials, Y Food"""
		results = []
		
		for k, r in resource_list.data_dict.items():
			if k not in self.value: continue
			if self.value[k] == 0: continue
			
			if self.value[k] == int(self.value[k]):
				results.append("{0:d} {1}".format(int(self.value[k]), r.name))
			else:
				results.append("{0} {1}".format(self.value[k], r.name))
		
		return ", ".join(results)
	
	def as_db_string(self):
		"""A sensical string such as: X Materials, Y Food"""
		results = []
		
		for k, r in resource_list.data_dict.items():
			if k not in self.value: continue
			if self.value[k] == 0: continue
			
			if self.value[k] == int(self.value[k]):
				results.append("{0}:{1:d}".format(r.name, int(self.value[k])))
			else:
				results.append("{0}:{1}".format(r.name, self.value[k]))
		
		return ", ".join(results)
	
	def discrete(self):
		"""Removes all non-discrete values from the res_dict"""
		for k, r in resource_list.data_dict.items():
			if k not in self.value: continue
			
			if r.type != "discrete":
				del self.value[k]
		
		return self.value
	
	def make_set_queries(self, team_id):
		"""Make queries for setting these resources as the team's new resources"""
		results = []
		
		for k, r in enumerate(resource_list.data_list):
			if k not in self.value: continue
			
			# query = "INSERT INTO team_resources (resource, team, amount) values (%s, %s, 0);" % (k, team_id)
			# try: database.cursor.execute(query)
			# except Exception, e: pass
			
			results.append("UPDATE team_resources SET amount = %s WHERE team = %s AND resource = %s;" % (self.value[k], team_id, k))
		
		return results
	

