import unittest
from classes import city
from functions import path_f

class Pythagoras_tester(unittest.TestCase):
	test_targets = [path_f.pythagoras_tuples, path_f.pythagoras_cities, path_f.pythagoras]
	
	tuple_vals = (
		((0, 0), (3, 4), 5),
	)
	def test_pythagoras_tuples(self):
		for a, b, expected in self.tuple_vals:
			r = path_f.pythagoras_tuples(a, b)
			self.assertAlmostEqual(r, expected, places=2)
	
	city_vals = (
		(city.City({"x":0, "y":0}), city.City({"x":3, "y":4}), 5),
		(city.City({"x":100, "y":100}), city.City({"x":250, "y":250}), 212.13),
	)
	def test_pythagoras_cities(self):
		for a, b, expected in self.city_vals:
			r = path_f.pythagoras_cities(a, b)
			self.assertAlmostEqual(r, expected, places=2)
	
	pure_vals = (
		(3, 4, 5),
	)
	# Now to test that all of them are called correctly by the main function
	def test_pythagoras(self):
		data_set = []
		data_set.extend(self.tuple_vals)
		data_set.extend(self.city_vals)
		data_set.extend(self.pure_vals)
		
		for a, b, expected in data_set:
			r = path_f.pythagoras(a, b)
			self.assertAlmostEqual(r, expected, places=2)