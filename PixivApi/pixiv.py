from public import PixivPublicApi
from app import PixivAppApi
import livejson


class PixivApi(PixivPublicApi, PixivAppApi):
    def __init__(self, username=None, password=None, authFile=None, usePublic=False):
        if authFile:
            authFile = livejson.File(authFile)
        if usePublic:
            PixivPublicApi.__init__(self, username, password, authFile)
        else:
            PixivAppApi.__init__(self, username, password, authFile)


if __name__ == "__main__":
    cl = PixivApi(authFile='pixiv_auth.json')
    # print(cl.getIllustDetail('77246761'))
    cl.downloadIllust('https://i.pximg.net/c/600x1200_90_webp/img-master/img/2019/10/12/18/43/02/77246761_p0_master1200.jpg')