import database
import collections
from classes import intorder, order_post
from orders import monster_o

def _intorder_query(cursor,
				where = '',
				orderby = 'id',
				start = 0,
				limit = 0):
	
	query = "SELECT * FROM intorders"
	
	# Where
	if where != '': query += " WHERE %s" % where
	
	# Order by
	if orderby != '': query += " ORDER BY %s" % orderby
	
	# Limit stuff
	if start > 0 and limit > 0: query += " LIMIT %s, %s" % (start, limit)
	if start > 0 and limit < 1: query += " LIMIT 0, %s" % (limit)
	if start < 1 and limit > 0: query += " LIMIT %s" % (limit)
	
	results = collections.OrderedDict()
	try:
		cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		results[row['id']] = intorder.Intorder(row)
	
	return results

def get_all_intorders(cursor):
	return _intorder_query(cursor)

def get_orders_from_posts(cursor, post_list):
	if post_list == []: return collections.OrderedDict()
	return _intorder_query(cursor, where="id in (%s)" % ",".join([str(p) for p in post_list]))

def get_one_intorder(cursor, the_intorder):
	query = "SELECT * FROM intorders WHERE id = {0:d} LIMIT 1;".format(int(the_intorder))
	
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		return intorder.Intorder(row)


def mass_get_parents(cursor, order_dict):
	for k, o in order_dict.items():
		o.parent = None
	
	query = "SELECT * FROM orders WHERE post_id IN (%s)" % ",".join([str(o.id) for i, o in order_dict.items()])
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	for row in cursor:
		if row['post_id'] not in order_dict: continue
		order_dict[row['post_id']].parent = order_post.Order_post(the_world=None, row=row)
	
	return order_dict

int_order_matchup = {
	"Monsters":	monster_o.Monster_block,
}

def get_interactive(cursor, order_id):
	query = """SELECT * FROM interactive_orders WHERE id = %d""" % order_id
	try: cursor.execute(query)
	except Exception as e:
		raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
	
	row = cursor.fetchone()
	
	return int_order_matchup[row['title']](the_world=None, team=row['team'], title_name=row['title'], content=row['content'])