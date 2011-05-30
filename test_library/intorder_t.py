import unittest
from classes import intorder, order_post

class Matches(unittest.TestCase):
	test_targets = []
	
	re_matches = (
		# Rob box
		("[rob]Content[/rob]", "rob_box", {"content":"Content"}),
		("[rob][b]Bold:[/b] Text[/rob]", "rob_box", {"content":"[b]Bold:[/b] Text"}),
		
		# Target
		("[b]Targets:[/b] Lithuania\n", "targets", {"targets":" Lithuania"}),
		("[b]Targets:[/b] Lithuania\nLine", "targets", {"targets":" Lithuania"}),
		
		# Cities
		("[b]Cities:[/b] Batch, Blotch, Splotch\n", "cities", {"cities":" Batch, Blotch, Splotch"}),
		
		# Departure
		("[b]Departure:[/b] Lithuania\n", "departure", {"departure":" Lithuania"}),
		
		# Allies
		("[b]Allies:[/b] Lithuania\n", "allies", {"allies":" Lithuania"}),
		
		# Forces
		("[b]Forces:[/b] Lithuania\n", "forces", {"forces":" Lithuania"}),
	)
	
	def test_sizes(self):
		for content, pattern_name, expected_dict in self.re_matches:
			result = intorder.patterns[pattern_name].search(content)
			
			try:
				self.assertEqual(result.groupdict(), expected_dict)
			except Exception as e:
				print("\n\n")
				print("Pattern name: %s" % pattern_name)
				print("Content: %s" % content)
				print("\n\n")
				raise

