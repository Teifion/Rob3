from queries import deity_q

def deity_option_list(cursor, remove_list=[], default=0):
	output = []
	
	deity_dict = deity_q.get_all_deities(cursor)
	
	for deity_id, the_deity in deity_dict.items():
		if deity_id in remove_list:
			continue
		
		if deity_id == default:
			output.append("<option value='{0}' selected='selected'>{1}</option>".format(deity_id, the_deity.name))
		else:
			output.append("<option value='{0}'>{1}</option>".format(deity_id, the_deity.name))
	
	return "".join(output)

# def find_attitude(deity_1, deity_2):
# 	deity_dict_n = deity.get_deity_dict_n()
# 	deity_dict_c = deity.get_deity_dict_c()
# 	
# 	# If they're a name/id, convert them to deity class
# 	if deity_1.__class__ == str: deity_1 = deity_dict_c[deity_dict_n[deity_1]]
# 	if deity_1.__class__ == int: deity_1 = deity_dict_c[deity_1]
# 	
# 	if deity_2.__class__ == str: deity_2 = deity_dict_c[deity_dict_n[deity_2]]
# 	if deity_2.__class__ == int: deity_2 = deity_dict_c[deity_2]
# 	
# 	if deity_2.name in deity_1.likes: return "Likes"
# 	if deity_2.name in deity_1.dislikes: return "Dislikes"
# 	if deity_2.name in deity_1.hates: return "Hates"
# 	
# 	return "Neutral"