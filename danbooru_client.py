from .DanbooruApi.danbooru import Danbooru
import requests
import json


class DanbooruGetter():
    def __init__(self):
        self.cl = Danbooru()

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
            "self"
        ]
        for g in ngWords:
            text = text.replace(g, "")
        return text

    def getIllustSourceUrl(self, danbooru_address):
        try:
            if "https://danbooru.donmai.us/posts/" not in danbooru_address:
                raise Exception()
            hasParam = danbooru_address.find("?")
            if hasParam != -1:
                danbooru_address = danbooru_address[:hasParam]
            danbooru_id = int(danbooru_address.split("/")[-1])
            sourceUrl = self.cl.getIllustSourceUrl(danbooru_id)
        except Exception as e:
            raise Exception("Fetch failed")
        return sourceUrl

    def downloadIllust(self, illust_src, path):
        resp = requests.get(illust_src)
        if resp.status_code != 200:
            raise Exception("HTTP Error")
        with open(path, "wb") as f:
            f.write(resp.content)
        return True

    def getArt(self, danbooru_address):
        try:
            if "https://danbooru.donmai.us/posts/" not in danbooru_address:
                raise Exception()
            hasParam = danbooru_address.find("?")
            if hasParam != -1:
                danbooru_address = danbooru_address[:hasParam]
            danbooru_id = int(danbooru_address.split("/")[-1])
            art = self.cl.getIllustDetail(danbooru_id)
        except Exception as e:
            return {}
        resp = {
            'illust': {
                'type': 'danbooru',
                'id': danbooru_id,
                'title': '',
                'caption': '',
                'imgs': [{"thumb_src": art["preview_file_url"]}],
                'tags': art['tag_string_general'].split(' '),
                'source': danbooru_address,
                'artist': art["tag_string_artist"],
                'R18': True if art['rating'] not in ['s', 'q'] else False
            },
            'user': {
                'id': '0',
                'name': art["tag_string_artist"],
                'profile_image': ''
            }
        }
        return resp


if __name__ == "__main__":
    sg = DanbooruGetter()
    print(sg.getArt("https://twitter.com/usagicandy_taku/status/1246029844590149633"))
