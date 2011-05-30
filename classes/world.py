import re
import database
import collections
from pages import common
from queries import city_q, team_q, unit_q, army_q, operative_q, squad_q, campaign_q, battle_q
from queries import artefact_q, wonder_q, player_q, power_q, mapper_q, ti_q
from queries import building_q, deity_q, evolution_q, servant_q, tech_q, spell_q, equipment_q, monster_q, trait_q

class World (object):
	"""Used to store states of things, useful as a cache for things such as the TI but also as a state holder for things such as orders."""
	
	def __init__(self, cursor):
		super(World, self).__init__()
		
		self.cursor = cursor
		self.built_from_team			= []
		self.built_lookup_from_team		= []
		self._relations					= {}
		self._border_history			= {}
		
		self.mass_get_checker			= set()
		self.suppliers					= {}
		
		# Teams
		self._teams					= {}
		self._teams_lookup			= {}
		self._teams_lookup_l		= {}
		self._active_teams			= {}
		self._json_ti				= {}
		
		# Armies
		self._armies				= {}
		self._armies_from_team		= {}
		self._armies_lookup			= {}
		self._armies_lookup_l		= {}
		self._armies_lookup_from_team	= {}# Assumed to be lower case
		self._garrisons				= {}
		
		# Artefacts
		self._artefacts				= {}
		self._artefacts_lookup		= {}
		self._artefacts_lookup_l	= {}
		self._cities_with_artefacts	= set()
		
		# Buildings
		self._buildings				= {}
		self._buildings_lookup		= {}
		self._buildings_lookup_l	= {}
		self._building_requirements	= {}
		
		# Battles
		self._battles				= {}
		self._battles_from_campaign	= {}
		
		# Cities
		self._cities				= {}
		self._live_cities			= {}
		self._cities_from_team		= {}
		self._live_cities_from_team	= {}
		self._cities_lookup			= {}
		self._cities_lookup_l		= {}
		
		# Campaigns
		self._campaigns				= {}
		self._campaigns_lookup		= {}
		self._campaigns_lookup_l	= {}
		self._campaigns_from_turn	= {}
		
		# Monsters
		self._monsters				= {}
		self._monsters_lookup		= {}
		self._monsters_lookup_l		= {}
		
		# Deities
		self._deities				= {}
		self._deities_lookup		= {}
		self._deities_lookup_l		= {}
		
		# Equipment
		self._equipment				= {}
		self._equipment_lookup		= {}
		self._equipment_lookup_l	= {}
		
		# Evolutions
		self._evolutions			= {}
		self._evolutions_lookup		= {}
		self._evolutions_lookup_l	= {}
		
		# Players
		self._players				= {}
		self._players_from_team		= {}
		
		self._kills					= []
		self._kills_from_player		= {}
		self._kills_from_camp		= {}
		self._kills_from_turn		= {}
		
		# Powers
		self._powers				= {}
		self._powers_lookup			= {}
		self._powers_lookup_l		= {}
		
		# Operatives
		self._operatives			= {}
		self._operatives_lookup		= {}
		self._operatives_lookup_l	= {}
		self._operatives_from_team	= {}
		
		# Servants
		self._servants				= {}
		self._servants_lookup		= {}
		self._servants_lookup_l		= {}
		
		# Spells
		self._spells				= {}
		self._spells_lookup			= {}
		self._spells_lookup_l		= {}
		
		# Squads
		self._squads				= {}
		self._squads_from_team		= {}
		self._squads_lookup			= {}
		self._squads_lookup_l		= {}
		self._squads_lookup_from_army = {}
		
		# Techs
		self._techs					= {}
		self._techs_lookup			= {}
		self._techs_lookup_l		= {}
		
		# Traits
		self._traits				= {}
		self._traits_lookup			= {}
		self._traits_lookup_l		= {}
		
		# Units
		self._units					= {}
		self._units_from_team		= {}
		self._units_lookup			= {}
		self._units_lookup_l		= {}
		self._units_lookup_from_team		= {}
		
		# Wonders
		self._wonders				= {}
		self._wonders_lookup		= {}
		self._wonders_lookup_l		= {}
		self._cities_with_wonders	= set()
	
	# Other
	def relations(self, force_requery=False):
		if not force_requery and self._relations != {}:
			return self._relations
		
		self._relations = team_q.get_relations(self.cursor)
		return self._relations
	
	def border_history(self, force_requery=False):
		if not force_requery and self._border_history != {}:
			return self._border_history
		
		self._border_history = team_q.get_border_history(self.cursor)
		return self._border_history
	
	def get_border(self, host, visitor, force_requery=False):
		self.teams(force_requery)
		self.relations(force_requery)
		
		if host in self._relations:
			if visitor in self._relations[host]:
				if 'border' in self._relations[host][visitor]:
					return self._relations[host][visitor]['border']
		
		return self._teams[host].default_borders
		
		# return self.relations(force_requery).get(host, {}).get(visitor, {}).get('border', self._teams[host].default_borders)
	
	def get_taxes(self, host, visitor, force_requery=False):
		self.teams(force_requery)
		self.relations(force_requery)
		
		if host in self._relations:
			if visitor in self._relations[host]:
				if 'taxes' in self._relations[host][visitor]:
					return self._relations[host][visitor]['taxes']#, self._teams[host].default_taxes)
		
		return self._teams[host].default_taxes
		
		# return self.relations(force_requery).get(host, {}).get(visitor, {}).get('taxes', self._teams[host].default_taxes)
	
	def prep_for_orders(self):
		"""Runs a set of prep functions for orders"""
		# player_q.mass_get_player_powers(self.cursor, self._players)
		mapper_q.get_terrain(self.cursor, 0, 0)
		
		self.teams()
		# team_q.mass_get_team_deities(self.cursor, self._teams)
		team_q.mass_get_team_spells(self.cursor, self._teams)
		team_q.mass_get_team_techs(self.cursor, self._teams)
		# team_q.mass_get_team_resources(self.cursor, self._teams)
		self.mass_get_team_resources()
		team_q.mass_get_team_evolutions(self.cursor, self._teams)
		
		self.buildings()
		self.cities()
		city_q.mass_get_city_buildings(self.cursor, self._cities)
		# city_q.mass_get_city_artefacts(self.cursor, self._cities)
		# city_q.mass_get_city_wonders(self.cursor, self._cities)
		
		# squad_q.mass_get_squads(self.cursor, self._armies)
		
		unit_q.mass_get_unit_equipment(self.cursor, self._units)
		
		for k, v in self._buildings.items():
			if v.upgrades > -1:
				if v.upgrades not in self._building_requirements:
					self._building_requirements[v.upgrades] = []
				
				self._building_requirements[v.upgrades].append(k)
	
	def prep_for_to(self):
		self.teams()
		self.cities()
		
		team_q.mass_get_team_evolutions(self.cursor, self._teams)
		team_q.mass_get_team_deities(self.cursor, self._teams)
		
		city_q.mass_get_city_artefacts(self.cursor, self._cities)
		city_q.mass_get_city_wonders(self.cursor, self._cities)
	
	def prep_for_stats(self):
		pass
	
	def prep_for_oh(self):
		"""Runs a set of prep functions for the OH"""
		
		self.teams()
		team_q.mass_get_team_spells(self.cursor, self._teams)
		team_q.mass_get_team_techs(self.cursor, self._teams)		
		# team_q.mass_get_team_resources(self.cursor, self._teams)
		self.mass_get_team_resources()
		
		self.buildings()
		self.cities()
		city_q.mass_get_city_buildings(self.cursor, self._cities)
		city_q.mass_get_city_artefacts(self.cursor, self._cities)
		city_q.mass_get_city_wonders(self.cursor, self._cities)
		
		self.armies()
		# squad_q.mass_get_squads(self.cursor, self._armies)
		self.mass_get_army_squads()
		
		self.units()
		unit_q.mass_get_unit_equipment(self.cursor, self._units)
		
		for k, v in self._buildings.items():
			if v.upgrades > -1:
				if v.upgrades not in self._building_requirements:
					self._building_requirements[v.upgrades] = []
				
				self._building_requirements[v.upgrades].append(k)
	
	def prep_for_ti(self):
		self.players()
		player_q.mass_get_player_powers(self.cursor, self._players)
		
		self.teams()
		team_q.mass_get_team_deities(self.cursor, self._teams)
		team_q.mass_get_team_spells(self.cursor, self._teams)
		team_q.mass_get_team_techs(self.cursor, self._teams)
		team_q.mass_get_team_stats(self.cursor, self._teams, common.current_turn())
		team_q.mass_get_team_stats(self.cursor, self._teams, common.current_turn()-1)
		team_q.mass_get_team_stats(self.cursor, self._teams, common.current_turn()-2)
		
		self.cities()
		city_q.mass_get_city_buildings(self.cursor, self._cities)
		city_q.mass_get_city_artefacts(self.cursor, self._cities)
		city_q.mass_get_city_wonders(self.cursor, self._cities)
		
		self.armies()
		# squad_q.mass_get_squads(self.cursor, self._armies)
		self.mass_get_army_squads()
		self.mass_get_army_monsters()
		
		self.units()
		unit_q.mass_get_unit_equipment(self.cursor, self._units)
	
	def prep_for_start(self):
		self.teams()
		team_q.mass_get_team_deities(self.cursor, self._teams)
	
	
	#	ORDER LOOKUPS
	#------------------------
	def building_requirements(self):
		# Assumes that it's been built already
		return self._building_requirements
	
	#	LOOKUPS
	#------------------------
	def _lookup(self, name, lower=False, force_requery=False):
		lname = '_%s_lookup' % name
		llname = '_%s_lookup_l' % name
		dname = '_%s' % name
		
		# Check cache
		if not force_requery and self.__dict__[lname] != {}:
			if lower:
				return self.__dict__[llname]
			else:
				return self.__dict__[lname]
		
		# First lets check we've got the dictionary itself
		if force_requery or self.__dict__[dname] == {}:
			self._dict(name, True)
		
		# Iterate and build name lookup
		self.__dict__[lname] = {}
		for k, v in self.__dict__[dname].items():
			self.__dict__[lname][v.name] = k
			self.__dict__[llname][v.name.lower()] = k
		
		# Return
		if lower:
			return self.__dict__[llname]
		else:
			return self.__dict__[lname]
	
	def artefacts_lookup(self, lower=False, force_requery=False):
		return self._lookup('artefacts', lower, force_requery)
	
	def armies_lookup(self, lower=False, force_requery=False):
		return self._lookup('armies', lower, force_requery)
	
	def buildings_lookup(self, lower=False, force_requery=False):
		return self._lookup('buildings', lower, force_requery)
	
	def monsters_lookup(self, lower=False, force_requery=False):
		return self._lookup('monsters', lower, force_requery)
	
	def cities_lookup(self, lower=False, force_requery=False):
		return self._lookup('cities', lower, force_requery)
	
	def campaigns_lookup(self, lower=False, force_requery=False):
		return self._lookup('campaigns', lower, force_requery)
	
	def deities_lookup(self, lower=False, force_requery=False):
		return self._lookup('deities', lower, force_requery)
	
	def equipment_lookup(self, lower=False, force_requery=False):
		return self._lookup('equipment', lower, force_requery)
	
	def evolutions_lookup(self, lower=False, force_requery=False):
		return self._lookup('evolutions', lower, force_requery)
	
	def operatives_lookup(self, lower=False, force_requery=False):
		return self._lookup('operatives', lower, force_requery)

	def powers_lookup(self, lower=False, force_requery=False):
		return self._lookup('powers', lower, force_requery)

	def spells_lookup(self, lower=False, force_requery=False):
		return self._lookup('spells', lower, force_requery)
	
	def techs_lookup(self, lower=False, force_requery=False):
		return self._lookup('techs', lower, force_requery)
	
	def teams_lookup(self, lower=False, force_requery=False):
		return self._lookup('teams', lower, force_requery)
	
	def squads_lookup(self, lower=False, force_requery=False):
		return self._lookup('squads', lower, force_requery)
	
	def traits_lookup(self, lower=False, force_requery=False):
		return self._lookup('traits', lower, force_requery)
	
	def units_lookup(self, lower=False, force_requery=False):
		return self._lookup('units', lower, force_requery)

	def wonders_lookup(self, lower=False, force_requery=False):
		return self._lookup('wonders', lower, force_requery)
	
	#	BY TEAM GROUPING LOOKUPS, useful for when some teams may name some things the same way
	#------------------------
	def _build_lookup_from_team(self, name, force_requery=False):
		dname = '_%s' % name
		lname = '_%s_lookup_from_team' % name
		
		self.teams()
		self._dict(name, force_requery)
		
		for k, v in self.__dict__[dname].items():
			if v.team not in self.__dict__[lname]:
				self.__dict__[lname][v.team] = collections.OrderedDict()
			
			self.__dict__[lname][v.team][v.name.lower()] = k
		
		self.built_lookup_from_team.append(name)
	
	def _lookup_all_from_team(self, name, force_requery=False):
		lname = '_%s_lookup_from_team' % name
		
		if not force_requery and name in self.built_lookup_from_team:
			return self.__dict__[lname]
		
		self._build_lookup_from_team(name, force_requery)
		return self.__dict__[lname]
	
	def _lookup_from_team(self, name, team_id, force_requery=False):
		lname = '_%s_lookup_from_team' % name
		
		# Get all the ones for it
		if team_id == -1:
			return self._lookup_all_from_team(name, force_requery)
		
		if not force_requery and name in self.built_lookup_from_team:
			return self.__dict__[lname].get(team_id, {})
		
		self._build_lookup_from_team(name, force_requery)
		return self.__dict__[lname].get(team_id, {})
	
	def armies_lookup_from_team(self, team_id, force_requery=False):
		return self._lookup_from_team('armies', team_id, force_requery)
	
	def units_lookup_from_team(self, team_id, force_requery=False):
		return self._lookup_from_team('units', team_id, force_requery)
	
	
	#	DICTIONARIES
	#------------------------
	def _dict(self, name, force_requery=False):
		dname = '_%s' % name
		
		# Check cache
		if not force_requery and self.__dict__[dname] != {} and self.__dict__[dname] != []:
			return self.__dict__[dname]
		
		# Main
		if name == "armies":		func = army_q.get_all_armies
		elif name == "artefacts":	func = artefact_q.get_all_artefacts
		elif name == "battles":		func = battle_q.get_all_battles
		elif name == "cities":		func = city_q.get_all_cities
		elif name == "campaigns":	func = campaign_q.get_all_campaigns
		elif name == "operatives":	func = operative_q.get_all_operatives
		elif name == "kills":		func = player_q.get_kills
		elif name == "players":		func = player_q.get_all_players
		elif name == "teams":		func = team_q.get_all_teams
		elif name == "squads":		func = squad_q.get_all_squads
		elif name == "units":		func = unit_q.get_all_units
		elif name == "wonders":		func = wonder_q.get_all_wonders
		
		# Lists
		elif name == "buildings":	func = building_q.get_all_buildings
		elif name == "monsters":	func = monster_q.get_all_monsters
		elif name == "deities":		func = deity_q.get_all_deities
		elif name == "equipment":	func = equipment_q.get_all_equipment
		elif name == "evolutions":	func = evolution_q.get_all_evolutions
		elif name == "powers":		func = power_q.get_all_powers
		elif name == "servants":	func = servant_q.get_all_servants
		elif name == "spells":		func = spell_q.get_all_spells
		elif name == "techs":		func = tech_q.get_all_techs
		elif name == "traits":		func = trait_q.get_all_traits
		
		# Not found
		else:
			raise Exception("No classes.world.World dictionary holder for '%s'" % name)
		
		self.__dict__[dname] = func(self.cursor)
		return self.__dict__[dname]

	def armies(self, force_requery=False):
		return self._dict('armies', force_requery)

	def artefacts(self, force_requery=False):
		return self._dict('artefacts', force_requery)
	
	def buildings(self, force_requery=False):
		return self._dict('buildings', force_requery)
	
	def battles(self, force_requery=False):
		return self._dict('battles', force_requery)
	
	
	
	def monsters(self, force_requery=False):
		return self._dict('monsters', force_requery)
	
	def cities(self, force_requery=False):
		return self._dict('cities', force_requery)
	
	def campaigns(self, force_requery=False):
		return self._dict('campaigns', force_requery)
	
	def deities(self, force_requery=False):
		return self._dict('deities', force_requery)
	
	def equipment(self, force_requery = False):
		return self._dict('equipment', force_requery)
	
	def evolutions(self, force_requery=False):
		return self._dict('evolutions', force_requery)
	
	def kills(self, force_requery=False):
		return self._dict('kills', force_requery)
	
	def servants(self, force_requery=False):
		return self._dict('servants', force_requery)
	
	def operatives(self, force_requery=False):
		return self._dict('operatives', force_requery)

	def powers(self, force_requery=False):
		return self._dict('powers', force_requery)

	def players(self, force_requery=False):
		return self._dict('players', force_requery)

	def spells(self, force_requery=False):
		return self._dict('spells', force_requery)
		
	def techs(self, force_requery=False):
		return self._dict('techs', force_requery)
	
	def traits(self, force_requery=False):
		return self._dict('traits', force_requery)
	
	def squads(self, force_requery=False):
		return self._dict('squads', force_requery)
	
	def teams(self, force_requery=False):
		return self._dict('teams', force_requery)
	
	def units(self, force_requery=False):
		return self._dict('units', force_requery)
	
	def wonders(self, force_requery=False):
		return self._dict('wonders', force_requery)
	
	
	#	BY TEAM GROUPINGS
	#------------------------
	def _build_from_team(self, name, force_requery=False):
		fname = '_%s_from_team' % name
		dname = '_%s' % name
		
		self.teams()
		self._dict(name, force_requery)
		
		for k, v in self.__dict__[dname].items():
			if v.team not in self.__dict__[fname]:
				self.__dict__[fname][v.team] = collections.OrderedDict()
			
			self.__dict__[fname][v.team][k] = v
		
		self.built_from_team.append(name)
	
	def _all_from_team(self, name, force_requery=False):
		fname = '_%s_from_team' % name
		
		if not force_requery and name in self.built_from_team:
			return self.__dict__[fname]
		
		self._build_from_team(name, force_requery)
		return self.__dict__[fname]
		
	def _from_team(self, name, team_id, force_requery=False):
		fname = '_%s_from_team' % name
		
		# Get all the ones for it
		if team_id == -1:
			return self._all_from_team(name, force_requery)
		
		if not force_requery and name in self.built_from_team:
			return self.__dict__[fname].get(team_id, {})
		
		self._build_from_team(name, force_requery)
		return self.__dict__[fname].get(team_id, {})
	
	def armies_from_team(self, team_id, force_requery=False):
		return self._from_team('armies', team_id, force_requery)
	
	def cities_from_team(self, team_id, force_requery=False):
		return self._from_team('cities', team_id, force_requery)
	
	def players_from_team(self, team_id, force_requery=False):
		return self._from_team('players', team_id, force_requery)
	
	def operatives_from_team(self, team_id, force_requery=False):
		return self._from_team('operatives', team_id, force_requery)
	
	def squads_from_team(self, team_id, force_requery=False):
		return self._from_team('squads', team_id, force_requery)
		
	def units_from_team(self, team_id, force_requery=False):
		return self._from_team('units', team_id, force_requery)
	
	#	VERY UNIQUE LOOKUPS
	#------------------------
	def garrison(self, city_id, force_requery=False):
		if self._garrisons != {} and not force_requery:
			return self._garrisons.get(city_id, -1)
		
		self.armies()
		self._garrisons = collections.OrderedDict()
		
		for k, v in self._armies.items():
			if v.garrison > 0:
				self._garrisons[v.garrison] = k
		
		return self._garrisons.get(city_id, -1)	
	
	def kills_from_player(self, player, force_requery=False):
		if self._kills_from_turn != {} and not force_requery:
			return self._kills_from_player.get(player, {})
		
		self.kills()
		self._kills_from_player = collections.OrderedDict()
		
		for k in self._kills:
			if k.player not in self._kills_from_player:
				self._kills_from_player[k.player] = []
			
			self._kills_from_player[k.player].append(k)
		
		return self._kills_from_player.get(turn, {})
	
	def kills_from_turn(self, turn, force_requery=False):
		if self._kills_from_turn != {} and not force_requery:
			return self._kills_from_turn.get(turn, {})
		
		self.kills()
		self._kills_from_turn = collections.OrderedDict()
		
		for k in self._kills:
			if k['turn'] not in self._kills_from_turn:
				self._kills_from_turn[k['turn']] = []
			
			self._kills_from_turn[k['turn']].append(k)
		
		return self._kills_from_turn.get(turn, {})
	
	def kills_from_camp(self, campaign, force_requery=False):
		if self.kills_from_camp != {} and not force_requery:
			return self.kills_from_camp.get(campaign, {})
		
		self.kills()
		self.kills_from_camp = collections.OrderedDict()
		
		for k in self._kills:
			if k.turn not in self.kills_from_camp:
				self.kills_from_camp[k.campaign] = []
			
			self.kills_from_camp[k.campaign].append(k)
		
		return self.kills_from_camp.get(campaign, {})
	
	def squads_lookup_from_army(self, army_id, force_requery=False):
		if self._squads_lookup_from_army != {} and not force_requery:
			return self._squads_lookup_from_army.get(army_id, {})
		
		self.squads()
		self._squads_lookup_from_army = collections.OrderedDict()
		
		for k, s in self._squads.items():
			if s.army not in self._squads_lookup_from_army:
				self._squads_lookup_from_army[s.army] = collections.OrderedDict()
			
			self._squads_lookup_from_army[s.army][s.name.lower()] = k
		
		return self._squads_lookup_from_army.get(army_id, {})
	
	def cities_with_wonders(self, force_requery=False):
		if self._cities_with_wonders != set() and not force_requery:
			return self._cities_with_wonders
		
		self._cities_with_wonders = set()
		self.wonders()
		
		for k, v in self._wonders.items():
			self._cities_with_wonders.add(v.city)
		
		return self._cities_with_wonders
	
	def cities_with_artefacts(self, force_requery=False):
		if self._cities_with_artefacts != set() and not force_requery:
			return self._cities_with_artefacts
		
		self._cities_with_artefacts = set()
		self.artefacts()
		
		for k, v in self._artefacts.items():
			self._cities_with_artefacts.add(v.city)
		
		return self._cities_with_artefacts
	
	def active_teams(self, force_requery=False):
		if self._active_teams != {} and not force_requery:
			return self._active_teams
		
		self.teams(force_requery)
		self._active_teams = collections.OrderedDict()
		
		for t, the_team in self._teams.items():
			if the_team.not_a_team: continue
			if the_team.not_in_queue: continue
			if the_team.dead: continue
			if not the_team.active: continue
			
			self._active_teams[t] = the_team
		
		return self._active_teams
	
	def json_ti(self, team, turn, force_requery=False):
		if team not in self._json_ti:
			self._json_ti[team] = {}
			self._json_ti[team][turn] = ti_q.get_json_ti(self.cursor, team, turn)
			return self._json_ti[team][turn]
		
		if turn not in self._json_ti[team] or force_requery:
			self._json_ti[team][turn] = ti_q.get_json_ti(self.cursor, team, turn)
			return self._json_ti[team][turn]
		
		return self._json_ti[team][turn]
	
	def json_tis_from_turn(self, turn, force_requery=False):
		results = ti_q.get_json_tis_from_turn(self.cursor, turn)
		
		for team, json_ti in results.items():
			if team not in self._json_ti: self._json_ti[team] = {}
			if turn not in self._json_ti[team]:
				self._json_ti[team][turn] = json_ti
		
		return results
		
	
	def live_cities(self, force_requery=False):
		if self._live_cities != {} and not force_requery:
			return self._live_cities
		
		self.teams(force_requery)
		self.cities(force_requery)
		self._live_cities = collections.OrderedDict()
		self._live_cities_from_team = {}
		
		for c, the_city in self._cities.items():
			if the_city.dead > 0: continue
			if not self._teams[the_city.team].active: continue
			if self._teams[the_city.team].dead: continue
			
			self._live_cities[c] = the_city
			if the_city.team not in self._live_cities_from_team:
				self._live_cities_from_team[the_city.team] = collections.OrderedDict()
			self._live_cities_from_team[the_city.team][c] = the_city
		
		return self._live_cities
	
	def live_cities_from_team(self, team_id, force_requery=False):
		if self._live_cities != {} and not force_requery:
			return self._live_cities_from_team.get(team_id, {})
		
		self.live_cities(force_requery)
		return self._live_cities_from_team.get(team_id, {})
	
	def campaigns_from_turn(self, turn, force_requery=False):
		if self._campaigns_from_turn != {} and not force_requery:
			return self._campaigns_from_turn.get(turn, {})
		
		self.campaigns()
		self._campaigns_from_turn = {}
		
		for k, camp in self._campaigns.items():
			if camp.turn not in self._campaigns_from_turn:
				self._campaigns_from_turn[camp.turn] = []
			
			self._campaigns_from_turn[camp.turn].append(k)
		
		return self._campaigns_from_turn.get(turn, {})
	
	def battles_from_campaign(self, campaign, force_requery=False):
		if self._battles_from_campaign != {} and not force_requery:
			return self._battles_from_campaign.get(campaign, {})
		
		self.battles()
		self._battles_from_campaign = {}
		
		for k, battle in self._battles.items():
			if battle.campaign not in self._battles_from_campaign:
				self._battles_from_campaign[battle.campaign] = []
			
			self._battles_from_campaign[battle.campaign].append(k)
		
		return self._battles_from_campaign.get(campaign, {})
	
	def recent_campaigns(self, recentness = 5):
		result = []
		for t in range(common.current_turn()-recentness, common.current_turn()):
			result.extend(self.campaigns_from_turn(t))
		
		return result
			
	
	#	Mass get - Team
	#------------------------
	def mass_get_team_resources(self, force_requery=False):
		if "mass_get_team_resources" not in self.mass_get_checker or force_requery:
			team_q.mass_get_team_resources(self.cursor, self.teams())
			self.mass_get_checker.add("mass_get_team_resources")
	
	def mass_get_team_deities(self, force_requery=False):
		if "mass_get_team_deities" not in self.mass_get_checker or force_requery:
			team_q.mass_get_team_deities(self.cursor, self.teams())
			self.mass_get_checker.add("mass_get_team_deities")
	
	def mass_get_team_techs(self, force_requery=False):
		if "mass_get_team_techs" not in self.mass_get_checker or force_requery:
			team_q.mass_get_team_techs(self.cursor, self.teams())
			self.mass_get_checker.add("mass_get_team_techs")
	
	def mass_get_team_evolutions(self, force_requery=False):
		if "mass_get_team_evolutions" not in self.mass_get_checker or force_requery:
			team_q.mass_get_team_evolutions(self.cursor, self.teams())
			self.mass_get_checker.add("mass_get_team_evolutions")
	
	def mass_get_team_traits(self, force_requery=False):
		if "mass_get_team_traits" not in self.mass_get_checker or force_requery:
			team_q.mass_get_team_traits(self.cursor, self.teams())
			self.mass_get_checker.add("mass_get_team_traits")
	
			# team_q.mass_get_team_techs(the_world.cursor, the_world._teams)
			# team_q.mass_get_team_deities(the_world.cursor, the_world._teams)
			# team_q.mass_get_team_evolutions(the_world.cursor, the_world._teams)
	
	
	#	Mass get - City
	#------------------------
	def mass_get_city_buildings(self, force_requery=False):
		if "mass_get_city_buildings" not in self.mass_get_checker or force_requery:
			city_q.mass_get_city_buildings(self.cursor, self.cities())
			self.mass_get_checker.add("mass_get_city_buildings")
	
	#	Mass get - Army
	#------------------------
	def mass_get_army_monsters(self, force_requery=False):
		if "mass_get_army_monsters" not in self.mass_get_checker or force_requery:
			army_q.mass_get_army_monsters(self.cursor, self.armies())
			self.mass_get_checker.add("mass_get_army_monsters")
	
	def mass_get_army_squads(self, force_requery=False):
		if "mass_get_army_squads" not in self.mass_get_checker or force_requery:
			squad_q.mass_get_squads(self.cursor, self.armies())
			self.mass_get_checker.add("mass_get_army_squads")
	
	#	Mass get - Campaign
	#------------------------
	def mass_get_campaign_teams(self, force_requery=False):
		if "mass_get_campaign_teams" not in self.mass_get_checker or force_requery:
			campaign_q.mass_get_campaign_teams(self.cursor, self.campaigns())
			self.mass_get_checker.add("mass_get_campaign_teams")
	