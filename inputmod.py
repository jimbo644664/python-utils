class UserChoice:
    def __init__(self, question='', options=[], timeout=3):
        self.question = str(question)
        
        if type(options) is list:
            self.options = [str(x) for x in options]
        elif type(options) is dict:
            self.options = {}
            for x in options:
                self.options[str(x)] = str(options[x])

        self.timeout = int(timeout)
        self.lastresponse = ''

    def prompt(self):
        for x in range(0, self.timeout):
            query = self.question + ' (' + str(self.timeout-x) + ' tries remaining)\n'
            if self.timeout-x == 1:
                query = query.replace('tries', 'try')
            response = str(input(query))
            if response in self.options:
                if type(self.options) is list:
                    self.lastresponse = response
                    return self.lastresponse
                elif type(self.options) is dict:
                    self.lastresponse = self.options[response]
                    return self.lastresponse
            else:
                print('Invalid selection!')
        return None
