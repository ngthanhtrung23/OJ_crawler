import os
from generic_crawler import GenericCrawler
from VOJ import main

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code/Timus')
BASE_URL = 'http://acm.timus.ru/'


class TimusCrawler(GenericCrawler):
    def __init__(self):
        GenericCrawler.__init__(
            self,
            BASE_URL,
            BASE_URL + 'author.aspx?id={user}',
            BASE_URL + 'status.aspx?space=1&num={problem}&author={user}&count=100',
            BASE_URL + 'getsubmit.aspx/{id}',
            '<a href="status.aspx\?space=1&amp;num=(?P<id>\d+)&amp;author={user}"',
            '<tr class="(even|odd).*Accepted',
            '.*<a href="getsubmit\.aspx/(?P<id>[\da-z\.]+)"'
        )

    def login(self, username, password):
        pass


if __name__ == '__main__':
    crawler = TimusCralwer()
    main(crawler, OUTPUT_DIR)
