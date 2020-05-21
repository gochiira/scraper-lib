import requests


class SauceNaoClient():
    endpoint = "https://saucenao.com/search.php"
    params = {
        "output_type": "2",
        "api_key": "",
        "db": 999,
        "numres": 10,
        "url": ""
    }

    def __init__(self, apiKey):
        self.params["api_key"] = apiKey

    def search(self, url):
        self.params['url'] = url
        resp = requests.get(self.endpoint, params=self.params)
        if resp.status_code != 200:
            raise Exception(f'[ERROR] SauceNao response: {resp.status_code}')
        results = resp.json()["results"]
        return results
