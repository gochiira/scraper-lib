import requests
import lxml.html
import json
import datetime
import re


class BoothConfig():
    ENDPOINT = "https://booth.pm/ja"
    KEYWORD_ENDPOINT = f"{ENDPOINT}/search"
    USER_ENDPOINT = f"{ENDPOINT}/user/illust"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"


class Booth(BoothConfig):
    def __init__(self):
        BoothConfig.__init__(self)
        self.headers = {
            "User-Agent": self.USER_AGENT,
            "Referer": self.ENDPOINT+"/"
        }
        self.cookies = {
            "adult": "t",
            "signed_in": "1"
        }

    def searchProduct(
        self,
        keyword,
        sortMethod="new",
        pageID=1
    ):
        raise NotImplementedError()

    def getShopDetail(self, shopAddress):
        resp = requests.get(
            shopAddress,
            headers=self.headers,
            cookies=self.cookies
        )
        page = lxml.html.fromstring(resp.text)
        shop_title = page.xpath(
            '//a[@title="ホーム"]/text()'
        )[0]
        shop_description = page.xpath(
            '//div[@class="booth-description autolink"]/div[@class="u-mb-300"]'
        )[0].text_content()
        products_images = page.xpath(
            '//div[@class="thumb-inside"]/div[@class="swap-image"]/img/@src'
        )
        products_ids = [
            re.search(r'\/i\/\d{5,10}\/', p)[0][3:-1]
            for p in products_images
        ]
        products_category = page.xpath('//div[@class="item-category"]/text()')
        products_name = page.xpath('//h2[@class="item-name"]/a/text()')
        products_price = [
            int(p.replace('¥ ', '').replace(',', ''))
            for p in page.xpath('//div[@class="price u-align-middle"]/text()')
        ]
        return {
            "shop": {
                "title": shop_title,
                "description": shop_description
            },
            "products": {
                id: {
                    "category": products_category[i],
                    "name": products_name[i],
                    "price": products_price[i],
                    "image": [p for p in products_images if id in p][0]
                }
                for i, id in enumerate(products_ids)
            }
        }

    def getProductDetail(self, productID):
        resp = requests.get(
            f"{self.ENDPOINT}/items/{productID}",
            headers=self.headers,
            cookies=self.cookies
        )
        page = lxml.html.fromstring(resp.text)
        with open("site.html", "w", encoding="utf8") as f:
            f.write(resp.text)
        shop_title = page.xpath(
            '//div[@class="u-text-ellipsis"]/text()'
        )[0]
        shop_link = page.xpath(
            '//a[@data-product-list="from market_show via market_item_detail to shop_index"]/@href'
        )[0]
        product_title = page.xpath(
            '//h2[@class="u-text-wrap u-tpg-title1 u-mt-0 u-mb-400"]/text()'
        )[0]
        product_description = page.xpath(
            '//p[@class="autolink u-text-wrap"]/text()'
        )[0]
        product_images = [
            i.replace('c/72x72_a2_g5/', '')
            for i in page.xpath(
                '//div[@class="slick-thumbnail-border"]/img/@src'
            )
        ]
        product_tags = page.xpath(
            '//div[@class="search-guide-tablet-label-inner"]/text()'
        )
        return {
            "shop": {
                "title": shop_title,
                "link": shop_link
            },
            "product": {
                "title": product_title,
                "description": product_description,
                "images": product_images,
                "tags": product_tags
            }
        }

    def getIllustSourceUrl(self, productID):
        return self.getProductDetail(productID)["product"]["images"]

    def downloadIllust(self, productID, filename=None, num=0):
        if filename is None:
            filename = f"{productID}.jpg"
        resp = requests.get(self.getIllustSourceUrl(productID)[num])
        with open(filename, "wb") as f:
            f.write(resp.content)
        return True


if __name__ == '__main__':
    cl = Booth()
    # print(cl.searchProduct("ご注文はうさぎですか"))
    print(cl.getProductDetail("2313733"))
    print(cl.getShopDetail("https://bitter-crown.booth.pm/"))