import ffparser
import random
import requests
import webbrowser
from collections import OrderedDict

domain = 'https://www.fanfiction.net'
fandoms = {
    'Harry Potter': '/book/Harry-Potter/'
}

restrict = {'srt': '1', 'lan': '1', 'r': '10'}
fpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

l = ffparser.LinkExtractor(fandoms['Harry Potter'], params=restrict)
l.feed(fpage.text)

pages = [int(x.split('&')[-1][2:]) for x in l.output_list]
pages.sort()
lpage = pages[-1]

random.seed()
npage = random.randint(1, lpage)

restrict['p'] = str(npage)
rpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

l = ffparser.LinkExtractor('/s/')
l.feed(rpage.text)

stories = l.output_list
random.shuffle(stories)

webbrowser.open(domain+stories[0], new=1)
