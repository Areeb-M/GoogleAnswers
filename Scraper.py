import requests
from html.parser import HTMLParser


class Target:
    def __init__(self, elements):
        self.elements = elements

    def check_path(self, path):
        length = len(self.elements)
        for i in range(length):
            index = -length + i
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


def scrape(url, header_payload, targets):
    data = requests.get(url, headers=header_payload).text
    results = []

    for target in targets:
        results += Parser(target).feed(data)

    for result in results:
        print(result)

targets = [
    Target([['div', 'class="_sPg"']]),
    Target([['div', 'class="_XWk"']]),
    Target([['span', 'class="_Tgc"']])
]

payload = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
