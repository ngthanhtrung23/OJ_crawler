import os
import sys
from generic_crawler import GenericCrawler

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
        self.user_code = ''

    def login(self, _, password):
        self.password = password

    def download_solution(self, output_dir, username, problem_code):
        submission_id, _ = self.get_accepted_submission_id(username, problem_code)
        code_url = self.code_url.format(id=submission_id)
        request = self.session.post(code_url, data={
            'Action': 'getsubmit',
            'JudgeId': username + self.user_code,
            'PASSWORD': self.password
        })
        self.store_code(output_dir, problem_code, submission_id[submission_id.find('.')+1:], request.text)
        print submission_id


def main(crawler, output_dir):
    if len(sys.argv) >= 4:
        username = sys.argv[1]
        password = sys.argv[2]
        crawler.user_code = sys.argv[3]
    else:
        username = raw_input('Your username: ')
        password = raw_input('Your password: ')
        crawler.user_code = raw_input('Your 2 character user code: ')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    crawler.login(username, password)

    problems = crawler.get_solved_problems(username)
    print '{} has solved {} problems'.format(username, len(problems))

    for problem in problems:
        for extension in ['java', 'cpp', 'py', 'pas']:
            if os.path.isfile(os.path.join(output_dir, problem + '.' + extension)):
                break
        else:
            crawler.download_solution(output_dir, username, problem)

if __name__ == '__main__':
    crawler = TimusCrawler()
    main(crawler, OUTPUT_DIR)
