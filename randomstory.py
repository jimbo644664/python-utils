import ffparser
import random
import requests
import webbrowser
from collections import OrderedDict

domain = 'https://www.fanfiction.net'
fandoms = {
    'Harry Potter': '/book/Harry-Potter/'
}

restrict = {'srt': 1, 'lan': 1, 'r': 10, 'len': 100} # sorted by updates, English,, all ratings, length > 100k 
fpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

# we get all the links to more results on the page, in order to find the total number of pages
l = ffparser.LinkExtractor(fandoms['Harry Potter'], params=restrict)
l.feed(fpage.text)

# split each link into it's get parameters
pages = [int(x.split('&')[-1][2:]) for x in l.output_list] # page number is always the last get parameter
pages.sort()
lpage = pages[-1]

random.seed()
npage = random.randint(1, lpage)

restrict['p'] = npage
rpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

# get all the story links on the current random page
l = ffparser.LinkExtractor('/s/')
l.feed(rpage.text)

stories = l.output_list
random.shuffle(stories)

webbrowser.open(domain+stories[0], new=1)
