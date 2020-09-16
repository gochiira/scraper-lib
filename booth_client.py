from .BoothApi.booth import Booth
import requests
import json


class BoothGetter():
    def __init__(self):
        self.cl = Booth()

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

    def getIllustSourceUrl(self, booth_address):
        try:
            if "https://booth.pm/ja/items/" not in booth_address:
                raise Exception()
            hasParam = booth_address.find("?")
            if hasParam != -1:
                booth_address = booth_address[:hasParam]
            booth_id = int(booth_address.split("items/")[-1])
            sourceUrls = self.cl.getIllustSourceUrl(booth_id)
        except Exception as e:
            raise Exception("Fetch failed")
        return sourceUrls

    def downloadIllust(self, illust_src, path):
        resp = requests.get(illust_src)
        if resp.status_code != 200:
            raise Exception("HTTP Error")
        with open(path, "wb") as f:
            f.write(resp.content)
        return True

    def getProduct(self, booth_address):
        try:
            if "https://booth.pm/ja/items/" not in booth_address:
                raise Exception()
            hasParam = booth_address.find("?")
            if hasParam != -1:
                booth_address = booth_address[:hasParam]
            booth_id = int(booth_address.split("items/")[-1])
            product = self.cl.getProductDetail(booth_id)
        except Exception as e:
            return {}
        resp = {
            'illust': {
                'type': 'booth_product',
                'id': booth_id,
                'title': product["product"]['title'],
                'caption': product["product"]['description'],
                'imgs': [
                    {"thumb_src": i}
                    for i in product["product"]['images']
                ],
                'tags': product["product"]['tags'],
                'source': booth_address,
                'artist': product["shop"]["title"],
                'R18': False
            },
            'shop': {
                'name': product["shop"]["title"],
                'link': product["shop"]["link"]
            }
        }
        return resp


if __name__ == "__main__":
    bg = BoothGetter()
    print(bg.getProduct("https://twitter.com/usagicandy_taku/status/1246029844590149633"))
