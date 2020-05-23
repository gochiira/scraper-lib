from .OneSignal.Api.onesignal import OneSignalClient


class OneSignalNotifyClient():
    def __init__(self, onesignalAppId, onesignalToken):
        self.cl = OneSignalClient(onesignalAppId, onesignalToken)

    def sendNotify(self, title, text, playerIds, url=None, image=None):
        # ボタンは自動生成('見に行く') にしたい
        return self.cl.sendNotify(
            title=title,
            text=text,
            playerIds=playerIds,
            url=url,
            image=image,
            buttons=None
        )


if __name__ == "__main__":
    import json
    with open('onesignal_auth.json', 'r') as f:
        auth = json.loads(f.read())
    cl = OneSignalNotifyClient(auth["appId"], auth["token"])
    print(cl.sendNotify('title', 'caption', ['ids']))
