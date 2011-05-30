import database
from data_classes import monster

cat_lookup = monster.categories.index

class Monster (database.DB_list_row):
	defaults = {
		"min_men":		0,
		"max_men":		1,
		
		"min_budget":	0,
		"max_budget":	1,
		
		"max_amount":	10,
	}
	
	def __init__(self, **kwargs):
		super(Monster, self).__init__(**kwargs)
	
	def check(self):
		pass

data_list = []
data_list.append(Monster(
	name			= "Hydra",
	category		= cat_lookup("Big"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 12
	min_budget	= 12,	max_budget	= 36,
	max_amount	= 3,
))

data_list.append(Monster(
	name			= "Karithor",
	category		= cat_lookup("Big"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 5
	min_budget	= 10,	max_budget	= 40,
	max_amount	= 8,
))

data_list.append(Monster(
	name			= "Troll",
	category		= cat_lookup("Herded"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 1
	min_budget	= 10,	max_budget	= 100,
	max_amount	= 100,
))

data_list.append(Monster(
	name			= "Gorquithor",
	category		= cat_lookup("Herded"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 2.4
	min_budget	= 10,	max_budget	= 57.6,
	max_amount	= 24,
))

data_list.append(Monster(
	name			= "Costal salamander",
	category		= cat_lookup("Ridden"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 1
	min_budget	= 10,	max_budget	= 200,
	max_amount	= 200,
))

data_list.append(Monster(
	name			= "Murdaphant",
	category		= cat_lookup("Ridden"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 5
	min_budget	= 10,	max_budget	= 20,
	max_amount	= 4,
))

data_list.append(Monster(
	name			= "Tishrashi condor",
	category		= cat_lookup("Flying"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 1.2
	min_budget	= 10,	max_budget	= 48,
	max_amount	= 40,
))

data_list.append(Monster(
	name			= "Gryphon",
	category		= cat_lookup("Flying"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 3
	min_budget	= 12,	max_budget	= 72,
	max_amount	= 24,
))

data_list.append(Monster(
	name			= "Peyam",
	category		= cat_lookup("Flying"),
	good_terrain	= "",
	bad_terrain		= "",
	none_terrain	= "",
	
	min_men		= 30,	max_men		= 120,
	
	# Materials per monster: 20
	min_budget	= 10,	max_budget	= 40,
	max_amount	= 2,
))
