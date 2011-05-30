import database

def new_log(tags, content, cost, player = -1, team = -1, turn = -1):
	from pages import common
	
	if type(cost) != str:
		cost = str(cost)
	
	if turn < 0:
		turn = common.current_turn()
	
	query = """INSERT INTO logs (tags, content, cost, player, team, turn)
		values
		('{tags}', '{content}', '{cost}', {player}, {team}, {turn})""".format(
			tags = 			database.escape(tags),
			content = 		database.escape(content),
			cost = 			database.escape(cost),
			
			player = player,
			team = team,
			turn = turn,
		)
	
	return query