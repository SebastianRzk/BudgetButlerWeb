from butler_offline.viewcore import requester
import requests

INSTANCE = None

def instance():
    if not requester.INSTANCE:
        requester.INSTANCE = Requester()
    return requester.INSTANCE


class Requester:

    def post(self, server_url, data={}, cookies=None):
        print('requested url', server_url, data)
        response = requests.post(server_url, data=data, cookies=cookies)
        response.raise_for_status()
        return self.decode(response)

    def decode(self, response):
        print('response:', response)
        decoded_response = response.content.decode("utf-8")
        print('decoded repsonse:', decoded_response)
        return decoded_response

    def post_raw(self, server_url, data):
        print('requested url', server_url, data)
        response = requests.post(server_url, data=data)
        response.raise_for_status()
        return response

    def put(self, server_url, data, cookies):
        print('requested url', server_url, data)
        response = requests.put(url=server_url, json=data, cookies=cookies)
        response.raise_for_status()
        return self.decode(response)
