from pages import common
from data_classes import deity
from queries import deity_q

page_data = {
	"Title":	"Deity summary",
	"Admin":	True,
}

def main(cursor):
	deity_dict = deity_q.get_all_deities(cursor)

	output = ["""
	<h1><a href="#top">The pantheon</a></h1>
	Click the name of a deity to see their favour requirements, grand objective and backstory.
	<br /><br />
	"""]

	for d, the_deity in deity_dict.items():
		output.append("""<strong><a class="clear_link" href="%s.php">%s</a></strong>: %s
		<br /><br />""" % (
			the_deity.name.lower().replace(' ', ''),
			the_deity.name,
			the_deity.summary,
		))
	
	return "".join(output)