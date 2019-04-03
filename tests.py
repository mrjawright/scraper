import io
import sys
import os
from contextlib import redirect_stdout
from scraper import WhizRssAggregator 
import shutil
import unittest
from unittest import mock 

def setUpModule():
	print("Set up module")

def tearDownModule():
	print("Tear down module")


class TestParse(unittest.TestCase):
	cachedir = "test"

	@classmethod
	def setUpClass(cls):
		print("Set up TestParseClass")
		pwd = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(pwd, cls.cachedir)
		if os.path.isdir(path):
			shutil.rmtree(path)

	@classmethod
	def tearDownClass(cls):
		print("Tear down TestParseClass")
		pwd = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(pwd, cls.cachedir)
		if os.path.isdir(path):
			shutil.rmtree(path)
	
	def setUp(self):
		print("Set up")

	def tearDown(self):
		print("Tear down")

	def test_parse_none(self):
		print("test_parse_none")
		with self.assertRaises(TypeError,msg="__init__() missing 1 required positional argument: 'subreddit'"):
			rssobject = WhizRssAggregator()

	def test_parse_test(self):
		print("test_parse_test")
		with io.StringIO() as buf, redirect_stdout(buf):
			rssobject = WhizRssAggregator(self.cachedir,"test")
			self.assertNotEqual(buf.getvalue(),"")

	@mock.patch('scraper.WhizRssAggregator')
	def test_MockScraper(mock_class, cachedir, subreddit ):
		mock_class.return_value.fetchfeed.returnvalue = r"{'tags': [{'term': 'EarthPorn', 'scheme': None, 'label': 'r/EarthPorn'}], 'updated': '2019-04-03T15:28:08+00:00', 'updated_parsed': time.struct_time(tm_year=2019, tm_mon=4, tm_mday=3, tm_hour=15, tm_min=28, tm_sec=8, tm_wday=2, tm_yday=93, tm_isdst=0), 'icon': 'https://www.redditstatic.com/icon.png/', 'id': 'https://www.reddit.com/r/earthporn.rss', 'guidislink': True, 'link': 'https://www.reddit.com/r/earthporn', 'links': [{'rel': 'self', 'href': 'https://www.reddit.com/r/earthporn.rss', 'type': 'application/atom+xml'}, {'rel': 'alternate', 'href': 'https://www.reddit.com/r/earthporn', 'type': 'text/html'}], 'logo': 'https://b.thumbs.redditmedia.com/ksUDkpsi-29HAGUhp7k-qq2029z3FqC4fad686B4jGE.png', 'subtitle': 'EarthPorn is your community of landscape photographers and those who appreciate the natural beauty of our home planet.', 'subtitle_detail': {'type': 'text/plain', 'language': None, 'base': 'https://www.reddit.com/r/earthporn.rss', 'value': 'EarthPorn is your community of landscape photographers and those who appreciate the natural beauty of our home planet.'}, 'title': 'EarthPorn: Amazing images of light and landscape', 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://www.reddit.com/r/earthporn.rss', 'value': 'EarthPorn: Amazing images of light and landscape'}}"
		mock_class.return_value.__init__ = lambda testclass, cachedir, subreddit:None
		inst = scraper.WhizRssAggregator(cachedir = self.cachedir,subreddit = "mock")
		#inst.subreddit='mock'
		#inst.parse()

if __name__ == "__main__":
	unittest.main()	

