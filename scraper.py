from __future__ import print_function
import builtins as __builtin__
import feedparser
import re
import sys
import urllib.request 
import os

class WhizRssAggregator():
	
	def debug(self, value = None):
		if not value is None:
			self.debug = value
		return self.debug

	def print(self, *args, **kwargs):
		if self.debug:
			return __builtin__.print(*args, **kwargs)

	def __init__(self, cachedir, subreddit):
		try:
			self.print("WhizRssAggregator cacheing %s images to %s" % (subreddit, cachedir))
			self.cachedir = cachedir
			self.pwd = os.path.dirname(os.path.abspath(__file__))
			#self.print ("PWD: %s" % self.pwd)
			path = os.path.join(self.pwd, self.cachedir)
			self.print ("Cache path: %s" % path)
			if os.path.isdir(path):
				self.print("%s already exists" % path)
			else:
    				os.mkdir(path)
    				self.print ("Successfully created the directory %s " %path)
		except OSError:  
			print("OS error: {0}".format(err)) 
	
		if subreddit != "":
			self.subreddit = subreddit
			self.feedurl = 'https://reddit.com/r/'+subreddit+".rss"
		else:
			raise RuntimeError("Null or Empty subreddit name")

	def fetchfeed(self):
		print("Getting Feed Data for %s " % self.subreddit)
		thefeed = feedparser.parse(self.feedurl)
		self.print(thefeed['feed'])
		return thefeed

	def parsefeed(self):
		thefeed = self.fetchfeed()
		self.print(thefeed['feed']['title'])
		try:
			self.print(thefeed.feed.subtitle)
		except:	
			self.print("/n")	
		print("%s Entries" % len(thefeed['entries']))
		return thefeed

	def parseentries(self, thefeed):
		link_regex = r"<span><a href=\"((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?\">\[link\]<\/a><\/span>"
		self.print("__________")
		testfordir=True
		for thefeedentry in thefeed.entries:
			self.print(thefeedentry['id'])
			self.print(thefeedentry['title'])
			self.print(thefeedentry['tags'])
			self.print(thefeedentry['link'])
			self.print(thefeedentry['author'])
			self.print(thefeedentry['summary'])
			for content in thefeedentry['content']:
				link = re.search(link_regex, content['value'])
				if not link == None:
					if (link.start()+15 < link.end()-19): 
						link_href = content['value'][link.start()+15:link.end()-19]
						self.print(link_href)
						href_split = re.split('\/',link_href)
						subreddit_path = os.path.join(self.pwd, self.cachedir ,self.subreddit)
						file = os.path.join(subreddit_path,href_split[len(href_split)-1])
						if file.endswith(".jpg") and not os.path.exists(file):
							try:
								#if there are images to fetch, check to see if we've set up the
								#folder for the current subreddit
								if testfordir:
								#there's no use checking in every iteration of the loop
									if os.path.isdir(subreddit_path):
										print("%s already exists" % subreddit_path)
									else:
    										os.mkdir(subreddit_path)
    										print ("Successfully created the directory %s " % subreddit_path)
									testfordir = False
								urllib.request.urlretrieve(link_href,file)
							except urllib.error.HTTPError as http_err:
								print(http_err)
								print("Processing: %s" % link_href)
							except OSError as err: 
								print("OS error: %s" % format(err)) 
								print("** error: %s" % err.errno) 
								print("** file: %s" % err.filename) 
							except:	
								print("Unexpected Error:", sys.exc_info()[0])
				self.print("__________")

	def parse(self):
		thefeed = self.parsefeed()
		self.parseentries(thefeed)

def main():
	try:
		if len(sys.argv) == 2:
			rssobject = WhizRssAggregator('imagecache', sys.argv[1])
			rssobject.debug(False)
			rssobject.parse()
		else:
			print ("usage:"+ sys.argv[0] + " subredditname")
	except Exception as e:	
		print ("Unexpected error:", sys.exc_info()[0])
		print ("Unexpected error:", e)
main()

