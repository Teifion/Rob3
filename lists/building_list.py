import database

class Building (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Building, self).__init__()
		self.set_values(wall=False, economy=False, upgrades=0, needs_port=False, public=True)
		self.set_values(cost_per_turn="Materials:5")
		self.set_values(cost_up_front="")
		self.set_values(upkeep="")
		self.set_values(limit_per_city=1, description="")
		self.set_values(upgrades=-1, has_upgrade=False)
	
	def check(self):
		pass
	
data_list = []
def find(item_name):
	for i, d in enumerate(data_list):
		if d.name == item_name:
			return i
			
data_list.append(Building())
data_list[-1].set_values(name="25k Walls")
data_list[-1].set_values(build_time=300, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")
data_list[-1].set_values(description="")

data_list.append(Building())
data_list[-1].set_values(name="25k Fortifications")
data_list[-1].set_values(build_time=300, wall=True, upgrades=find("25k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="50k Walls")
data_list[-1].set_values(build_time=400, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="50k Fortifications")
data_list[-1].set_values(build_time=400, wall=True, upgrades=find("50k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="75k Walls")
data_list[-1].set_values(build_time=500, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="75k Fortifications")
data_list[-1].set_values(build_time=500, wall=True, upgrades=find("75k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="100k Walls")
data_list[-1].set_values(build_time=600, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="100k Fortifications")
data_list[-1].set_values(build_time=600, wall=True, upgrades=find("100k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="125k Walls")
data_list[-1].set_values(build_time=700, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="125k Fortifications")
data_list[-1].set_values(build_time=700, wall=True, upgrades=find("125k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="150k Walls")
data_list[-1].set_values(build_time=800, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="150k Fortifications")
data_list[-1].set_values(build_time=800, wall=True, upgrades=find("150k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="200k Walls")
data_list[-1].set_values(build_time=900, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="200k Fortifications")
data_list[-1].set_values(build_time=900, wall=True, upgrades=find("200k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="250k Walls")
data_list[-1].set_values(build_time=1100, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="250k Fortifications")
data_list[-1].set_values(build_time=1100, wall=True, upgrades=find("250k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="300k Walls")
data_list[-1].set_values(build_time=1300, wall=True)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="300k Fortifications")
data_list[-1].set_values(build_time=1300, wall=True, upgrades=find("300k Walls"))
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")

data_list.append(Building())
data_list[-1].set_values(name="Harbour walls")
data_list[-1].set_values(build_time=1000, wall=True, needs_port=1)
data_list[-1].set_values(cost_per_turn="Materials:5,stone:1")
data_list[-1].set_values(description="Provides protection against enemy ships and storms")

#	Normal buildings
#------------------------
data_list.append(Building())
data_list[-1].set_values(name="Shipyard")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Produces 100 ship points if on the shore, airship points otherwise")

data_list.append(Building())
data_list[-1].set_values(name="Airport")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Stores Airships")

data_list.append(Building())
data_list[-1].set_values(name="University")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Produces 50 mundane research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Produces 50 magical research points")

data_list.append(Building())
data_list[-1].set_values(name="Temple")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Produces 1 temple point")

data_list.append(Building())
data_list[-1].set_values(name="Castle")
data_list[-1].set_values(build_time=200, limit_per_city=4)
data_list[-1].set_values(description="Holds up to 5,000 people safely")


data_list.append(Building())
data_list[-1].set_values(name="Expanded shipyard")
data_list[-1].set_values(build_time=400, upgrades=find("Shipyard"))
data_list[-1].set_values(description="Produces 200 ship points if on the shore, airship points otherwise")

data_list.append(Building())
data_list[-1].set_values(name="Expanded airport")
data_list[-1].set_values(build_time=400, upgrades=find("Airport"))
data_list[-1].set_values(description="Holds many airships")

data_list.append(Building())
data_list[-1].set_values(name="Expanded university")
data_list[-1].set_values(build_time=400, upgrades=find("University"))
data_list[-1].set_values(description="Produces 100 mundane research points")


data_list.append(Building())
data_list[-1].set_values(name="Academy of Light")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 light research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Dark")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 dark research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Abjuration")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 abjuration research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Destruction")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 destruction research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Daemonic")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 daemonic research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Necromancy")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 necromancy research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Alchemy", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 alchemy research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Enchantment", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 50 magical research points and 100 enchantment research points")

data_list.append(Building())
data_list[-1].set_values(name="Academy of Animation", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))

data_list.append(Building())
data_list[-1].set_values(name="Academy of Sourcery", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))

data_list.append(Building())
data_list[-1].set_values(name="Academy of something_else_2", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))

data_list.append(Building())
data_list[-1].set_values(name="Academy of something_else_3", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))

data_list.append(Building())
data_list[-1].set_values(name="Academy of something_else_4", public=False)
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))

data_list.append(Building())
data_list[-1].set_values(name="2nd castle")
data_list[-1].set_values(build_time=200, upgrades=find("Castle"))
data_list[-1].set_values(description="Holds another 5000 people securely")

data_list.append(Building())
data_list[-1].set_values(name="3rd castle")
data_list[-1].set_values(build_time=200, upgrades=find("2nd castle"))
data_list[-1].set_values(description="Holds another 5000 people securely")

data_list.append(Building())
data_list[-1].set_values(name="4th castle")
data_list[-1].set_values(build_time=200, upgrades=find("3rd castle"))
data_list[-1].set_values(description="Holds another 5000 people securely")

data_list.append(Building())
data_list[-1].set_values(name="Border forts")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Provides early warning of attackers")

data_list.append(Building())
data_list[-1].set_values(name="Slave prison")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Holds slaves in a more secure area")

data_list.append(Building())
data_list[-1].set_values(name="Scary walls", public=False)
data_list[-1].set_values(build_time=200)

data_list.append(Building())
data_list[-1].set_values(name="Expanded academy")
data_list[-1].set_values(build_time=400, upgrades=find("Academy"))
data_list[-1].set_values(description="Produces 100 magical research points")

data_list.append(Building())
data_list[-1].set_values(name="Militia centre")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Improves the response time and equipment of the militia")

data_list.append(Building())
data_list[-1].set_values(name="Covert centre")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Provides increased couterspy ability")

data_list.append(Building())
data_list[-1].set_values(name="Expanded temple")
data_list[-1].set_values(build_time=400, upgrades=find("Temple"))
data_list[-1].set_values(description="Produces two temple points")

data_list.append(Building())
data_list[-1].set_values(name="Hospital")
data_list[-1].set_values(build_time=200)
data_list[-1].set_values(description="Reduces the effect of overcrowding by 10,000")

data_list.append(Building())
data_list[-1].set_values(name="Sewer system")
data_list[-1].set_values(build_time=400, upgrades=find("Hospital"))
data_list[-1].set_values(description="Reduces the effect of overcrowding by 20,000")

data_list.append(Building())
data_list[-1].set_values(name="Courthouse")
data_list[-1].set_values(build_time=800)
data_list[-1].set_values(description="Reduces the upkeep of the city")

for d in data_list:
	if d.upgrades > 0:
		data_list[d.upgrades].has_upgrade = True