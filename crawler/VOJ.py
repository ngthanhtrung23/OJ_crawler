# -*- coding: utf-8 -*-

import os
import sys
import requests
from generic_crawler import GenericCrawler


OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BASE_URL = 'http://vn.spoj.com/'


class VojCrawler(GenericCrawler):
    def __init__(self):
        GenericCrawler.__init__(
            self,
            BASE_URL,
            BASE_URL + 'users/{user}/',
            BASE_URL + 'status/{problem},{user}/',
            BASE_URL + 'files/src/save/{id}',
            '<a href="/status/[^,]+,{user}/">(?P<id>.+)</a>',
            '<tr class="kol.*(Đạt yêu cầu|accepted|100)',
            '.*href="/files/src/(?P<id>\d+)/'
        )

    def login(self, username, password):
        super(VojCrawler, self)._login(data={
            'login_user': username,
            'password': password
        })


def main(crawler, output_dir):
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        if len(sys.argv) >= 4:
            output_dir = sys.argv[3]
    else:
        username = raw_input('Your username: ')
        password = raw_input('Your password: ')

    output_dir = os.path.join(output_dir, username, 'VOJ')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    crawler.login(username, password)

    problems = crawler.get_solved_problems(username)
    print '{} has solved {} problems'.format(username, len(problems))

    for problem in problems:
        for extension in ['java', 'cpp', 'py', 'pas', 'txt']:
            if os.path.isfile(os.path.join(output_dir, problem + '.' + extension)):
                break
        else:
            crawler.download_solution(output_dir, username, problem)


if __name__ == '__main__':
    crawler = VojCrawler()
    main(crawler, OUTPUT_DIR)
