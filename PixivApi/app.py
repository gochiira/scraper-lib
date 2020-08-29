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

    @checkRefresh
    def getUgoiraDetail(self, illustID):
        """Get ugoira metadatas"""
        endpoint = 'ugoira/metadata'
        params = {
            'illust_id': illustID
        }
        return self.session.get(endpoint=endpoint, params=params).json()

    @checkRefresh
    def searchIllust(
        self,
        keyword,
        search_target='partial_match_for_tags',
        sort='date_desc',
        duration=None,
        start_date=None,
        end_date=None,
        filter='for_ios',
        offset=None
    ):
        """
        Search illust
            params:
                keyword: str
                    query keyword
                search_target: str
                    ['partial_match_for_tags', 'exact_match_for_tags', 'title_and_caption']
                sort: str
                   ['date_desc', 'date_asc']
                   ['popular_desc'] *require premium
                duration: str
                   ['within_last_day', 'within_last_week', 'within_last_month']
                start_date: str
                end_date: str
                    '2020-07-01'
                filter: str
                    ['for_android',  'for_ios']
                offset: int
                    0/30/60...
        """
        endpoint = 'search/illust'
        params = {
            'word': keyword,
            'search_target': search_target,
            'sort': sort,
            'filter': filter,
        }
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if duration:
            params['duration'] = duration
        if offset:
            params['offset'] = offset
        return self.session.get(endpoint=endpoint, params=params).json()

    @checkRefresh
    def getUserIllusts(
        self,
        user_id,
        filter='for_ios',
        filter_type=None,
        offset=None
    ):
        """
        Usaer illusts
            params:
                user_id: int
                filter: str
                    ['for_android',  'for_ios']
                filter_type: str
                    ['illust', 'manga']
        """
        endpoint = 'user/illusts'
        params = {
            'user_id': user_id,
            'filter': filter,
        }
        if filter_type:
            params['type'] = filter_type
        if offset:
            params['offset'] = offset
        return self.session.get(endpoint=endpoint, params=params).json()
