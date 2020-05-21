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
    def downloadIllust(self, url, prefix='', name=None, path=os.path.curdir, replace=False):
        """Download image"""
        if not name:
            name = os.path.basename(url)
        name = prefix + name
        imgPath = os.path.join(path, name)
        if os.path.exists(imgPath) and not replace:
            return False
        response = self.session.get(url)
        if response.status_code != 200:
            raise PixivError(
                f'Download Illust error! Response: {response.text}'
            )
        with open(imgPath, 'wb') as outFile:
            outFile.write(response.content)
        return True
