import unittest
import database

class DB_func_tester(unittest.TestCase):
	test_targets = [
		database.get_cursor,
		database.get_custom_cursor,
		database.get_test_cursor,
		
		database.query_batch,
		database.query_list,
		database.query,
		
		database.shell_text
	]
	
	def test_shell_text(self):
		vals = (
			("", ""),
			("BLUE", "BLUE"),
			("''BLUE''", "\033[1;1mBLUE\033[30;0m"),
		)
		
		for arg, expected in vals:
			self.assertEqual(expected, database.shell_text(arg))
	

class DB_class_tester(unittest.TestCase):
	test_targets = [
		database.DB_Field,
		database.DB_Field.validate,
		database.DB_Field.escape,
		database.DB_Field.data_type_syntax,
		database.DB_Field.create_field,
		
		database.DB_Field.create_column,
	]
	
	def test_db_field(self):
		vals = (
			({"name":"simple", "field_type":"varchar"}, "simple varchar NOT NULL default ''"),
			({"name":"integer_field", "field_type":"integer", "default":-1}, "integer_field integer NOT NULL default -1"),
		)
		
		for kwargs, expected in vals:
			r = database.DB_Field(**kwargs)
			self.assertEqual(r.create_column().strip(), expected)


