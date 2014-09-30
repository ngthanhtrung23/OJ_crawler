import os
from generic_crawler import GenericCrawler
from VOJ import main


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code/SPOJ')
BASE_URL = 'https://www.spoj.com/'


class SpojCrawler(object, GenericCrawler):
    def __init__(self):
        GenericCrawler.__init__(
            self,
            BASE_URL,
            BASE_URL + 'users/{}/',
            BASE_URL + 'status/{},{}/',
            BASE_URL + 'files/src/save/{}',
            '<a href="/status/[^,]+,{}/">(?P<id>.+)</a>',
            '.*(Đạt yêu cầu|Accepted|100)',
            '.*href="/files/src/(?P<id>\d+)/'
        )


if __name__ == '__main__':
    crawler = SpojCrawler()
    main(crawler, OUTPUT_DIR)
