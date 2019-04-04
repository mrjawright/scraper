import io
import sys
import os
from contextlib import redirect_stdout
import shutil
import unittest
import feedparser
from unittest import mock 
from unittest.mock import MagicMock
from scraper import WhizRssAggregator 

def setUpModule():
	print("\nSet up module")

def tearDownModule():
	print("\nTear down module")


class TestParse(unittest.TestCase):
	cachedir = "test"
	pwd = os.path.dirname(os.path.abspath(__file__))
	cache_path = os.path.join(pwd, cachedir)

	@classmethod
	def setUpClass(cls):
		print("\nSet up TestParseClass")
		if os.path.isdir(cls.cache_path):
			shutil.rmtree(cls.cache_path)

	@classmethod
	def tearDownClass(cls):
		print("\nTear down TestParseClass")
		if os.path.isdir(cls.cache_path):
			shutil.rmtree(cls.cache_path)
	
	def setUp(self):
		print("\nSet up")

	def tearDown(self):
		print("\nTear down")

	def test_parse_none(self):
		print("test_parse_none")
		with self.assertRaises(TypeError,msg="__init__() missing 1 required positional argument: 'subreddit'"):
			rssobject = WhizRssAggregator()

	def test_parse_test(self):
		print("test_parse_test")
		with io.StringIO() as buf, redirect_stdout(buf):
			rssobject = WhizRssAggregator(self.cachedir,"test")
			self.assertNotEqual(buf.getvalue(),"")


	@mock.patch('scraper.WhizRssAggregator.fetchfeed')
	def test_parse_with_mock(self, fetchfeed_mock):
		print("test_parse_with_mock")
		self.assertTrue(os.path.isfile(os.path.join(self.pwd,'sample.feed')))
		testfeed = feedparser.parse(os.path.join(self.pwd,'sample.feed'))
		self.assertFalse(testfeed['feed'] == {})
		
		test_obj = WhizRssAggregator(self.cachedir, "spaceporn")
		test_obj.debug(True)
		fetchfeed_mock.return_value=testfeed
		test_obj.parse()
		self.assertTrue(test_obj.entries==25)		
		self.assertTrue(fetchfeed_mock.called)		


if __name__ == "__main__":
	unittest.main()	

