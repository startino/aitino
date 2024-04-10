import requests
import uuid
from ._utils.consts import *
from ._utils.exceptions import WrongCreds, APIException
from typing import Optional


class _RedditAuthBase:
    def __init__(self, api_token=None, reddit_session=None):
        self.api_token = api_token
        self.sb_access_token = None
        self.user_id = None
        self._reddit_session = reddit_session

    @property
    def is_reauthable(self):
        return self._reddit_session is not None and self.api_token is not None

    def _get_repr_pkl(self):
        raise NotImplementedError("unreachable")

    def authenticate(self):
        self._get_userid_sb_token()
        return {'sb_access_token': self.sb_access_token, 'user_id': self.user_id}

    def _get_userid_sb_token(self):
        headers = {
            'User-Agent': MOBILE_USERAGENT,
            'Authorization': f'Bearer {self.api_token}'
        }
        sb_token_j = requests.get(f'{S_REDDIT}/api/v1/sendbird/me', headers=headers).json()
        self.sb_access_token = sb_token_j['sb_access_token']
        user_id_j = requests.get(f'{OAUTH_REDDIT}/api/v1/me.json', headers=headers).json()
        self.user_id = 't2_' + user_id_j['id']

    def refresh_api_token(self):
        cookies = {'reddit_session': self._reddit_session}
        headers = {
            'User-Agent': WEB_USERAGENT,
            'Authorization': f'Bearer {self.api_token}',
        }
        data = {
            'accessToken': self.api_token,
            'unsafeLoggedOut': 'false',
            'safe': 'true'
        }
        response = requests.post(f'{WWW_REDDIT}/refreshproxy', headers=headers, cookies=cookies, data=data).json()
        self.api_token = response['accessToken']
        return self.api_token


class PasswordAuth(_RedditAuthBase):
    def __init__(self, reddit_username: str, reddit_password: str, twofa: Optional[str] = None):
        super().__init__()
        self.reddit_username = reddit_username
        self.reddit_password = reddit_password
        self.twofa = twofa
        self._client_vendor_uuid = str(uuid.uuid4())
        self._reddit_session = None

    def authenticate(self):
        if self.is_reauthable:
            self.refresh_api_token()
        else:
            self._reddit_session = self._do_login()
            if self._reddit_session is None:
                raise WrongCreds("Wrong username or password")
            self.api_token = self._get_api_token()

        return super(PasswordAuth, self).authenticate()

    def _get_api_token(self):
        cookies = {'reddit_session': self._reddit_session}
        headers = {
            'Authorization': f'Basic {OAUTH_CLIENT_ID_B64}',
            'User-Agent': MOBILE_USERAGENT,
            'client-vendor-id': self._client_vendor_uuid,
        }
        data = '{"scopes":["*"]}'
        response = requests.post(f'{ACCOUNTS_REDDIT}/api/access_token', headers=headers, cookies=cookies, data=data)
        try:
            access_token = response.json()['access_token']
        except KeyError:
            raise APIException(response.text)
        return access_token

    def _do_login(self):
        headers = {
            'User-Agent': WEB_USERAGENT,
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': 'https://old.reddit.com/login',
            'Origin': 'https://old.reddit.com',
        }
        data = {
            'op': 'login',
            'user': self.reddit_username,
            'passwd': f'{self.reddit_password}:{self.twofa}' if bool(self.twofa) else self.reddit_password,
            'api_type': 'json'
        }
        response = requests.post(f'{WWW_REDDIT}/api/login/{self.reddit_username}', headers=headers, data=data)
        reddit_session = response.cookies.get("reddit_session")
        return reddit_session

    def _get_repr_pkl(self):
        return self.reddit_username


class TokenAuth(_RedditAuthBase):
    def __init__(self, token, reddit_session=None):
        super().__init__(token, reddit_session)

    def _get_repr_pkl(self):
        return self.api_token
