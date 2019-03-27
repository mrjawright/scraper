#!/usr/bin/python
import sys
import time
import urllib2
from urllib2 import urlopen
import re
import cookielib, urllib2
from cookielib import CookieJar
import datetime
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

def main():
    try:
        if len(sys.argv) == 2:
        	page = 'https://reddit.com/r/'+sys.argv[1]+".rss"
        	sourceCode = opener.open(page).read()
        	try:
            		titles = re.findall(r"<title>(.*?)</title>",sourceCode)
            		contents = re.findall(r"<content>(.*?)</content>",sourceCode)
            		ids = re.findall(r"<id>(.*?)</id>",sourceCode)
            		authors = re.findall(r"<author>(.*?)</author>",sourceCode)
            		for title  in titles:
                		print title
            		for content  in contents:
                		print content
            		for id in ids:
                		print id
 			for author in authors:
				name = re.search("<name>(.*?)</name>",author)
                                print author[(name.start() + 6): (name.end() - 7):]  
        	except Exception, e:
            		print str(e)
	else:
		print sys.argv[0] + " subredditname"	
    except Exception,e:
    	print str(e)
        pass

main()
