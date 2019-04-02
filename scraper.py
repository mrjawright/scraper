#!/usr/bin/python
import feedparser
import re
import sys
import urllib.request 
import os

class WhizRssAggregator():
	feedurl = ""
	subreddit = ""
	pwd = os.path.dirname(os.path.abspath(__file__))

	def __init__(self, subreddit):
		if subreddit != "":
			self.subreddit = subreddit
			self.feedurl = 'https://reddit.com/r/'+subreddit+".rss"
			self.parse()
		else:
			raise RuntimeError("Null or Empty subreddit name")
			
	def parse(self):
		link_regex = r"<span><a href=\"((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?\">\[link\]<\/a><\/span>"
		print("Getting Feed Data for %s " % self.subreddit)
		thefeed = feedparser.parse(self.feedurl)
		print(thefeed['feed'])
		print(thefeed['feed']['title'])
		print(thefeed.feed.subtitle)
		print(len(thefeed['entries']))
		print("__________")
		testfordir=True
		for thefeedentry in thefeed.entries:
			print(thefeedentry['id'])
			print(thefeedentry['title'])
			print(thefeedentry['tags'])
			print(thefeedentry['link'])
			print(thefeedentry['author'])
			print(thefeedentry['summary'])
			for content in thefeedentry['content']:
				link = re.search(link_regex, content['value'])
				link_href = content['value'][link.start()+15:link.end()-19]
				print(link_href)
				href_split = re.split('\/',link_href)
				path = os.path.join(self.pwd,'imagecache',self.subreddit)
				file = os.path.join(path,href_split[len(href_split)-1])
				if file.endswith(".jpg") and not os.path.exists(file):
					try:
						#if there are images to fetch, check to see if we've set up the
						#folder for the current subreddit
						if testfordir:
						#there's no use checking in every iteration of the loop
							if os.path.isdir(path):
								print("%s already exists" % path)
							else:
    								os.mkdir(path)
    								print ("Successfully created the directory %s " % path)
							testfordir = False
						urllib.request.urlretrieve(link_href,file)
					except OSError:  
    						print ("Creation of the directory %s failed" % path)
					except:	
						print("Error on: %s" % link_href)
			print("__________")

def main():
	try:
		pwd = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(pwd,'imagecache')
		if os.path.isdir(path):
			print("%s already exists" % path)
		else:
    			os.mkdir(path)
    			print ("Successfully created the directory %s " % path)
		if len(sys.argv) == 2:
			rssobject = WhizRssAggregator(sys.argv[1])				 
		else:
			print ("usage:"+ sys.argv[0] + " subredditname")
	
	except OSError:  
    		print ("Creation of the directory %s failed" % path)
	except:
		print ("Unexpected error:", sys.exc_info()[0])
main()

