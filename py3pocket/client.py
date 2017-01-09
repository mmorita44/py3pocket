# -*- coding: utf-8 -*-
import re
from requests import Session
from requests.exceptions import RequestException


class Client:
    """
    Pocket API Client.
    """

    def __init__(self, consumer_key: str, username: str, password: str):

        self.__consumer_key = consumer_key
        self.__session = Session()

        # initial access
        resp = self.__session.get('https://getpocket.com/login')
        if resp.status_code != 200:
            raise PocketError('Pocket Initial Access Error', response=resp)

        # get form_check parameter
        match = re.compile('<input[^<]+name="form_check"[^>]+>').search(resp.content.decode())
        match = re.compile('value="([^"]+)"').search(match.group(0))
        form_check = match.group(1)

        # login
        resp = self.__session.post('https://getpocket.com/login_process.php',
                                   data={'feed_id': username, 'password': password, 'form_check': form_check,
                                         'is_ajax': 1})
        if resp.status_code != 200:
            raise PocketError('Pocket Login Error', response=resp)

        # confirm login result
        if resp.json()['status'] != 1:
            raise PocketError('Pocket Confirming Login Result Error: username or password is incorrect.', response=resp)

        # get request token via OAuth
        resp = self.__session.post('https://getpocket.com/v3/oauth/request',
                                   json={'consumer_key': self.__consumer_key, 'redirect_uri': 'http://localhost'},
                                   headers={'X-Accept': 'application/json'})
        if resp.status_code != 200:
            raise PocketError('Pocket Getting Request Token via OAuth Error', response=resp)
        code = resp.json()['code']

        # authorize via OAuth
        resp = self.__session.get('https://getpocket.com/auth/authorize',
                                  params={'request_token': code, 'redirect_uri': 'http://localhost'},
                                  allow_redirects=False)
        if resp.status_code != 302:
            raise PocketError('Pocket Authorizing via OAuth Error: possible to not yet complete the authorization. ' +
                              'Access %s and allows to permissions.' % resp.request.url, response=resp)

        # get access token via OAuth
        resp = self.__session.post('https://getpocket.com/v3/oauth/authorize',
                                   json={'consumer_key': self.__consumer_key, 'code': code},
                                   headers={'X-Accept': 'application/json'})
        if resp.status_code != 200:
            raise PocketError('Pocket Getting Access Token via OAuth Error', response=resp)
        self.__access_token = resp.json()['access_token']

    def add(self, data: dict, **kwargs) -> dict:
        """Adding Items to Pocket.

        :param data: json to send in the body of the :class:`request.Session`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        data.update({'consumer_key': self.__consumer_key, 'access_token': self.__access_token})

        resp = self.__session.post('https://getpocket.com/v3/add', json=data, **kwargs)
        if resp.status_code != 200:
            raise PocketError('Pocket Adding Error', response=resp)

        return resp.json()

    def modify(self, data: dict, **kwargs) -> dict:
        """Modifying a User's Pocket Data.

        :param data: json to send in the body of the :class:`request.Session`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        data.update({'consumer_key': self.__consumer_key, 'access_token': self.__access_token})

        resp = self.__session.post('https://getpocket.com/v3/send', json=data, **kwargs)
        if resp.status_code != 200:
            raise PocketError('Pocket Modifying Error', response=resp)

        return resp.json()

    def retrieve(self, data: dict=None, **kwargs):
        """Retrieving a User's Pocket Data.

        :param data: json to send in the body of the :class:`request.Session`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        data = dict() if data is None else data
        data.update({'consumer_key': self.__consumer_key, 'access_token': self.__access_token})

        resp = self.__session.post('https://getpocket.com/v3/get', json=data, **kwargs)
        if resp.status_code != 200:
            raise PocketError('Pocket Retrieving Error', response=resp)

        return resp.json()


class PocketError(RequestException):
    """An Connection error occurred."""
