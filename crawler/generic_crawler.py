import os
import re
from bs4 import BeautifulSoup


class GenericCrawler:
    def __init__(self,
                 base_url, user_profile_url, problem_status_url, code_url,
                 status_regex, accepted_status_regex, submission_id_regex):
        self.BASE_URL = base_url
        self.USER_PROFILE_URL = user_profile_url
        self.PROBLEM_STATUS_URL = problem_status_url
        self.CODE_URL = code_url
        self.STATUS_REGEX = status_regex
        self.ACCEPTED_STATUS_REGEX = accepted_status_regex
        self.SUBMISSION_ID_REGEX = submission_id_regex

    @staticmethod
    def get_element_by_selector(session, url, selector):
        request = session.get(url)
        if request.status_code != 200:
            print 'Unable to crawl page {}'.format(url)
            return None
        html = BeautifulSoup(request.text)
        return html.select(selector)

    @staticmethod
    def store_code(output_dir, problem_code, extension, text):
        with open(os.path.join(output_dir, problem_code + '.' + extension), 'w') as f:
            f.write(text.encode('utf-8'))

    def _login(self, session, data):
        session.post(self.BASE_URL, data)

    def is_accepted(self, text):
        return re.match(self.ACCEPTED_STATUS_REGEX, text)

    def get_solved_problems(self, session, username):
        profile_url = self.USER_PROFILE_URL.format(username)
        print 'Crawling profile page from url = {}'.format(profile_url)

        elements = self.get_element_by_selector(session, profile_url, 'a')
        if elements is None:
            return []

        problems_solved = []
        for element in elements:
            text = element.__str__().replace('\n', ' ')
            pattern = self.STATUS_REGEX.format(username)
            problem_re = re.compile(pattern).match(text)

            if problem_re:
                problems_solved.append(problem_re.groupdict()['id'])

        return problems_solved

    def download_solution(self, session, output_dir, username, problem_code):
        status_url = self.PROBLEM_STATUS_URL.format(username, problem_code)
        print 'Find submission ID from {}'.format(status_url)

        request = session.get(status_url)
        if request.status_code != 200:
            print 'Unable to crawl page'
            return 1

        html = BeautifulSoup(request.text.replace('kol1', 'kol'))
        elements = html.select('tr[class="kol"]')
        for element in elements:
            text = element.__str__().replace('\n', ' ')
            if self.is_accepted(text) is None:
                continue

            match_pattern = re.match(self.SUBMISSION_ID_REGEX, text)

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
                code_url = self.CODE_URL.format(submission_id)
                request = session.get(code_url)
                self.store_code(output_dir, problem_code, extension, request.text)
                break
