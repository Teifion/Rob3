import unittest
from functions import log_f

class Log_tester(unittest.TestCase):
	test_targets = [
		log_f.new_log,
	]
	
	def test_new_log(self):
		vals = (
			(("a, b, c", "abc", "", -1, -1, 40), "INSERT INTO logs (tags, content, cost, player, team, turn)\n\t\tvalues\n\t\t('a, b, c', 'abc', '', -1, -1, 40)"),
		)
		
		for args, expected in vals:
			r = log_f.new_log(*args)
			
			self.assertEqual(expected, r)

