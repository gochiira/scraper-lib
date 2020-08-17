from .NicoSeigaApi.nicoseiga import NicoSeiga
import requests
import json


class SeigaGetter():
    def __init__(self, authFile="seiga_auth.json"):
        self.cl = NicoSeiga(
            filename=authFile
        )

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

    def getIllustSourceUrl(self, seiga_address):
        try:
            if "https://seiga.nicovideo.jp/seiga/" not in seiga_address:
                raise Exception()
            hasParam = seiga_address.find("?")
            if hasParam != -1:
                seiga_address = seiga_address[:hasParam]
            seiga_id = int(seiga_address.split("im")[-1])
            sourceUrl = self.cl.getIllustSourceUrl(seiga_id)
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

    def getSeiga(self, seiga_address):
        try:
            if "https://seiga.nicovideo.jp/seiga/" not in seiga_address:
                raise Exception()
            hasParam = seiga_address.find("?")
            if hasParam != -1:
                seiga_address = seiga_address[:hasParam]
            seiga_id = int(seiga_address.split("im")[-1])
            seiga = self.cl.getIllustDetail(seiga_id)
        except Exception as e:
            return {}
        resp = {
            'illust': {
                'type': 'twitter',
                'id': seiga_id,
                'title': seiga['title'],
                'caption': seiga['description'],
                'imgs': [{"thumb_src":seiga['thumbnail']}],
                'tags': seiga['tags'],
                'source': seiga_address,
                'artist': seiga["user"]["name"],
                'R18': False
            },
            'user': {
                'id': seiga["user"]["id"],
                'name': seiga["user"]["name"],
                'profile_image': seiga['user']['thumbnail']
            }
        }
        return resp


if __name__ == "__main__":
    sg = SeigaGetter("seiga_auth.json")
    print(sg.getSeiga("https://twitter.com/usagicandy_taku/status/1246029844590149633"))
