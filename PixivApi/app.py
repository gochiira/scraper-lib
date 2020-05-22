from .util import checkRefresh, PixivError
from .login import PixivLoginApi
import os.path


class PixivAppApi(PixivLoginApi):
    def __init__(self, username=None, password=None, authDict=None):
        PixivLoginApi.__init__(
            self,
            username,
            password,
            authDict,
            'https://app-api.pixiv.net/v1/',
            'https://app-api.pixiv.net'
        )

    @checkRefresh
    def getIllustDetail(self, illustID):
        endpoint = 'illust/detail'
        params = {
            'illust_id': illustID
        }
        return self.session.get(endpoint=endpoint, params=params).json()

    @checkRefresh
    def downloadIllust(self, url, name='', path='', prefix='', replace=False):
        """Download image"""
        if not path:
            if not name:
                name = os.path.basename(url)
            name = prefix + name
            path = os.path.join(os.path.curdir, name)
        if os.path.exists(path) and not replace:
            return False
        response = self.session.get(url)
        if response.status_code != 200:
            raise PixivError(
                f'Download Illust error! Response: {response.text}'
            )
        with open(path, 'wb') as outFile:
            outFile.write(response.content)
        return True
