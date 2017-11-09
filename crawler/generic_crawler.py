import os
import re
from bs4 import BeautifulSoup
import requests


class GenericCrawler(object):
    def __init__(self,
                 base_url, user_profile_url, problem_status_url, code_url,
                 status_regex, accepted_status_regex, submission_id_regex):
        self.base_url = base_url
        self.user_profile_url = user_profile_url
        self.problem_status_url = problem_status_url
        self.code_url = code_url
        self.status_regex = status_regex
        self.accepted_status_regex = accepted_status_regex
        self.submission_id_regex = submission_id_regex
        self.session = requests.Session()

    def get_element_by_selector(self, url, selector):
        request = self.session.get(url)
        if request.status_code != 200:
            print 'Unable to crawl page {}'.format(url)
            return None
        html = BeautifulSoup(request.text)
        return html.select(selector)

    @staticmethod
    def store_code(output_dir, problem_code, extension, text):
        if extension is not None:
            problem_code += '.' + extension
        with open(os.path.join(output_dir, problem_code), 'w') as file_id:
            file_id.write(text.encode('utf-8'))

    def _login(self, data):
        self.session.post(self.base_url, data)

    def is_accepted(self, text):
        return re.match(self.accepted_status_regex, text)

    def get_solved_problems(self, username):
        profile_url = self.user_profile_url.format(user=username)
        print 'Crawling profile page from url = {}'.format(profile_url)

        elements = self.get_element_by_selector(profile_url, 'a')
        if elements is None:
            print 'No element found'
            return []

        problems_solved = []
        for element in elements:
            text = element.__str__().replace('\n', ' ')
            pattern = self.status_regex.format(user=username)
            problem_re = re.compile(pattern).match(text)

            if problem_re:
                problems_solved.append(problem_re.groupdict()['id'])

        return problems_solved

    def get_accepted_submission_id(self, username, problem_code):
        status_url = self.problem_status_url.format(user=username, problem=problem_code)
        print 'Find submission ID from {}'.format(status_url)

        elements = self.get_element_by_selector(status_url, 'tr')
        for element in elements:
            text = element.__str__().replace('\n', ' ')
            if self.is_accepted(text) is None:
                continue

            match_pattern = re.match(self.submission_id_regex, text)

            extension = 'txt'
            if text.find('JAVA') >= 0:
                extension = 'java'
            elif text.find('C++') >= 0:
                extension = 'cpp'
            elif text.find('CPP') >= 0:
                extension = 'cpp'
            elif text.find('PAS') >= 0:
                extension = 'pas'
            elif text.find('PYTH') >= 0:
                extension = 'py'

            if match_pattern:
                return match_pattern.groupdict()['id'], extension

        return None, None

    def download_solution(self, output_dir, username, problem_code):
        submission_id, extension = self.get_accepted_submission_id(username, problem_code)

        if submission_id is not None:
            code_url = self.code_url.format(id=submission_id)
            request = self.session.get(code_url)
            self.store_code(output_dir, problem_code, extension, request.text)
