#!/usr/bin/python
import io
from contextlib import redirect_stdout
from scraper import WhizRssAggregator 
import sys
import unittest

class TestParse(unittest.TestCase):
	def test_parse_none(self):
		print("test_parse_none")
		with self.assertRaises(TypeError,msg="__init__() missing 1 required positional argument: 'subreddit'"):
			rssobject = WhizRssAggregator()

	def test_parse_test(self):
		print("test_parse_test")
		with io.StringIO() as buf, redirect_stdout(buf):
			rssobject = WhizRssAggregator("test")
			self.assertNotEqual(buf.getvalue(),"")

if __name__ == "__main__":
	unittest.main()	

