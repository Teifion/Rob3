from pages import common
from rules import region_data

page_data = {
	"Title":	"Map selector",
	"Admin":	True,
	"Header":	False,
}

def main(cursor):
	return make_map_select(cursor, True)

def make_map_select(cursor, dev_mode=False):
	output = []
	
	#	DEV MODE
	#------------------------
	if dev_mode:
		with_analytics	= False
		local_path		= True
		thumb_path		= "http://localhost/woa/map/images/regions"
	else:
		with_analytics	= True
		local_path		= False
		thumb_path		= "images/regions"
	
	#	HEADER
	#------------------------
	output.append(common.headers(title_name="World of Arl: Map select", css="", javascript="", local_path=local_path))
	
	output.append("<div style='width:790px;margin:0 auto;'>")
	
	#	CORE OUTPUT
	#------------------------
	output.append("""
	<div style="margin-top: 10px;">
		<div style="height: 275px; float: left; margin: 5px;">
			<div style="text-align:center;font-weight:bold;font-size:1.1em;">Full map</div>
			<a href="latest.html">
				<img src="%(thumb_path)s/full_thumb.png" width="250" height="250" />
			</a>
		</div>
		<br />
		Warning: The full sized map is very large in terms of image size and also loading time due to all the cities that will be displayed.
		<br /><br />
		
		If you are after a specific section of the map you will find that the sections listed below will both load faster and display at a higher quality. Most of the sections overlap their neighbours so it doesn't matter if you cannot find one centred on your nation.
	</div>
	<div style="clear: left;">&nbsp;</div>
	""" % {
		"thumb_path":	thumb_path,
	})
	
	grid_mode = True
	
	if not grid_mode:
		for r in region_data.region_list:
			if dev_mode:
				link = "http://localhost/rob2/web.py?mode=view_region&region=%s" % r.name.lower()
			else:
				link = "http://woarl.com/map/latest_%s.html" % r.name.lower()
		
			output.append("""
			<div style="width: 250px; height: 275px; float: left; margin: 5px;">
				<div style="text-align:center;font-weight:bold;font-size:1.1em;">%(name)s</div>
				<a href="%(link)s">
					<img src="%(thumb_path)s/%(lower_name)s_thumb.png" width="250" height="250" />
				</a>
			</div>
			""" % {
				"thumb_path":	thumb_path,
				"lower_name":	r.name.lower(),
				"name":			r.name,
				"link":			link,
			})
	else:
		link = "http://woarl.com/map/latest_"
		# if dev_mode:
		# 	link = "http://localhost/rob2/web.py?mode=view_region&region="
		# else:
		# 	link = "http://woarl.com/map/latest_"
		
		output.append("""
		<table border="0" cellspacing="0" cellpadding="3">
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>
					<a href="%(link)sbazniraz.html">
						<img src="%(thumb_path)s/bazniraz_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)srayti.html">
						<img src="%(thumb_path)s/rayti_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)skilpellershe.html">
						<img src="%(thumb_path)s/kilpellershe_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)shumyti.html">
						<img src="%(thumb_path)s/humyti_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)stishrashi.html">
						<img src="%(thumb_path)s/tishrashi_thumb.png" />
					</a>
				</td>
				<td>
					<a href="%(link)smesmelamls.html">
						<img src="%(thumb_path)s/mesmelamls_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>
					<a href="%(link)scarippi.html">
						<img src="%(thumb_path)s/carippi_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)suxebrith.html">
						<img src="%(thumb_path)s/uxebrith_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>
					<a href="%(link)shetayze.html">
						<img src="%(thumb_path)s/hetayze_thumb.png" />
					</a>
				</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
		</table>
		""" % {
			"link":			link,
			"thumb_path":	thumb_path,
		})
	
	
	#	FOOTER
	#------------------------
	output.append("</div>")
	output.append(common.footers(with_analytics))
	
	return "".join(output)
	

