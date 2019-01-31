# pylint:disable=C0103,C0111,W0212,W0611

import logging
import unittest

from things_organizer import utils


class TestUtils(unittest.TestCase):
    """
    Unitary tests for utils.
    """

    @classmethod
    def setUpClass(cls):
        """
        Global setUp.
        """

        logging.basicConfig(level=logging.INFO)

    def setUp(self):
        """
        Test setUp.
        """

    def test_sort_alphanumeric_list(self):
        """
        Unit Test to check the behaviour of the sort alphanumeric list method
        """
        lst_comparable = ["AA1", "AA4", "AE1", "AL1", "CC2"]
        lst_return = utils.sort_alphanumeric_list(["AA4", "AL1", "AA1", "CC2", "AE1"])

        self.assertEquals(lst_comparable, lst_return,
                          "Expected: {}, Obtained: {}".format(lst_comparable, lst_return))

    def tearDown(self):
        """
        Test tearDown.
        """

    @classmethod
    def tearDownClass(cls):
        """
        Global tearDown.
        """
