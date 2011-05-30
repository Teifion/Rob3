from pages import common
import math
import database
from classes import team

friendly_border = team.border_states.index("Open")
allied_border = team.border_states.index("Allied")

class Mission (object):
	def __init__(self, name, func, acc):
		super(Mission, self).__init__()
		self.name			= name
		self.get_results	= func
		self.acc_type		= acc
	
	def __call__(self, the_world, team_id, area, radius):
		success = self.accuracy(the_world, team_id, area, radius)
		
		return self.get_results(the_world, area, radius, success)
	
	def accuracy(self, the_world, team_id, area, radius):
		return accuracy_types[self.acc_type](the_world, team_id, area, radius)


def _certain(the_world, team_id, area, radius):
	return 1

def _near_certain(the_world, team_id, area, radius):
	return 0.99

def _impossible(the_world, team_id, area, radius):
	return 0

def _near_impossible(the_world, team_id, area, radius):
	return 0.01

# Your obs score divided by their obs score
def _basic_observation(the_world, team_id, area, radius):
	your_ops, their_ops = _op_lists(the_world, team_id, area, radius)
	# Allied aid is the sum of their observation
	your_score = 0
	for o in your_ops:
		age = 1 + math.sqrt(max(common.current_turn() - o.arrival, 1)) * 0.1
		your_score += o.observation * math.sqrt(o.size) * age
	
	# Hostile score is the sum of the squares of observation
	their_score = 0
	for o in their_ops:
		age = 1 + math.sqrt(max(common.current_turn() - o.arrival, 1)) * 0.2# Age counts for more when it's home ground
		their_score += math.sqrt(o.observation) * math.sqrt(o.size) * age
	
	your_score = sum([o.observation * math.sqrt(o.size) for o in your_ops]) + 1
	their_score = sum([o.observation * math.sqrt(o.size) for o in their_ops]) + 1
	
	return your_score/their_score


# Builds a list of the ops for yourself and any ops that'd report you if they saw you
def _op_lists(the_world, team_id, area, radius):
	relations	= the_world.relations()# [Host][Visitor]
	op_dict = the_world.operatives()
	op_list = the_world.operatives_in_area(area, radius)
	team_dict = the_world.teams()
	
	your_ops = []
	their_ops = []
	
	for o in op_list:
		the_op = op_dict[o]
		if the_op.died > 0: continue
		
		# They're you
		if the_op.team == team_id:
			your_ops.append(the_op)
		
		# They're at least seggregated
		elif relations.get(the_op.team, {}).get(team_id, {}).get('border', team_dict[the_op.team].default_borders) < friendly_border:
			their_ops.append(the_op)
		
		# They are allied with you
		elif relations.get(the_op.team, {}).get(team_id, {}).get('border', team_dict[the_op.team].default_borders) >= allied_border:
			your_ops.append(the_op)
	
	return your_ops, their_ops

def _op_lists_city(the_world, team_id, city_id):
	relations	= the_world.relations()# [Host][Visitor]
	op_dict = the_world.operatives()
	op_list = the_world.operatives_in_city(city_id)
	team_dict = the_world.teams()
	
	your_ops = []
	their_ops = []
	
	for o in op_list:
		the_op = op_dict[o]
		if the_op.died > 0: continue
		
		# They're you
		if the_op.team == team_id:
			your_ops.append(the_op)
		
		# They're at least seggregated
		elif relations.get(the_op.team, {}).get(team_id, {}).get('border', team_dict[the_op.team].default_borders) < friendly_border:
			their_ops.append(the_op)
		
		# They are allied with you
		elif relations.get(the_op.team, {}).get(team_id, {}).get('border', team_dict[the_op.team].default_borders) >= allied_border:
			your_ops.append(the_op)
	
	return your_ops, their_ops

accuracy_types = {
	"Certain":				_certain,
	"Impossible":			_impossible,
	
	"Near certain":			_near_certain,
	"Near impossible":		_near_impossible,
	
	"Basic observation":	_basic_observation,
	
	"Default":				_basic_observation,
}

class Spy_report (database.DB_connected_object):
	table_info = {
		"Name":			"spy_reports",
		"Indexes":		{
			"turn": "turn",
			"team":	"team",
		},
		"Fields":		(
			database.Serial_field("id",				primary_key=True),
			database.Integer_field("mission",		foreign_key=("missions", "id")),
			database.Integer_field("team",			foreign_key=("teams", "id")),
			database.Integer_field("enemy",			foreign_key=("teams", "id")),
			database.Integer_field("city"),
			database.Integer_field("turn"),
			
			database.Varchar_field("report_type",	max_length=40),
			database.Text_field("content"),
		),
	}
	
	def __init__(self, row = {}):
		super(Spy_report, self).__init__(row)
	
def empty_report(row = {}):
	row['content'] = row.get("Content", "")
	
	return Spy_report(row)