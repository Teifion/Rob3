import math
import unittest
from rules import map_resources, region_data

class Map_functions(unittest.TestCase):
	test_targets = [map_resources.add, region_data.get_source_dict]
	
	def test_misc(self):
		pass