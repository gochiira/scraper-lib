

def checkRefresh(func):
    def __checkRefresh(*args, **kwargs):
        args[0].refreshLogin()
        result = func(*args, **kwargs)
        if type(result) == dict:
            if "error" in result.keys():
                if "check your Access Token to fix" in result["error"]["message"]:
                    args[0].refreshLogin(force=True)
                    args[0].session.setHeaders(
                        {'Authorization': f"Bearer {args[0].tokens['access_token']}"}
                    )
                    result = func(*args, **kwargs)
        return result
    return __checkRefresh


class PixivError(Exception):
    """Pixiv API exception"""
    def __init__(self, reason):
        self.reason = str(reason)
        super(Exception, self).__init__(self, reason)