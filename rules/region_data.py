"""
(c) Copyright 2009 Teifion Jordan. All Rights Reserved.

Governs the sectors of the map for export
"""

class Map_region (object):
	# Bounds = X1, Y1, X2, Y2
	def __init__(self, name, bounds):
		super(Map_region, self).__init__()
		self.name	= name
		self.bounds	= bounds
	

region_list = []

# 6250, 1500, 2250, 2550
region_list.append(Map_region('Rayti', (-500, 600, 400, 1500)))

# 7000, 2000, 2000, 2000
region_list.append(Map_region('Humyti', (-200, 800, 600, 1600)))

# 7250, 2750, 2000, 2000
region_list.append(Map_region('Tishrashi', (-100, 1100, 700, 1900)))

# 6750, 3750, 2000, 2000
region_list.append(Map_region('Uxebrith', (-300, 1500, 500, 2300)))

# 8000, 3000, 2000, 2000
region_list.append(Map_region('Mesmelamls', (200, 1200, 1000, 2000)))

# 8750, 1750, 2000, 2000
region_list.append(Map_region('Kilpellershe', (500, 700, 1300, 1500)))

# 4500, 1750, 2250, 2250
region_list.append(Map_region('Bazniraz', (-1200, 700, -300, 1600)))

# 5000, 3500, 2000, 2000
region_list.append(Map_region('Carippi', (-1000, 1400, -200, 2200)))

# 6250, 4250, 2250, 1500
region_list.append(Map_region('Hetayze', (-500, 1700, 400, 2300)))

def get_source_dict(the_map, region_name, build_mode=1):
	"""Returns a source dict for a given region"""
	source_dict = {
		"build":				build_mode,
		"margin_left":			0,
		"margin_top":			0,
		
		"map_path":				"http://localhost/WoA/map/images/regions/%s.jpg" % region_name.lower(),
		"title":				"World of Arl regional map: %s" % region_name,
	}
	
	# Build uses a different map path
	if build_mode:
		source_dict['map_path'] = "images/regions/%s.jpg" % region_name.lower()
	
	# Fix it for that region
	for r in region_list:
		if r.name.lower() == region_name.lower():
			the_map.left	= r.bounds[0]
			the_map.top		= r.bounds[1]
			the_map.right	= r.bounds[2]
			the_map.bottom	= r.bounds[3]
			
			source_dict['left']	= r.bounds[0] * 2.5
			source_dict['top']	= r.bounds[1] * 2.5
			
			source_dict['map_width'] = (r.bounds[2] - r.bounds[0]) * 2.5
			source_dict['map_height'] = (r.bounds[3] - r.bounds[1]) * 2.5
	
	return source_dict
