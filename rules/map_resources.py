import database
from lists import resource_list
import math

# Build a lookup dictionary simply because we'll need it so much
lookup = {}
for k, v in resource_list.data_dict.items():
	lookup[v.name] = k

data_list = []
def add(rname, x, y):
	data_list.append((lookup[rname], x, y))

#	RAYTI, TIVAYTI, FERNYTI, KAHALAN
#------------------------
add("Iron", -19, 1076)
add("Iron", -19, 1052)
add("Iron", -74, 1034)
add("Iron", 64, 961)
add("Iron", 83, 932)
add("Iron", 175, 1072)

add("Stone", 56, 942)
add("Stone", 41, 946)
add("Stone", -44, 1016)
add("Stone", -26, 1000)
add("Stone", 169, 1012)

add("Wood", -25, 923)
add("Wood", -70, 966)
add("Wood", 20, 1052)
add("Wood", 41, 1042)
add("Wood", -2, 1145)
add("Wood", 144, 961)
add("Wood", 223, 1022)

#	INDRIN, REETHTAK
#------------------------
add("Iron", -51, 782)
add("Iron", 187, 726)
add("Iron", 280, 713)

add("Stone", -182, 721)
add("Stone", -194, 784)
add("Stone", 313, 753)

add("Wood", 97, 762)
add("Wood", -90, 719)
add("Wood", -114, 775)

add("Giant hill", 184, 801)

add("Fertile lands", 132, 780)
add("Fertile lands", 207, 760)
add("Fertile lands", 283, 766)

# Nagamra
add("Stone", 490, 953)

add("Giant hill", -186, 750)
add("Gateway to Enkhingi", 483, 976)

# NORTH HUMYTI - By Nurzum
#-----------------------
# I dont know if anyone did this, but it has been a work in progress and I have completed the top half of the Humyti Continent.

add("Wood", 84, 1164)
add("Wood", 114, 1171)
add("Wood", 181, 1237)
add("Wood", 190, 1360)
add("Wood", 494, 1242)
add("Wood", 640, 1398)
add("Wood", 849, 1458)
add("Wood", 941, 1476)
add("Wood", 681, 1364)

add("Stone", 129, 1250)
add("Stone", 423, 1268)
add("Stone", 461, 1266)
add("Stone", 468, 1298)
add("Stone", 492, 1338)
add("Stone", 508, 1382)
add("Stone", 512, 1426)
add("Stone", 347, 1519)
add("Stone", 508, 1469)
add("Stone", 428, 1492)
add("Stone", 618, 1344)
add("Stone", 753, 1332)
add("Stone", 768, 1307)
add("Stone", 558, 1309)
add("Stone", 614, 1262)

add("Iron", 210, 1180)
add("Iron", 646, 1186)
add("Iron", 838, 1148)
add("Iron", 102, 1256)

add("Natural harbour", 138, 1223)
add("Natural harbour", 51, 1361)
add("Natural harbour", 219, 1484)

add("Giant hill", 322, 1290)
add("Giant hill", 380, 1270)
add("Giant hill", 359, 1468)
add("Giant hill", 503, 1558)
add("Giant hill", 338, 1590)
add("Giant hill", 715, 1207)
add("Giant hill", 774, 1196)
add("Giant hill", 806, 1172)
add("Giant hill", 830, 1190)
add("Giant hill", 814, 1218)
add("Giant hill", 850, 1216)
add("Giant hill", 859, 1177)
add("Giant hill", 883, 1194)
add("Giant hill", 846, 1332)
add("Giant hill", 906, 1298)
add("Giant hill", 984, 1376)

add("Fertile lands", 578, 1372)
add("Fertile lands", 578, 1215)
add("Fertile lands", 565, 1258)
add("Fertile lands", 511, 1296)
add("Fertile lands", 808, 1403)
add("Fertile lands", 78, 1341)
add("Fertile lands", 118, 1358)

#	DO-JA
#------------------------
add("Stone", -398, 806)
add("Wood", -408, 904)
add("Giant hill", -317, 906)
add("Wood", -463, 1030)
add("Iron", -430, 1531)
add("Stone", -423, 1289)

#	Werepysgo
#------------------------
add("Stone", 93, 1431)
add("Fertile lands", 65, 1506)
add("Natural harbour", 24, 1611)

#	Carippi
#------------------------
add("Wood", -881, 1510)
add("Wood", -825, 1578)
add("Wood", -603, 1554)
add("Wood", -587, 1624)
add("Iron", -767, 1587)
add("Iron", -726, 1645)
add("Iron", -748, 1672)
add("Stone", -858, 1644)
add("Stone", -802, 1624)
add("Stone", -815, 1523)
add("Stone", -774, 1549)
add("Stone", -738, 1587)

add("Natural harbour", -892, 1622)
add("Natural harbour", -713, 1670)
add("Natural harbour", -640, 1578)
add("Giant hill", -832, 1684)


#	Bazniraz
#------------------------
add("Stone", -1042, 872)
add("Stone", -1015, 909)
add("Wood", -959, 896)
add("Iron", -887, 1037)
add("Natural harbour", -1048, 942)
add("Natural harbour", -876, 969)
add("Giant hill", -1028, 956)
add("Fertile lands", -892, 992)
add("Fertile lands", -944, 1004)

#	Adothasha
#------------------------
add("Stone", -743, 789)
add("Wood", -659, 776)
add("Iron", -778, 842)
add("Natural harbour", -689, 834)
add("Natural harbour", -781, 788)

#	Dragon isles
#------------------------
add("Wood", 810, 924)
add("Iron", 1034, 1078)
add("Stone", 1147, 899)

#	Ekederlin
#------------------------
add("Giant hill", 834, 1648)
add("Giant hill", 950, 1631)

#	Rainforest
#------------------------
add("Wood", 232, 1623)
add("Wood", 371, 1662)
add("Wood", 406, 1726)
add("Wood", 482, 1764)
add("Wood", 487, 1667)
add("Wood", 561, 1763)
add("Wood", 570, 1670)
add("Wood", 626, 1596)
add("Wood", 733, 1609)
add("Wood", 746, 1502)
add("Wood", 781, 1588)
add("Wood", 977, 1520)
add("Giant hill", 565, 1824)
add("Natural harbour", 194, 1664)

#	Oplessan desert
#------------------------
add("Natural harbour", 249, 1551)

#	Uxebrith desert
#------------------------
add("Giant hill", -58, 1854)
add("Giant hill", 171, 1854)
add("Natural harbour", 350, 1877)

#	Anos Eloxnard
#------------------------
add("Stone", -154, 1853)

#	Hetayze & Hathnecm Tew
#------------------------
add("Stone", -26, 1940)
add("Stone", -81, 2046)
add("Wood", -71, 1984)
add("Wood", -107, 2119)
add("Wood", 62, 2069)
add("Wood", 278, 2189)
add("Wood", 318, 2044)
add("Iron", 159, 1947)
add("Giant hill", 366, 2023)

#	East of the continent
#------------------------
add("Fertile lands", 646, 1508)

# Now to check them
i = 0
max_dist = 0
for r1, x1, y1 in data_list:
	i += 1
	j = 0
	for r2, x2, y2 in data_list:
		j += 1
		
		if i == j: continue
		
		xdist = abs(x1 - x2)
		ydist = abs(y1 - y2)
		dist = math.sqrt(xdist*xdist + ydist*ydist)
		
		if dist < 7:
			max_dist = max(max_dist, dist)
			print("%s (%s, %s) is near %s (%s, %s)" % (
				resource_list.data_list[r1].name, x1, y1,
				resource_list.data_list[r2].name, x2, y2))

# print(max_dist)