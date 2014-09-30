from unittest import TestCase
from crawler.SPOJ import SpojCrawler


class TestSpojCrawler(TestCase):
    def setUp(self):
        self.spoj_crawler = SpojCrawler()

    def test_login(self):
        self.spoj_crawler.login('ntu_gladiators', 'acmacm')
        request = self.spoj_crawler.session.get('http://www.spoj.com/')
        self.assertTrue(request.text.find('ntu_gladiators') > 0)

    def test_problem_solved(self):
        self.assertEqual(self.spoj_crawler.get_solved_problems('ntu_gladiators'), ['ABCDEF', 'TEST', 'VPALIN'])

    def test_get_submission_id(self):
        self.spoj_crawler.login('ntu_gladiators', 'acmacm')
        self.assertEqual(self.spoj_crawler.get_accepted_submission_id('ntu_gladiators', 'ABCDEF'), ('12500327', 'pas'))
        self.assertEqual(self.spoj_crawler.get_accepted_submission_id('ntu_gladiators', 'TEST'), ('4211734', 'cpp'))
        self.assertEqual(self.spoj_crawler.get_accepted_submission_id('ntu_gladiators', 'VPALIN'), (None, None))
        self.assertEqual(self.spoj_crawler.get_accepted_submission_id('ntu_gladiators', 'MOEBIUS'), (None, None))
