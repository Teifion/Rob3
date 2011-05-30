

def new_intorder(order_id):
	return """INSERT INTO intorders (id)
		values
		({id});
	""".format(
		id=order_id,
	)

def create_default(cursor, the_order):
	query = new_intorder(the_order.post_id)
	try: cursor.execute(query)
	except Exception as e: pass