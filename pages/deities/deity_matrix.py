import math
from pages import common
from queries import deity_q

page_data = {
	"Title":	"Deity like/dislike matrix",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	deity_dict = deity_q.get_all_deities(cursor)
	
	output.append('''<table border="0" cellspacing="0" cellpadding="5">
		<tr>
			<td>&nbsp;</td>''')
	
	for d, the_deity in deity_dict.items():
		output.append("<td>{}</td>".format(the_deity.sname))
	output.append("</tr>")
	
	for d, the_deity in deity_dict.items():
		output.append("<tr><td>{}</td>".format(the_deity.name))
		for d2, the_deity2 in deity_dict.items():
			if d == d2:
				output.append("<td style='background-color:#AAA;'>&nbsp;</td>")
			else:
				if the_deity2.name in the_deity.likes:
					output.append("<td style='background-color:#0A0;color:#FFF;'>Like</td>")
				elif the_deity2.name in the_deity.dislikes:
					output.append("<td style='background-color:#FA0;color:#FFF;'>Disl</td>")
				elif the_deity2.name in the_deity.hates:
					output.append("<td style='background-color:#A00;color:#FFF;'>Hate</td>")
				else:
					output.append("<td>&nbsp;</td>")
		output.append("</tr>")
	
	output.append('</table>')
	
	return "".join(output)