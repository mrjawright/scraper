from __future__ import print_function
import builtins as __builtin__
import feedparser
import re
import sys
import urllib.request 
import os

class WhizRssAggregator():
	
	def print(self, *args, **kwargs):
		if self.debug:
			return __builtin__.print(*args, **kwargs)

	def debug(self, value = None):
		if not value is None:
			self.debug = value
		self.print("Debug is %s" % self.debug)
		return self.debug

	def testing(self, value = None):
		if not value is None:
			self.testing = value
		self.print("Testing is %s" % self.testing)
		return self.testing

	def __init__(self, cachedir, subreddit):
		try:
			self.print("WhizRssAggregator cacheing %s images to %s" % (subreddit, cachedir))
			pwd = os.path.dirname(os.path.abspath(__file__))
			#self.print ("PWD: %s" % self.pwd)
			self.cachedir = os.path.join(pwd, cachedir)
			self.print ("Cache path: %s" % self.cachedir)
			if os.path.isdir(self.cachedir):
				self.print("%s already exists" % self.cachedir)
			else:
    				os.mkdir(self.cachedir)
    				self.print ("Successfully created the directory %s " % self.cachedir)
		except OSError:  
			print("OS error: {0}".format(err)) 
	
		if subreddit != "":
			self.subreddit = subreddit
		else:
			raise RuntimeError("Null or Empty subreddit name")

	def fetchfeed(self):
		print("Getting Feed Data for %s " % self.subreddit)
		feedurl = 'https://reddit.com/r/'+subreddit+".rss"
		if self.debug and not self.testing:
			urllib.request.urlretrieve(feedurl,self.subreddit+".feed")
		thefeed = feedparser.parse(feedurl)
		self.print(thefeed['feed'])
		return thefeed

	def parsefeed(self, thefeed):
		self.print(thefeed['feed']['title'])
		try:
			self.print(thefeed.feed.subtitle)
		except:	
			self.print("/n")
		self.entries = len(thefeed['entries'])
		print("%s Entries" % self.entries)
		return thefeed['entries']

	def getfilefromcontent(self, content):
		file = None
		link_href = None
		link_regex = r"<span><a href=\"((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?\">\[link\]<\/a><\/span>"
		link = re.search(link_regex, content)
		if not link == None:
			if (link.start()+15 < link.end()-19): 
				tlink_href = content[link.start()+15:link.end()-19]
				self.print(tlink_href)
				href_split = re.split('\/',tlink_href)
				subreddit_path = os.path.join(self.cachedir ,self.subreddit)
				tfile = os.path.join(subreddit_path,href_split[len(href_split)-1])
				if tfile.endswith(".jpg") and not os.path.exists(tfile):
					try:
						file = tfile
						link_href = tlink_href
						#if there are images to fetch, check to see if we've set up the
						#folder for the current subreddit
						if self.testfordir:
							#there's no use checking in every iteration of the loop
							if os.path.isdir(subreddit_path):
								print("%s already exists" % subreddit_path)
							else:
    								os.mkdir(subreddit_path)
    								print ("Successfully created the directory %s " % subreddit_path)
							self.testfordir = False
					except OSError as err: 
						print("OS error: %s" % format(err)) 
						print("** error: %s" % err.errno) 
						print("** file: %s" % err.filename) 
					except:	
						print("Unexpected Error:", sys.exc_info()[0])
		return link_href, file

	def parsecontent(self, content):
		link_href, file = self.getfilefromcontent(content['value'])
		if not file == None:
			try:
				urllib.request.urlretrieve(link_href,file)
			except urllib.error.HTTPError as http_err:
				print(http_err)
				print("While processing: %s" % link_href)

	def parseentries(self, theentries):
		self.testfordir=True
		self.print("__________")
		for entry in theentries:
			self.print(entry['id'])
			self.print(entry['title'])
			self.print(entry['tags'])
			self.print(entry['link'])
			self.print(entry['author'])
			self.print(entry['summary'])
			for content in entry['content']:
				self.parsecontent(content)
		self.print("__________")

	def parse(self):
		thefeed = self.fetchfeed()
		theentries = self.parsefeed(thefeed)
		self.parseentries(theentries)

def main():
	try:
		if len(sys.argv) == 2:
			rssobject = WhizRssAggregator('imagecache', sys.argv[1])
			rssobject.debug(False)
			rssobject.testing(False)
			rssobject.parse()
		else:
			print ("usage:"+ sys.argv[0] + " subredditname")
	except Exception as e:	
		print ("Unexpected error:", sys.exc_info()[0])
		print ("Unexpected error:", e)
main()

