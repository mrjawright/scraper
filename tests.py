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

#	def test_init_mock(self):
#		print("test_init_mock")
#		img_path = os.path.join(self.cache_path, "earthporn")
#		with mock.patch.object(WhizRssAggregator, "__init__", lambda obj, dir, sub: None):
#			test_obj = WhizRssAggregator(self.cachedir, "spaceporn")
#			#create attributes from __init__
#			test_obj.pwd = self.pwd
#			#test_obj.cachedir = self.cachedir
#			#test_obj.subreddit = "spaceporn"
#			test_obj.debug(True)
#			self.assertTrue(os.path.isfile(os.path.join(self.pwd,'sample.feed')))
#			testfeed = feedparser.parse(os.path.join(self.pwd,'sample.feed'))
#			self.assertFalse(testfeed['feed'] == {})
#			test_obj.fetchfeed = MagicMock(return_value = testfeed)
#			test_obj.parse()
#			self.assertTrue(test_obj.entries==25)		
#		#self.assertTrue(os.path.isdir(img_path))
#		self.assertTrue(test_obj.fetchfeed.called)		

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



#	@mock.patch('scraper.WhizRssAggregator')
#	def test_MockScraper(mock_class, cachedir, subreddit ):
#		mock_class.return_value.fetchfeed.returnvalue = r"{'tags': [{'term': 'EarthPorn', 'scheme': None, 'label': 'r/EarthPorn'}], 'updated': '2019-04-03T15:28:08+00:00', 'updated_parsed': time.struct_time(tm_year=2019, tm_mon=4, tm_mday=3, tm_hour=15, tm_min=28, tm_sec=8, tm_wday=2, tm_yday=93, tm_isdst=0), 'icon': 'https://www.redditstatic.com/icon.png/', 'id': 'https://www.reddit.com/r/earthporn.rss', 'guidislink': True, 'link': 'https://www.reddit.com/r/earthporn', 'links': [{'rel': 'self', 'href': 'https://www.reddit.com/r/earthporn.rss', 'type': 'application/atom+xml'}, {'rel': 'alternate', 'href': 'https://www.reddit.com/r/earthporn', 'type': 'text/html'}], 'logo': 'https://b.thumbs.redditmedia.com/ksUDkpsi-29HAGUhp7k-qq2029z3FqC4fad686B4jGE.png', 'subtitle': 'EarthPorn is your community of landscape photographers and those who appreciate the natural beauty of our home planet.', 'subtitle_detail': {'type': 'text/plain', 'language': None, 'base': 'https://www.reddit.com/r/earthporn.rss', 'value': 'EarthPorn is your community of landscape photographers and those who appreciate the natural beauty of our home planet.'}, 'title': 'EarthPorn: Amazing images of light and landscape', 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://www.reddit.com/r/earthporn.rss', 'value': 'EarthPorn: Amazing images of light and landscape'}}"
#		mock_class.return_value.__init__ = lambda testclass, cachedir, subreddit:None
#		inst = scraper.WhizRssAggregator(cachedir = self.cachedir,subreddit = "mock")
		#inst.subreddit='mock'
		#inst.parse()

if __name__ == "__main__":
	unittest.main()	

