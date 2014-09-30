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
        self.password = ''

    def login(self, _, password):
        self.password = password

    def download_solution(self, output_dir, username, problem_code):
        submission_id, _ = self.get_accepted_submission_id(username, problem_code)
        code_url = self.code_url.format(id=submission_id)
        request = self.session.post(code_url, data={
            'Action': 'getsubmit',
            'JudgeId': username + 'PC',
            'PASSWORD': self.password
        })
        self.store_code(output_dir, problem_code, submission_id[submission_id.find('.')+1:], request.text)
        print submission_id

if __name__ == '__main__':
    crawler = TimusCrawler()
    main(crawler, OUTPUT_DIR)
