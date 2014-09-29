# -*- coding: utf-8 -*-

import os
import re
import sys
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../code')
BASE_URL = 'https://vn.spoj.com/'
USER_PROFILE_URL = BASE_URL + 'users/{}/'
PROBLEM_STATUS_URL = BASE_URL + 'status/{},{}/'
CODE_URL = BASE_URL + 'files/src/save/{}'

STATUS_REGEX = '<a href="/status/[^,]+,{}/">(?P<id>.+)</a>'
ACCEPTED_STATUS_REGEX = re.compile('.*(Đạt yêu cầu)|(Accepted)|(100)')
SUBMISSION_ID_REGEX = re.compile('.*href="/files/src/(?P<id>\d+)/')

SESSION_OBJECT = requests.Session()


def get_solved_problems(username):
    profile_url = USER_PROFILE_URL.format(username)
    print 'Crawling profile page from url = {}'.format(profile_url)

    request = SESSION_OBJECT.get(profile_url)
    if request.status_code != 200:
        print 'Unable to crawl page'
        return []

    html = BeautifulSoup(request.text)
    elements = html.select('a')
    
    problems_solved = []
    for element in elements:
        text = element.__str__().replace('\n', ' ')
        pattern = STATUS_REGEX.format(username)
        problem_re = re.compile(pattern).match(text)

        if problem_re:
            problems_solved.append(problem_re.groupdict()['id'])

    return problems_solved
   

def is_accepted(text):
    return ACCEPTED_STATUS_REGEX.match(text)


def download_solution(SESSION_OBJECT, username, problem_code):
    status_url = PROBLEM_STATUS_URL.format(username, problem_code)
    print 'Find submission ID from {}'.format(status_url)

    request = SESSION_OBJECT.get(status_url)
    if request.status_code != 200:
        print 'Unable to crawl page'
        return 1

    html = BeautifulSoup(request.text.replace('kol1', 'kol'))
    elements = html.select('tr[class="kol"]')
    for element in elements:
        text = element.__str__().replace('\n', ' ')
        if is_accepted(text) is None:
            continue

        match_pattern = SUBMISSION_ID_REGEX.match(text)

        extension = 'txt'
        if text.find('JAVA') >= 0:
            extension = 'java'
        elif text.find('C++') >= 0:
            extension = 'cpp'
        elif text.find('PAS') >= 0:
            extension = 'pas'
        elif text.find('PYTH') >= 0:
            extension = 'py'

        if match_pattern:
            submission_id = match_pattern.groupdict()['id']
            code_url = CODE_URL.format(submission_id)
            request = SESSION_OBJECT.get(code_url)
            with open(os.path.join(OUTPUT_DIR, problem_code + '.' + extension), 'w') as f:
                f.write(request.text)


def login(username, password):
    SESSION_OBJECT.post(BASE_URL, data={
        'login_user': username,
        'password': password
    })


if __name__ == '__main__':
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

    login(username, password)

    problems = get_solved_problems(username)
    print '{} has solved {} problems'.format(username, len(problems))

    for problem in problems:
        download_solution(SESSION_OBJECT, username, problem)
