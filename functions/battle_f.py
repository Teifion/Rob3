import database

def new_battle(name, campaign, start, duration, x, y, btype, city=0):
	return """INSERT INTO battles (campaign, name, start, duration, x, y, type, city)
		values
		({c}, '{n}', {s}, {d}, {x}, {y}, {btype}, {city});""".format(
			c = campaign,
			n = database.escape(name),
			s = start,
			d = duration,
			x = x,
			y = y,
			btype = btype,
			city = city,
	)

def make_delete_query(battle_id):
	return ["DELETE FROM battles WHERE id = %d" % battle_id]


# def teams_in_battle(battle_id, include_secret=True):
# 	"""Returns a list of the teams involved in a battle"""
# 	if include_secret:
# 		query = """SELECT team FROM battle_teams WHERE battle = %d""" % battle_id
# 	else:
# 		query = """SELECT team FROM battle_teams WHERE battle = %d AND secret = False""" % battle_id
# 	
# 	team_list = []
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		team_list.append(row['team'])
# 	
# 	return team_list
# 
# def armies_in_battle(battle_id, team_id=-1):
# 	"""Returns a list of the armies involved in a battle"""
# 	army_list = []
# 	if team_id < 1:
# 		query = """SELECT army FROM army_battle_history WHERE battle = %d""" % battle_id
# 	else:
# 		query = """SELECT b.army FROM army_battle_history b, armies a
# 			WHERE b.battle = %d
# 				AND b.army = a.id
# 				AND a.team = %d""" % (battle_id, team_id)
# 	
# 	try:
# 		database.cursor.execute(query)#TODO Use new method
# 	except Exception as e:
# 		print("Query: %s\n" % query)
# 		raise e
# 	while (1):
# 		row = database.cursor.fetchone()
# 		if row == None: break
# 		army_list.append(row['army'])
# 	
# 	return army_list

def remove_loss(cursor, amount, squad_id, battle_id):
	"""Removes losses to a squad"""
	current_losses = 0
	squad_id	= int(squad_id)
	battle_id	= int(battle_id)
	
	# Find out how many losses they have so far
	query = "SELECT losses FROM squad_battle_history WHERE battle = %d AND squad = %d LIMIT 1;" % (battle_id, squad_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		current_losses = row['losses']
	
	new_losses = current_losses - amount
	try:
		# Insert a new one
		query = "INSERT INTO squad_battle_history (losses, squad, battle) values (%d, %d, %d);" % (new_losses, squad_id, battle_id)
		cursor.execute(query)
		
	except Exception as e:
		# Insert didn't work, lets try update instead
		query = """UPDATE squad_battle_history SET losses = %d WHERE squad = %d AND battle = %d;""" % (new_losses, squad_id, battle_id)
		cursor.execute(query)
	
	# Update squad itself
	query = """UPDATE squads SET amount = amount+%d WHERE id = %d;""" % (amount, squad_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	

def add_loss(cursor, amount, squad_id, battle_id):
	"""Adds losses to a squad"""
	current_losses = 0
	squad_id	= int(squad_id)
	battle_id	= int(battle_id)
	
	# Find out how many losses they have so far
	query = "SELECT losses FROM squad_battle_history WHERE battle = %d AND squad = %d LIMIT 1;" % (battle_id, squad_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		current_losses = row['losses']
	
	new_losses = amount+current_losses
	try:
		# Insert a new one
		query = "INSERT INTO squad_battle_history (losses, squad, battle) values (%d, %d, %d);" % (new_losses, squad_id, battle_id)
		cursor.execute(query)
		
	except Exception as e:
		# Insert didn't work, lets try update instead
		query = """UPDATE squad_battle_history SET losses = %d WHERE squad = %d AND battle = %d;""" % (new_losses, squad_id, battle_id)
		cursor.execute(query)
	
	# Update squad itself
	query = """UPDATE squads SET amount = amount-%d WHERE id = %d;""" % (amount, squad_id)
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
