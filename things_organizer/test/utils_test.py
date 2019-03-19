# pylint:disable=C0103,C0111,W0212,W0611
import os
import logging
import unittest

from things_organizer import utils


class TestUtilsWithoutTempFiles(unittest.TestCase):
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

        self.assertEqual(lst_comparable, lst_return,
                         msg="Expected: {}, Obtained: {}".format(lst_comparable, lst_return))

    def test_str_to_bln(self):
        """
        Unit Test to check the behaviour of the sort alphanumeric list method

        """

        dict_to_check = {'y': 1, 'yes': 1, 't': 1, 'true': 1, 'on': 1, '1': 1, 'n': 0, 'no': 0,
                         'f': 0, 'false': 0, 'off': 0, '0': 0}

        lst_exception = ['loco', 'crazy']

        for dict_key in dict_to_check:
            bln_return = utils.str_to_bln(dict_key)
            self.assertEqual(bln_return, dict_to_check[dict_key],
                             msg="Expected: {}, Obtained: {}".format(
                                 dict_to_check[dict_key], bln_return))

        for item in lst_exception:
            with self.assertRaises(ValueError) as exe_error:
                utils.str_to_bln(item)
                self.assertTrue('is not compatible to convert into boolean.' in exe_error.exception)

    def tearDown(self):
        """
        Test tearDown.
        """

    @classmethod
    def tearDownClass(cls):
        """
        Global tearDown.
        """


class TestUtilsWithTempFiles(unittest.TestCase):
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

        self.zip_name = 'test_files'
        self.temp_directory = os.path.join(os.getcwd(), 'temp')
        zip_path = os.path.join(self.temp_directory, '{}.zip'.format(self.zip_name))

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

        if os.path.exists(zip_path):
            os.remove(zip_path)

        self.files_directory = os.path.join(os.getcwd(), 'temp')

        self.files = ['file{}.txt'.format(x) for x in range(1, 6)]

        for index, item in enumerate(self.files):
            file_path = os.path.join(self.temp_directory, item)
            with open(file_path, 'w') as txt_file:
                txt_file.write('File created: {}\nIndex: {}'.format(item, index))
            txt_file.close()

    def test_zip_dir(self):
        """
        Unit test for the `zip_dir` function from utils module.

        """

        str_return = utils.zip_dir(self.temp_directory, self.zip_name, self.temp_directory)

        zip_path = os.path.join(self.temp_directory, '{}.zip'.format(self.zip_name))

        if os.path.exists(zip_path):
            bln_execution = True
            os.remove(zip_path)
        else:
            bln_execution = False

        self.assertTrue(bln_execution, msg="Expected: 1, Obtained: {}".format(bln_execution))
        self.assertEqual(str_return, zip_path,
                         msg="Expected: {}, Obtained: {}".format(zip_path, str_return))

    def tearDown(self):
        """
        Test tearDown.
        """

        for file in self.files:
            file_path = os.path.join(self.temp_directory, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        os.removedirs(self.temp_directory)

    @classmethod
    def tearDownClass(cls):
        """
        Global tearDown.
        """


