import math
from pages import common
from queries import city_q
from rules import city_rules
import collections
from functions import path_f, trade_f

page_data = {
	"Title":	"Trade matrix",
	"Admin":	True,
}

def main(cursor):
	output = []
	
	# Takes a while to run...
	# trade_f.build_distance_matrix(cursor)
	
	return "".join(output)