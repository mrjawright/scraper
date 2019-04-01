#!/usr/bin/python
import io
from contextlib import redirect_stdout
from scraper import WhizRssAggregator 
import sys
import unittest

class TestParse(unittest.TestCase):
	def test_parse_none(self):
		print("test_parse_none")
		with io.StringIO() as buf, redirect_stdout(buf):
			print("test")
			#rssobject = WhizRssAggregator()
			print("output:" + buf.getvalue())
			self.assertEqual(buf.getvalue(), "./tests.py subredditname")

	def test_parse_test(self):
		print("test_parse_test")
		rssobject = WhizRssAggregator("test")	

if __name__ == "__main__":
	unittest.main()	
