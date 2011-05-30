from pages import common
from data_classes import deity
from queries import deity_q

page_data = {
	"Title":	"Deity information",
	"Admin":	True,
}

def main(cursor):
	name = common.get_val('deity', '')
	
	the_deity = deity_q.get_one_deity(cursor, name)
	
	output = ['<h1><a href="#top">%s</a></h1>' % the_deity.name]

	if the_deity.likes != "": the_deity.likes = "<strong>Likes:</strong> %s<br />" % the_deity.likes
	if the_deity.dislikes != "": the_deity.dislikes = "<strong>Dislikes:</strong> %s<br />" % the_deity.dislikes
	if the_deity.hates != "": the_deity.hates = "<strong>Hates:</strong> %s<br />" % the_deity.hates

	output.append("""
	%(summary)s<br />
	<br />

	<strong>Major favour:</strong> %(major)s<br />
	<strong>Minor favour:</strong> %(minor)s<br />
	<strong>Negative favour:</strong> %(negative)s<br />
	<strong>Favour bonus:</strong> %(bonus)s<br />

	%(likes)s
	%(dislikes)s
	%(hates)s
	<br />

	<strong>Grand objective:</strong> %(objective)s<br />
	<strong>Divine intervention:</strong> %(di)s<br />
	<br /><br />

	<strong>Backstory:</strong>
	%(backstory)s
	""" % {
		"summary":		the_deity.summary,
	
		"major":		the_deity.major,
		"minor":		the_deity.minor,
		"negative":		the_deity.negative,
		"bonus":		the_deity.bonus,
	
		"objective":	the_deity.objective,
		"di":			the_deity.di,
	
		"likes":		the_deity.likes,
		"dislikes":		the_deity.dislikes,
		"hates":		the_deity.hates,
	
		"backstory":	the_deity.backstory.replace("\n", "<br />").replace("  ", "&nbsp;&nbsp;"),
	})
	
	return "".join(output)