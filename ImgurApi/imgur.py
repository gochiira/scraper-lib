import requests


class ImgurClient():
    ENDPOINT = "https://api.imgur.com/3/upload"
    HEADER = {
        "Authorization": "Client-ID "
    }

    def __init__(self, clientID):
        self.HEADER["Authorization"] = "Client-ID " + clientID

    def upload(self, fileName):
        with open(fileName, "rb") as f:
            files = {'image': (fileName, f.read(), "image/jpeg")}
        resp = requests.post(self.ENDPOINT, files=files, headers=self.HEADER)
        return resp.json()
