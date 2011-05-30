import unittest
from lore import pages
from lists import deity_list
import database

class Lore_tester(unittest.TestCase):
	cursor = database.get_cursor()
	
	test_targets = [
		pages._filter,
		
		pages.convert,
		
		pages.get_plaintext,
		pages.get_bbcode,
		pages.get_html,
	]
	
	def _check(self, cat, page):
		query = "SELECT * FROM lore_entries WHERE cat = '{0:s}' AND page = '{1:s}' LIMIT 1;".format(database.escape(cat.lower().replace(" ", "_")), database.escape(page.lower().replace(" ", "_")))
		try: self.cursor.execute(query)
		except Exception as e:
			raise Exception("Database error: %s\nQuery: %s" % (str(e.args[0]).replace("\n",""), query))
		
		r = self.cursor.fetchone()
		
		if r == None:
			self.assertEqual("Entry not found: %s.%s" % (cat, page), "")
	
	def test_existance(self):
		# Built in
		tries = (
			('Test',	'Test'),
		)
		for c, p in tries:
			self._check(c, p)
		
		# Deities
		for d in deity_list.data_list:
			self._check("Deities", d.name)
		
		# Monsters
		
		# Buildings
		
		# Equipment
		
		# Servant
		
		# Spells
		
		# Techs
		
	
	def test_filter(self):
		data = pages.get_plaintext(self.cursor, "test", "test", "public")
		self.assertEqual(data, "Summary\nSummary text\n\nDescription\nDescription text and more")
		
		data = pages.get_plaintext(self.cursor, "test", "test", "secret")
		self.assertEqual(data, "Summary\nSummary text\n\nDescription\nDescription text and more\n\n\nSecret info")
		
		data = pages.get_plaintext(self.cursor, "test", "test", "gm")
		self.assertEqual(data, "Summary\nSummary text\n\nDescription\nDescription text and more\n\n\nSecret info\n\nGm_notes\nGM info")
	
	def test_plaintext(self):
		data = pages.get_plaintext(self.cursor, "test", "test", "public")
		self.assertEqual(data, "Summary\nSummary text\n\nDescription\nDescription text and more")
	
	def test_bbcode(self):
		data = pages.get_bbcode(self.cursor, "test", "test", "public")
		self.assertEqual(data, "[o]Summary[/o]\nSummary text\n\n[o]Description[/o]\nDescription [b]text[/b] and more")
	
	def test_html(self):
		data = pages.get_html(self.cursor, "test", "test", "public")
		self.assertEqual(data, "Summary text\n<br /><br />\nDescription <strong>text</strong> and more\n<br /><br />")
	
	def test_bbcode_convert(self):
		vals = (
			("<strong>XYZ</strong>", "[o][/o]\n[b]XYZ[/b]"),
		)
		
		for str_in, expected in vals:
			result = pages.convert([{"description":str_in}], "bbcode")
			self.assertEqual(result, expected)
	
	def test_plaintext_convert(self):
		vals = (
			("<strong>XYZ</strong>", "XYZ"),
		)
		
		for str_in, expected in vals:
			result = pages.convert([{"description":str_in}], "plaintext")
			self.assertEqual(result, expected)


