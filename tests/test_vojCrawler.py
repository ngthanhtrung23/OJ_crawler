from unittest import TestCase, main as unittest_main
from crawler.VOJ import VojCrawler


class TestVojCrawler(TestCase):
    def setUp(self):
        self.voj_crawler = VojCrawler()

    def test_login(self):
        # Login
        self.voj_crawler.login('mrtrung', '22330066')
        # After login, should see account on home page
        request = self.voj_crawler.session.get('https://vn.spoj.com/')
        self.assertTrue(request.text.find('mrtrung') > 0)

    def test_problem_solved(self):
        self.assertEqual(self.voj_crawler.get_solved_problems('mrtrung'), ['NPR'])
        solved_problems = self.voj_crawler.get_solved_problems('ntu_gladiators')

        # Number of solved problems on Sep 30th, 2014
        self.assertTrue(solved_problems >= 55)

        # Solved problems should appear
        some_problems = [
            'ALERT', 'EARTHQK', 'HEAP1', 'MATCH2', 'NKBM', 'PIZZALOC', 'TJALG',
            'COP3', 'FLOW1', 'KWAY', 'MILITARY', 'NKMSG', 'QMAX2', 'SUBSTR',
            'BOXES', 'PALINX', 'BWGAME'
        ]
        for problem in some_problems:
            self.assertTrue(problem in solved_problems)

    def test_get_submission_id(self):
        self.voj_crawler.login('ntu_gladiators', 'acmacm')
        self.assertEqual(self.voj_crawler.get_accepted_submission_id('ntu_gladiators', 'THREE'), ('4182941', 'cpp'))
        self.assertEqual(self.voj_crawler.get_accepted_submission_id('ntu_gladiators', 'ETF'), ('4181866', 'cpp'))
        self.assertEqual(self.voj_crawler.get_accepted_submission_id('ntu_gladiators', 'POST'), ('9680683', 'pas'))
        self.assertEqual(self.voj_crawler.get_accepted_submission_id('ntu_gladiators', 'BWTRI'), (None, None))
        self.assertEqual(self.voj_crawler.get_accepted_submission_id('ntu_gladiators', 'BWGAME'), (None, None))

if __name__ == '__main__':
    unittest_main()
