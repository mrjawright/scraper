#!/usr/bin/python
import feedparser
import sys

class WhizRssAggregator():
    feedurl = ""

    def __init__(self, subreddit):
        self.feedurl = 'https://reddit.com/r/'+subreddit+".rss"
        self.parse()
    def parse(self):
        thefeed = feedparser.parse(self.feedurl)
        print("Getting Feed Data")
       	print("__________")
	for thefeedentry in thefeed.entries:
            	print(thefeedentry.get("id", ""))
            	print(thefeedentry.get("title", ""))
            	print(thefeedentry.get("link", ""))
        	print(thefeedentry.get("author", ""))
            	print(thefeedentry.get("content", ""))
            	print("__________")

def main():
    try:
        if len(sys.argv) == 2:
#                from whizrssaggregator import WhizRssAggregator
		rssobject = WhizRssAggregator(sys.argv[1])				 
	else:
		print sys.argv[0] + " subredditname"	
    except Exception,e:
    	print str(e)
        pass

main()
