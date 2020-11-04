from .Ascii2dApi.ascii2d import Ascii2d
from .ImgurApi.imgur import ImgurClient


class Ascii2dImageSearch():
    def __init__(self, imgurToken):
        self.ascii2d = Ascii2d()
        self.imgur = ImgurClient(imgurToken)

    def search(self, fileName):
        url = self.imgur.upload(fileName)["data"]["link"]
        colorResult = self.ascii2d.searchByUrl(url)
        bovwResult = self.ascii2d.getBovwSearchResult(
            colorResult["url"]["bovw"]
        )
        return {
            "color": {
                "url": colorResult["url"]["color"],
                "result": colorResult["result"]
            },
            "bovw": {
               "url": colorResult["url"]["bovw"],
               "result": bovwResult["result"]
            }
        }


if __name__ == "__main__":
    import json
    with open('imgur_auth.json', 'r') as f:
        imgurToken = json.loads(f.read())['token']
    cl = Ascii2dImageSearch(imgurToken)
    print(cl.search('79.jpg'))
