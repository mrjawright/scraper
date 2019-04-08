import io
import sys
import os
import json
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

	@mock.patch('urllib.request.urlretrieve')
	@mock.patch('feedparser.parse')
	def test_parse_test(self, parse_mock,urlretrieve_mock):
		print("test_parse_test")
		self.assertTrue(os.path.isfile(os.path.join(self.pwd,'sample.out')))
		testout_file = open(os.path.join(self.pwd,'sample.out'),'r')
		testout = json.loads(testout_file.read())
		testout_file.close()
		with io.StringIO() as buf, redirect_stdout(buf):
			parse_mock.return_value=testout
			rssobject = WhizRssAggregator(self.cachedir,"test")
			rssobject.parse()
			self.assertNotEqual(buf.getvalue(),"")
			parse_mock.assert_called_once_with("https://reddit.com/r/test.rss")
			urlretrieve_mock.assert_called
			self.assertEqual(urlretrieve_mock.call_count,21)



	@mock.patch('scraper.WhizRssAggregator.parseentries')
	@mock.patch('scraper.WhizRssAggregator.parsefeed')
	@mock.patch('scraper.WhizRssAggregator.fetchfeed')
	def test_parse_with_mock(self, fetchfeed_mock, parsefeed_mock, parseentries_mock ):
		print("test_parse_with_mock")
		self.assertTrue(os.path.isfile(os.path.join(self.pwd,'sample.feed')))
		testfeed = feedparser.parse(os.path.join(self.pwd,'sample.feed'))
		self.assertFalse(testfeed['feed'] == {})

		test_obj = WhizRssAggregator(self.cachedir, "spaceporn")
		test_obj.debug(True)
		fetchfeed_mock.return_value=testfeed
		parsefeed_mock.return_value=testfeed['entries']
		test_obj.parse()
		#self.assertTrue(test_obj.entries==25)
		fetchfeed_mock.assert_called_once		
		parsefeed_mock.assert_called_once
		parsefeed_mock.assert_called_once_with(testfeed)		
		parseentries_mock.assert_called_once_with(testfeed['entries'])


if __name__ == "__main__":
	unittest.main()	

