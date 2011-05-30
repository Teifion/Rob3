temple_points_dict = {
	23:					1,
	"Temple":			1,
	
	50:					2,
	"Expanded temple":	2,
}

def temple_points(the_building):
	"""docstring for temple_points"""
	
	if the_building in temple_points_dict:
		return temple_points_dict[the_building]
	
	return 0