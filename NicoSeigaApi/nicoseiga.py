import requests
import lxml.html
import json
import datetime


class NicoSeigaConfig():
    SEIGA_BASE_ENDPOINT = "https://seiga.nicovideo.jp"
    LOGIN_BASE_ENDPOINT = "https://account.nicovideo.jp"
    KEYWORD_ENDPOINT = f"{SEIGA_BASE_ENDPOINT}/search"
    USER_ENDPOINT = f"{SEIGA_BASE_ENDPOINT}/user/illust"
    SEIGA_ENDPOINT = f"{SEIGA_BASE_ENDPOINT}/seiga"
    LOGIN_ENDPOINT = f"{LOGIN_BASE_ENDPOINT}/login/redirector"
    LOGIN_REFERER = f"{LOGIN_BASE_ENDPOINT}/login?site=seiga&next_url=%2Fseiga%2Fim10579022"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"


class NicoSeiga(NicoSeigaConfig):
    def __init__(self, username=None, password=None, filename=None):
        NicoSeigaConfig.__init__(self)
        self.headers = {
            "User-Agent": self.USER_AGENT,
            "Referer": self.SEIGA_BASE_ENDPOINT+"/"
        }
        self.cookies = None
        if not filename and username and password:
            self.login(username, password)
        elif filename:
            with open(filename, "r", encoding="utf8") as f:
                self.cookies = json.loads(f.read())
        else:
            print("NicoSeiga: Not logged in.")

    def login(self, username, password):
        resp = requests.post(
            self.LOGIN_ENDPOINT,
            headers={
                "Referer": self.LOGIN_REFERER,
                "User-Agent": self.USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            params={
                "show_button_twitter": 1,
                "site": "seiga",
                "show_button_facebook": 1,
                "next_url": "/seiga/im10579022"
            },
            data={
                "mail_tel": username,
                "password": password
            }
        )
        cookies = resp.history[0].cookies.get_dict()
        if "user_session" not in cookies:
            raise Exception("Login failed")
        self.cookies = cookies
        print("NicoSeiga: Login succeed.")

    def exportToken(self, filename):
        with open(filename, "w", encoding="utf8") as f:
            f.write(json.dumps(self.cookies, sort_keys=True, indent=4))

    def searchIllust(
        self,
        keyword,
        sortMethod="image_created",
        target="illust_all",
        pageID=1
    ):
        '''
        sort:
            image_created
            image_created_a
            comment_created
            comment_created_a
            clip_created
            clip_created_a
            image_view
            image_view_a
            comment_count
            comment_count_a
            clip_count
            clip_count_a
        target:
            illust
            syunga
            illust_all
        '''
        resp = requests.get(
            f"{self.KEYWORD_ENDPOINT}/{keyword}",
            headers=self.headers,
            cookies=self.cookies,
            params={"page": pageID, "sort": sortMethod, "target": target}
        )
        page = lxml.html.fromstring(resp.text)
        # 0: 一般 / 1: 春画 / 2:全て
        counts = page.xpath('//*[@id="main_area_all"]/div/div[5]/span//text()')
        counts = [int(c[1:-1]) for c in counts]
        # 検索結果 タイトルリスト
        titles = page.xpath('//p[@class="thumb_title"]//a/text()')
        # 検索結果 サムネイルリスト
        thumbs = page.xpath('//a[@class="center_img_inner "]/img/@src')
        # 検索結果 リンクリスト
        links = page.xpath('//a[@class="center_img_inner "]/@href')
        # 検索結果 IDリスト
        ids = [
            int(
                l[:l.find("?")].replace(
                    "https://seiga.nicovideo.jp/seiga/", ""
                ).replace(
                    "im", ""
                )
            )
            for l in links
        ]
        # 検索結果 [閲覧, コメ,クリップ]リスト
        counters = page.xpath('//div[@class="counter_info"]//text()')
        # くっついた文字列が返ってくるので整形する
        counters = [[y.split(" ") for y in c.split("：")] for c in counters]
        counters = [sum(c, []) for c in counters]
        for i in range(len(counters)):
            del counters[i][::2]
        counters = [[int(i) for i in c] for c in counters]
        total_pages, amari = divmod(counts[2], 20)
        if amari > 0:
            total_pages += 1
        return {
            "page": {
                "total": total_pages,
                "current": pageID,
                "sort": sortMethod,
                "target": target
            },
            "count": {
                "illust": counts[0],
                "syunga": counts[1],
                "total": counts[2]
            },
            "result": [
                {
                    "id": ids[i],
                    "title": t,
                    "thumbnail": thumbs[i],
                    "link": links[i],
                    "views": counters[i][0],
                    "comments": counters[i][1],
                    "clips": counters[i][2],
                }
                for i, t in enumerate(titles)
            ]
        }

    def getIllustDetail(self, illustID):
        resp = requests.get(
            f"{self.SEIGA_ENDPOINT}/im{illustID}",
            headers=self.headers,
            cookies=self.cookies
        )
        page = lxml.html.fromstring(resp.text)
        created_time = page.xpath(
            '//span[@class="created"]/text()'
        )
        counts = page.xpath(
            '//span[@class="count_value"]/text()'
        )
        title = page.xpath(
            '//h1[@class="title"]/text()'
        )
        description = page.xpath(
            '//p[@class="discription"]/text()'
        )
        thumbnail = page.xpath(
            '//a[@id="illust_link"]/img/@src'
        )
        # タグは別途ajaxで取得している
        resp2 = requests.get(
            f"{self.SEIGA_BASE_ENDPOINT}/ajax/illust/tag/list?id={illustID}",
            headers=self.headers,
            cookies=self.cookies
        )
        tags = [t["name"] for t in resp2.json()["tag_list"]]
        uploader_name = page.xpath('//li[@class="user_name"]/strong/text()')
        uploader_id = page.xpath('//li[@class="user_link"]/a/@href')
        uploader_thumb = page.xpath('//li[@class="thum"]/img/@src')
        # コメントは data-initializeにjsonとして入っている
        comments = page.xpath(
            '//section[@id="ko_comment"]/@data-initialize'
        )[0].replace("&quot;", '"')
        comments = json.loads(comments)
        return {
            "created_time": datetime.datetime.strptime(
                created_time[0],
                '%Y年%m月%d日 %H:%M'
            ),
            "count": {
                "view": int(counts[0]),
                "comment": int(counts[1]),
                "clip": int(counts[2]),
            },
            "title": title[0],
            "description": " ".join(description).replace(
                "\n", ""
            ).replace(
                " ", ""
            ).replace(
                "\u3000", " "
            ),
            "thumbnail": thumbnail[0],
            "tags": tags,
            "user": {
                "id": int(uploader_id[0].replace("/user/illust/", "")),
                "name": uploader_name[0],
                "thumbnail": uploader_thumb[0],
            },
            "latest_comments": comments
        }

    def getUserDetail(self, userID):
        pass

    def getIllustSourceUrl(self, illustID):
        resp = requests.get(
            f"{self.SEIGA_BASE_ENDPOINT}/image/source/{illustID}",
            headers=self.headers,
            cookies=self.cookies
        )
        page = lxml.html.fromstring(resp.text)
        url = page.xpath("//div[@class='illust_view_big']/@data-src")[0]
        return url

    def downloadIllust(self, illustID, filename=None):
        if filename is None:
            filename = f"{illustID}.jpg"
        resp = requests.get(self.getIllustSourceUrl(illustID))
        with open(filename, "wb") as f:
            f.write(resp.content)
        return True


if __name__ == '__main__':
    cl = NicoSeiga(filename="authToken.json")
    # print(cl.searchIllust("ご注文はうさぎですか"))
    print(cl.getIllustDetail("9749818"))
    # print(cl.getIllustSourceUrl("9749818"))
    # print(cl.downloadIllust("9749818"))
