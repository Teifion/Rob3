from pages import common
from data_classes import spell
from queries import spell_q

page_data = {
	"Title":	"Spell summary",
	"Admin":	True,
}

def main(cursor):
	spell_dict = spell_q._spell_query(cursor, orderby="category DESC, tier ASC, name")
	
	output = ['''<table border="0" cellspacing="0" cellpadding="5">
		<tr class="row2">
			<th>Lore</th>
			<th>Low</th>
			<th>Mid</th>
			<th>High</th>
			<th>Master</th>
		</tr>
	''']
	
	last_tier = -1
	last_lore = -1
	count = -1
	for s, the_spell in spell_dict.items():
		# New row
		if last_lore != the_spell.category:
			last_tier = 0
			count += 1
			if last_lore != -1:
				output.append("</tr>")
			
			last_lore = the_spell.category
			
			output.append("""
			<tr class="row%(count)s">
				<td><strong>%(name)s</strong></td>
				<td>
			""" % {
				"count":	count%2,
				"name":		spell.categories[the_spell.category]
			})
	
		# Now column
		if last_tier != the_spell.tier:
			last_tier = the_spell.tier
			output.append("</td><td>")
	
		category_page = spell.categories[the_spell.category].lower()
		url_name = the_spell.name.replace(' ', '%20')
	
		output.append("<a class='clear_link' href='%s.php#%s'>%s</a><br />" % (category_page, url_name, the_spell.name))
	
	output.append("</tr></table>")
	return "".join(output)