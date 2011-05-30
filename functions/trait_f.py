from queries import trait_q

def trait_option_list(cursor, remove_list=[], default=0):
	output = []
	
	trait_dict = trait_q.get_all_traits(cursor)
	
	for trait_id, the_trait in trait_dict.items():
		if trait_id in remove_list: continue
		if the_trait.name == "VOID": continue
		
		if trait_id == default:
			output.append("<option value='{0}' selected='selected'>{1}</option>".format(trait_id, the_trait.name))
		else:
			output.append("<option value='{0}'>{1}</option>".format(trait_id, the_trait.name))
	
	return "".join(output)