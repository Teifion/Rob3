from pages import common
from data_classes import evolution
from queries import evolution_q

page_data = {
	"Title":	"Team list",
	"Admin":	True,
}

def main(cursor):
	evolution_dict = evolution_q.get_all_evolutions(cursor)
	
	output = []
	
	output_dict = {}
	for i in range(0,5):
		output_dict[i] = []
	
	for d, the_evolution in evolution_dict.items():
		if the_evolution.category == 3: continue
		if the_evolution.name == "VOID": continue
		
		# self.add_field("cost_per_level",	"int")
		# self.add_field("max_level",			"int")
		# self.add_field("min_level",			"int")
		# self.add_field("category",			"int")
		# self.add_field("physical_change",	"double")
		# self.add_field("combat_relevant",	"bool")
		# self.add_field("description",		"blob")
	
		output_dict[the_evolution.category].append("""<strong><a class="clear_link" id="%(js_name)s" href="#%(js_name)s">%(evo_name)s</a></strong>
		&nbsp;&nbsp;&nbsp;
		Max level: %(max_level)s
		&nbsp;&nbsp;&nbsp;
		Min level: %(min_level)s
		&nbsp;&nbsp;&nbsp;
		Cost: %(cost)s
		<br />
		%(description)s
		<br /><br />""" % {
			"js_name":		common.js_name(the_evolution.name),
			"evo_name":		the_evolution.name,
		
			"max_level":	the_evolution.max_level,
			"min_level":	the_evolution.min_level,
			"cost":			the_evolution.cost_per_level,
			"description":	the_evolution.description,
		})

	for i in range(0,5):
		if output_dict[i] != []:
			output.append("""<h3><a id="%s" href="#%s">%s</a></h3>""" % (
				common.js_name(evolution.categories[i]),
				common.js_name(evolution.categories[i]),
				evolution.categories[i],
			))
		
			output.append("".join(output_dict[i]))
	
	return "".join(output)