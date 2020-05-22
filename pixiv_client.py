from .PixivApi.pixiv import PixivClient
from datetime import datetime
import traceback
import os.path


class IllustGetter():
    def __init__(self, authFile="pixiv_auth.json"):
        self.cl = PixivClient(authFile=authFile)

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

    def downloadIllust(self, url, name='', path='', prefix='', replace=False):
        self.cl.downloadIllust(
            url,
            name=name,
            path=path,
            prefix=prefix,
            replace=replace
        )
        return True

    def getIllust(self, illust_address):
        try:
            if "pixiv.net/artworks/" not in illust_address:
                raise Exception()
            has_param = illust_address.find("?")
            if has_param != -1:
                illust_address = illust_address[:has_param]
            illust_id = int(illust_address.split("/")[-1])
            illust = self.cl.getIllustDetail(illust_id)
            illust = illust["illust"]
        except:
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
                'tags': [t["name"] for t in illust['tags']],
                'source': illust_address,
                'artist': self.validateText(illust['user']['name']),
                'R18': illust['x_restrict']
            },
            'user': {
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
