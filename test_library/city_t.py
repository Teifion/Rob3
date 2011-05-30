import math
import unittest
from classes import city
from functions import city_f
from rules import map_data, city_rules

def empty_city(x, y, pop):
	return city.City({"x":x,"y":y,"population":pop})

class Icon_size(unittest.TestCase):
	test_targets = [map_data.map_image_size]
	
	city_sets = [
		(1000, 30),
		(10000000, 100),
		(50000, 54)
	]
	
	def test_sizes(self):
		for size, expected in self.city_sets:
			r = map_data.map_image_size(size)
			
			self.assertEqual(expected, r)

class Overlap_amount(unittest.TestCase):
	test_targets = [city_f.overlap]
	
	city_sets = [
		# Dummy case 1
		(empty_city(1000, 1000, 50000), empty_city(1010, 1000, 50000), 158),
	]
	
	def test_overlapping(self):
		for city_1, city_2, overlap in self.city_sets:
			r = round(city_f.overlap(city_1, city_2))
			r2 = round(city_f.overlap(city_2, city_1))# Make sure it works both ways round
			
			try:
				self.assertEqual(overlap, r)
				self.assertEqual(r, r2)
			except Exception as e:
				r = city_f.overlap(city_1, city_2, debug=True)
				raise


class Overlap_percentage(unittest.TestCase):
	test_targets = [city_f.overlap_percentage, city_rules.overlap]
	
	city_sets = [
		(empty_city(100, 100, 50000), 100, 27.29),
	]
	
	def test_overlapping(self):
		for the_city, amount, correct_answer in self.city_sets:
			real_area = map_data.map_image_size(the_city.size)/2.5
			real_area = math.pi * (real_area ** 2)
			
			r = city_f.overlap_percentage(the_city, amount)
			
			try:
				self.assertAlmostEqual(correct_answer, r, places=2)
			except Exception as e:
				print("")
				print("City size: %d" % the_city.size)
				print("City area: %d" % real_area)
				print("Overlap amount: %d" % amount)
				print("Correct amount: %d" % correct_answer)
				print("Incorrect answer: %d" % r)
				print("")
				raise
	
	overlap_tests = (
		(-10, 1),
		(0, 1),
		(100, 0),
		(150, 0),
		(70, 0.3),
		(60, 0.4),
		(10, 0.9),
	)
	
	def test_overlap_rule(self):
		for amount, correct_answer in self.overlap_tests:
			r = city_rules.overlap(amount)
			
			try:
				self.assertAlmostEqual(correct_answer, r, places=2)
			except Exception as e:
				print("")
				print("city_rules.overlap(%d) != %d" % (amount, correct_answer))
				raise
				
			
		
class City_rule_minifuncs(unittest.TestCase):
	test_targets = [city_rules._hunger_rate]
		
	hunger_tests = (
		(1000, 0,	(1, 0)),# 0% shortage, full rate, no constant alter
		(1000, 100,	(0.5, 0)),# 10% shortage, half rate, no constant alter
		(1000, 200,	(0, 0)),# 20% shortage, 0 rate, no constant alter
		
		# Different sizes to make sure
		(5000, 500, (0.5, 0)),# 10% shortage, half rate, no constant alter
		(10000, 2000, (0, 0)),# 20% shortage, 0 rate, no constant alter
		
		# Over 20% shortage
		(1000, 300, (0, -90)),# 30% shortage, 0 rate, negative 5% of population
		(1000, 400, (0, -160)),# 40% shortage, 50% reduction
		(1000, 500, (0, -250)),# 50% shortage, 80% reduction
		(1000, 600, (0, -360)),# 60% shortage, 120% reduction
		(1000, 700, (0, -489)),# 70% shortage, 160% reduction
		(1000, 800, (0, -640)),# 80% shortage, 220% reduction
		(1000, 900, (0, -810)),# 90% shortage, 280% reduction
		(1000, 1000, (0, -1000)),# 100% shortage, 400% reduction
	)
	
	def test_hunger_rate(self):
		for size, shortage, expected in self.hunger_tests:
			r = city_rules._hunger_rate(size, shortage)
			self.assertEqual(expected, (r[0], int(r[1])))
		
		# Now test it throws an exception
		self.assertRaises(ArithmeticError, city_rules._hunger_rate, *(1000, -2))
		self.assertRaises(ArithmeticError, city_rules._hunger_rate, *(-2, 1000))
	
	
	# city_rules.city_control(distance, the_city, team_dict)
	# city_rules.city_growth_rate(cursor, the_team, the_city, the_world=None)
		
	
