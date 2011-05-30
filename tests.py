#!/usr/bin/env python3
# http://diveintopython3.org/unit-testing.html
# /Library/WebServer/CGI-Executables/rob3/tests.py

import os
import sys
import re
import unittest
import covers
from pages import common

import test_library
from collections import OrderedDict

class Add_deity(test_library.team_t.Add_deity): pass
class Remove_deity(test_library.team_t.Remove_deity): pass
class Get_hash(test_library.team_t.Get_hash): pass
class Start_script_tester(test_library.team_t.Start_script_tester): pass
class Start_script_exception_tester(test_library.team_t.Start_script_exception_tester): pass

class Icon_size(test_library.city_t.Icon_size): pass
class Overlap_amount(test_library.city_t.Overlap_amount): pass
class Overlap_percentage(test_library.city_t.Overlap_percentage): pass
class City_rule_minifuncs(test_library.city_t.City_rule_minifuncs): pass

#	FAVOUR
#------------------------
class Arl_favour_tester(test_library.deity_t.Arl_favour_tester): pass
class Trchkithin_favour_tester(test_library.deity_t.Trchkithin_favour_tester): pass
class Adyl_favour_tester(test_library.deity_t.Adyl_favour_tester): pass
class Ssai_favour_tester(test_library.deity_t.Ssai_favour_tester): pass
class Orakt_favour_tester(test_library.deity_t.Orakt_favour_tester): pass
class Agashn_favour_tester(test_library.deity_t.Agashn_favour_tester): pass
class Ldura_favour_tester(test_library.deity_t.Ldura_favour_tester): pass
class Azmodius_favour_tester(test_library.deity_t.Azmodius_favour_tester): pass
class Phraela_and_Caist_favour_tester(test_library.deity_t.Phraela_and_Caist_favour_tester): pass
class Soag_chi_favour_tester(test_library.deity_t.Soag_chi_favour_tester): pass
class Khystrik_favour_tester(test_library.deity_t.Khystrik_favour_tester): pass
class Laegus_favour_tester(test_library.deity_t.Laegus_favour_tester): pass
class Zasha_favour_tester(test_library.deity_t.Zasha_favour_tester): pass
class Alki_favour_tester(test_library.deity_t.Alki_favour_tester): pass

# Database
class DB_func_tester(test_library.database_t.DB_func_tester): pass
class DB_class_tester(test_library.database_t.DB_class_tester): pass

# Misc funcs
class Log_tester(test_library.log_t.Log_tester): pass
class Pythagoras_tester(test_library.path_t.Pythagoras_tester): pass

# Rules
class Operative_rule_functions(test_library.operative_t.Operative_rule_functions): pass
class Tech_cost_rules(test_library.tech_t.Tech_cost_rules): pass
class Spell_cost_rules(test_library.spell_t.Spell_cost_rules): pass

# Buildings
class Building_function_tests(test_library.building_t.Building_function_tests): pass
class Building_rules_tests(test_library.building_t.Building_rules_tests): pass

# Map
class Map_functions(test_library.map_t.Map_functions): pass


class Matches(test_library.intorder_t.Matches): pass

class Lore_tester(test_library.lore_t.Lore_tester): pass

# class SAD_loop(test_library.sad_t.SAD_loop): pass
# class Basic_functions(test_library.sad_t.Basic_functions): pass
# class Dict_entries(test_library.sad_t.Dict_entries): pass
# class Function_args(test_library.sad_t.Function_args): pass
# class Supply_results(test_library.sad_t.Supply_results): pass
# class Demand_results(test_library.sad_t.Demand_results): pass

class Trade_functions(test_library.trade_t.Trade_functions): pass

#	ORDERS
#------------------------

# Construction
class Construction_orders(test_library.construction_orders_t.Construction_orders): pass
class Construction_orders_debug(test_library.construction_orders_t.Construction_orders_debug): pass

# Monsters
class Monster_orders(test_library.monster_orders_t.Monster_orders): pass

# Research
class Research_orders(test_library.research_orders_t.Research_orders): pass

# Military
class Military_squad_orders(test_library.military_orders_t.Military_squad_orders): pass
class Military_army_orders(test_library.military_orders_t.Military_army_orders): pass

# Trade
class Trade_orders(test_library.trade_orders_t.Trade_orders): pass

class Res_dict_class(test_library.res_dict_t.Res_dict_class): pass
# class Res_dict_class(test_library.res_dict_t.Res_dict_class): pass

class Unit_cost(test_library.unit_t.Unit_cost): pass

"""
Orders tests (For each function type)
 - Test regex matches
 - Affordability
 - Queries get sent back
 - Results get sent back
 - Cost gets sent back
 - Case insensitivity for keywords

Construction:
 - Non-existant building
 - Non-existant city
 - City that is not ours
 - Nomadic city
 - Dead city
 - City tries to build 2 buildings
 - City tries to build 2 walls
 - City tries to build 1 wall and 1 building (Pass)
 - Build rate/ability with and without Stone
 - Upgrades to something we have so overflows the limit
 - Requires upgrade

Spell research
 - Cost in pure points, lore points, mix of points
 - Same as above but with partial completion
"""

def main():
	test_program = unittest.main(exit=False)
	
	if test_program.result.failures == [] and test_program.result.errors == []:
		verbose = False
		if len(sys.argv) > 1:
			verbose = True
		
		module_skip = ['bpgsql3', 'cli', 'db_convert', 'exec', 'rob_server', 'sync', 'tests', 'web', 'web (for server)', 'world_test', 'world', 'spy_world', 'ploc', 'cli_f']
		dirs_skip = ['backup', 'cache', 'covers', 'includes', 'lists', 'misc', 'msn', 'msn_old', 'profile_library', 'script_output', 'test_library', 'pages', 'lore']
		
		covers.get_coverage(test_program, common.data['server_fpath'], verbose, module_skip, dirs_skip)

# The function to run the tests
if __name__ == '__main__':
	main()
