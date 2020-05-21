from .SauceNaoApi.saucenao import SauceNaoClient
from .ImgurApi.imgur import ImgurClient


class SauceNaoImageSearch():
    def __init__(self, imgurToken, saucenaoToken):
        self.saucenao = SauceNaoClient(saucenaoToken)
        self.imgur = ImgurClient(imgurToken)

    def search(self, fileName):
        url = self.imgur.upload(fileName)["data"]["link"]
        return self.saucenao.search(url)


if __name__ == "__main__":
    import json
    with open('imgur_auth.json', 'r') as f:
        imgurToken = json.loads(f.read())['token']
    with open('saucenao_auth.json', 'r') as f:
        saucenaoToken = json.loads(f.read())['token']
    cl = SauceNaoImageSearch(imgurToken, saucenaoToken)
    print(cl.search('1.jpg'))
