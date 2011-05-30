import database
from functions import path_f

def main():
	"""Tests a set of paths"""
	
	cursor = database.get_cursor()
	
	tests = []
	
	# Goes from one end to the other of the Tishrashi desert, nothing special
	# tests.append(([(267, 1414), (438, 1405)], "Marching", "Medium foot"))
	
	# One end of Cayim to the other
	# tests.append(([(75, 1180), (986, 1664)], "Marching", "Medium foot"))
	
	# Top left to bottom right
	# tests.append(([(-1176, 636), (1276, 2283)], "Sailing", "Sail"))
	
	# 3 waypoints
	tests.append(([(400, 853), (565, 815), (605, 1003)], "Marching", "Medium foot"))
	
	# Noamdic test
	# tests.append(([(110,1190), (930,1690)], "Nomads", "Nomads"))
	
	# Round Cantharan
	tests.append(([(174, 1941), (392, 1965), (400, 2264), (-209, 2276), (-266, 1878), (-43, 1441)], "Sailing", "Sail"))
	
	
	# print("Waypoints: %s -> %s" % (str(p.start_point), str(p.end_point)))
	# print("Cost: %s" % p.time_cost)
	# print("Distance: %s" % round(p.distance, 2))
	# print("Step count: %d" % len(p.steps))
	# print("Steps: ", ", ".join([str(s['tile']) for s in p.steps]))
	
	map_path = "http://localhost/rob3/web.py?mode=path_map&"
	
	for t in tests:
		points = []
		for w in t[0]:
			points.append(w[0])
			points.append(w[1])
		
		p = path_f.path(cursor, t[0], t[1], t[2])
		print("%spoints=%s&move_speed=%s&move_type=%s - %s days, %skm" % (
			map_path,
			",".join([str(w) for w in points]),# Waypoints
			t[1].replace(" ", "%20"),
			t[2].replace(" ", "%20"),
			p.time_cost,
			p.walk_distance,
		))
		
		# We've just got 1 test setup, lets give more info
		if len(tests) == 1:
			print("")
			if p.steps[-1] == p.end_point:
				print("Success")
			else:
				print("Failure")
			print("Cost: %s" % p.time_cost)
			
			total_cost = 0
			for i, s in enumerate(p.steps):
				total_cost += s['time_cost']
				
				print("{i}	{cost}	{total}".format(
					i=i,
					cost=s['time_cost'],
					total=total_cost,
				))
		
		
		
	
