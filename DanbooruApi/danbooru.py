import requests
import lxml.html
import json
import datetime


class DanbooruConfig():
    DANBOORU_BASE_ENDPOINT = "https://danbooru.donmai.us"
    DANBOORU_ARTS_ENDPOINT = DANBOORU_BASE_ENDPOINT + '/posts'
    USER_AGENT = "Gochiira_Scraper/1.0.0 (dsgamer777@gmail.com)"


class Danbooru(DanbooruConfig):
    def __init__(self, username=None, password=None, filename=None):
        DanbooruConfig.__init__(self)
        self.headers = {
            "User-Agent": self.USER_AGENT
        }
        self.cookies = None

    def searchIllust(
        self,
        keyword,
        sortMethod="image_created",
        target="illust_all",
        pageID=1
    ):
        # TODO: Implement by watching https://danbooru.donmai.us/wiki_pages/help:api
        raise Exception('Not Implemented')

    def getIllustSourceUrl(self, illustID):
        return self.getIllustDetail(illustID)['file_url']

    def getIllustDetail(self, illustID):
        resp = requests.get(
            f'{self.DANBOORU_ARTS_ENDPOINT}/{illustID}.json',
            headers=self.headers
        ).json()
        return resp

    def downloadIllust(self, fileUrl, filename=None):
        if filename is None:
            filename = fileUrl.split('/')[-1]
        resp = requests.get(fileUrl)
        with open(filename, "wb") as f:
            f.write(resp.content)
        return True


if __name__ == '__main__':
    cl = Danbooru()
    # print(cl.searchIllust("ご注文はうさぎですか"))
    print(cl.getIllustDetail("833123"))
    # print(cl.getIllustSourceUrl("9749818"))
    # print(cl.downloadIllust("9749818"))
