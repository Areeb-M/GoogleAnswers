import requests
from html.parser import HTMLParser


class Target:
    def __init__(self, elements):
        self.elements = elements

    def check_path(self, path):
        length = len(self.elements)
        for i in range(length):
            index = -length + i
            # print(path[index][0] == self.elements[0][0], path[index][0], self.elements[0][0], path[index][1] == self.elements[0][1], path[index][1], self.elements[0][1])
            if path[index][0] == self.elements[index][0] and (path[index][1] == self.elements[index][1] or self.elements[index][1] == ''):
                continue
            else:
                return False
        return True


class Parser(HTMLParser):
    def __init__(self, target):
        HTMLParser.__init__(self)
        self.target = target
        self.target_depth = 0
        self.path = []
        self.occurrences = []

    def handle_starttag(self, tag, attributes):
        attr_string = ""
        for attribute in attributes:
            attr_string += attribute[0] + '="' + attribute[1] + '" '
        attr_string = attr_string[:-1]

        self.path.append([tag, attr_string])
        if self.target.check_path(self.path) or self.target_depth > 0:
            if self.target_depth == 0:
                self.occurrences.append('')
            self.target_depth += 1

    def handle_endtag(self, tag):
        self.path.pop()
        if self.target_depth > 0:
            self.target_depth -= 1

    def handle_data(self, data):
        if self.target_depth > 0:
            self.occurrences[-1] += data

    def feed(self, data):
        HTMLParser.feed(self, data)
        return self.occurrences


def scrape(url):
    data = requests.get(url).text
    results = Parser(Target([['div', 'class="_sPg"']])).feed(data)
    for r in results:
        print(r)

scrape("http://www.google.com/search?q=what+is+the+radius+of+a+circle")