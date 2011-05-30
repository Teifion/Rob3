from classes import res_dict

def get_cost(as_dict={}, **kwargs):
	if as_dict == {}:
		as_dict = kwargs
	
	# Input checking
	if as_dict['Stealth'] < 1:
		raise Exception("Stealth is less than 1")
	if as_dict['Integration'] < 1:
		raise Exception("Integration is less than 1")
	if as_dict['Observation'] < 1:
		raise Exception("Observation is less than 1")
	if as_dict['Size'] < 1:
		raise Exception("Size is less than 1")
	
	material_cost = (as_dict['Stealth'] * as_dict['Integration'])
	material_cost += (as_dict['Sedition'] + as_dict['Sabotage'] + as_dict['Assassination'] + 1) * as_dict['Observation']
	material_cost *= as_dict['Size']
	
	return res_dict.Res_dict("Materials:%s" % material_cost)

def get_reinforce_cost(the_op, amount = 1):
	as_dict = {}
	as_dict['Stealth'] = the_op.stealth
	as_dict['Observation'] = the_op.observation
	as_dict['Integration'] = the_op.integration
	as_dict['Sedition'] = the_op.sedition
	as_dict['Sabotage'] = the_op.sabotage
	as_dict['Assassination'] = the_op.assassination
	as_dict['Size'] = amount
	
	return get_cost(as_dict)