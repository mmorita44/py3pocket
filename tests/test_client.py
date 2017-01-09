# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock
from py3pocket import Client, PocketError
from requests import Session


class StubClient(Client):

    def __init__(self):
        self._Client__consumer_key = ''
        self._Client__access_token = ''
        self._Client__session = Session()


class TestClient(unittest.TestCase):
    """
    Test Case of Pocket API Client.
    """

    @classmethod
    def setUpClass(cls):
        cls.__client = StubClient()

    def test_initial_access_error(self):

        get_obj = type('', (), {'status_code': 400})

        with patch.object(Session, 'get', MagicMock(return_value=get_obj)):
            with self.assertRaises(PocketError) as e:
                Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Initial Access Error')

    def test_login_error(self):

        get_obj = type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()})
        post_obj = type('', (), {'status_code': 400})

        with patch.object(Session, 'get', MagicMock(return_value=get_obj)):
            with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
                with self.assertRaises(PocketError) as e:
                    Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Login Error')

    def test_confirming_login_result_error(self):

        get_obj = type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()})
        post_obj = type('', (), {'status_code': 200, 'json': lambda: {'status': 0}})

        with patch.object(Session, 'get', MagicMock(return_value=get_obj)):
            with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
                with self.assertRaises(PocketError) as e:
                    Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Confirming Login Result Error: username or password is incorrect.')

    def test_getting_request_token_via_oauth_error(self):

        get_obj = type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()})
        post_obj = [type('', (), {'status_code': 200, 'json': lambda: {'status': 1}}),
                    type('', (), {'status_code': 400})]

        with patch.object(Session, 'get', MagicMock(return_value=get_obj)):
            with patch.object(Session, 'post', MagicMock(side_effect=post_obj)):
                with self.assertRaises(PocketError) as e:
                    Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Getting Request Token via OAuth Error')

    def test_authorizing_via_oauth_error(self):

        get_obj = [type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()}),
                   type('', (), {'status_code': 400, 'request': type('', (), {'url': 'localhost'})})]
        post_obj = [type('', (), {'status_code': 200, 'json': lambda: {'status': 1}}),
                    type('', (), {'status_code': 200, 'json': lambda: {'code': 'code'}})]

        with patch.object(Session, 'get', MagicMock(side_effect=get_obj)):
            with patch.object(Session, 'post', MagicMock(side_effect=post_obj)):
                with self.assertRaises(PocketError) as e:
                    Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Authorizing via OAuth Error: possible to not yet complete the ' +
                                           'authorization. Access %s and allow to permissions.' % 'localhost')

    def test_getting_access_token_via_oauth_error(self):

        get_obj = [type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()}),
                   type('', (), {'status_code': 302})]
        post_obj = [type('', (), {'status_code': 200, 'json': lambda: {'status': 1}}),
                    type('', (), {'status_code': 200, 'json': lambda: {'code': 'code'}}),
                    type('', (), {'status_code': 400})]

        with patch.object(Session, 'get', MagicMock(side_effect=get_obj)):
            with patch.object(Session, 'post', MagicMock(side_effect=post_obj)):
                with self.assertRaises(PocketError) as e:
                    Client('', '', '')

        self.assertEqual(str(e.exception), 'Pocket Getting Access Token via OAuth Error')

    def test_init_success(self):

        get_obj = [type('', (), {'status_code': 200, 'content': '<input name="form_check" value="value">'.encode()}),
                   type('', (), {'status_code': 302})]
        post_obj = [type('', (), {'status_code': 200, 'json': lambda: {'status': 1}}),
                    type('', (), {'status_code': 200, 'json': lambda: {'code': 'code'}}),
                    type('', (), {'status_code': 200, 'json': lambda: {'access_token': 'access token'}})]

        with patch.object(Session, 'get', MagicMock(side_effect=get_obj)):
            with patch.object(Session, 'post', MagicMock(side_effect=post_obj)):
                client = Client('consumer key', '', '')

        self.assertEqual(client._Client__consumer_key, 'consumer key')
        self.assertEqual(client._Client__access_token, 'access token')

    def test_adding_error(self):

        post_obj = type('', (), {'status_code': 400})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            with self.assertRaises(PocketError) as e:
                TestClient.__client.add({})

        self.assertEqual(str(e.exception), 'Pocket Adding Error')

    def test_adding_success(self):

        post_obj = type('', (), {'status_code': 200, 'json': lambda: {'item_id': 1}})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            resp = TestClient.__client.add({})

        self.assertEqual(resp, {'item_id': 1})

    def test_modifying_error(self):

        post_obj = type('', (), {'status_code': 400})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            with self.assertRaises(PocketError) as e:
                TestClient.__client.modify({})

        self.assertEqual(str(e.exception), 'Pocket Modifying Error')

    def test_modifying_success(self):

        post_obj = type('', (), {'status_code': 200, 'json': lambda: {'item_id': 1}})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            resp = TestClient.__client.modify({})

        self.assertEqual(resp, {'item_id': 1})

    def test_retrieving_error(self):

        post_obj = type('', (), {'status_code': 400})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            with self.assertRaises(PocketError) as e:
                TestClient.__client.retrieve()

        self.assertEqual(str(e.exception), 'Pocket Retrieving Error')

    def test_retrieving_success(self):

        post_obj = type('', (), {'status_code': 200, 'json': lambda: {'item_id': 1}})

        with patch.object(Session, 'post', MagicMock(return_value=post_obj)):
            resp = TestClient.__client.retrieve()

        self.assertEqual(resp, {'item_id': 1})

