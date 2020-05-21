from util import PixivError
import requests


class Requester():
    """Requests session wrapper"""
    def __init__(self, baseUrl, referer, token=None):
        self.session = requests.Session()
        self.baseUrl = baseUrl
        self.headers = {
            'Referer': referer,
            'Accept-Language': 'ja',
            'User-Agent': 'PixivAndroidApp/5.0.115 (Android 9.0.0; Android SDK built for x86)',
            'App-OS': 'android',
            'App-OS-Version': '9.0.0',
            'App-Version': '5.0.115',
        }
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def setHeaders(self, headers):
        self.headers.update(headers)

    def get(self, url=None, endpoint=None, params=None, headers=None, data=None):
        if not headers:
            headers = self.headers
        if not url and not endpoint:
            raise PixivError(
                '[ERROR] get() but no url or endpoint is set.'
            )
        if endpoint:
            url = self.baseUrl + endpoint
        return self.session.get(url, params=params, headers=headers, data=data)

    def post(self, url=None, endpoint=None, params=None, headers=None, data=None):
        if not headers:
            headers = self.headers
        if not url and not endpoint:
            raise PixivError(
                '[ERROR] post() but no url or endpoint is set.'
            )
        if endpoint:
            url = self.baseUrl + endpoint
        return self.session.post(url, params=params, headers=headers, data=data)
