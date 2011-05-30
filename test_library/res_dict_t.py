import unittest
from classes import res_dict
from functions import res_dict_f
from lists import resource_list

def strip_dict(input_dict):
	strip_list = []
	for k, v in input_dict.items():
		if v == 0 or v == "":
			strip_list.append(k)
			
	for s in strip_list:
		del(input_dict[s])
	return input_dict

class Res_dict_class(unittest.TestCase):
	test_targets = [
		res_dict.Res_dict,
		res_dict.lineno,
		
		res_dict.Res_dict.__add__,
		res_dict.Res_dict.__sub__,
		res_dict.Res_dict.__mul__,
		res_dict.Res_dict.__truediv__,
		
		res_dict.Res_dict.flatten,
		res_dict.Res_dict.affordable,
		res_dict.Res_dict.as_string,
	]
	
	round_trip_values = [
		# From string
		("Materials:10", {0:10}, "10 Materials"),
		("Materials:10.33", {0:10.33}, "10.33 Materials"),
		("Materials:0.112", {0:0.112}, "0.112 Materials"),
		("Materials:6,Spell points:100", {0:6, 3:100}, "6 Materials, 100 Spell points"),
		
		# From dict
		({0:0.112}, {0:0.112}, "0.112 Materials"),
		({1:19.1}, {1:19.1}, "19.1 Food"),
		({6:19}, {6:19}, "19 Stone"),
	]
	
	# One long string...
	long_str = []
	long_dict = {}
	clean_str = []
	for i, r in resource_list.data_dict.items():
		long_str.append("{0}:{1}".format(r.name, 1))
		long_dict[i] = 1
		clean_str.append("{1} {0}".format(r.name, 1))
	
	round_trip_values.append((",".join(long_str), long_dict, ", ".join(clean_str)))
	
	def test_round_trip(self):
		for input_value, output_dict, output_string in self.round_trip_values:
			c = res_dict.Res_dict(input_value)
			
			dict_result = c.value
			str_result	= str(c)
			
			self.assertEqual(dict_result, output_dict)
			self.assertEqual(str_result, output_string)
	
	def test_string_input(self):
		vals = (
			("", {}),
			("", {}),
		)
		
		for input_value, expected in vals:
			r = res_dict.Res_dict(input_value)
			self.assertEqual(expected, r.value)
	
	
	# Maths time!
	# op = {	"+" : lambda a,b: a+b,
	# 		"-" : lambda a,b: a-b,
	# 		"*" : lambda a,b: a*b,
	# 		"/" : lambda a,b: a/b
	# }
	
	math_sets = (
		# +
		({0:10},		{0:7},		"+",	{0:17}),
		({0:10,1:10},	{0:7,2:10},	"+",	{0:17,1:10,2:10}),
		
		# -
		({0:10},		{0:10},		"-",	{}),
		({1:10},		{0:11,2:5},	"-",	{0:-11,1:10,2:-5}),
		
		# *
		({0:10},		{0:10},		"*",	{0:100}),
		({1:10,2:10},	{0:10,1:10},"*",	{1:100}),
		
		({1:10,2:10},	1,			"*",	{1:10,2:10}),
		({1:10,2:10},	2,			"*",	{1:20,2:20}),
		({1:10,2:10},	-1,			"*",	{1:-10,2:-10}),
		({1:10,2:10},	2.5,		"*",	{1:25,2:25}),
		
		# /
		({0:10},		{0:10},		"/",	{0:1}),
		({1:10},		{0:11,2:5},	"/",	{1:10}),
		
		({1:10,2:10},	1,			"/",	{1:10,2:10}),
		({1:10,2:10},	2,			"/",	{1:5,2:5}),
		({1:10,2:10},	-1,			"/",	{1:-10,2:-10}),
		({1:10,2:10},	2.5,		"/",	{1:4,2:4}),
	)
	
	def test_maths(self):
		for first_value, second_value, op, expected_answer in self.math_sets:
			a = res_dict.Res_dict(first_value)
			if second_value.__class__ == dict:
				b = res_dict.Res_dict(second_value)
			else:
				b = second_value
			
			c = res_dict.operator[op](a, b)
			self.assertEqual(strip_dict(c.value), expected_answer)
	
	flatten_tests = (
		("Materials:10",							{},		{0:10}),
		("Materials:40,Iron:Materials/4",			{},		{0:40}),
		("Materials:40,Iron:Materials/4",			{5:1},	{0:10}),
		("Materials:40,Food:40,Iron:Materials/4",	{5:1},	{0:10,1:40}),
	)
	
	def test_flatten(self):
		for input_value, host_resources, expected_answer in self.flatten_tests:
			c = res_dict.Res_dict(input_value)
			c.flatten(host_resources)
			
			self.assertEqual(strip_dict(c.value), expected_answer)
			
	
	affordable_values = (
			# Standard
			("Materials:10", "Materials:10", [], (True, {0:10}), {}),
			("Materials:10", "Materials:50", [], (True, {0:10}), {0:40}),
			("Materials:50", "Materials:50", [], (True, {0:50}), {}),
			("Materials:50", "Materials:10", [], (False, {}), {}),
			
			# Conditional
			("Materials:40,Iron:Materials/4", "Materials:10", [], (False, {}), {}),
			("Materials:80,Iron:Materials/4", "Materials:20,Iron:1", [], (True, {0:20}), {5:1}),
			
			# Swappable
			("Balloon points:10,(Ship points:Balloon points)", "Ship points:10", [], (True, {4:10}), {}),
			("Destruction points:100,(Spell points:Destruction points)",
				"Destruction points:20,Spell points:20", [], (False, {}), {}),
			
	)
	
	def test_affordable(self):
		for cost, host, overbudget, expected_result, remainder in self.affordable_values:
			host_dict = res_dict.Res_dict(host)
			host_dict.overbudget = overbudget
			
			# Now check it's affordable
			found_affordable, found_cost = host_dict.affordable(cost, overbudget, verbose=False)
			expected_affordable, expected_cost_final = expected_result
			self.assertEqual(expected_affordable, found_affordable)
			
			if not found_affordable and expected_cost_final != {}:
				raise Exception("""Item is not affordable yet still has an expected cost. The expected cost should be {{}} as all that is returned is an empty dictionary.
	Cost: {0}
	Availiable: {1}
	Expected (final): {2}""".format(cost, availiable_resources, expected_cost_final))
			
			# Check costs
			self.assertEqual(expected_cost_final, strip_dict(found_cost))
			
			# Now to find out what remains
			if found_affordable:
				# print("")
				# print(strip_dict(host_dict.value))
				host_dict = host_dict - cost
				# print(strip_dict(host_dict.value))
				self.assertEqual(remainder, strip_dict(host_dict.value))
		
	
