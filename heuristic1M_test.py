import unittest

import heuristics
from model import *


class Heuristic1MTestCase(unittest.TestCase):
    def test_define_execution_order(self):
        self.assertEqual([[2], [3], [4]], heuristics.define_execution_order([[2, 3, 4], [3, 4], [4, 5], [5]]))

    def test_ranking_heuristic(self):
        rankin = heuristics.create_ranking_by_processingrate(
            [Activity(0, 20, 2), Activity(1, 20, 2), Activity(2, 40, 1), Activity(3, 40, 1), Activity(4, 10, 1)])
        # heuristics.ranking_heuristic([[0, 1], [2, 3, 4], [2, 3]],
        #                          [Activity(0, 20, 2), Activity(1, 20, 2), Activity(2, 40, 1), Activity(3, 40, 1),
        #                          Activity(4, 10, 1)], rankin)


if __name__ == '__main__':
    unittest.main()
