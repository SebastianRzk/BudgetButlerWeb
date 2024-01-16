class OnlineAuth:

    def __init__(self, online_name, cookies):
        self._online_name = online_name
        self._cookies = cookies

    def online_name(self):
        return self._online_name

    def cookies(self):
        return self._cookies
