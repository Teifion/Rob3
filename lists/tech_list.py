import database
from data_classes import tech

category = tech.category

class Tech (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Tech, self).__init__()
		self.set_values(max_level=0, description="", category=category["common"])
		self.set_values(base_cost="", extra_cost="")
		self.set_values(tradable=True)
	
	def check(self):
		pass

data_list = []
data_list.append(Tech())
data_list[-1].set_values(name="Farming")
data_list[-1].set_values(base_cost="Materials:3,tech points:100")
data_list[-1].set_values(extra_cost="Materials:8,tech points:40")
data_list[-1].set_values(max_level=0, category=category["common"])
data_list[-1].set_values(description="Each city productes 5% more food")

data_list.append(Tech())
data_list[-1].set_values(name="Economy")
data_list[-1].set_values(base_cost="Materials:4,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:12,Tech points:60")
data_list[-1].set_values(description="Each city productes 5% more materials")

data_list.append(Tech())
data_list[-1].set_values(name="Army training")
data_list[-1].set_values(base_cost="Materials:3,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:6,Tech points:40")
data_list[-1].set_values(description="All units count as having a bonus month of experience")

data_list.append(Tech())
data_list[-1].set_values(name="Shipbuilding")
data_list[-1].set_values(base_cost="Materials:3,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:6,Tech points:40")
data_list[-1].set_values(description="Each shipyard produces 10% more points")

data_list.append(Tech())
data_list[-1].set_values(name="Covert training")
data_list[-1].set_values(base_cost="Materials:1,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:6,Tech points:40")
data_list[-1].set_values(description="Your spies become 5% harder to catch")

data_list.append(Tech())
data_list[-1].set_values(name="Siege equipment")
data_list[-1].set_values(base_cost="Materials:1,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:6,Tech points:40")
data_list[-1].set_values(description="Your siege equipment becomes 5% better")

data_list.append(Tech())
data_list[-1].set_values(name="Architecture")
data_list[-1].set_values(base_cost="Materials:1,Tech points:100")
data_list[-1].set_values(extra_cost="Materials:8,Tech points:40")
data_list[-1].set_values(description="Your buildings become 5% stronger")

data_list.append(Tech())
data_list[-1].set_values(name="Taranskan fire", max_level=1)
data_list[-1].set_values(base_cost="Materials:60,Tech points:1500")
data_list[-1].set_values(description="A fire that burns even on water")
data_list[-1].set_values(tradable=False)

# Used to be steam
data_list.append(Tech())
data_list[-1].set_values(name="NONE", max_level=1)
data_list[-1].set_values(base_cost="")
data_list[-1].set_values(tradable=False)

data_list.append(Tech())
data_list[-1].set_values(name="Gunpowder", max_level=3)
data_list[-1].set_values(base_cost="Materials:50,Tech points:500")
data_list[-1].set_values(extra_cost="Materials:40,Tech points:1000")
data_list[-1].set_values(description="See notes")
data_list[-1].set_values(tradable=False)

data_list.append(Tech())
data_list[-1].set_values(name="Airships", max_level=1)
data_list[-1].set_values(base_cost="Materials:75,Tech points:1000")
data_list[-1].set_values(description="Allows the production of balloons")
data_list[-1].set_values(tradable=False)

for s in data_list:
	s.check()