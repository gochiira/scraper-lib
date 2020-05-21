from .util import checkRefresh
from .login import PixivLoginApi


class PixivPublicApi(PixivLoginApi):
    def __init__(self, username=None, password=None, authDict=None):
        PixivLoginApi.__init__(
            self,
            username,
            password,
            authDict,
            'https://public-api.secure.pixiv.net/v1/',
            'http://spapi.pixiv.net/'
        )

    @checkRefresh
    def getFollowing(self, page=1, per_page=20, publicity='public'):
        endpoint = '/me/following.json'
        params = {
            'page': page,
            'per_page': per_page,
            'publicity': publicity,
        }
        return self.session.get(endpoint=endpoint, params=params).json()
