from collections import OrderedDict

import ffparser
import random
import requests
import webbrowser
import inputmod

domain = 'https://www.fanfiction.net'
fandoms = {
    'Harry Potter': '/book/Harry-Potter/'
}

restrict = {'lan': 1}

ratings = OrderedDict([
    ('All', 10),
    ('K->T', 103),
    ('K->K+', 102),
    ('K', 1),
    ('K+', 2),
    ('T', 3),
    ('M', 4)
])

length = OrderedDict([
    ('None', 0),
    ('<1k', 11),
    ('<5k', 51),
    ('>1k', 1),
    ('>5k', 5),
    ('>10k', 10),
    ('>20k', 20),
    ('>40k', 40),
    ('>60k', 60),
    ('>100k', 100)
])

sorts = OrderedDict([
    ('Updated', 1),
    ('Published', 2),
    ('Reviews', 3),
    ('Favourites', 4),
    ('Follows', 5),
])

uc = inputmod.UserChoice('Rating of fics?', ratings)
restrict['r'] = uc.prompt()

uc = inputmod.UserChoice('Length of fics?', length)
if uc.prompt() != 0:
    restrict['len'] = uc.lastresponse

uc = inputmod.UserChoice('Sorted by?', sorts)
restrict['srt'] = uc.prompt()

fpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

l = ffparser.LinkExtractor(fandoms['Harry Potter'], params=restrict)
l.feed(fpage.text)

pages = [int(x.split('&')[-1][2:]) for x in l.output_list]
pages.sort()
lpage = pages[-1]

uc = inputmod.UserChoice('First n pages?', range(1, lpage+1))
lpage = uc.prompt()

random.seed()
npage = random.randint(1, lpage)

restrict['p'] = npage
rpage = requests.get(domain+fandoms['Harry Potter'], params=restrict)

l = ffparser.LinkExtractor('/s/')
l.feed(rpage.text)

stories = l.output_list
random.shuffle(stories)

webbrowser.open(domain+stories[0], new=1)
