from functions import sync_f, lore_f
from pages import common
from data_classes import lore_entry
import lore
import database

def clear_tables(cursor):
	# Clear data
	query = """DROP TABLE lore_blocks"""
	try: cursor.execute(query)
	except Exception as e:
		pass
		# raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	query = """DROP TABLE lore_entries"""
	try: cursor.execute(query)
	except Exception as e:
		pass
		# raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	# Build the tables back up thus resetting all the ID values
	sync_f.check_table(cursor, lore_entry.Lore_entry().table_info, fix=True, show_fixes=False)
	sync_f.check_table(cursor, lore_entry.Lore_block, fix=True, show_fixes=False)


from . import test_lore

from .deities import adyl_l
from .deities import agashn_l
from .deities import alki_l
from .deities import arl_l
from .deities import azmodius_l
from .deities import khystrik_l
from .deities import laegus_l
from .deities import ldura_l
from .deities import orakt_l
from .deities import phraela_and_caist_l
from .deities import soag_chi_l
from .deities import ssai_l
from .deities import trchkithin_l
from .deities import zasha_l

from .irs import greymin_l
from .irs import jjaro_l
from .irs import trchig_l

from .monsters import costal_salamander_l
# from .monsters import giant_eagle_l
from .monsters import gorquithor_l
from .monsters import gryphon_l
from .monsters import hydra_l
from .monsters import karithor_l
from .monsters import murdaphant_l
# from .monsters import peyam_l
from .monsters import troll_l
from .monsters import tishrashi_condor_l
from .monsters import unicorn_l

from .nations import chosen_l
from .nations import construction_l
from .nations import cultures_l
from .nations import economy_l
from .nations import happiness_l
from .nations import evolution_l
from .nations import ir_l
from .nations import technology_l

from .site import index_l as site_index_l

from .general import about_l
from .general import contact_l
from .general import crazy_l
from .general import gateway_l
from .general import history_l
from .general import improvement_l
from .general import orders_l
from .general import starting_l

from .guide import guide_l

from .magic import progression_l
from .magic import how_l
from .magic import spells_l
from .magic import worlds_l
from .magic import light_l
from .magic import dark_l
from .magic import destruction_l
from .magic import abjuration_l
from .magic import daemonic_l
from .magic import necromancy_l
from .magic import alchemy_l
from .magic import enchantment_l
from .magic import sourcery_l

from .military import army_l
from .military import equipment_l
from .military import navy_l
from .military import naval_guide_l
from .military import spies_l
from .military import unit_l

def rebuild_pages(cursor):
	clear_tables(cursor)
	
	# Main site
	add_entry(cursor, site_index_l)
	add_entry(cursor, test_lore)# Test item
	
	# General
	add_entry(cursor, about_l)
	add_entry(cursor, contact_l)
	add_entry(cursor, crazy_l)
	add_entry(cursor, gateway_l)
	add_entry(cursor, history_l)
	add_entry(cursor, improvement_l)
	add_entry(cursor, orders_l)
	add_entry(cursor, starting_l)
	
	# Deities
	add_entry(cursor, adyl_l)
	add_entry(cursor, agashn_l)
	add_entry(cursor, alki_l)
	add_entry(cursor, arl_l)
	add_entry(cursor, azmodius_l)
	add_entry(cursor, khystrik_l)
	add_entry(cursor, laegus_l)
	add_entry(cursor, ldura_l)
	add_entry(cursor, orakt_l)
	add_entry(cursor, phraela_and_caist_l)
	add_entry(cursor, soag_chi_l)
	add_entry(cursor, ssai_l)
	add_entry(cursor, trchkithin_l)
	add_entry(cursor, zasha_l)
	
	# IRs
	add_entry(cursor, greymin_l)
	add_entry(cursor, jjaro_l)
	add_entry(cursor, trchig_l)
	
	# Monsters
	add_entry(cursor, costal_salamander_l)
	# add_entry(cursor, giant_eagle_l)
	add_entry(cursor, gorquithor_l)
	add_entry(cursor, gryphon_l)
	add_entry(cursor, hydra_l)
	add_entry(cursor, karithor_l)
	add_entry(cursor, murdaphant_l)
	# add_entry(cursor, peyam_l)
	add_entry(cursor, troll_l)
	add_entry(cursor, tishrashi_condor_l)
	# add_entry(cursor, unicorn_l)
	
	# Nations
	add_entry(cursor, chosen_l)
	add_entry(cursor, construction_l)
	add_entry(cursor, cultures_l)
	add_entry(cursor, economy_l)
	add_entry(cursor, happiness_l)
	add_entry(cursor, evolution_l)
	add_entry(cursor, ir_l)
	add_entry(cursor, technology_l)
	
	#	Guide
	#------------------------
	add_entry(cursor, guide_l)
	
	#	Magic
	#------------------------
	add_entry(cursor, progression_l)
	add_entry(cursor, how_l)
	add_entry(cursor, spells_l)
	add_entry(cursor, worlds_l)
	add_entry(cursor, light_l)
	add_entry(cursor, dark_l)
	add_entry(cursor, destruction_l)
	add_entry(cursor, abjuration_l)
	add_entry(cursor, daemonic_l)
	add_entry(cursor, necromancy_l)
	add_entry(cursor, alchemy_l)
	add_entry(cursor, enchantment_l)
	
	#	Military
	#------------------------
	add_entry(cursor, army_l)
	add_entry(cursor, equipment_l)
	add_entry(cursor, navy_l)
	add_entry(cursor, naval_guide_l)
	add_entry(cursor, spies_l)
	add_entry(cursor, unit_l)
	


saves = {}

def add_entry(cursor, m):
	# Insert entry
	try:
		database.query(cursor, lore_f.new_entry(m.data['cat'], m.data['page']))
	except Exception as e:
		print("Inserting %s.%s" % (m.data['cat'], m.data['page']))
		# print(saves[(m.data['cat'], m.data['page'])])
		raise
	
	# saves[(m.data['cat'], m.data['page'])] = m
	
	# Get entry ID
	query = """SELECT id FROM lore_entries WHERE cat = '%s' AND page = '%s' LIMIT 1;""" % (database.escape(m.data['cat']), database.escape(m.data['page']))
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	le = cursor.fetchone()['id']
	
	# Insert blocks
	for b in m.blocks:
		database.query(cursor, lore_f.new_block(le, b))
	




