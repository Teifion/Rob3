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

# Material economy
data_list.append(Tech())
data_list[-1].set_values(name="Mining")
data_list[-1].set_values(base_cost="Materials:14,Tech points:200")
data_list[-1].set_values(extra_cost="Materials:4,Tech points:300")
data_list[-1].set_values(description="Cities in mountains produce 2% more wealth")

data_list.append(Tech())
data_list[-1].set_values(name="Herding")
data_list[-1].set_values(base_cost="Materials:14,Tech points:200")
data_list[-1].set_values(extra_cost="Materials:4,Tech points:300")
data_list[-1].set_values(description="Cities in hills produce 2% more wealth")

data_list.append(Tech())
data_list[-1].set_values(name="Irrigation")
data_list[-1].set_values(base_cost="Materials:14,Tech points:200")
data_list[-1].set_values(extra_cost="Materials:4,Tech points:300")
data_list[-1].set_values(description="Cities in lowlands and shores produce 2% more wealth")

data_list.append(Tech())
data_list[-1].set_values(name="Farming")
data_list[-1].set_values(base_cost="Materials:10,tech points:200")
data_list[-1].set_values(extra_cost="Materials:4,tech points:200")
data_list[-1].set_values(description="Each city productes 2% more food")

# Internal
data_list.append(Tech())
data_list[-1].set_values(name="Architecture")
data_list[-1].set_values(base_cost="Materials:10,Tech points:250")
data_list[-1].set_values(extra_cost="Materials:2,Tech points:250")
data_list[-1].set_values(description="All buildings are 5% stronger")

data_list.append(Tech())
data_list[-1].set_values(name="Ship building")
data_list[-1].set_values(base_cost="Materials:20,Tech points:200")
data_list[-1].set_values(extra_cost="Materials:2,Tech points:200")
data_list[-1].set_values(description="Each shipyard produces 10% more points")

data_list.append(Tech())
data_list[-1].set_values(name="Beastmastery")
data_list[-1].set_values(base_cost="Materials:10,Tech points:250")
data_list[-1].set_values(extra_cost="Materials:4,Tech points:250")
data_list[-1].set_values(description="Improves the amount of monsters caught by 5% per level but does not raise the maximum limit of the monster in question.")

data_list.append(Tech())
data_list[-1].set_values(name="Covert techniques")
data_list[-1].set_values(base_cost="Materials:16,Tech points:200")
data_list[-1].set_values(extra_cost="Materials:2,Tech points:200")
data_list[-1].set_values(description="Improves your operatives chance of evasion by 5%")

data_list.append(Tech())
data_list[-1].set_values(name="Sanitation")
data_list[-1].set_values(base_cost="Materials:16,Tech points:250")
data_list[-1].set_values(extra_cost="Materials:4,Tech points:250")
data_list[-1].set_values(description="All cities shrink by 500 fewer people (this tech does not improve growth rate)")

# Super internal
data_list.append(Tech())
data_list[-1].set_values(name="Airships", max_level=3)
data_list[-1].set_values(base_cost="Materials:150,Tech points:1500")
data_list[-1].set_values(extra_cost="Materials:50,Tech points:3000")
data_list[-1].set_values(description="All units count as having a bonus month of experience")

data_list.append(Tech())
data_list[-1].set_values(name="Taranskan fire", max_level=1)
data_list[-1].set_values(base_cost="Materials:120,Tech points:3000")
data_list[-1].set_values(description="A fire that burns even on water")
data_list[-1].set_values(tradable=False)

data_list.append(Tech())
data_list[-1].set_values(name="Gunpowder", max_level=3)
data_list[-1].set_values(base_cost="Materials:100,Tech points:2000")
data_list[-1].set_values(extra_cost="Materials:100,Tech points:4000")
data_list[-1].set_values(description="See notes")
data_list[-1].set_values(tradable=False)

# Army stuff
data_list.append(Tech())
data_list[-1].set_values(name="Armour training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved protection from their armour")

data_list.append(Tech())
data_list[-1].set_values(name="Sword training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved damage from their sword")

data_list.append(Tech())
data_list[-1].set_values(name="Axe training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved damage from their axe")

data_list.append(Tech())
data_list[-1].set_values(name="Polearm training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved damage with their polearm")

data_list.append(Tech())
data_list[-1].set_values(name="Bow training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved fire rate with their bow")

data_list.append(Tech())
data_list[-1].set_values(name="Crossbow training")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All troops gain 3% improved fire rate with their crossbow")

data_list.append(Tech())
data_list[-1].set_values(name="Husbandry")
data_list[-1].set_values(base_cost="Materials:5,tech points:100")
data_list[-1].set_values(extra_cost="Materials:5,tech points:300")
data_list[-1].set_values(description="All mounted troops have 3% more control over their mount")


for s in data_list:
	s.check()