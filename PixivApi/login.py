from util import PixivError
from session import Requester
from datetime import datetime
import hashlib


class PixivLoginApi():
    client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'
    tokens = {
        'access_token': '',
        'refresh_token': '',
        'last_refresh': '',
        'user_id': ''
    }

    def __init__(self, username=None, password=None, authDict={}, baseUrl='', referer=''):
        if authDict:
            self.tokens = authDict
            self.session = Requester(
                token=self.tokens['access_token'],
                baseUrl=baseUrl,
                referer=referer
            )
            self.refreshLogin()
        elif username and password:
            self.session = Requester(
                baseUrl=baseUrl,
                referer=referer
            )
            self.login(username, password)
        else:
            raise PixivError(
                '[ERROR] login() but no password or refresh_token is set.'
            )

    def login(self, username=None, password=None, refresh_token=None):
        """Login to acquire a new token"""
        url = 'https://oauth.secure.pixiv.net/auth/token'
        localTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        clientHash = hashlib.md5(
            (localTime + self.hash_secret).encode('utf-8')
        ).hexdigest()
        headers = {
            'Referer': 'https://app-api.pixiv.net/',
            'Accept-Language': 'ja',
            'User-Agent': 'PixivAndroidApp/5.0.115 (Android 9.0.0; Android SDK built for x86)',
            'App-OS': 'android',
            'App-OS-Version': '9.0.0',
            'App-Version': '5.0.115',
            'X-Client-Time': localTime,
            'X-Client-Hash': clientHash
        }
        data = {
            'get_secure_url': 1,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        if (username is not None) and (password is not None):
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif refresh_token:
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token
        else:
            raise PixivError(
                '[ERROR] login() but no password or refresh_token is set.'
            )
        r = self.session.post(url, headers=headers, data=data)
        if r.status_code not in [200, 301, 302]:
            if data['grant_type'] == 'password':
                raise PixivError(
                    '[ERROR] login() failed! check username and password.'
                )
            else:
                raise PixivError(
                    '[ERROR] login() failed! check refresh_token.'
                )
        try:
            token = r.json()
            self.tokens['user_id'] = token["response"]["user"]["id"]
            self.tokens['access_token'] = token["response"]["access_token"]
            self.tokens['refresh_token'] = token["response"]["refresh_token"]
            self.tokens['last_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise PixivError(
                f'Get access_token error! Response: {e}'
            )

    def refreshLogin(self, force=False):
        now = datetime.now()
        last_refresh = datetime.strptime(
            self.tokens['last_refresh'],
            '%Y-%m-%d %H:%M:%S'
        )
        if (now - last_refresh).seconds > 3600 or force:
            try:
                self.login(refresh_token=self.tokens['refresh_token'])
            except:
                self.login(
                    username=self.tokens['username'],
                    password=self.tokens['password']
                )
