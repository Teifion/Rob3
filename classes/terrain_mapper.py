from queries import mapper_q
from classes import mapper
from rules import map_data

class Terrain_mapper (mapper.Map_maker):
	def __init__(self):
		super(Terrain_mapper, self).__init__()
	
	def map_terrain(self, cursor, colour_mode = False):
		output = []
		
		mapper_q.get_terrain(cursor, 0, 0)
		terrain_grid = mapper_q.terrain_cache_dict
		
		# self.grid_size is the MAP UNITS size
		# self.pgrid_size is the PIXEL size
		self.pgrid_size = self.grid_size * 2.5
		
		font_size = 1
		
		if		self.grid_size == 10: font_size = 0.2
		elif	self.grid_size == 20: font_size = 0.6
		elif	self.grid_size == 30: font_size = 1
		elif	self.grid_size == 40: font_size = 1.1
		elif	self.grid_size == 60: font_size = 1.4
		elif	self.grid_size == 80: font_size = 1.7
		elif	self.grid_size == 100: font_size = 2.1
		
		for x in range(self.left, self.right, self.grid_size):
			for y in range(self.top, self.bottom, self.grid_size):
				
				scan_left	= x
				scan_right	= x+self.grid_size
				
				scan_top	= y
				scan_bottom	= y+self.grid_size
				
				# print "\n\n<!-- BLOCK %s - %s, %s - %s -->" % (scan_left, scan_right, scan_top, scan_bottom)
				
				current_terrain = ""
				for xx in range(scan_left, scan_right, 10):
					if current_terrain == "MIXED": break
					# print ""

					for yy in range(scan_top, scan_bottom, 10):
						try:
							this_terrain = map_data.terrain[terrain_grid[(xx, yy)]]
						except KeyError as e:
							this_terrain = "water"
						except Exception as e:
							raise e

						# print "<!-- %s, %s: %s -->" % (xx, yy, this_terrain)


						if current_terrain == "": current_terrain = this_terrain

						if current_terrain != this_terrain:
							current_terrain = "MIXED"
							break

				terrain_colour = map_data.terrain_colour[current_terrain]

				if current_terrain == "water":
					current_terrain = ""
				else:
					if self.grid_size < 20:
						current_terrain = current_terrain[0:3]
					else:
						current_terrain = "<br />%s" % current_terrain

				if colour_mode and self.grid_size < 20:
					current_terrain = ""

				if colour_mode:
					output.append("""
				<div class="edit_box" style="top:%(top)spx;left:%(left)spx;width:%(pgrid_size)spx;height:%(pgrid_size)spx;font-size:%(font_size)sem;border:2px solid %(terrain_colour)s" id="%(x)s_%(y)s" onclick="$(this).load('web.py', {'mode':'edit_map_ajax','x':'%(x)s','y':'%(y)s','grid':'%(grid_size)s','terrain':$('#terrain').val()});">
					%(current_terrain)s
				</div>""" % {
					"x": x,
					"y": y,
					"left": int((x-self.left)*2.5),
					"top": int((y-self.top)*2.5),
					"pgrid_size": int(self.pgrid_size)-6,
					"grid_size": int(self.grid_size),
					"font_size": font_size,
					"current_terrain": current_terrain,
					"terrain_colour": terrain_colour,
				})

				else:		
					output.append("""
				<div class="edit_box" style="top:%(top)spx;left:%(left)spx;width:%(pgrid_size)spx;height:%(pgrid_size)spx;font-size:%(font_size)sem;" id="%(x)s_%(y)s" onclick="$(this).load('web.py', {'mode':'edit_map_ajax','x':'%(x)s','y':'%(y)s','grid':'%(grid_size)s','terrain':$('#terrain').val()});">
					%(current_terrain)s
				</div>""" % {
					"x": x,
					"y": y,
					"left": int((x-self.left)*2.5),
					"top": int((y-self.top)*2.5),
					"pgrid_size": int(self.pgrid_size),
					"grid_size": int(self.grid_size),
					"font_size": font_size,
					"current_terrain": current_terrain,
				})

		return "".join(output)

def map_source(source_dict, zoom=1):
	return mapper.map_source(source_dict, zoom)