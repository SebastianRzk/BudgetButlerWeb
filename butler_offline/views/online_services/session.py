from butler_offline.viewcore import requester
import json


def get_partnername(serverurl, auth_container):
    partner_configuration_string = requester.instance().post(serverurl + '/partner.php', cookies=auth_container.cookies())
    partner_configuration = json.loads(partner_configuration_string)
    return partner_configuration['partnername']


def login(server_url, email, password):
    auth_request = requester.instance().post_raw(server_url + '/login.php', data={'email': email, 'password': password})
    auth_container = json.loads(requester.instance().decode(auth_request))
    return OnlineAuth(server_url, auth_container['username'], auth_request.cookies)


class OnlineAuth:

    def __init__(self, server_url, online_name, cookies):
        self._server_url = server_url
        self._online_name = online_name
        self._cookies = cookies

    def server_url(self):
        return self._server_url

    def online_name(self):
        return self._online_name

    def cookies(self):
        return self._cookies
