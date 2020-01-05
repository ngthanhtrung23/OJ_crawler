import os
import re
from bs4 import BeautifulSoup
import requests


class SPOJCrawler(object):
    def __init__(self,
                 base_url, code_url):
        self.base_url = base_url
        self.code_url = code_url
        self.session = requests.Session()

    @staticmethod
    def store_code(output_dir, extension, text):
        with open(output_dir+ '.' + extension, 'wb') as file_id:
            file_id.write(text.encode('utf-8'))

    def _login(self, username, password):
        data =  {'login_user': username,
                'password': password}

        self.session.post(self.base_url, data)

    def download_solution(self, output_dir, username, submission_id, extension):
        if extension == 'JAVA':
            extension = 'java'
        elif extension == 'C++':
            extension = 'cpp'
        elif extension == 'CPP':
            extension = 'cpp'
        elif extension == 'PAS':
            extension = 'pas'
        elif extension == 'PYTH':
            extension = 'py'
        else:
            extension = 'txt'
        code_url = self.code_url.format(id = submission_id)
        request = self.session.get(code_url)
        self.store_code(output_dir, extension, request.text)
