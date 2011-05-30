import math

# Export size
# 4500, 1500, 6250, 4250
# 3250, 1500, 7500, 4250

dimensions = {
	"left":			-600,
	"right":		1300,
	"top":			600,
	"bottom":		2300,
	"margin_left":	-600,
	"margin_top":	0,
	
	"left":			-1200,
	"margin_left":	0,
}

terrain = ["water", "lowlands", "shore", "hills", "mountains", "swamp", "XYZ_1", "desert", "lake", "forest", "river", "large river", "XYZ_2", "XYZ_3", "forest swamp", "volcano"]

terrain_colour = {
	"MIXED":		"#000",
	"water":		"#00A",
	"lowlands":		"#ACA",
	"shore":		"#66F",
	"hills":		"#A33",
	"mountains":	"#777",
	"swamp":		"#ACF",
	"XYZ_1":		"",
	"desert":		"#FF0",
	"lake":			"#CCF",
	"forest":		"#0A0",
	"river":		"#AAF",
	"large river":	"#44F",
	"XYZ_2":		"",
	"XYZ_3":		"",
	"forest swamp":	"#0FF",
	"volcano":		"#FA0",}


move_costs = {}

move_costs["water"] = {
	"Light foot":	9999999,
	"Medium foot":	9999999,
	"Heavy foot":	9999999,
	"Colonists":	0.1,# They're using a boat, boats go 10 times as fast as colonists
	"Nomads":		9999999,
	
	"Light cav":	9999999,
	"Medium cav":	9999999,
	"Heavy cav":	9999999,
	
	"Sail":			1.0,
	"Oar":			1.0,
	"Air":			1.0,
	
	"Merchant":		9999999,
	
	"Generic path":	0.13,
}
move_costs["lowlands"] = {
	"Light foot":	1.0,
	"Medium foot":	1.0,
	"Heavy foot":	1.0,
	"Colonists":	1.0,
	"Nomads":		1.0,
	
	"Light cav":	1.0,
	"Medium cav":	1.0,
	"Heavy cav":	1.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		1,
	
	"Generic path":	1.0,
}
move_costs["shore"] = {
	"Light foot":	1.2,
	"Medium foot":	1.2,
	"Heavy foot":	1.2,
	"Colonists":	0.1,# Using a boat
	"Nomads":		1.2,
	
	"Light cav":	1.2,
	"Medium cav":	1.2,
	"Heavy cav":	1.2,
	
	"Sail":			1.2,
	"Oar":			1.0,
	"Air":			1.0,
	
	"Merchant":		0,
	
	"Generic path":	1.2,
}
move_costs["hills"] = {
	"Light foot":	1.5,
	"Medium foot":	2.0,
	"Heavy foot":	2.5,
	"Colonists":	2.5,
	"Nomads":		2.5,
	
	"Light cav":	1.5,
	"Medium cav":	2.0,
	"Heavy cav":	2.5,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		1.5,
	
	"Generic path":	2.5,
}
move_costs["mountains"] = {
	"Light foot":	2.5,
	"Medium foot":	3.5,
	"Heavy foot":	4.5,
	"Colonists":	4.5,
	"Nomads":		4.5,
	
	"Light cav":	3.0,
	"Medium cav":	4.0,
	"Heavy cav":	5.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		3,
	
	"Generic path":	3.5,
}
move_costs["swamp"] = {
	"Light foot":	1.5,
	"Medium foot":	2.0,
	"Heavy foot":	3.0,
	"Colonists":	3.0,
	"Nomads":		3.0,
	
	"Light cav":	2.0,
	"Medium cav":	2.5,
	"Heavy cav":	3.5,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		6,
	
	"Generic path":	2.0,
}
move_costs["XYZ_1"] = {
	"Light foot":	1.0,
	"Medium foot":	1.0,
	"Heavy foot":	1.0,
	"Colonists":	1.0,
	"Nomads":		1.0,
	
	"Light cav":	1.0,
	"Medium cav":	1.0,
	"Heavy cav":	1.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		0,
	
	"Generic path":	1.0,
}
move_costs["desert"] = {
	"Light foot":	1.3,
	"Medium foot":	1.5,
	"Heavy foot":	1.8,
	"Colonists":	1.8,
	"Nomads":		1.8,
	
	"Light cav":	1.1,
	"Medium cav":	1.3,
	"Heavy cav":	1.6,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		2,
	
	"Generic path":	1.5,
}
move_costs["lake"] = {
	"Light foot":	9999999,
	"Medium foot":	9999999,
	"Heavy foot":	9999999,
	"Colonists":	9999999,
	"Nomads":		9999999,
	
	"Light cav":	9999999,
	"Medium cav":	9999999,
	"Heavy cav":	9999999,
	
	"Sail":			9999999,#Should not be able to reach it
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		9999999,
	
	"Generic path":	9999999,
}
move_costs["forest"] = {
	"Light foot":	1.2,
	"Medium foot":	1.4,
	"Heavy foot":	1.6,
	"Colonists":	1.6,
	"Nomads":		1.6,
	
	"Light cav":	1.8,
	"Medium cav":	2.0,
	"Heavy cav":	2.2,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		1.5,
	
	"Generic path":	1.4,
}
move_costs["river"] = {
	"Light foot":	1.4,
	"Medium foot":	1.5,
	"Heavy foot":	1.6,
	"Colonists":	1.6,
	"Nomads":		1.6,
	
	"Light cav":	1.2,
	"Medium cav":	1.3,
	"Heavy cav":	1.4,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		1.3,
	
	"Generic path":	1.5,
}
move_costs["large river"] = {
	"Light foot":	1.8,
	"Medium foot":	1.9,
	"Heavy foot":	2.0,
	"Colonists":	2.0,
	"Nomads":		2.0,
	
	"Light cav":	2.3,
	"Medium cav":	2.4,
	"Heavy cav":	2.5,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		3,
	
	"Generic path":	1.9,
}
move_costs["XYZ_2"] = {
	"Light foot":	1.0,
	"Medium foot":	1.0,
	"Heavy foot":	1.0,
	"Colonists":	1.0,
	"Nomads":		1.0,
	
	"Light cav":	1.0,
	"Medium cav":	1.0,
	"Heavy cav":	1.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		0,
	
	"Generic path":	1.0,
}
move_costs["XYZ_3"] = {
	"Light foot":	1.0,
	"Medium foot":	1.0,
	"Heavy foot":	1.0,
	"Colonists":	1.0,
	"Nomads":		1.0,
	
	"Light cav":	1.0,
	"Medium cav":	1.0,
	"Heavy cav":	1.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		0,
	
	"Generic path":	1.0,
}
move_costs["forest swamp"] = {
	"Light foot":	1.5,
	"Medium foot":	2.0,
	"Heavy foot":	3.0,
	"Colonists":	3.0,
	"Nomads":		3.0,
	
	"Light cav":	2.1,
	"Medium cav":	2.6,
	"Heavy cav":	3.7,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		8,
	
	"Generic path":	2.0,
}
move_costs["volcano"] = {
	"Light foot":	2.5,
	"Medium foot":	3.5,
	"Heavy foot":	4.5,
	"Colonists":	4.5,
	"Nomads":		4.5,
	
	"Light cav":	3.0,
	"Medium cav":	4.0,
	"Heavy cav":	5.0,
	
	"Sail":			9999999,
	"Oar":			9999999,
	"Air":			1.0,
	
	"Merchant":		9,
	
	"Generic path":	3.5,
}

# KM per day
movement_speeds = {
	"Marching":		40,
	"Forced march":	60,
	
	"Riding":		120,
	"Forced ride":	150,
	
	"Sailing":		300,
	
	"Nomads":		40,
	"Colonists":	30,
	
	"Merchant":		30,
	
	"Generic path":	40,
}

# For list boxes
move_speed_list = (
	"Marching",
	"Forced march",
	"Riding",
	"Forced ride",
	"Sailing",
	"Nomads",
	"Colonists",
	"Generic path",
	"Merchant",
)

move_type_list = (
	"Light foot",
	"Medium foot",
	"Heavy foot",
	"Colonists",
	"Nomads",
	
	"Light cav",
	"Medium cav",
	"Heavy cav",
	
	"Sail",
	"Oar",
	"Air",
	"Generic path",
	"Merchant",
)

icon_max_size = 100
icon_min_size = 30
def map_image_size(size_value):
	if size_value < 1: return 0
	s = size_value/1000
	
	# image_size = round(math.sqrt(size_value)/4)
	image_size = round(s**1.02)
	# image_size = round(math.sqrt(size_value)*0.28)
	# image_size *= 1.21
	
	return max(min(image_size, icon_max_size), icon_min_size)
