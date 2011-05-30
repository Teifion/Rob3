import database
from rules import equipment_stats
from lists import continent_list
from rules import map_data
from data_classes import equipment
from classes import unit

the_stats = equipment_stats.the_stats

def get_cont(name):
	for i, c in enumerate(continent_list.data_list):
		if c == "": continue
		if c.name == name:
			return i
	
	raise Exception("No continent of name %s found" % name)

def get_terrain(terrain_name):
	return map_data.terrain.index(terrain_name.lower())
	
	raise Exception("No continent of name %s found" % name)
		

cat_list	= equipment.cat_list
damage_list	= equipment.damage_list
speed_list	= equipment.speed_list
mspeed_list	= equipment.move_speed
mtype_list	= equipment.move_type

armour_cat = unit.armour_categories
move_cat = unit.move_categories
training_cat = unit.training_categories
# training_cat = unit.armour_categories

# Subclass so that we can do calc'd stats
class Equipment_list_item (database.DB_list_row):
	"""docstring for Equipment_list_item"""
	def __init__(self, **values):
		super(Equipment_list_item, self).__init__(**values)
		
		self.set_values(cost="", cost_multiplier="", description="")
		self.set_values(upkeep="", upkeep_multiplier="")
		self.set_values(crew=0, public=True)
		self.set_values(transport=0, large_transport=0)
		self.set_values(continent=-1, terrain=-1, tech=-1, tech_level=-1)
		self.set_values(move_type=-1, move_speed=-1)
		
		self.set_values(damage_type=0, range=-1, one_handed=0, two_handed=0, weight=0, speed=0)
		self.set_values(armour_cat=0, move_cat=0, training_cat=0)
	
	def check(self):
		# Work out grep_priority
		self.set_values(grep_priority=len(self.name))
		
		try:
			if self.name in the_stats:
				self.damage_type	= damage_list.index(the_stats[self.name].get("damage", "Slash"))
				self.range			= the_stats[self.name].get("range", 0)
				self.one_handed		= the_stats[self.name].get("one handed", True)
				self.two_handed		= the_stats[self.name].get("two handed", True)
				
				self.weight			= the_stats[self.name].get("weight", 0)
				self.speed			= speed_list.index(the_stats[self.name].get("speed", "Average"))
				
				self.description	= the_stats[self.name].get("description", "")
		except Exception:
			print("")
			print("Current item: %s" % self.name)
			raise
			

data_list = []

data_list.append(Equipment_list_item(name="No training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:0", upkeep="Materials:0", training_cat = training_cat.index("Low"))
data_list[-1].set_values(cost_multiplier="Materials:0.5", upkeep_multiplier="Materials:0")

data_list.append(Equipment_list_item(name="Basic training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:0", upkeep="Materials:0", training_cat = training_cat.index("Low"))
data_list[-1].set_values(cost_multiplier="Materials:0.75", upkeep_multiplier="Materials:0.1875")
# 0.75 cost * 0.25 upkeep = 0.1875

data_list.append(Equipment_list_item(name="Standard training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1", training_cat = training_cat.index("Normal"))
data_list[-1].set_values(cost_multiplier="Materials:1", upkeep_multiplier="Materials:0.25")
# 1.0 cost * 0.25 upkeep = 0.25

data_list.append(Equipment_list_item(name="Good training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:2", upkeep="Materials:2", training_cat = training_cat.index("Normal"))
data_list[-1].set_values(cost_multiplier="Materials:1.5", upkeep_multiplier="Materials:0.45")
# 1.5 cost * 0.3 upkeep = .5 (if you get 0.495 or so it's rounding errors)

data_list.append(Equipment_list_item(name="Exceptional training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:2.5", upkeep="Materials:2.5", training_cat = training_cat.index("High"))
data_list[-1].set_values(cost_multiplier="Materials:2", upkeep_multiplier="Materials:0.66")
# 2 cost * 0.3 upkeep = .66666666666666666666 - I hate rounding errors

data_list.append(Equipment_list_item(name="Elite training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:2", upkeep="Materials:2", training_cat = training_cat.index("High"))
data_list[-1].set_values(cost_multiplier="Materials:5", upkeep_multiplier="Materials:2.5")
# 5 cost * 0.5 upkeep = 2.5

# Training		Constant	Multiplier		Upkeep %	Correct Costings
# Untrained		0			50%				0%			(0.25/1)		(0/0)
# Low			0			75%				25%			(0.375/1.5)		(0.09375/0.375)
# Standard		1			100%			25%			(1.5/3)			(.375/.75)
# Good			3			150%			33%			(3.75/6)		(1.25/2)
# Exceptional	5			200%			33%			(6/9)			(2/3)
# Elite			10			500%			50%			(12.5/20)		(6.25/10)
# 
# 
# Flail	1.5 / 4
# Full plate suit	5 / 20
# Tower shield	1 / 1

#	SHIP TRAINING
#------------------------
data_list.append(Equipment_list_item(name="Transport ship"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="", upkeep="", public=False)
# data_list[-1].set_values(cost_multiplier="Materials:1,Ship points:2")

data_list.append(Equipment_list_item(name="Gunship"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="", upkeep="", public=False)
# data_list[-1].set_values(cost_multiplier="Materials:1,Ship points:2")

data_list.append(Equipment_list_item(name="Assault craft"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="", upkeep="", public=False)
# data_list[-1].set_values(cost_multiplier="Materials:1,Ship points:2")

#	MAGIC TRAINING
#------------------------
data_list.append(Equipment_list_item(name="Low tier magic"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:333", upkeep="Materials:333", public=True)

data_list.append(Equipment_list_item(name="Mid tier magic"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:1000", upkeep="Materials:1000", public=True)

data_list.append(Equipment_list_item(name="High tier magic"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:1600", upkeep="Materials:1600", public=True)

#	Operative training
#------------------------
data_list.append(Equipment_list_item(name="Grade 1 Operative training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:1000", upkeep="Materials:1000", public=False)

data_list.append(Equipment_list_item(name="Grade 2 Operative training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:2000", upkeep="Materials:2000", public=False)

data_list.append(Equipment_list_item(name="Grade 3 Operative training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:4000", upkeep="Materials:4000", public=False)

data_list.append(Equipment_list_item(name="Grade 4 Operative training"))
data_list[-1].set_values(category=cat_list.index("Training"))
data_list[-1].set_values(cost="Materials:8000", upkeep="Materials:8000", public=False)

#	Swords
#------------------------
data_list.append(Equipment_list_item(name="Short sword"))
data_list[-1].set_values(category=cat_list.index("Sword"))
data_list[-1].set_values(cost="Materials:2,Iron:Materials/4", upkeep="Materials:2,Iron:Materials/4")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Long sword"))
data_list[-1].set_values(category=cat_list.index("Sword"))
data_list[-1].set_values(cost="Materials:4,Iron:Materials/4", upkeep="Materials:4,Iron:Materials/4")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Great sword"))
data_list[-1].set_values(category=cat_list.index("Sword"))
data_list[-1].set_values(cost="Materials:6,Iron:Materials/4", upkeep="Materials:6,Iron:Materials/4")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Twin swords"))
data_list[-1].set_values(category=cat_list.index("Sword"))
data_list[-1].set_values(cost="Materials:4,Iron:Materials/4", upkeep="Materials:4,Iron:Materials/4")
data_list[-1].set_values(range=0)

#	Axes
#------------------------
data_list.append(Equipment_list_item(name="Axe"))
data_list[-1].set_values(category=cat_list.index("Axe"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Great axe"))
data_list[-1].set_values(category=cat_list.index("Axe"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Twin axes"))
data_list[-1].set_values(category=cat_list.index("Axe"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)

#	Blunt
#------------------------
data_list.append(Equipment_list_item(name="Mace"))
data_list[-1].set_values(category=cat_list.index("Hammer"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Twin maces"))
data_list[-1].set_values(category=cat_list.index("Hammer"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Hammer"))
data_list[-1].set_values(category=cat_list.index("Hammer"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Flail"))
data_list[-1].set_values(category=cat_list.index("Flail"))
data_list[-1].set_values(cost="Materials:4,Iron:Materials/2.5", upkeep="Materials:4,Iron:Materials/2.5")
data_list[-1].set_values(range=0)

#	Polearms
#------------------------
data_list.append(Equipment_list_item(name="Spear"))
data_list[-1].set_values(category=cat_list.index("Polearm"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Pike"))
data_list[-1].set_values(category=cat_list.index("Polearm"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Halberd"))
data_list[-1].set_values(category=cat_list.index("Polearm"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=0)

data_list.append(Equipment_list_item(name="Lance"))
data_list[-1].set_values(category=cat_list.index("Polearm"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=0)


#	BOW
#------------------------
data_list.append(Equipment_list_item(name="Shortbow"))
data_list[-1].set_values(category=cat_list.index("Bow"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Bow"))
data_list[-1].set_values(category=cat_list.index("Bow"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Longbow"))
data_list[-1].set_values(category=cat_list.index("Bow"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Composite bow"))
data_list[-1].set_values(category=cat_list.index("Bow"))
data_list[-1].set_values(cost="Materials:2", upkeep="Materials:2")
data_list[-1].set_values(range=10)

#	CROSSBOW
#------------------------
data_list.append(Equipment_list_item(name="Crossbow"))
data_list[-1].set_values(category=cat_list.index("Crossbow"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Repeating crossbow"))
data_list[-1].set_values(category=cat_list.index("Crossbow"))
data_list[-1].set_values(cost="Materials:1.5", upkeep="Materials:1.5")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Arbalest"))
data_list[-1].set_values(category=cat_list.index("Crossbow"))
data_list[-1].set_values(cost="Materials:12,Iron:Materials/4", upkeep="Materials:12,Iron:Materials/4")
data_list[-1].set_values(range=10)


#	GUNPOWDER
#------------------------
data_list.append(Equipment_list_item(name="Arquebus"))
data_list[-1].set_values(category=cat_list.index("Gunpowder"))
data_list[-1].set_values(cost="Materials:4,Iron:Materials/4", upkeep="Materials:4,Iron:Materials/4")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Musket"))
data_list[-1].set_values(category=cat_list.index("Gunpowder"))
data_list[-1].set_values(cost="Materials:6,Iron:Materials/4", upkeep="Materials:6,Iron:Materials/4")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Rockets"))
data_list[-1].set_values(category=cat_list.index("Gunpowder"))
data_list[-1].set_values(cost="Materials:10", upkeep="Materials:10")
data_list[-1].set_values(range=10)

#	THROWN
#------------------------
data_list.append(Equipment_list_item(name="Javelins"))
data_list[-1].set_values(category=cat_list.index("Thrown"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")
data_list[-1].set_values(range=10)

data_list.append(Equipment_list_item(name="Slings"))
data_list[-1].set_values(category=cat_list.index("Thrown"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")
data_list[-1].set_values(range=10)



#	ARMOUR
#------------------------
data_list.append(Equipment_list_item(name="Leather jacket"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Leather"))
data_list[-1].set_values(cost="Materials:0.25", upkeep="Materials:0.25")

data_list.append(Equipment_list_item(name="Leather suit"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Leather"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")

data_list.append(Equipment_list_item(name="Chainmail jacket"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Mail"))
data_list[-1].set_values(cost="Materials:4,Iron:Materials/4", upkeep="Materials:4,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Chainmail suit"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Mail"))
data_list[-1].set_values(cost="Materials:8,Iron:Materials/4", upkeep="Materials:8,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Banded armour jacket"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Mail"))
data_list[-1].set_values(cost="Materials:6,Iron:Materials/4", upkeep="Materials:6,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Banded armour suit"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Mail"))
data_list[-1].set_values(cost="Materials:10,Iron:Materials/4", upkeep="Materials:10,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Breastplate"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Plate"))
data_list[-1].set_values(cost="Materials:10,Iron:Materials/4", upkeep="Materials:10,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Full plate suit"))
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Plate"))
data_list[-1].set_values(cost="Materials:40,Iron:Materials/4", upkeep="Materials:40,Iron:Materials/4")

#	SHIELDS
#------------------------
data_list.append(Equipment_list_item(name="Buckler"))
data_list[-1].set_values(category=cat_list.index("Shield"))
data_list[-1].set_values(cost="Materials:0.25", upkeep="Materials:0.25")

data_list.append(Equipment_list_item(name="Small shield"))
data_list[-1].set_values(category=cat_list.index("Shield"))
data_list[-1].set_values(cost="Materials:0.5", upkeep="Materials:0.5")

data_list.append(Equipment_list_item(name="Large shield"))
data_list[-1].set_values(category=cat_list.index("Shield"))
data_list[-1].set_values(cost="Materials:0.75", upkeep="Materials:0.75")

data_list.append(Equipment_list_item(name="Tower shield"))
data_list[-1].set_values(category=cat_list.index("Shield"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")


#	Centaur armour
#------------------------
data_list.append(Equipment_list_item(name="Centaur leather"))
data_list[-1].set_values(description="", public=False)
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Leather"))
data_list[-1].set_values(cost="Materials:1", upkeep="Materials:1")

data_list.append(Equipment_list_item(name="Centaur chainmail"))
data_list[-1].set_values(description="", public=False)
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Mail"))
data_list[-1].set_values(cost="Materials:16,Iron:Materials/4", upkeep="Materials:16,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Centaur plate"))
data_list[-1].set_values(description="", public=False)
data_list[-1].set_values(category=cat_list.index("Armour"), armour_cat = armour_cat.index("Plate"))
data_list[-1].set_values(cost="Materials:40,Iron:Materials/4", upkeep="Materials:40,Iron:Materials/4")


#	MOUNTS
#------------------------
data_list.append(Equipment_list_item(name="Horse"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:3", upkeep="Materials:3", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Warhorse"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:6", upkeep="Materials:6", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Barded warhorse"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:22,Iron:Materials=10", upkeep="Materials:22,Iron:Materials=10", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Etiwcem"))
# The Etiwcem is about twice the height of a human and 4 metres long. It resembles a bear in colour and texture but the fur is much longer. It has 8 legs on each side and can shuffle along slowly. They are strong but not fast nor tough. Etiwcem are found all over the world. Typically only a small herd will be captured in one area. 6 humans can fit atop a single Etiwcem.
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:13.3", upkeep="Materials:13.3", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))


data_list.append(Equipment_list_item(name="Barded etiwcem"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:45.3,Iron:Materials=21.3", upkeep="Materials:45.3,Iron:Materials=21.3", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Mules"))
data_list[-1].set_values(description="Not battle-worthy like a horse but provide a faster march speed")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:2", upkeep="Materials:2", move_cat = move_cat.index("Mule"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Mule"))

data_list.append(Equipment_list_item(name="Camel"))
data_list[-1].set_values(description="Slower and less agile than a horse but more aggressive. Horses are afraid of camels. Camels also have much higher stamina than horses and are ideal for desert fighting.")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:5", upkeep="Materials:5", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Barded camel"))
data_list[-1].set_values(description="A camel with leather barding")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:9", upkeep="Materials:9", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Warboar"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:9", upkeep="Materials:9", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Mule"))

data_list.append(Equipment_list_item(name="Pegasus"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:50", upkeep="Materials:50", move_cat = move_cat.index("Flight"))
# $equipArray[$i]->description = 'They are essentially a flying pony. Pegasai are very frail and cannot carry much more weight than a human, they are docile and exist over most of the world. It is possible to catch small herds of Pegasai in one area.';
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Wing"))

data_list.append(Equipment_list_item(name="Vizzig"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:10", upkeep="Materials:10", move_cat = move_cat.index("Horse"))
# $equipArray[$i]->description = 'They are akin to giant ducks but without the wings and weak bone structure. With giant webbed feet the Vizzig make fighting in a swamp possible. They can support the weight of people with armour but wearing such a thing in a swamp is a bad idea, if you fall off the Vizzig you will surely die. Vizzig are found in swamps and on the banks of rivers all around the world. They eat mainly grass and make poor fighters. It is easy to catch entire herds of Vizzig in one area.';
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Large chariot"))
data_list[-1].set_values(description="A 4 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:12", upkeep="Materials:12", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Large chariot with barded warhorses"))
data_list[-1].set_values(description="A 4 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:28,Iron:Materials=16", upkeep="Materials:28,Iron:Materials=16", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Medium chariot"))
data_list[-1].set_values(description="A 3 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:10", upkeep="Materials:10", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Medium chariot with barded warhorses"))
data_list[-1].set_values(description="A 3 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:25,Iron:Materials=14", upkeep="Materials:25,Iron:Materials=14", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Small chariot"))
data_list[-1].set_values(description="A 2 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:8", upkeep="Materials:8", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Small chariot with normal horses"))
data_list[-1].set_values(description="A 2 man chariot")
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:5", upkeep="Materials:5", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

#	SIEGE ENGINES
#------------------------
data_list.append(Equipment_list_item(name="Catapult"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:500")

data_list.append(Equipment_list_item(name="Mangonel"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:1000")

data_list.append(Equipment_list_item(name="Onager"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:2000")

data_list.append(Equipment_list_item(name="Scorpion"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:300")

data_list.append(Equipment_list_item(name="Ballista"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:2000")

data_list.append(Equipment_list_item(name="Trebuchet"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:10000")

#	BOAT HULLS
#------------------------
data_list.append(Equipment_list_item(name="Small craft"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:0.05", upkeep="Materials:0.05", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=20, crew=5)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="Longship"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:0.1,Ship points:1", upkeep="Materials:0.1", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=50, crew=5)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="100 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:0.15,Ship points:1", upkeep="Materials:0.15", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=50, crew=20)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="250 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:0.5,Ship points:2", upkeep="Materials:0.5", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=100, crew=30)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="400 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:2,Ship points:5", upkeep="Materials:2", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=250, crew=60)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="600 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:5,Ship points:15", upkeep="Materials:5", move_cat = move_cat.index("Large boat"))
data_list[-1].set_values(transport=500, crew=100)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="800 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:10,Ship points:30", upkeep="Materials:10", move_cat = move_cat.index("Large boat"))
data_list[-1].set_values(transport=900, crew=200)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="1000 tonne hull"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:15,Ship points:50", upkeep="Materials:15", move_cat = move_cat.index("Large boat"))
data_list[-1].set_values(transport=1000, crew=300)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="Horse transport"))
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:0.5,Ship points:2", upkeep="Materials:0.5", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=120, large_transport=1, crew=30)
data_list[-1].set_values(move_speed=mspeed_list.index("Sail"), move_type=mtype_list.index("Sail"))


data_list.append(Equipment_list_item(name="Basic sub hull"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Boat hull"))
data_list[-1].set_values(cost="Materials:15,Ship points:45", upkeep="Materials:15,Ship points:45", move_cat = move_cat.index("Boat"))
data_list[-1].set_values(transport=20)


#	BALLOONS
#------------------------
data_list.append(Equipment_list_item(name="160kg Balloon"))
data_list[-1].set_values(category=cat_list.index("Balloon"))
data_list[-1].set_values(cost="Materials:1,Balloon points:20,(Ship points:Balloon points)", upkeep="Materials:1", move_cat = move_cat.index("Balloon"))
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Balloon"))

data_list.append(Equipment_list_item(name="350kg Balloon"))
data_list[-1].set_values(category=cat_list.index("Balloon"))
data_list[-1].set_values(cost="Materials:3,Balloon points:20,(Balloon points:Ship points)", upkeep="Materials:3", move_cat = move_cat.index("Balloon"))
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Balloon"))

data_list.append(Equipment_list_item(name="650kg Balloon"))
data_list[-1].set_values(category=cat_list.index("Balloon"))
data_list[-1].set_values(cost="Materials:6,Balloon points:45,(Ship points:Balloon points)", upkeep="Materials:6", move_cat = move_cat.index("Balloon"))
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Balloon"))

data_list.append(Equipment_list_item(name="1000kg Balloon"))
data_list[-1].set_values(category=cat_list.index("Balloon"))
data_list[-1].set_values(cost="Materials:10,Balloon points:50,(Ship points:Balloon points)", upkeep="Materials:10", move_cat = move_cat.index("Balloon"))
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Balloon"))

data_list.append(Equipment_list_item(name="1800kg Balloon"))
data_list[-1].set_values(category=cat_list.index("Balloon"))
data_list[-1].set_values(cost="Materials:15,Balloon points:75,(Ship points:Balloon points)", upkeep="Materials:15", move_cat = move_cat.index("Balloon"))
data_list[-1].set_values(move_speed=mspeed_list.index("Fly"), move_type=mtype_list.index("Balloon"))

#	Beasts
#------------------------
data_list.append(Equipment_list_item(name="Semyrid"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:1400", upkeep="Materials:1400", move_cat = move_cat.index("Horse"))
# $equipArray[$i]->description = 'They are giant winged birds, they have been described as bears with wings. Indeed, they have the body of a bear and with a wingspan capable of making short flights. Semyrid are violent creatures but respect strength.';
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

data_list.append(Equipment_list_item(name="Peyam"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:12000", upkeep="Materials:12000", move_cat = move_cat.index("Horse"))
data_list[-1].set_values(continent=get_cont("Rayti"))
# $equipArray[$i]->description = 'Giant flying beasts, their hide is like clay and hard to cut with swords. They posses two limbs just below the wing joints, these end in claws capable of ripping a man in two, it\'s hind legs are thick as trees and capable of supporting it\'s weight. Peyam are approximately 4m from head to the base of the tail, the tail itself is another 4m in length and ends in a giant club-link growth of bone. Peyam cannot fly long distances.';
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Horse"))

# data_list.append(Equipment_list_item(name="Qenki Wolves"))
# # data_list[-1].set_values(category=cat_list.index("Beast"))
# data_list[-1].set_values(cost="Materials:10", upkeep="Materials:10")
# $equipArray[$i]->description = 'They are half a meter longer than normal wolves and bulkier to keep in proportion. Their mouths are disproportionately large and they are capable of swallowing teenage humans. They are similar to wolves in every other way, their strength and endurance scaling up with their size but their speed and agility scaling down. They are found wherever there is food for them to eat, they live in packs. It is possible to capture entire packs in one area.';

data_list.append(Equipment_list_item(name="Omhettri"))
data_list[-1].set_values(category=cat_list.index("Beast"))
data_list[-1].set_values(cost="Materials:400", upkeep="Materials:400")
# $equipArray[$i]->description = 'They are about the size of a bear and resemble nothing more than a mass of fur. Omhettri however possess 12 "limbs" that appear to be a cross between a normal arm or leg and a tentacle. The limbs are about a metre in length and capable of pummeling a man to death. Omhettri have a mouth on their underside, they swallow their prey and digest every single part of them, they have been known to spit out people wearing metal armour. 
# 
# The most astounding thing about the Omhettri is that they can regenerate. "Limbs" grow back after a couple of days and even removing large portions of their main body will grow back in weeks. All their vital organs have redundant copies of themselves so the only way to kill an Omhettri is to completely carve it apart until it dies. Omhettri are found in hilly areas, normally hiding to avoid detection. Capturing Omhettri is hard but it can be done, generally only one is captured at a time in an area.';

data_list.append(Equipment_list_item(name="Qenki Wolves"))
data_list[-1].set_values(category=cat_list.index("Beast"))
data_list[-1].set_values(cost="Materials:10", upkeep="Materials:10")

data_list.append(Equipment_list_item(name="Giant metal suit"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:8000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Crushinator"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:40000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Angel of Steel"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:12000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="GPU"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:6000")

#	MORE BEASTS
#------------------------
data_list.append(Equipment_list_item(name="Murtnk"))
data_list[-1].set_values(category=cat_list.index("Beast"))
data_list[-1].set_values(cost="Materials:24", upkeep="Materials:24")
# $equipArray[$i]->description = 'They are a snake-like creature with a most amazing ability, they can wrap shadows around them to give them shape. While a Murtnk is in the shadow of the sun it will take on whatever appearance it chooses. Murtnk in reality are approximately 8 feet long and generally move with 4-6ft of their body held upwards. Their bite has a poison that enters the bloodstream and renders a victim unconscious.';

data_list.append(Equipment_list_item(name="Enkny"))
data_list[-1].set_values(category=cat_list.index("Beast"))
data_list[-1].set_values(cost="Materials:28", upkeep="Materials:28")
data_list[-1].set_values(terrain=get_terrain("Lowlands"))
# $equipArray[$i]->description = 'They are giant humans, however, they are lanky and their knuckles drag along the floor, giving the impression that they are stupid, they are not. Enkny fashion spears and are very good at hunting with them, they can throw far and accurately. Enkny primarily live anywhere there is enough for them to eat but never living near Fidwy or Humans if they can help it. It is easy to catch small groups of Enkny in one area.';

data_list.append(Equipment_list_item(name="Gorquithur"))
data_list[-1].set_values(category=cat_list.index("Beast"))
data_list[-1].set_values(cost="Materials:32", upkeep="Materials:32")
data_list[-1].set_values(terrain=get_terrain("Lowlands"))
# $equipArray[$i]->description = 'They are a creature that looks like it was designed as a weapon of war by some race long forgotten. Gorquithur are simply bears with boney spines protruding from the back of their limbs, head and body; much like a hedgehog. Gorquithur have a massive appetite and can run very fast for short distances of time. They are also stronger than bears but not by a lot. Very temporary friendship with a Gorquithur can be bought with food. Gorquithur are found only in small numbers.';

# Todo, remove these
data_list.append(Equipment_list_item(name="Grak beetles"))
data_list[-1].set_values(category=cat_list.index("Seabourne mount"))
data_list[-1].set_values(cost="Materials:18", upkeep="Materials:18")
# $equipArray[$i]->description = 'Grak beetles are like massive water bugs. They congregate along the shores of the Indrin isle, conveniently within the territories of the kliktaren. The creatures look much like blue-shelled wide-bodied beetles possessing six-legs. At the ends of the legs are webbed claws that they use to propel themselves through the water and they can dive under as well. They have compound eyes that enable them to see underwater as well as out of water. They have grinding mandibles they use to consume small fish and seaweed as well as plants and cacti. Grak beetles can breathe underwater.';
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Sail"))

data_list.append(Equipment_list_item(name="Toruk bugs"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:18", upkeep="Materials:18")
data_list[-1].set_values(continent=get_cont("Indrin"))
# $equipArray[$i]->description = 'Toruk bugs are fairly sedentary insectoid creatures that have a number of physical characteristics that aren\'t typical of a giant bug. They have a course, shaggy fur that grows from their exoskeleton at the neck, back and lower thorax. They have six legs and wide, multi-eyed heads with tusk-like mandibles jutting from an oversized lower jaw. They naturally form herds and reside in the same regions near many Kliktaren hive cities and roving tribes. Toruk bugs are only hostile when their tribal brethren are threatened or their herd is in danger. They will attempt to trample or gouge aggressors but ultimately will do this to drive them away or to get away themselves.';

data_list.append(Equipment_list_item(name="Drake wasps"))
data_list[-1].set_values(category=cat_list.index("Mount"))
data_list[-1].set_values(cost="Materials:40", upkeep="Materials:40", move_cat = move_cat.index("Flight"))
data_list[-1].set_values(continent=get_cont("Indrin"))
# data_list[-1].set_values(continent=get_cont("Indrin"), terrain=get_terrain("Lowlands"))
# $equipArray[$i]->description = 'These are 3 or 4m long insectoid creatures with some oddly draconian aspects, particularly in the head and along the vertebrae. They have small claws too that look like they belong on a drake instead of an insect. The eyes look like slightly larger drake eyes but still compound like an insect and their backs have a definite spiky ridge all the way to the tail. These features are even more pronounced in the Warriors and Queens.';
data_list[-1].set_values(move_speed=mspeed_list.index("Ride"), move_type=mtype_list.index("Wing"))



#	MORE CUSTOM STUFF
#------------------------
data_list.append(Equipment_list_item(name="Terjzion railgun"))
data_list[-1].set_values(category=cat_list.index("Custom"), public=False)
data_list[-1].set_values(cost="Materials:8,Iron:1", upkeep="Materials:8,Iron:Materials=1")

data_list.append(Equipment_list_item(name="Iron bomb"))
data_list[-1].set_values(category=cat_list.index("Custom"), public=False)
data_list[-1].set_values(cost="Materials:5", upkeep="Materials:5")

data_list.append(Equipment_list_item(name="Sloan hovercraft"))
data_list[-1].set_values(category=cat_list.index("Boat hull"), public=False)
data_list[-1].set_values(cost="Materials:0.3,Balloon points:3,(Ship points:Balloon points)", upkeep="Materials:0.3")
data_list[-1].set_values(transport=40, crew=10)

data_list.append(Equipment_list_item(name="Revenant mk I"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:40000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Revenant mk II"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:44000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Ankvor tank"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:96000,Iron:Materials/8")

data_list.append(Equipment_list_item(name="Kiadu'Rhei"))
data_list[-1].set_values(public=False, description="")
data_list[-1].set_values(category=cat_list.index("Custom"))
data_list[-1].set_values(cost="Materials:8000,Iron:Materials/4")

data_list.append(Equipment_list_item(name="Polybolos on a wagon"))
data_list[-1].set_values(category=cat_list.index("Siege engine"))
data_list[-1].set_values(cost="Materials:700", public=False)

for e in data_list:
	if e == "": continue
	e.check()

data_dict = {}
for i, d in enumerate(data_list): data_dict[i] = d