# ([A-Za-z0-9_ ]*?) (-?[0-9]{1,4}), (-?[0-9]{1,4})

# data_list.append(Continent())
# # data_list[-1].set_values(name="$1", x=$2, y=$3)

import database

class Continent (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Continent, self).__init__()
		self.set_values(x=0, y=0)
	
	def check(self):
		# Works out the tile coords
		self.x = self.x - (self.x % 10)
		self.y = self.y - (self.y % 10)

data_list = []

data_list.append(Continent())
data_list[-1].set_values(name="Indrin", x=-130, y=750)

data_list.append(Continent())
data_list[-1].set_values(name="Reethtak", x=200, y=760)

data_list.append(Continent())
data_list[-1].set_values(name="Fernyti", x=-20, y=920)

data_list.append(Continent())
data_list[-1].set_values(name="Rayti", x=-10, y=990)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_1", x=40, y=1080)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_2", x=-10, y=1110)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_3", x=10, y=1110)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_4", x=30, y=1110)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_5", x=50, y=1110)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_6", x=0, y=1140)

data_list.append(Continent())
data_list[-1].set_values(name="Khalanatdillik_7", x=30, y=1140)

data_list.append(Continent())
data_list[-1].set_values(name="Tivayti", x=190, y=1010)

data_list.append(Continent())
data_list[-1].set_values(name="Cayim_north", x=380, y=1410)

data_list.append(Continent())
data_list[-1].set_values(name="Cayim_south", x=230, y=1770)

data_list.append(Continent())
data_list[-1].set_values(name="Nagamra", x=480, y=970)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_1", x=-390, y=820)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_2", x=-310, y=890)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_3", x=-420, y=920)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_4", x=-480, y=1010)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_5", x=-410, y=1090)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_6", x=-460, y=1200)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_7", x=-400, y=1310)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_8", x=-450, y=1370)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_9", x=-440, y=1520)

data_list.append(Continent())
data_list[-1].set_values(name="Do-ja_10", x=-350, y=1620)


data_list.append(Continent())
data_list[-1].set_values(name="Werepysgo_nw", x=0, y=1440)

data_list.append(Continent())
data_list[-1].set_values(name="Werepysgo_ne", x=110, y=1460)

data_list.append(Continent())
data_list[-1].set_values(name="Werepysgo_centre", x=50, y=1510)

data_list.append(Continent())
data_list[-1].set_values(name="Werepysgo_south", x=50, y=1590)

data_list.append(Continent())
data_list[-1].set_values(name="Werepysgo_west", x=-30, y=1540)

data_list.append(Continent())
data_list[-1].set_values(name="Guhyg", x=900, y=940)

data_list.append(Continent())
data_list[-1].set_values(name="Sepparm", x=1120, y=920)

data_list.append(Continent())
data_list[-1].set_values(name="Oorbem", x=1030, y=1060)

data_list.append(Continent())
data_list[-1].set_values(name="Adothasha", x=-700, y=820)

data_list.append(Continent())
data_list[-1].set_values(name="Bazniraz", x=-950, y=950)

data_list.append(Continent())
data_list[-1].set_values(name="Carippi", x=-750, y=1620)

data_list.append(Continent())
data_list[-1].set_values(name="Outer Edeck", x=-340, y=1990)

data_list.append(Continent())
data_list[-1].set_values(name="Inner Edeck", x=-360, y=2050)

for b in data_list:
	if b == "": continue
	b.check()