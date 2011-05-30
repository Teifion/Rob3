import re
from lists import resource_list

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

def get_id(res_name):
	for r in resource_list.data_list:
		if r.name == res_name:
			return r.id
	
	# Can't find it, try using .lower()
	for r in resource_list.data_list:
		if r.name.lower() == res_name.lower():
			return r.id

def convert_cost_string(costs, my_resources={}):
	"""Returns a dictionary version of the string"""
	if costs == "":
		return {}, []
	
	output = {}
	swappables = []
	for i, r in resource_list.data_dict.items():
		result = re_cache["Initial_search_{0}".format(r.name)].search(costs)
		if result == None: continue
		
		output[i] = result.groups()[0]
	
	# Now flatten out conditionals
	not_flat = {}
	
	for k, v in output.items():
		if re_cache['Amount'].search(str(v)) == None:
			not_flat[k] = v
		else:
			output[k] = float(v)
	
	# Are there any swappables?
	if re_cache['Swappable_start'].search(costs) != None:
		results = re_cache['Swappable_block'].findall(costs)
		
		for r in results:
			resource_0_id = -1
			resource_1_id = -1
			
			for res_id, the_res in resource_list.data_dict.items():
				if r[0].lower() == the_res.name.lower():
					resource_0_id = res_id
				
				if r[1].lower() == the_res.name.lower():
					resource_1_id = res_id
			
			if resource_0_id > 0 and resource_1_id > 0:
				swappables.append((resource_0_id,resource_1_id))
	
	# If no conditionals then skip the next bit
	if len(not_flat) == 0: return output, swappables
	
	for r, v in not_flat.items():
		if r in my_resources and my_resources[r] > 0:
			result = re.search(r'^(.*)([-+/*=])(.*)$', v)
			# results = re_cache['Swappable_operands'].search(v)# For some resaon this isn't working
			
			if result == None:
				output[r] = 0
				continue
			
			res_id		= get_id(result.groups()[0])
			operator	= result.groups()[1]
			amount		= result.groups()[2]
			
			# Type them because they're strings at the moment
			output[res_id] = float(output[res_id])
			
			amount = float(amount)
			
			# print output[res_id], operator, amount, "="			
			if res_id in output:
				if operator == "+":		output[res_id] += amount
				elif operator == "-":	output[res_id] -= amount
				elif operator == "*":	output[res_id] *= amount
				elif operator == "/":	output[res_id] /= amount
				elif operator == "=":	output[res_id] = amount
			
			# print output[res_id], "<br />"
			
			output[r] = 0
		else:
			output[r] = 0
	
	return output, swappables

def make_cost_string(costs_input, costs_swappables=[]):
	"""In goes a dictionary, out comes a string"""
	if costs_input.__class__ == dict and costs_swappables.__class__ == list:
		costs		= costs_input
		costs_swap	= costs_swappables
	else:#costs_input.__class__ == res_dict.Res_dict:
		costs		= costs_input.value
		costs_swap	= costs_input.swappables
	# else:
	# 	raise Exception("No ability to handle a costs_input.__class__ of %s" % costs_input.__class__)
	
	output = []
	
	for k, v in costs.items():
		if v == int(v):
			value = int(v)
		else:
			value = float(v)
		
		# Don't want it clogged up with a load of empty resources
		if v != 0:
			output.append("{0}:{1}".format(resource_list.data_dict[k].name, value))
	
	# If they're sending us a whole Res_dict then we can look for swappables too
	for s in costs_swap:
		output.append("({0}:{1})".format(resource_list.data_dict[s[0]].name, resource_list.data_dict[s[1]].name))
	
	return ",".join(output)

def discrete_only(input_value):
	"""Input a cost_string, dict or Res_dict and you get back a Res_dict with only discrete values"""
	if input_value.__class__ == dict:
		costs = input_value
	else:
		costs = input_value.value
	
	for k, r in resource_list.data_dict.items():
		if k not in costs: continue
		
		if r.type != "discrete":
			del costs[k]
	
	return costs