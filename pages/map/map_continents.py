from pages import common
from data import mapper_q

continent_list, continent_dict = mapper_q.get_continents()

output = []

output.append("""
<table border="0" cellspacing="0" cellpadding="5">
	<tr class="row2">
		<th>Continent</th>
		<th colspan="2">Location</th>
		<th>&nbsp;</th>
	</tr>
""")

count = -1
for c in continent_list:
	count += 1
	
	the_cont = continent_dict[c]
	
	output.append("""
	<tr class="row%(count)s">
		<td>%(name)s</td>
		<td>%(x)s</td>
		<td>%(y)s</td>
		<td>&nbsp;</td>
	</tr>
	""" % {
		"count":	count%2,
		"name":		common.doubleclick_text("map_continents", "name", the_cont.id, the_cont.name, size=10),
		"x":		common.doubleclick_text("map_continents", "x", the_cont.id, the_cont.x, size=4),
		"y":		common.doubleclick_text("map_continents", "y", the_cont.id, the_cont.y, size=4),
	})

count += 1
output.append("""
	<tr class="row%(count)s">
		<form action="exec.py" method="post" accept-charset="utf-8">
			<input type="hidden" name="mode" value="add_continent" />
			<td style="padding:1px;"><input type="text" name="name" id="name" value="" /></td>
			<td style="padding:1px;" colspan="2"><input type="text" name="location" value="" /></td>
			<td><input type="submit" value="Add" /></td>
		</form>
		%(onload)s
	</tr>
""" % {
	"count":	count%2,
	"onload":	common.onload("$('#name').focus();"),
})


output.append("</table>")

print("".join(output))