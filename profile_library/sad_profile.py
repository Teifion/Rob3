import time
from functions import sad_f, city_f
from classes import world

def main(cursor, options=None):
	w = world.World(cursor)
	
	city_f.apply_city_matrix(w)
	sad_f.supply_and_demand(w)
	
	return ""