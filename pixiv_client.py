from pixivpy3 import *
from datetime import datetime
import livejson
import traceback


class IllustGetter():
    def __init__(self, authFile="pixiv_auth.json"):
        self.cl = AppPixivAPI()
        self.tokens = livejson.File(authFile)
        self.cl.set_auth(
            access_token=self.tokens['access_token'],
            refresh_token=self.tokens['refresh_token']
        )
        self.refreshToken()

    def refreshToken(self):
        now = datetime.now()
        last_refresh = datetime.strptime(
            self.tokens['last_refresh'],
            '%Y-%m-%d %H:%M:%S'
        )
        if (now - last_refresh).seconds > 3600:
            try:
                self.cl.auth()
            except:
                self.cl.login(
                    self.tokens['username'],
                    self.tokens['password']
                )
            self.tokens['access_token'] = self.cl.access_token
            self.tokens['refresh_token'] = self.cl.refresh_token
            self.tokens['last_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def validateText(self, text):
        ngWords = [
            "{",
            "}",
            "[",
            "]",
            "request",
            "config",
            "<script>",
            "</script>",
            "class",
            "import",
            "__globals__",
            "__getitem__",
            "self",
            "<br />",
            "<strong>",
            "</strong>",
            '<a href="',
            '" target="_blank">',
            "</a>"
        ]
        for g in ngWords:
            text = text.replace(g, "")
        return text

    def downloadIllust(self, illust_src, path):
        self.refreshToken()
        self.cl.download(illust_src, fname=path)
        return True

    def getIllust(self, illust_address):
        self.refreshToken()
        try:
            if "pixiv.net/artworks/" not in illust_address:
                raise Exception()
            has_param = illust_address.find("?")
            if has_param != -1:
                illust_address = illust_address[:has_param]
            print(illust_address)
            illust_id = int(illust_address.split("/")[-1])
            print(illust_id)
            illust = self.cl.illust_detail(illust_id)
            print(illust)
            illust = illust["illust"]
        except Exception as e:
            traceback.print_exc()
            return {}
        if illust['meta_single_page'] != {}:
            illust['meta_pages'] = [{
                'large_src': illust['meta_single_page']['original_image_url'],
                'thumb_src': illust['image_urls']['square_medium']
            }]
        else:
            illust['meta_pages'] = [{
                'large_src': m['image_urls']['original'],
                'thumb_src': m['image_urls']['square_medium']
            } for m in illust['meta_pages']]
        # 2であればグロ判定なのだがごちイラはサポートしないこととする(?)
        if illust['x_restrict'] > 1:
            illust['x_restrict'] = 1
        resp = {
            'illust': {
                'type': 'pixiv',
                'id': illust_id,
                'title': self.validateText(illust['title']),
                'caption': self.validateText(illust['caption']),
                'imgs': [{
                    "width": illust['width'],
                    "height": illust['height'],
                    "large_src": m["large_src"],
                    "thumb_src": m["thumb_src"]
                } for m in illust['meta_pages']],
                'tags': [ t["name"] for t in illust['tags'] ],
                'source': illust_address,
                'artist': self.validateText(illust['user']['name']),
                'R18': illust['x_restrict']
            },
            'user' : {
                'id': illust['user']['id'],
                'screen_name': illust['user']['account'],
                'name': self.validateText(illust['user']['name']),
                'description': '',
                'profile_image': illust['user']['profile_image_urls']['medium'],
                'banner_image': ''
            }
        }
        return resp


if __name__ == "__main__":
    ig = IllustGetter()
    print(ig.getIllust("https://www.pixiv.net/artworks/80047600"))
