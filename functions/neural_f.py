from rules import sad_rules
from functions import cli_f

rate_of_change = 0.1

class NN (object):
	"""docstring for NN"""
	def __init__(self, func, inputs, targets, mapping, cycles=10):
		super(NN, self).__init__()
		self.func		= func
		self.inputs		= inputs
		self.targets	= targets
		self.mapping	= mapping
		self.latest_results = {}
		
		self.cycles = cycles
	
	def train(self):
		self.current_inputs = self.inputs
		
		try:
			for c in cli_f.progressbar(range(0, self.cycles), prefix = "", size = 60, with_eta=True):
			# for c in range(0, self.cycles):
				self._cycle()
		except KeyboardInterrupt as e:
			# Flush progress bar
			print(" ".join([" " for x in range(0,40)]))
			print("Exiting due to keyboard interrupt:")
		except Exception as e:
			raise
		finally:
			self.end()
	
	def _cycle(self):
		# self.current_inputs = self.inputs
		self.latest_results = self.func(self.current_inputs)
		
		for k, v in self.latest_results.items():
			diff = self.targets[k] - v
			
			self.current_inputs[k] *= 1 + (diff/100 * rate_of_change)
			
			# if k == 'Wool':
			# 	print("{result:6} {target:6} {diff:6} {percent:6} {current:8}          ".format(
			# 		result = round(self.latest_results[k], 2),
			# 		target = self.targets[k],
			# 		diff = round(diff, 2),
			# 		percent = round(1 + (diff/100 * rate_of_change), 2),
			# 		current = round(self.current_inputs[k], 2),
			# 	))
		
		# exit()
	
	def end(self):
		# Inputs
		print("\nInputs")
		for r in sad_rules.res_list:
			print("{res:17} {avg:6}".format(
				res = r,
				avg = self.current_inputs[r],
			))
		
		print("\nAccurate outputs          Got    Targ    Offset")
		# Correct output
		for r in sad_rules.res_list:
			print("{res:17} {got:6} {target:6} {offset:6}".format(
				res = r,
				got = round(self.latest_results[r], 2),
				target = round(self.targets[r], 2),
				offset = round(abs(self.latest_results[r] - self.targets[r]), 2),
			))
		
		print("")
		total_diff = 0
		for k, v in self.latest_results.items():
			total_diff += (self.targets[k] - v)
		
		print("Average difference: %s\n" % (total_diff/len(self.latest_results)))
		print(str(self.current_inputs))
