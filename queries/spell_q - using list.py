# Works a little differently, allows for some sorting methods

from lists import spell_list

ASC = False
DESC = True
default_filter = lambda s: True

def _get_spells(filter_func=default_filter, order_by=()):
	result = []
	
	# First we filter out what we want
	narrow_list = []
	for i, s in enumerate(spell_list.data_list):
		if filter_func(s):
			narrow_list.append(i)
	
	# Now to sort
	for l in range(0,len(narrow_list)):
		cur_index = None
		found_spell = None
		
		for i, s in enumerate(narrow_list):
			found = False
			
			for o in order_by:
				# If we've already picked this then it's not a big deal
				if found: continue
				
				# If nothing is even as a temporary winner we assume it's this one
				if found_spell == None:
					cur_index = i
					found_spell = s
					found = True
					continue
				
				# At this point the item is a contender
				t_val = spell_list.data_list[s].__dict__[o[0]]
				c_val = spell_list.data_list[found_spell].__dict__[o[0]]
				
				# If both are equal here then we try the next order_by item
				if t_val == c_val: continue
				
				# ASC means we want the lowest values first
				if (o[1] == ASC and t_val < c_val) or (
					o[1] == DESC and t_val > c_val):
					cur_index = i
					found_spell = s
					found = True
					continue
				
				# If we reach this line then this item is out of the running
				found = True
		
		result.append(narrow_list[cur_index])
		del(narrow_list[cur_index])
	
	return result

def spells_by_name():
	return _get_spells(order_by="name")

def spells_from_category(category):
	def func_filter(s):
		if s.category != category: return False
		else: return True
	return _get_spells(func_filter, order_by=(("tier", ASC), ("name", ASC)))