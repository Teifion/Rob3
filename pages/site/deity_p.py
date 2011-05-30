from lore import pages
import string
from queries import deity_q

def deity_info(cursor, cat, page, **kwargs):
	deity_name = kwargs.get("name", string.capwords(page))
	the_deity = deity_q.get_one_deity(cursor, deity_name)
	
	if the_deity == None:
		raise Exception("Could not find deity %s" % deity_name)
	
	source = pages.get_html(cursor, cat, page, level="public")
	output = []
	
	output.append("""
	<h1><a href="#top">{name}</a></h1>
	{summary}<br />
	<br />
	
	<strong>Major favour:</strong> {major}<br />
	<strong>Minor favour:</strong> {minor}<br />
	<strong>Negative favour:</strong> {negative}<br />
	<strong>Favour bonus:</strong> {bonus}<br />
	
	<strong>Dislikes:</strong> {dislikes}<br />
	<strong>Hates:</strong> {hates}<br />
	<br />
	
	<strong>Grand objective:</strong> {objective}<br />
	<strong>Divine intervention:</strong> {di}<br />
	<br /><br />
	
	<strong>Backstory:</strong><br />
	""".format(
		name = the_deity.name,
		summary = the_deity.summary,
		major = the_deity.major,
		minor = the_deity.minor,
		negative = the_deity.negative,
		bonus = the_deity.bonus,
		dislikes = the_deity.dislikes,
		hates = the_deity.hates,
		objective = the_deity.objective,
		di = the_deity.di,
	))
	output.append(source)
	
	return "".join(output)
	# return _wrap_template("".join(output), string.capwords(cat))