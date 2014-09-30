from unittest import TestCase
from crawler.timus import TimusCrawler


class TestTimusCrawler(TestCase):
    def setUp(self):
        self.timus_crawler = TimusCrawler()
        pass

    def test_problem_solved(self):
        solved_problems = self.timus_crawler.get_solved_problems('68734')
        self.assertTrue(len(solved_problems) >= 187)

        some_problems = [
            '1000', '1001', '1002', '1004', '1100', '1102', '1283', '1306', '1400'
        ]
        for problem in some_problems:
            self.assertTrue(problem in solved_problems)

    def test_get_submission_id(self):
        # Note: For timus problem, the submission ID already contains extension, thus the extension part is
        # not important
        self.assertEqual(self.timus_crawler.get_accepted_submission_id('68734', '1675'), ('4168295.cpp', 'cpp'))
        self.assertEqual(self.timus_crawler.get_accepted_submission_id('68734', '1679'), ('4168185.cpp', 'cpp'))
        self.assertEqual(self.timus_crawler.get_accepted_submission_id('68734', '1069'), ('3374609.pas', 'txt'))
