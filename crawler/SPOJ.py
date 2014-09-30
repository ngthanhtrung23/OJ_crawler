import os
from generic_crawler import GenericCrawler
from VOJ import main, VojCrawler


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code/SPOJ')
BASE_URL = 'https://www.spoj.com/'


class SpojCrawler(VojCrawler):
    def __init__(self):
        GenericCrawler.__init__(
            self,
            BASE_URL,
            BASE_URL + 'users/{user}/',
            BASE_URL + 'status/{problem},{user}/',
            BASE_URL + 'files/src/save/{id}',
            '<a href="/status/[^,]+,{user}/">(?P<id>.+)</a>',
            '<tr class="kol.*(accepted|100)',
            '.*href="/files/src/(?P<id>\d+)/'
        )


if __name__ == '__main__':
    crawler = SpojCrawler()
    main(crawler, OUTPUT_DIR)
