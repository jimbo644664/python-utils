from html.parser import HTMLParser

def order_params(params):
    for x in ['srt', 'g1', 'g2', '_g1', 'lan', 'r', 'len', 't', 's',
              'c1', 'c2', 'c3', 'c4', '_c1', '_c2', 'v1', '_v1', 'p']:
        if x in params:
            yield (x, params[x])

class LinkExtractor(HTMLParser):
    
    def __init__(self, lookfor, params={}):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.output_list = []

        self.__trigger = lookfor
        if params:
            self.__trigger += '?'
            for param in order_params(params):
                self.__trigger += '&' + param[0] + '=' + str(param[1])

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            link = dict(attrs).get('href')
            if link.find(self.__trigger) != -1:
                self.output_list.append(link)

class TextExtractor(HTMLParser):
    
    def __init__(self, lookfor):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.data = ''

        self.__depthcount = 0
        self.__trigger = self.looktype[lookfor]

    def handle_starttag(self, tag, attrs):
        if self.__depthcount > 0:
            self.__depthcount += 1
        else:
            for attr in attrs:
                if attr[0] == 'id':
                    if attr[1] == self.__trigger:
                        self.__depthcount = 1
        
        if self.__depthcount > 0:
            line = "<" + tag
            for attr in attrs:
                line += " " + attr[0] + "=\"" + str(attr[1]) + "\""
            line += ">"
            if tag == "img":
                line += "</img>"
                self.__depthcount -= 1
            self.data += line
        
    def handle_endtag(self, tag):
        if self.__depthcount > 0:
            line = "</" + tag + ">"
            self.data += line
        self.__depthcount -= 1
        
    def handle_data(self, data):
        if self.__depthcount > 0:
            self.data += data
        
