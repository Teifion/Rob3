from pages import common
from queries import trait_q
from data_classes import trait

def evolution_list(cursor, cat=None, page=None, **kwargs):
	trait_dict = trait_q.get_all_traits(cursor)
	
	output = []
	output_dict = {}
	
	for trait_id, the_trait in trait_dict.items():
		if not the_trait.show: continue
		if the_trait.category not in output_dict:
			output_dict[the_trait.category] = []
		
		output_dict[the_trait.category].append("""
		<strong><a class="clear_link" id="%(js_name)s" href="#%(js_name)s">%(trait_name)s</a></strong>
		<br />
		%(description)s
		<br /><br />""" % {
			"js_name":		common.js_name(the_trait.name),
			"trait_name":	the_trait.name,
			"description":	the_trait.description,
		})
	
	for i in range(len(trait.categories)):
		if output_dict[i] != []:
			output.append("""<h3><a id="%s" href="#%s">%s</a></h3>""" % (
				common.js_name(trait.categories[i]),
				common.js_name(trait.categories[i]),
				trait.categories[i],
			))
		
			output.append("".join(output_dict[i]))
	
	return "".join(output)