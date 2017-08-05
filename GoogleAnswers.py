from Scraper import scrape


class Result:
    def __init__(self, query, scraper_results):
        self.query = query
        self.results = scraper_results

        if len(self.results) > 0:
            self.string = 'Answer(s) to "{0}":\n'.format(self.query)
            for i in range(len(self.results)):
                self.string += '[{0}] {1}'.format(i+1, self.results[i]).replace('  ', ' ')
        else:
            self.string = 'No results found for the query: {0}'.format(self.query)

    def __str__(self):
        return self.string


def ask(query):
    url = convert_query(query)
    result = Result(query, scrape(url))
    return result


def convert_query(query):
    result = query
    result = result.replace(' ', '+')
    result = result.replace('?', '')
    result = "http://www.google.com/search?q=" + result
    return result

while True:
    ask(input("Question: "))