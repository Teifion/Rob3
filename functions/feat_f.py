import database

def set_feat(player_id, feat_id, feat_level = 0):
	query = "DELETE FROM feats WHERE player = %d AND feat = %d;" % (player_id, feat_id)
	try: database.cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	if feat_level > 0:
		query = "INSERT INTO feats (player, feat, level) values (%d, %d, %d);" % (player_id, feat_id, feat_level)
		try: database.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
