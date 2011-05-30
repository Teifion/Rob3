from data import mapper
from data import resource
from rules import map_data
from pages import common

grid_size = int(common.get_val('grid_size', 0))
value_list = common.get_val('list', 0)
grid_size = 10

the_map = mapper.Map_maker()
the_map.mouseover = 0
the_map.grid_size = grid_size

the_map.top		= map_data.dimensions['top']
the_map.bottom	= map_data.dimensions['bottom']
the_map.left	= map_data.dimensions['left']
the_map.right	= map_data.dimensions['right']

map_output = the_map.map_value(value_list)

onclick_js = """
var map_x = parseInt(document.getElementById('labelHideX').innerHTML);
var map_y = parseInt(document.getElementById('labelHideY').innerHTML);

use_map_xy(map_x, map_y);"""

map_width	= (the_map.right - the_map.left) * 2.5
map_height	= (the_map.bottom - the_map.top) * 2.5

map_path = "http://localhost/WoA/map/images/theMap.jpg"
jquery = "%s%s" % (common.data['media_path'], "jquery-1.3.2.min.js")
transparent_path = "http://localhost/WoA/map/images/trans75.png"


css = mapper.CSS.replace('{W}', str(map_width)).replace('{H}', str(map_height)).replace('{P}', map_path).replace('{T}', transparent_path)

# Option box
res_dict = resource.get_resources_dict()
resource_select_list = ["<option value='&nbsp;'>No resource</option>"]
for i,r in res_dict.items():
	resource_select_list.append("<option value='%s'>%s</option>" % (r, r))

resource_select = "".join(resource_select_list)

output = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<title>World of Arl Map</title>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<script src="%(jquery)s" type="text/javascript" charset="utf-8"></script>
		%(mapper_css)s
	</head>
	<body>
		<div class="theMap">
			<div style="background-image: url('http://localhost/rob2/images/grid_%(pgrid_size)s.png'); position: absolute; top:0px; left:0px; width:%(map_width)spx; height:%(map_height)spx;" onclick="alert('The background recieved an onclick, this is probably not meant to happen.');">
		</div>
			<!-- this must go afterwards or the onclicks don't get recieved -->
			%(output)s
		<!--
			Whitespace at bottom is created from certain grid_sizes that don't fit
		-->
		<!--
		<div style="position:absolute;top:%(map_height)spx;width:%(map_width)spx;height:30px;background-color:#ACF;">
			&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=10">Minute</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=20">Tiny</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=30">Small</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=40">Normal</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=60">Big</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=80">Large</a>&nbsp;&nbsp;&nbsp;
			<a href="web.py?mode=supplies_map&amp;grid_size=100">Huge</a>&nbsp;&nbsp;&nbsp;
		</div>
		-->
</html>""" % {
		"mapper_css": css,
		"left": the_map.left,
		"right": the_map.right,
		"onclick_js": onclick_js,
		"output": map_output,
		"map_width": map_width,
		"map_height": map_height,
		"map_path": map_path,
		"jquery": jquery,
		"grid_size": grid_size,
		"pgrid_size": int(grid_size*2.5),
	}
	
print(output)