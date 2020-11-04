import requests
import lxml.html
import json
import datetime
from urllib.parse import quote


class Ascii2d():
    ENDPOINT = "https://ascii2d.net"

    def searchByUrl(self, url):
        return self.getResult(f"{self.ENDPOINT}/search/url/{url}")

    def getColorSearchResult(self, url):
        if "/search/color/" not in url:
            raise ValueError("Invalid url")
        return self.getResult(url)

    def getBovwSearchResult(self, url):
        if "/search/bovw/" not in url:
            raise ValueError("Invalid url")
        return self.getResult(url)

    def getResult(self, url):
        resp = requests.get(url)
        return {
            "url": {
                "color": resp.url.replace("bovw", "color"),
                "bovw": resp.url.replace("color", "bovw")
            },
            "result": self.parsePage(resp.text)
        }

    def parsePage(self, html):
        page = lxml.html.fromstring(html)
        # ハッシュリスト
        hashs = page.xpath('//div[@class="hash"]/text()')
        # 解像度 拡張子 ファイルサイズ
        sizes = page.xpath('//small[@class="text-muted"]/text()')
        # タイトルリスト
        titles = page.xpath('//div[@class="detail-box gray-link"]/h6/a/text()')
        titles = [titles[i:i+2] for i in range(0, len(titles)-2, 2)]
        # リンクリスト
        links = page.xpath('//div[@class="detail-box gray-link"]/h6/a/@href')
        links = [links[i:i+2] for i in range(0, len(links)-2, 2)]
        # 検索結果 サムネイルリスト
        thumbs = page.xpath('//img[@loading="lazy"]/@src')
        return [
            {
                'hash': hash,
                'size': size,
                'thumbnail': thumb,
                'title': title[0],
                'artist': title[1],
                'urls': {
                    'source': link[0],
                    'artist': link[1]
                }
            }
            for hash, size, thumb, title, link in zip(
                hashs[1:], sizes[1:], thumbs, titles, links
            )
        ]


if __name__ == '__main__':
    cl = Ascii2d()
    # print(cl.searchByUrl('https://pbs.twimg.com/media/CkmD7qxUgAIFfxz?format=jpg&name=orig'))
    print(cl.getBovwSearchResult('https://ascii2d.net/search/bovw/927e8cfee6643751dc20cf0f0431b93f'))
