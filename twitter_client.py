from .TwitterApi.twitter import TwitterClient
import requests
import json


class TweetGetter():
    def __init__(
        self,
        consumer_key,
        consumer_secret,
        auth_token,
        auth_secret
    ):
        self.cl = TwitterClient(
            consumer_key,
            consumer_secret,
            auth_token,
            auth_secret
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

    def downloadIllust(self, illust_src, path):
        illust_src = illust_src.replace(".png", "")
        resp = requests.get(illust_src)
        if resp.status_code != 200:
            raise Exception("HTTP Error")
        with open(path, "wb") as f:
            f.write(resp.content)
        return True

    def getTweet(self, tweet_address):
        try:
            if "/status/" not in tweet_address\
                    or "twitter.com" not in tweet_address:
                raise Exception()
            tweet_address = tweet_address.replace("mobile.","")
            hasParam = tweet_address.find("?")
            if hasParam != -1:
                tweet_address = tweet_address[:hasParam]
            tweet_id = int(tweet_address.split("/")[-1])
            tweet = self.cl.getTweet(tweet_id)
        except Exception as e:
            return {}
        if "media" in tweet["entities"]:
            if 'profile_banner_url' not in tweet['user']:
                tweet['user']['profile_banner_url'] = ''
            if 'profile_image_url_https' not in tweet['user']:
                tweet['user']['profile_image_url_https'] = ''
            resp = {
                'illust': {
                    'type': 'twitter',
                    'id': tweet_id,
                    'title': self.validateText(tweet["full_text"][:tweet["full_text"].find("https")]),
                    'caption': self.validateText(tweet["full_text"][:tweet["full_text"].find("https")]),
                    'imgs': [{
                        "width": m["sizes"]["large"]["w"],
                        "height": m["sizes"]["large"]["h"],
                        "large_src":m["media_url_https"]+"?format=jpg&name=orig",
                        "thumb_src":m["media_url_https"]+"?format=jpg&name=thumb"
                    } for m in tweet['extended_entities']["media"]
                    ],
                    'tags': [h["text"] for h in tweet['entities']['hashtags']],
                    'source': tweet_address,
                    'artist': self.validateText(tweet["user"]["name"]),
                    'R18': False
                },
                'user': {
                    'id': tweet["user"]["id"],
                    'screen_name': self.validateText(tweet["user"]["screen_name"]),
                    'name': self.validateText(tweet["user"]["name"]),
                    'description': self.validateText(tweet["user"]["description"]),
                    'profile_image': tweet['user']['profile_image_url_https'],
                    'banner_image': tweet['user']['profile_banner_url']
                }
            }
            for i in range(len(resp["illust"]["imgs"])):
                large_src = resp["illust"]["imgs"][i]['large_src']
                thumb_src = resp["illust"]["imgs"][i]['thumb_src']
                if ".png" in large_src:
                    resp["illust"]["imgs"][i]['large_src'] = large_src.replace(
                        "?format=jpg", "?format=png")
                if ".png" in thumb_src:
                    resp["illust"]["imgs"][i]['thumb_src'] = thumb_src.replace(
                        "?format=jpg", "?format=png")
            return resp
        else:
            return {}


if __name__ == "__main__":
    tg = TweetGetter()
    print(tg.getTweet("https://twitter.com/usagicandy_taku/status/1246029844590149633"))
