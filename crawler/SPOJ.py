# -*- coding: utf-8 -*-

import os
import sys
import requests
from generic_crawler import GenericCrawler


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code')
BASE_URL = 'https://vn.spoj.com/'


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

    def login(self, session, username, password):
        super(SpojCrawler, self)._login(session, data={
            'login_user': username,
            'password': password
        })


def main(crawler):
    global OUTPUT_DIR

    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        if len(sys.argv) >= 4:
            OUTPUT_DIR = sys.argv[3]
    else:
        username = raw_input('Your username: ')
        password = raw_input('Your password: ')

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    session = requests.Session()
    crawler.login(session, username, password)

    problems = crawler.get_solved_problems(session, username)
    print '{} has solved {} problems'.format(username, len(problems))

    for problem in problems:
        crawler.download_solution(session, OUTPUT_DIR, username, problem)


if __name__ == '__main__':
    crawler = SpojCrawler()
    main(crawler)
