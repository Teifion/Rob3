from lore import pages
import string
from queries import monster_q

def monster_info(cursor, cat, page, **kwargs):
	monster_name = kwargs.get("name", string.capwords(page))
	the_monster = monster_q.get_one_monster(cursor, monster_name)
	
	if the_monster == None:
		raise Exception("Could not find monster %s" % monster_name)
	
	source = pages.get_html(cursor, cat, page, level="public")
	output = []
	
	output.append("""
	<h1><a href="#top">{name}</a></h1>
	<!--Suggested men: {men}<br /> -->
	Approximate budget: {budget} materials<br />
	<!-- Habitat: {terrain}<br /> -->
	Expected amount: {amount}<br />
	<br />
	
	<strong>Eyewitness account:</strong><br />
	""".format(
		name = the_monster.name,
		budget = int((the_monster.min_budget * 2 + the_monster.max_budget)/3),
		men = int((the_monster.min_men * 2 + the_monster.max_men)/3),
		amount = int(the_monster.max_amount / 2),
		terrain = "",
	))
	
	output.append(source)
	
	return "".join(output)
	# return _wrap_template("".join(output), string.capwords(cat))