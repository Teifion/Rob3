import database

# Discrete = Normal counting
# Boolean = You have it or you don't

category = {
	"Standard":				1,
	"Supply":				2,
	"Point":				3,
	"Specialist point":		4,
	"Map terrain feature":	5,
}

class Resource (database.DB_list_row):
	"""docstring for Building"""
	def __init__(self):
		super(Resource, self).__init__()
		self.set_values(reset=False, tradable=True, map_supply=0)

data_list = []
data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Materials")
data_list[-1].set_values(type="discrete", category=category["Standard"])

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Food")
data_list[-1].set_values(type="discrete", reset=True, category=category["Standard"])

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Tech points")
data_list[-1].set_values(type="discrete", reset=True, category=category["Point"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Spell points")
data_list[-1].set_values(type="discrete", reset=True, category=category["Point"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Ship points")
data_list[-1].set_values(type="discrete", reset=True, category=category["Point"])

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Iron", type="boolean", map_supply=1, category=category["Supply"])
data_list[-1].set_values(reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Stone", type="boolean", map_supply=1, category=category["Supply"])
data_list[-1].set_values(reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Wood", type="boolean", map_supply=1, category=category["Supply"])
data_list[-1].set_values(reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Fertile lands", type="boolean", map_supply=1, category=category["Map terrain feature"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Giant hill", type="boolean", map_supply=1, category=category["Map terrain feature"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Natural harbour", type="boolean", map_supply=1, category=category["Map terrain feature"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Gateway to Enkhingi", type="boolean", map_supply=1, category=category["Map terrain feature"])
data_list[-1].set_values(tradable=False)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Light points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Dark points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Abjuration points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Destruction points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Daemonic points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Necromancy points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Balloon points", type="discrete", category=category["Point"])
data_list[-1].set_values(reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Alchemy points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)

data_list.append(Resource())
data_list[-1].set_values(id=len(data_list)-1)
data_list[-1].set_values(name="Enchantment points", type="discrete", category=category["Point"])
data_list[-1].set_values(tradable=False, reset=True)


data_dict = {}
for i, d in enumerate(data_list): data_dict[i] = d

data_dict_n = {}
data_dict_n_l = {}
for i, d in enumerate(data_list):
	data_dict_n[d.name] = i
	data_dict_n_l[d.name.lower()] = i