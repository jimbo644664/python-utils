from collections import OrderedDict

class UserChoice:
    def __init__(self, question='', options=[], timeout=3):
        self.question = str(question)
        
        if type(options) is range:
            self.options = options
        elif type(options) is list or type(options) is tuple:
            self.options = [str(x) for x in options]
        elif type(options) is dict or type(options) is OrderedDict:
            self.options = OrderedDict()
            for x in options:
                self.options[str(x)] = options[x]

        self.timeout = int(timeout)
        self.lastresponse = None

    def prompt(self):
        for x in range(0, self.timeout):
            query = '{0} ({1} tries remaining)\n'.format(self.question, self.timeout-x)
            if x == 0:
                print('Options are:')
                if type(self.options) is range:
                    print('[{0}, {1}]'.format(self.options[0], self.options[-1]))
                else:
                    for o in self.options:
                        print(o)
            if self.timeout-x == 1:
                query = query.replace('tries', 'try')
            response = input(query)
            if type(self.options) is range:
                response = int(response)
                if response in self.options:
                    self.lastresponse = response
                    return self.lastresponse
            elif response in self.options:
                if type(self.options) is list:
                    self.lastresponse = response
                    return self.lastresponse
                elif type(self.options) is OrderedDict:
                    self.lastresponse = self.options[response]
                    return self.lastresponse
            else:
                print('Invalid selection!')
        return None
