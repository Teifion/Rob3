import database
import collections

class Goods (object):
	def __init__(self):
		super(Goods, self).__init__()
		
		self.name = ""
		
		self.terrain	= collections.defaultdict(1)
		self.continent	= collections.defaultdict(1)
		self.supply		= collections.defaultdict(1)
		
		self.demand		= lambda x: x
		self.investment	= lambda x: 1
		
		self.public		= True
		
goods_list = []

#	FOODS
#------------------------
# WHEAT
g = Goods("Wheat")
g.terrain["Lowlands"] = 1.3
g.demand = lambda x: x*0.33
goods_list.append(g)

# CATTLE
g = Goods("Livestock")
g.terrain["Highlands"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

# RICE
g = Goods("Rice")
g.terrain["Swamps"] = 1.3
g.demand = lambda x: x*0.33
goods_list.append(g)


g = Goods("FOOD")
g.public = False
goods_list.append(g)

g = Goods("FOOD")
g.public = False
goods_list.append(g)

g = Goods("FOOD")
g.public = False
goods_list.append(g)

g = Goods("FOOD")
g.public = False
goods_list.append(g)

g = Goods("FOOD")
g.public = False
goods_list.append(g)

#	BASIC MATERIALS
#------------------------
g = Goods("Bricks")
g.terrain["Mountains"] = 1
g.supply["Stone"] = 1.5
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Timbers")
g.terrain["Mountains"] = 1
g.supply["Stone"] = 1.5
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Iron ingots")
g.terrain["Mountains"] = 1
g.supply["Stone"] = 1.5
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

g = Goods("BASIC")
g.public = False
goods_list.append(g)

#	MANUFACTURED GOODS
#------------------------
g = Goods("Silk")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Tools")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Glassware")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

g = Goods("MANUFACTURED")
g.public = False
goods_list.append(g)

#	LUXURY GOODS
#------------------------
g = Goods("Art")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Wine")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("Jewelry")
g.terrain["Swamps"] = 1.3
# g.continent[""] = 1
# g.supply[""] = 1
g.demand = lambda x: x*0.33
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)

g = Goods("LUXURY")
g.public = False
goods_list.append(g)