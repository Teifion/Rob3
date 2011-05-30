import database
from classes import res_dict
from data_classes import equipment
from queries import equipment_q

categories = (
	"Solo unit",
	"Melee infantry",
	"Ranged infantry",
	"Mixed infantry",
	"Melee cavalry",
	"Ranged cavalry",
	"Mixed cavalry",
	
	"Ship",
	"Airship",
)

weapon_categories = (
	'Melee',
	'Ranged',
	'Melee and Ranged',
	'Neither',
)

armour_categories = (
	'Unarmoured',
	'Leather',
	'Mail',
	'Plate',
)

move_categories = (
	'Foot',
	'Mule',
	'Horse',
	'Flight',
	'Boat',
	'Large boat',
	'Balloon',
)

training_categories = (
	'Low',
	'Normal',
	'High',
)

class Unit (database.DB_connected_object):
	table_info = {
		"Name":			"units",
		"Indexes":		{
			"name": "name",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Varchar_field("name",			max_length=40),
			
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Integer_field("size"),
			database.Boolean_field("available"),
			
			database.Integer_field("move_type"),
			database.Integer_field("move_speed"),
			
			database.Integer_field("type_cat"),
			database.Integer_field("transport"),
			database.Integer_field("crew", default=1),
			
			database.Integer_field("weapon_cat"),
			database.Integer_field("armour_cat"),
			database.Integer_field("move_cat"),
			database.Integer_field("training_cat"),
			
			database.Varchar_field("description",		max_length=255),
			database.Varchar_field("equipment_string",	max_length=255),
		),
	}
	
	def __init__(self, row = {}):
		super(Unit, self).__init__(row)
		
		# Other
		self.equipment			= []
		self.costs				= {}
		self.costs_breakdown	= {}
		
		self.cost_count = 0
	
	def get_equipment(self, cursor, force_requery=False):
		"""Sets the dictionary of our resources"""
		if self.equipment != [] and force_requery == False:
			return self.equipment
		
		self.equipment = []
		
		query = "SELECT equipment FROM unit_equipment WHERE unit = %d" % (self.id)
		try: cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		for row in cursor:
			self.equipment.append(row['equipment'])
		
		return self.equipment
	
	
	def get_cost(self, cursor=None, the_world=None, equipment_dict=None, breakdown_mode=False, force_requery=False):
		# Done to prevent it using the same equipment more than once
		self.equipment = list(set(self.equipment))
		
		if self.costs != {} and not force_requery:
			if breakdown_mode:
				return self.costs_breakdown
			else:
				return self.costs
		
		if the_world != None:
			return self._get_cost_with_world(the_world, breakdown_mode)
		elif cursor != None:
			if equipment_dict != None:
				return self._get_cost_with_dict(cursor, equipment_dict, breakdown_mode)
			else:
				return self._get_cost_with_cursor(cursor, breakdown_mode)
		else:
			raise Exception("Both cursor and the_world were None")
	
	def _get_cost_with_cursor(self, cursor, breakdown_mode):
		if self.equipment == []:
			self.get_equipment(cursor)
		
		return self._get_cost(equipment_q.get_all_equipment(cursor), breakdown_mode)
	
	def _get_cost_with_dict(self, cursor, equipment_dict, breakdown_mode):
		if self.equipment == []:
			self.get_equipment(cursor)
		
		return self._get_cost(equipment_dict, breakdown_mode)
	
	def _get_cost_with_world(self, the_world, breakdown_mode):
		if self.equipment == []:
			self.get_equipment(the_world.cursor)
		
		return self._get_cost(the_world.equipment(), breakdown_mode)
	
	def _get_cost(self, equipment_dict, breakdown_mode):
		"""Iron cost refers to the cost _with_ Iron"""
		
		self.costs = {}
		self.costs_breakdown = {}
		
		breakdown_cost		= []
		breakdown_upkeep	= []
		
		# Res dict has changed so this part needs a rewrite
		material_cost	= res_dict.Res_dict("")
		iron_cost		= res_dict.Res_dict("")
		
		material_upkeep	= res_dict.Res_dict("")
		iron_upkeep		= res_dict.Res_dict("")
		
		# Useful to know for upkeep purposes
		is_ship = False
		for e in self.equipment:
			if equipment_dict[e].category == equipment.cat_list.index("Boat hull"):
				is_ship = True
		
		for e in self.equipment:
			# Training
			if is_ship and equipment_dict[e].category == equipment.cat_list.index("Training"):
				continue
			
			# Get the res dicts for this item
			equip_cost		= res_dict.Res_dict(equipment_dict[e].cost)
			equip_cost_i	= res_dict.Res_dict(equipment_dict[e].cost)
			equip_cost.flatten("Iron:1")
			
			equip_upkeep	= res_dict.Res_dict(equipment_dict[e].upkeep)
			equip_upkeep_i	= res_dict.Res_dict(equipment_dict[e].upkeep)
			equip_upkeep.flatten("Iron:1")
			
			# Update the running totals
			material_cost += equip_cost
			iron_cost += equip_cost_i
			
			material_upkeep += equip_upkeep
			iron_upkeep += equip_upkeep_i
			
			# Print cost
			breakdown_cost.append("+ %s: %s/%s (Sub total: %s/%s)" % (
				equipment_dict[e].name,
				equip_cost.get("Materials"),
				equip_cost_i.get("Materials"),
				material_cost.get("Materials"),
				iron_cost.get("Materials"),
			))
			
			# Print upkeep
			breakdown_upkeep.append("+ %s: %s/%s (Sub total: %s/%s)" % (
				equipment_dict[e].name,
				equip_upkeep.get("Materials"),
				equip_upkeep_i.get("Materials"),
				material_upkeep.get("Materials"),
				iron_upkeep.get("Materials"),
			))
		
		for e in self.equipment:
			if equipment_dict[e].cost_multiplier != '':
				multiplier_dict = res_dict.Res_dict(equipment_dict[e].cost_multiplier)
				multiplier_dict_i = res_dict.Res_dict(equipment_dict[e].cost_multiplier)
				multiplier_dict.flatten("Iron:1")
				
				# Initial cost multiplier
				material_cost *= multiplier_dict
				iron_cost *= multiplier_dict_i
				
				# Cost breakdown
				breakdown_cost.append("* %s: %s/%s (Sub total: %s/%s)" % (
					equipment_dict[e].name,
					multiplier_dict.get("Materials"),
					multiplier_dict_i.get("Materials"),
					material_cost.get("Materials"),
					iron_cost.get("Materials"),
					))
			
			if equipment_dict[e].upkeep_multiplier != '':
				multiplier_dict = res_dict.Res_dict(equipment_dict[e].upkeep_multiplier)
				multiplier_dict_i = res_dict.Res_dict(equipment_dict[e].upkeep_multiplier)
				multiplier_dict.flatten("Iron:1")
				
				# Upkeep multiplier
				material_upkeep *= multiplier_dict
				iron_upkeep *= multiplier_dict_i
				
				# Upkeep breakdown
				breakdown_upkeep.append("* %s: %s/%s (Sub total: %s/%s)" % (
					equipment_dict[e].name,
					multiplier_dict.get("Materials"),
					multiplier_dict_i.get("Materials"),
					material_upkeep.get("Materials"),
					iron_upkeep.get("Materials"),
					))
		
		# Now set the values
		self.costs = {
			"material_cost": material_cost,
			"iron_cost": iron_cost,
			"material_upkeep": material_upkeep,
			"iron_upkeep": iron_upkeep,
		}
		
		# if self.id == 880:
		# 	print("")
		# 	print(material_cost)
		# 	print(iron_cost)
		# 	print("%s = %s" % (equipment_dict[29].name, res_dict.Res_dict(equipment_dict[29].cost)))
		# 	print("%s = %s" % (equipment_dict[25].name, res_dict.Res_dict(equipment_dict[25].cost)))
		# 	print("%s = %s" % (equipment_dict[50].name, res_dict.Res_dict(equipment_dict[50].cost)))
		# 	print("%s = %s" % (equipment_dict[3].name, res_dict.Res_dict(equipment_dict[3].cost)))
		# 	print("%s = %s" % (equipment_dict[3].name, res_dict.Res_dict(equipment_dict[3].cost_multiplier)))
		
		self.costs_breakdown = {
			"cost":		breakdown_cost,
			"upkeep":	breakdown_upkeep,
		}
		
		if breakdown_mode == True:
			return self.costs_breakdown
		
		return self.costs

Unit_equipment = {
	"Name":			"unit_equipment",
	"Indexes":		{
	},
	"Fields":		(
		database.Integer_field("unit", 		primary_key=True, foreign_key=("units", "id")),
		database.Integer_field("equipment",	primary_key=True),
	),
}