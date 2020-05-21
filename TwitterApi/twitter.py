import json
from requests_oauthlib import OAuth1Session


class TwitterClient(object):
    # CONSUMER_KEY
    CK = ""
    # CONSUMER_SECRET
    CS = ""
    # ACCESS_TOKEN
    AT = ""
    # ACCESS_TOKEN_SECRET
    ATS = ""
    # TWITTER_ADDRESS
    ENDPOINT = "https://api.twitter.com/1.1/"

    def __init__(self, CK, CS, AT, ATS):
        self.CK = CK
        self.CS = CS
        self.AT = AT
        self.ATS = ATS
        self.cl = OAuth1Session(CK, CS, AT, ATS)

    def __post(self, url, params={}):
        r = self.cl.post(self.ENDPOINT+url, params=params)
        if r.status_code != 200:
            raise Exception(r.status_code, r.text)
        return r.json()

    def __get(self, url, params={}):
        r = self.cl.get(self.ENDPOINT+url, params=params)
        if r.status_code != 200:
            raise Exception(r.status_code, r.text)
        return r.json()

    def __genUserIdParam(self, userId, screenId):
        '''
        userId または screenId が必要なパラメータ作成
        '''
        if userId == screenId == None:
            raise ValueError("userId or screenName is required.")
        if userId:
            return {"user_id": userId}
        else:
            return {"screen_name": screenId}

    def __genListIdParam(self, listId, listName, ownerId, ownerScreenId):
        '''
        listId または slugとownerId または　slugとownerScreenId
        が必要なパラメータ作成
        '''
        if listId == listName == None:
            raise ValueError("listId or listName is required.")
        if (listName == ownerId == None)\
                or (listName == ownerScreenId == None):
            raise ValueError("ownerId or ownerScreenId is required.")
        if listId:
            return {"list_id": listId}
        elif listName and ownerId:
            return {"slug": listName, "owner_id": ownerId}
        else:
            return {"slug": listName, "owner_screen_name": ownerScreenId}

    def verifyCredentials(self):
        return self.__get("account/verify_credentials.json")

    def getSettings(self):
        return self.__get("account/settings.json")

    def getRateLimitStatus(self):
        return self.__get("application/rate_limit_status")

    def getFavorites(self, userId=None, screenId=None, count=200, sinceId=None, maxId=None, includeEntities=False):
        '''
        userIdまたはscreenIdで指定したユーザーのいいね一覧を
        データ付きで取得する
        75 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        if sinceId:
            params["since_id"] = sinceId
        if maxId:
            params["max_id"] = maxId
        if includeEntities:
            params["includeEntities"] = True
        return self.__get("favorites/list.json", params=params)

    def getRetweets(self, count=100, sinceId=None, maxId=None, trimUser=True, includeEntities=False, includeUserEntities=False):
        '''
        ログインしているトークンのユーザーのリツイート一覧を取得する
        75 / 15min
        '''
        params = {}
        if count:
            params["count"] = count
        if sinceId:
            params["since_id"] = sinceId
        if maxId:
            params["max_id"] = maxId
        if trimUser:
            params["trim_user"] = True
        if includeEntities:
            params["include_entities"] = True
        if includeUserEntities:
            params["include_user_entities"] = True
        return self.__get("statuses/retweets_of_me.json", params=params)

    def getFollows(self, userId=None, screenId=None, count=200, cursor=None, skipStatus=True, includeUserEntities=False):
        '''
        指定したユーザーがフォローしているユーザー一覧をオブジェクトで取得する
        15 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        if count:
            params["count"] = count
        if cursor:
            params["cursor"] = cursor
        if skipStatus:
            params["skip_status"] = True
        if includeUserEntities:
            params["include_user_entities"] = True
        return self.__get("friends/list.json", params=params)

    def getFollowsIds(self, userId=None, screenId=None, count=5000, cursor=None, stringifyIds=True):
        '''
        userIdまたはscreenIdで指定したユーザーのフォローしているユーザーを
        IDで取得する
        '''
        params = self.__genUserIdParam(userId, screenId)
        if count:
            params["count"] = count
        if cursor:
            params["cursor"] = cursor
        if stringifyIds:
            params["stringify_ids"] = True
        return self.__get("friends/ids.json", params=params)

    def getFollowers(self, userId=None, screenId=None, count=200, cursor=None, skipStatus=True, includeUserEntities=False):
        '''
        userIdまたはscreenIdで指定したフォロワー一覧を
        データ付きで取得する
        15 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        params["count"] = count
        if cursor:
            params["cursor"] = cursor
        if skipStatus:
            params["skip_status"] = True
        if includeUserEntities:
            params["include_user_entities"] = True
        return self.__get("favorites/list.json", params=params)

    def getFollowerIds(self, userId=None, screenId=None, count=5000, cursor=None, stringifyIds=True):
        '''
        userIdまたはscreenIdで指定したフォロワー一覧を
        データ付きで取得する
        '''
        params = self.__genUserIdParam(userId, screenId)
        params["count"] = count
        if cursor:
            params["cursor"] = cursor
        if stringifyIds:
            params["stringify_ids"] = True
        return self.__get("followers/ids.json", params=params)

    def searchTweets(self, query, count=100, resultType="recent", lang="ja", until=None, sinceId=None, maxId=None, includeEntities=False):
        '''
        指定したクエリで検索した結果を取得する
        '''
        params = {"q": query}
        if count:
            params["count"] = count
        if resultType:
            params["result_type"] = resultType
        if lang:
            params["lang"] = lang
        if until:
            params["until"] = until
        if sinceId:
            params["since_id"] = sinceId
        if maxId:
            params["max_id"] = maxId
        if includeEntities:
            params["include_entities"] = True
        return self.__get("search/tweets.json", params=params)

    def getListList(self, userId=None, screenId=None, reverse=True):
        '''
        指定したユーザーの作成したリスト一覧を取得する
        (reverseがTrueの場合、そのユーザーが作成したリストを上位に表示)
        15 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        if reverse:
            params["reverse"] = True
        return self.__get("lists/list.json", params=params)

    def getListMembers(self, listId=None, listName=None, ownerId=None, ownerScreenId=None, count=5000, cursor=None, includeEntities=True, skipStatus=True):
        '''
        指定したListに追加されているユーザー一覧を取得する
        900 / 15min
        '''
        params = self.__genListIdParam(
            listId, listName, ownerId, ownerScreenId)
        params["count"] = count
        if cursor:
            params["cursor"] = cursor
        if includeEntities:
            params["include_entities"] = True
        if skipStatus:
            params["skip_status"] = True
        return self.__get("lists/members", params=params)

    def getListStatuses(self, listId=None, listName=None, ownerId=None, ownerScreenId=None, sinceId=None, maxId=None, count=10, includeEntities=True, includeRetweets=True):
        '''
        指定したListのタイムラインを取得する
        15 / 15min
        '''
        params = self.__genListIdParam(
            listId, listName, ownerId, ownerScreenId)
        params["count"] = count
        if sinceId:
            params["since_id"] = sinceId
        if maxId:
            params["max_id"] = maxId
        if includeEntities:
            params["include_entities"] = True
        if includeRetweets:
            params["include_rts"] = True
        return self.__get("lists/statuses", params=params)

    def getUser(self, userId=None, screenId=None, includeEntities=True):
        '''
        userIdまたはscreenIdで指定したユーザーの情報を取得する
        900 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        if includeEntities:
            params["include_entities"] = True
        return self.__get("users/show.json", params=params)

    def getUsers(self, userIds=[], screenIds=[], includeEntities=True):
        '''
        userIdsまたはscreenIdsで指定したユーザー一覧の情報を取得する
        900 / 15min
        '''
        params = {}
        if userIds == screenIds == []:
            raise ValueError("userIds or screenIds are required.")
        if userIds != []:
            params["user_id"] = ",".join(userIds)
        else:
            params["screen_name"] = ",".join(screenIds)
        if includeEntities:
            params["include_entities"] = True
        return self.__get("users/lookup.json", params=params)

    def getTweet(self, tweetId, trimUser=False, includeMyRetweet=True, includeEntities=True):
        '''
        指定したツイートを取得する
        900 / 15min
        '''
        params = {"id": tweetId}
        if trimUser:
            params["trim_user"] = True
        if includeMyRetweet:
            params["include_my_retweet"] = True
        if includeEntities:
            params["include_entities"] = True
        # 140文字以上のツイートでは これがないとオーバー分だけ消える
        params["tweet_mode"] = 'extended'
        return self.__get("statuses/show.json", params=params)

    def getTweets(self, tweetIds, map=True, trimUser=False, includeEntities=True):
        '''
        指定したツイートリストを取得する
        900 / 15min
        '''
        params = {"id": ",".join(tweetIds)}
        if map:
            params["map"] = True
        if trimUser:
            params["trim_user"] = True
        if includeEntities:
            params["include_entities"] = True
        return self.__get("statuses/lookup", params=params)

    def getStatuses(self, userId=None, screenId=None, count=200, sinceId=None, maxId=None, trimUser=False, excludeReplies=False, contributorDetails=True, includeRetweets=True):
        '''
        指定したユーザーのタイムラインを取得する
        900 / 15min
        '''
        params = self.__genUserIdParam(userId, screenId)
        if count:
            params["count"] = count
        if sinceId:
            params["since_id"] = sinceId
        if maxId:
            params["max_id"] = maxId
        if trimUser:
            params["trim_user"] = True
        if excludeReplies:
            params["exclude_replies"] = True
        if contributorDetails:
            params["contributor_details"] = True
        if includeRetweets:
            params["include_rts"] = True
        return self.__get("statuses/user_timeline.json", params=params)


if __name__ == "__main__":
    CK = "z2g3CeHmeu7SyfgWjTeCXh7fW"
    CS = "dlJB3LGolAb91BlERbhybdCFjXAM3mmMMZox1EJO3CG3tleZDA"
    AT = "906153506972753920-FuqWSzofM9mYVz6u2iBRUL8qvHmeMXq"
    ATS = "ulesAomwid1Gl2munA6XfBDJOr5uDVcb2509E9vsfOyLq"
    cl = TwitterClient(CK, CS, AT, ATS)
    print(cl.searchTweets(query="香風智乃"))
    # print(cl.getFollowers(screenId="deep_domao"))
