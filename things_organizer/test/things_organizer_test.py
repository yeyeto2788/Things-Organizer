# pylint:disable=C0103,C0111,W0212,W0611
import os
import time
import logging
import unittest

from things_organizer import app
from things_organizer.utils import DB_PATH


TEST_DB = 'test.db'


class TestAppEndPoints(unittest.TestCase):
    """
    Unitary tests for utils.
    """

    def register(self, email, username, password, password2):
        """
        Simple method to reuse on all test register a given user.

        Args:
            email: user's email.
            username: user's username
            password: user's password
            password2: user's password confirmation.

        Returns:

        """
        return self.app.post(
            '/register',
            data=dict(email=email, username=username, password=password, password2=password2),
            follow_redirects=True
        )

    def login(self, username, password):
        """
        Simle login method to be reuse on all tests for given user.

        Args:
            username: username of user.
            password: password for user.

        Returns:

        """
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        """
        Simle logout method to be reuse on all tests.

        Returns:

        """
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

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
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_PATH,
                                                                            TEST_DB)
        self.get_routes = [rule.__str__() for rule in app.url_map._rules if 'GET' in rule.methods and (not rule.__str__().endswith(
                        '/<int:int_id>') and not rule.__str__().endswith('/<path:filename>'))]

        self.app = app.test_client()

    def test_root(self):
        """
        Check whether the root path is enable.

        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200, msg="Expected: {}, Obtained: {}".format(
            200, response.status_code))

    def test_valid_login(self):
        """
        Single test for valid login.

        """

        response = self.login('admin', '1')
        self.assertEqual(response.status_code, 200, msg="Expected: {}, Obtained: {}".format(
            200, response.status_code))
        self.assertIn(b'Welcome, admin!', response.data)

    def test_invalid_login(self):
        """
        Single test for invalid login.

        """

        response = self.login('user_not_exist', 'non_password')
        self.assertEqual(response.status_code, 200, msg="Expected: {}, Obtained: {}".format(
            200, response.status_code))
        self.assertIn(b'Incorrect username or password.', response.data)

    def test_logout(self):
        """
        Single test for logout.

        """
        response = self.logout()
        self.assertEqual(response.status_code, 200, msg="Expected: {}, Obtained: {}".format(
            200, response.status_code))

    def test_valid_user_registration(self):
        """
        Single test for valid registration.

        """
        user_name = 'testuser{}'.format(str(int(time.time())))
        response = self.register('{}@mail.com'.format(user_name), user_name, 'psk', 'psk')
        self.assertEqual(response.status_code, 200)
        str_search = 'Welcome, {}! Please login.'.format(user_name)
        self.assertIn(str_search.encode('utf-8'), response.data)

    def test_invalid_user_registration(self):
        """
        Single test for invalid registration.

        """
        user_name = 'testuser{}'.format(str(int(time.time())))
        int_psswd = 548273
        response = self.register(
            '{}@mail.com'.format(user_name), user_name, str(int_psswd), str(int_psswd + 1))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hmmm, seems like there was an error registering you account.',
                      response.data)

    def test_get_routes(self):
        """
        Test to check whether all `GET` endpoints are fully working.

        """
        for route in self.get_routes:
            response = self.app.get(route, follow_redirects=True)
            self.assertEqual(response.status_code, 200, msg="Expected: {}, Obtained: {}".format(
                200, response.status_code))

    def tearDown(self):
        """
        Test tearDown.
        """

    @classmethod
    def tearDownClass(cls):
        """
        Global tearDown.
        """
